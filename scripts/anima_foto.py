"""Trasforma una foto (es. la copertina di un articolo) in un reel verticale 720x1280, gratis
(niente ElevenLabs): l'animale "respira" appena, erba e foglie ondeggiano, il cielo scorre,
granelli di luce galleggiano nell'aria. Niente zoom finto (Salvatore non lo vuole).

Impaginazione come i reel di Guida Energia: titolo bianco su banda nera in alto, foto quadrata
al centro, schede con i numeri in basso (una alla volta), domanda finale per i commenti.

Uso (con il venv che ha rembg e opencv):
  /home/salvatore/venv-reel/bin/python scripts/anima_foto.py FOTO.jpg OUT.mp4 "TITOLO" \
      "RIGA GRANDE|riga piccola" "RIGA GRANDE|riga piccola" ... [--domanda "E il tuo?|Scrivilo nei commenti"]
  --centro 0.5   posizione orizzontale del ritaglio quadrato (0 = sinistra, 1 = destra)
"""
import argparse
import math
import os
import subprocess
import tempfile
import wave

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, TOP, SQ, FPS, SR = 720, 1280, 250, 720, 30, 44100
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
VERDE = (90, 220, 60)
T_INTRO, T_SCHEDA = 0.6, 3.0


def font(s):
    return ImageFont.truetype(FONT, s)


def righe(d, testo, size, max_w):
    """Una riga se ci sta, altrimenti due righe bilanciate; riduce il corpo se serve."""
    parole = testo.split()
    for s in range(size, 20, -2):
        f = font(s)
        if d.textlength(testo, font=f) <= max_w:
            return [testo], f
        if len(parole) > 1:
            k = min(range(1, len(parole)), key=lambda k: abs(len(" ".join(parole[:k])) - len(" ".join(parole[k:]))))
            rr = [" ".join(parole[:k]), " ".join(parole[k:])]
            if s <= size * 0.85 and max(d.textlength(r, font=f) for r in rr) <= max_w:
                return rr, f
    return [testo], font(20)


def scrivi(d, y, testo, size, colore, max_w=W - 60):
    rr, f = righe(d, testo, size, max_w)
    for r in rr:
        w = d.textlength(r, font=f)
        d.text(((W - w) / 2, y), r, font=f, fill=colore, stroke_width=3, stroke_fill=(0, 0, 0))
        y += int(f.size * 1.2)
    return y


def banda_titolo(titolo):
    im = Image.new("RGB", (W, TOP), (0, 0, 0))
    d = ImageDraw.Draw(im)
    rr, f = righe(d, titolo, 48, W - 60)
    h = len(rr) * int(f.size * 1.2)
    scrivi(d, (TOP - h) // 2, titolo, 48, (255, 255, 255))
    return np.array(im)


def scheda(grande, piccola):
    im = Image.new("RGB", (W, H - TOP - SQ), (0, 0, 0))
    d = ImageDraw.Draw(im)
    y = scrivi(d, 55, grande, 58, VERDE)
    if piccola:
        scrivi(d, y + 12, piccola, 40, (255, 255, 255))
    return np.array(im)


def maschera_soggetto(img):
    from rembg import new_session, remove
    rgba = remove(Image.fromarray(img), session=new_session("isnet-general-use"))
    a = np.array(rgba)[:, :, 3].astype(np.float32) / 255
    return cv2.GaussianBlur(a, (0, 0), 2)


def maschere_sfondo(img, sogg):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)
    h, s, v = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    fuori = 1 - np.clip(sogg * 1.5, 0, 1)
    # vegetazione: tinte giallo-verdi abbastanza sature
    veg = ((h > 45) & (h < 170) & (s > 0.18) & (v > 0.12)).astype(np.float32)
    veg = cv2.GaussianBlur(veg, (0, 0), 3) * fuori
    # cielo: parte alta, azzurro chiaro o bianco luminoso
    yy = np.linspace(1, 0, img.shape[0])[:, None] * np.ones((1, img.shape[1]))
    cielo = (((h > 185) & (h < 250) & (s > 0.12) & (v > 0.45)) | ((s < 0.12) & (v > 0.8))).astype(np.float32)
    cielo = cv2.GaussianBlur(cielo * (yy > 0.45), (0, 0), 6) * fuori
    return veg, cielo


def nuvole(n, seed=3):
    """Texture morbida larga il doppio, da far scorrere orizzontalmente."""
    rng = np.random.default_rng(seed)
    t = np.zeros((n, 2 * n), np.float32)
    for sc, a in ((8, 1.0), (16, 0.5), (32, 0.25)):
        r = rng.random((sc, 2 * sc)).astype(np.float32)
        r[:, -1] = r[:, 0]  # bordo che si ripete senza stacco
        t += a * cv2.resize(r, (2 * n, n), interpolation=cv2.INTER_CUBIC)
    t = (t - t.min()) / (t.max() - t.min())
    return np.clip((t - 0.45) * 2.2, 0, 1)


