"""Reel verticale 9:16 da uno spezzone VERO di Pixabay (gratis, uso commerciale senza attribuzione).

Perche' (dati letti il 02/10/2026): i video con foto animata e titolo su banda nera fanno fermare
solo il 15-21% di chi li vede (142-209 persone raggiunte, 29-32 visualizzazioni da 3 secondi),
con 0 condivisioni. Nel feed sembrano una foto: nel primo secondo non si muove niente.
Questo formato invece:
  - spezzone vero a tutto schermo (un animale che si muove), niente bande nere;
  - la DOMANDA in cui ci si riconosce, grande, gia' nel primo fotogramma;
  - 3-4 schede brevi in basso, con fatti presi da fonti verificate;
  - chiusura che invita a pensare a qualcuno ("Conosci un cane cosi'?"), senza "condividi/tagga"
    espliciti, che Facebook penalizza come engagement bait.

Uso:
  python3 scripts/video_clip.py PIXABAY_ID out.mp4 "DOMANDA" "GRANDE|piccola" ... --fine "CHIUSURA|piccola"
      [--centro 0.5] [--inizio 0]
Richiede PIXABAY_API_KEY nell'ambiente (o in /home/salvatore/risparmio-energetico/.env).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anima_foto import audio, font, righe  # noqa: E402

W, H, FPS = 720, 1280, 25
T_GANCIO = 2.6      # secondi con la sola domanda
T_SCHEDA = 2.8
T_FINE = 2.6
FF = imageio_ffmpeg.get_ffmpeg_exe()


def chiave():
    k = os.environ.get("PIXABAY_API_KEY")
    if k:
        return k
    for riga in open("/home/salvatore/risparmio-energetico/.env"):
        if riga.startswith("PIXABAY_API_KEY="):
            return riga.strip().split("=", 1)[1]
    sys.exit("PIXABAY_API_KEY mancante")


def apri(url):
    # senza User-Agent da browser Pixabay risponde 403
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120)


def scarica(pid, dest):
    url = f"https://pixabay.com/api/videos/?key={chiave()}&id={pid}"
    v = json.load(apri(url))["hits"][0]["videos"]
    # la versione piu' grande sotto i 2000 px di larghezza: basta per un 720x1280 ritagliato
    scelta = max((x for x in v.values() if x.get("url") and x["width"] <= 2000), key=lambda x: x["width"])
    open(dest, "wb").write(apri(scelta["url"]).read())


def testo_centrato(d, y, testo, size, colore, stroke=4, max_w=W - 70):
    rr, f = righe(d, testo, size, max_w)
    for r in rr:
        w = d.textlength(r, font=f)
        d.text(((W - w) / 2, y), r, font=f, fill=colore, stroke_width=stroke, stroke_fill=(0, 0, 0))
        y += int(f.size * 1.18)
    return y


def livello_gancio(domanda):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # leggera ombra in alto per staccare il testo da qualunque sfondo
    sf = np.zeros((H, W, 4), np.uint8)
    sf[:, :, 3] = (np.clip(1 - np.arange(H) / 520, 0, 1) * 150).astype(np.uint8)[:, None]
    im = Image.alpha_composite(im, Image.fromarray(sf))
    d = ImageDraw.Draw(im)
    # tutte le righe della stessa grandezza: la piu' grande che sta in 3 righe
    parole = domanda.split()
    for size in range(76, 40, -2):
        f = font(size)
        rr, cur = [], ""
        for p in parole:
            prova = (cur + " " + p).strip()
            if d.textlength(prova, font=f) <= W - 70:
                cur = prova
            else:
                rr.append(cur)
                cur = p
        rr.append(cur)
        if len(rr) <= 3 and all(rr):
            break
    y = 130
    for r in rr:
        d.text(((W - d.textlength(r, font=f)) / 2, y), r, font=f, fill=(255, 255, 255),
               stroke_width=5, stroke_fill=(0, 0, 0))
        y += int(size * 1.15)
    return im


def livello_scheda(grande, piccola, colore=(255, 215, 64)):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    top, bot = 860, 1130
    d.rounded_rectangle((30, top, W - 30, bot), radius=28, fill=(0, 0, 0, 175))
    y = testo_centrato(d, top + 34, grande, 50, colore, stroke=3)
    testo_centrato(d, y + 8, piccola, 36, (255, 255, 255), stroke=2)
    return im


def compone(base, *livelli):
    out = base.astype(np.float32)
    for liv in livelli:
        a = np.asarray(liv, np.float32)
        al = a[:, :, 3:4] / 255
        out = out * (1 - al) + a[:, :, :3] * al
    return out.astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pixabay_id")
    ap.add_argument("out")
    ap.add_argument("domanda")
    ap.add_argument("schede", nargs="+")
    ap.add_argument("--fine", required=True)
    ap.add_argument("--centro", type=float, default=0.5, help="dove ritagliare in orizzontale (0-1)")
    ap.add_argument("--inizio", type=float, default=0, help="secondo dello spezzone da cui partire")
    a = ap.parse_args()

    dur = T_GANCIO + T_SCHEDA * len(a.schede) + T_FINE
    with tempfile.TemporaryDirectory() as tmp:
        clip = os.path.join(tmp, "clip.mp4")
        scarica(a.pixabay_id, clip)
        # ritaglio verticale 9:16 + scala a 720x1280; lo spezzone si ripete se e' piu' corto del reel
        vf = (f"scale=-2:{H},crop={W}:{H}:'(iw-{W})*{a.centro}':0,fps={FPS},"
              f"eq=saturation=1.08:contrast=1.03")
        dec = subprocess.Popen([FF, "-loglevel", "error", "-stream_loop", "-1", "-ss", str(a.inizio), "-i", clip,
                                "-t", str(dur), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                               stdout=subprocess.PIPE)
        wav = os.path.join(tmp, "a.wav")
        tics = [T_GANCIO + i * T_SCHEDA for i in range(len(a.schede))] + [dur - T_FINE]
        audio(wav, dur, tics)
        enc = subprocess.Popen([FF, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                                "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
                                "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", a.out],
                               stdin=subprocess.PIPE)
        gancio = livello_gancio(a.domanda)
        schede = [livello_scheda(*s.split("|", 1)) for s in a.schede]
        fine = livello_scheda(*a.fine.split("|", 1), colore=(90, 220, 60))
        n = int(dur * FPS)
        for i in range(n):
            buf = dec.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            t = i / FPS
            livelli = [gancio]
            if t >= T_GANCIO:
                k = int((t - T_GANCIO) // T_SCHEDA)
                livelli.append(schede[k] if k < len(schede) else fine)
            enc.stdin.write(compone(fr, *livelli).tobytes())
        enc.stdin.close()
        enc.wait()
        dec.kill()
    print(f"OK {a.out} ({dur:.1f} s, {os.path.getsize(a.out) // 1024} KB)")


if __name__ == "__main__":
    main()
