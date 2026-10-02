# Coda argomenti per la pubblicazione automatica

Uso interno del cron giornaliero (non è un articolo). Formato:
`- [ ] Titolo proposto | sezione | slug | keyword target (volume/mese, difficoltà) | note`

## Da pubblicare

(vuota: da rifornire con una ricerca keyword OpenSEO in una sessione interattiva)

## Pubblicati

- [x] Alghe in acquario: cause e come eliminarle | acquari | alghe-acquario-cause-eliminarle-2026 | "alghe acquario" / "alghe verdi acquario" / "alghe barba nera" | 2026-10-02, scelta senza dati di volume seguendo "Quando la coda è vuota" (sezioni acquari e piccoli-animali le più scarne con 4 articoli ciascuna; acquari non aveva ancora un articolo dedicato alle alghe, solo un cenno in "acqua torbida"). Fonti verificate: AcquaPortal, Green Aqua, zooplus Magazine, AcquarioPro. Prodotti reali verificati su Amazon.it (Easy-Life AlgExit, Tetra AlgoStop Depot, Sera Algovec, JBL PO4 Test Set).
- [x] Punti bianchi sui pesci d'acquario: cause, cura e come evitare l'Ich | acquari | punti-bianchi-pesci-acquario-ich-cause-cura-2026 | "punti bianchi pesci acquario" / "ich pesci" / "ictioftiriasi" | 2026-10-01, scelta senza dati di volume seguendo "Quando la coda è vuota" (sezione acquari la più scarna con 3 articoli, nessuno sulle malattie dei pesci). Fonti verificate: Aquarium Co-Op, Texas A&M AgriLife Extension, eSHa Labs, Acquariofilia.org. Prodotti reali verificati su Amazon.it (Sera Protazol, JBL Punktol Plus).
- [x] Alimentazione del coniglio nano: cosa mangia, quanto fieno e cosa evitare | piccoli-animali | alimentazione-coniglio-nano-2026 | "alimentazione coniglio nano" / "cosa mangia il coniglio nano" | 2026-09-30, scelta senza dati di volume seguendo "Quando la coda è vuota" (sezione piccoli-animali scarna: cavia, criceto e furetto coperti, coniglio no). Fonti verificate: Ca'Zampa BluVet, Vetpedia, Policlinico Veterinario Roma Sud (CVRS).
- [x] Acqua torbida in acquario: cause e come risolverla | acquari | acqua-torbida-acquario-cause-soluzioni-2026 | "acqua torbida acquario" / "acquario acqua torbida cause" | 2026-09-29, scelta senza dati di volume seguendo "Quando la coda è vuota" (sezione acquari la più scarna, solo 2 articoli, nessuno sul tema). Fonti verificate: My-Personal Trainer, Bluviva, zooplus Magazine, AcquarioPro.
- [x] Alimentazione del criceto: cosa mangia, quanto dargli e cosa evitare | piccoli-animali | alimentazione-criceto-cosa-mangia-2026 | "cosa mangia il criceto" / "alimentazione criceto" | 2026-09-28, scelta senza dati di volume seguendo "Quando la coda è vuota" (sezione piccoli-animali ancora scarna, criceto non ancora trattato dopo cavia e furetto). Fonti verificate: Associazione Italiana Criceti Onlus, Ambulatorio Veterinario Valdisieve, Viridea.
- [x] Alimentazione della cavia: cosa può mangiare il porcellino d'India e cosa evitare | piccoli-animali | alimentazione-cavia-porcellino-india-2026 | "alimentazione cavia" / "vitamina C porcellino d'india" / "cosa mangia il porcellino d'india" | 2026-09-27, scelta senza dati di volume seguendo "Quando la coda è vuota" (sezione piccoli-animali più scarna, solo il furetto). Fonti verificate: My-Personal Trainer, AniCura, Mondosanità, Petsblog, Centro Veterinario Specialistico Roma.
- [x] Il gatto beve poco: cause, quanto dovrebbe bere e cosa fare | salute | gatto-beve-poco-cause-cosa-fare-2026 | "gatto beve poco" / "gatto non beve" | 2026-09-26, scelta senza dati di volume. Angolo salute (non prodotto) per non duplicare la guida alle fontanelle, a cui rimanda.
- [x] Cane e castagne, ghiande, ippocastani: cosa è pericoloso in autunno | salute | cane-castagne-ghiande-ippocastani-autunno-2026 | "cane castagne" / "cane ghiande" / "ippocastano cane" | 2026-09-26, scelta senza dati di volume (stagionale autunno, coda lunga). Fonti verificate: Ticino Animal Hospital, Wamiz, Amore a quattro zampe.