def audio(path, dur, tics, seed=5):
    """Solo un 'tic' discreto a ogni scheda (09/10, Salvatore: il vecchio fruscio di "vento" + accordo fisso era
    un suono fastidioso). La musica vera arrivera' da un brano scelto apposta."""
    t = np.arange(int(SR * dur)) / SR
    sig = np.zeros_like(t)
    for t0 in tics:
        i0, n = int(t0 * SR), int(0.18 * SR)
        tt = np.arange(n) / SR
        sig[i0:i0 + n] += (0.12 * np.sin(2 * math.pi * 1318.5 * tt) * np.exp(-tt * 28))[:len(sig) - i0]
    st = np.repeat((np.clip(sig, -1, 1) * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto")
    ap.add_argument("out")
    ap.add_argument("titolo")
    ap.add_argument("schede", nargs="+")
    ap.add_argument("--domanda", default="")
    ap.add_argument("--centro", type=float, default=0.5)
    a = ap.parse_args()

    src = np.array(Image.open(a.foto).convert("RGB"))
    lato = min(src.shape[:2])
    x0 = int((src.shape[1] - lato) * a.centro)
    y0 = (src.shape[0] - lato) // 2
    img = cv2.resize(src[y0:y0 + lato, x0:x0 + lato], (SQ, SQ), interpolation=cv2.INTER_AREA)

    sogg = maschera_soggetto(img)
    veg, cielo = maschere_sfondo(img, sogg)
    tex = nuvole(SQ)
    ys, xs = np.nonzero(sogg > 0.5)
    base_y = ys.max() if len(ys) else SQ  # il soggetto "respira" appoggiato alla sua base
    cx = xs.mean() if len(xs) else SQ / 2

    schede = [s.split("|") + [""] for s in a.schede]
    if a.domanda:
        schede.append(a.domanda.split("|") + [""])
    card = [scheda(s[0], s[1]) for s in schede]
    starts = [T_INTRO + i * T_SCHEDA for i in range(len(card))]
    dur = T_INTRO + T_SCHEDA * len(card) + 0.4
    n = int(dur * FPS)

    rng = np.random.default_rng(11)
    P = 45  # granelli di luce
    px, py = rng.uniform(0, SQ, P), rng.uniform(0, SQ, P)
    pv, pr, pf = rng.uniform(6, 16, P), rng.uniform(1.2, 2.6, P), rng.uniform(0, 6.28, P)

    gx, gy = np.meshgrid(np.arange(SQ, dtype=np.float32), np.arange(SQ, dtype=np.float32))
    titolo = banda_titolo(a.titolo)
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "a.wav")
    audio(wav, dur, starts)
    ff = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-i", wav, "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest",
                           "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
    imgf = img.astype(np.float32)
    for i in range(n):
        t = i / FPS
        # 1. erba e foglie: ondeggiamento a onde, piu' ampio in alto nelle chiome e in basso nell'erba
        onda = np.sin(2 * math.pi * t / 2.6 + gy * 0.045 + gx * 0.012)
        dx = 2.6 * onda * veg
        dy = 0.8 * np.cos(2 * math.pi * t / 3.1 + gx * 0.03) * veg
        fr = cv2.remap(imgf, gx + dx, gy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        # 2. cielo: nuvole morbide che scorrono piano
        off = int(t * 14) % SQ
        nv = tex[:, off:off + SQ]
        fr = fr + (cielo * nv * 0.28)[..., None] * (255 - fr)
        # 3. soggetto che respira (solo ingrandimento minimo, cosi' copre sempre l'originale)
        s = 1 + 0.004 * (1 + math.sin(2 * math.pi * t / 3.4))
        M = np.float32([[s, 0, cx * (1 - s)], [0, s, base_y * (1 - s)]])
        sw = cv2.warpAffine(imgf, M, (SQ, SQ), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        ma = cv2.warpAffine(sogg, M, (SQ, SQ))[..., None]
        fr = fr * (1 - ma) + sw * ma
        # 4. granelli di luce che salgono piano e brillano
        ov = np.zeros((SQ, SQ), np.float32)
        yy = (py - pv * t) % SQ
        xx = px + 6 * np.sin(t * 0.8 + pf)
        lum = 0.5 + 0.5 * np.sin(t * 2.2 + pf)
        for k in range(P):
            cv2.circle(ov, (int(xx[k]), int(yy[k])), int(pr[k] + 0.5), float(lum[k]), -1, cv2.LINE_AA)
        ov = cv2.GaussianBlur(ov, (0, 0), 1.6) * 0.55
        fr = fr + ov[..., None] * (np.array([255, 245, 210], np.float32) - fr)

        frame = np.zeros((H, W, 3), np.uint8)
        frame[:TOP] = titolo
        frame[TOP:TOP + SQ] = np.clip(fr, 0, 255).astype(np.uint8)
        k = max([j for j, st in enumerate(starts) if t >= st], default=None)
        if k is not None:
            frame[TOP + SQ:] = card[k]
        ff.stdin.write(frame.tobytes())
    ff.stdin.close()
    ff.wait()
    print("ok", a.out, f"{dur:.1f} s")


if __name__ == "__main__":
    main()