## Quando la coda è vuota

1. Guarda quali sezioni sono più scarne (`ls content/*/`): oggi `piccoli-animali`, `acquari` e `salute` hanno pochi articoli.
2. Con WebSearch valida 2-3 idee che i padroni italiani cercano davvero: problemi concreti ("il gatto non beve", "cane che trema"), scelte d'acquisto ("miglior fontanella per gatti"), stagionalità (autunno: muta, freddo, zecche residue, castagne tossiche; dicembre: cibi natalizi pericolosi).
3. Preferisci domande specifiche a coda lunga rispetto a temi generici ("cibo per cani") dominati da grandi siti.
4. Scegli la più solida, pubblicala e aggiungila sotto "Pubblicati" con `- [x]`, data e la nota "scelta senza dati di volume".

## Da aggiornare

Articoli vecchi con prodotti, numeri o fonti inventati (controllo del 02/10/2026). Il cron li aggiorna lunedì, mercoledì e sabato, uno per volta, in quest'ordine. I link Amazon sbagliati sono già stati trasformati in ricerche il 02/10: ora vanno rifatti i contenuti.

- [ ] content/prodotti/antiparassitari-spot-on-cani-gatti-2026.md — prodotto per gatti (Frontline Combo Gatti) era nella sezione cani; verificare durate, specie, presenza di permetrina; non citare farmaci con ricetta come acquistabili online; coordinare con /prodotti/antiparassitari-cani-gatti-2026/ (già riscritto il 02/10)
- [ ] content/prodotti/fontanella-acqua-gatti-quale-scegliere-2026.md — nomi prodotti non corrispondenti a quelli venduti (FenSoda, HOPRO, Petsfit); un link era il codice di un libro; fonti vaghe ("pareri nefrologi, test comparativi")
- [ ] content/prodotti/miglior-cibo-secco-cani-2026.md — un link portava a un siero cosmetico; verificare tutte le marche e le percentuali di carne dichiarate
- [ ] content/prodotti/cibo-umido-gatti-migliori-brand-2026.md — "Purina Pro Plan Veterinary Diet" non è il prodotto linkato; fonti vaghe ("analisi Nutrienti, pareri proprietari")
- [ ] content/prodotti/miglior-cibo-gatti-sterilizzati-2026.md — verificare che i prodotti consigliati siano davvero per gatti sterilizzati (Whiskas generico in lista)
- [ ] content/prodotti/miglior-lettiera-gatto-autodetergente-2026.md — "CatGenie 120", "Whistle litter Box 2", "PetSafe ScoopFree Ultra": verificare che esistano e siano venduti in Italia; fonti vaghe
- [ ] content/prodotti/pettorina-cani-2026.md — marche americane (Lupine, Ruffwear, 2 Hounds, Blueberry) con link ad altri prodotti; rifare la selezione con modelli venduti su Amazon.it
- [ ] content/prodotti/tappetini-refrigeranti-animali-2026.md — tutti e 5 i prodotti nominati (PetSafe Coolaroo, Petmate, Armarkat, Furhaven...) non corrispondevano ai link; contenuto estivo, rifarlo con prodotti reali
- [ ] content/prodotti/cuccia-ortopedica-cani-anziani-2026.md — modelli americani (Majestic Royal Orthopedic, K&H, Bartex); fonti vaghe ("pareri ortopedici")
- [ ] content/prodotti/cuccia-cani-esterno-interno-guida-2026.md — un link era una fodera di ricambio, un altro una gabbia; fonti vaghe
- [ ] content/prodotti/tiragraffi-gatti-migliori-2026.md — "PetFusion" linkava un Trixie; nomi storpiati (Feanda, Vespera); fonti vaghe
- [ ] content/prodotti/guinzaglio-retrattile-cane-quale-scegliere-2026.md — "PetSafe Steel", "Kong Flexi" non corrispondenti; esiste anche cani/guinzagli-retrattili-cani-2026.md sullo stesso tema: differenziare i due articoli
- [ ] content/prodotti/trasportino-cane-auto-2026.md — un trasportino rigido era nella sezione morbidi; verificare omologazioni e prezzi
- [ ] content/acquari/acquario-autosufficiente-ecosistema-chiuso-2026.md — "Ecosphere" linkava una boccia per pesci (sconsigliata per il benessere dei pesci); il kit linkava un set di attrezzi
- [ ] content/gatti/come-scegliere-gatto-perfetto.md + content/gatti/come-scegliere-gatto-perfetto-casa.md + content/gatti/scelta-gatto-perfetto-per-casa.md — TRE articoli sullo stesso tema: segnalare a Salvatore quale tenere (non cancellare né fondere da soli)
