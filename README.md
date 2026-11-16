# Cabinet de Avocatură Pantelimon Rădoi

Site static în limba română, construit pe informațiile publicate de [Cabinetul de Avocatură Pantelimon Rădoi](https://avocatpantelimonradoi.ro/) și cu o direcție vizuală inspirată de structura și prezentarea site-ului [gunea.ro](https://gunea.ro/). Conținutul a fost verificat la 16 noiembrie 2026.

Designul folosește componentele CSS UIkit instalate local pentru carduri, butoane, formular și articole. Buildul copiază `uikit.min.css` din `node_modules`; `src/styles.css` aplică identitatea vizuală a cabinetului. Interacțiunile existente din `src/main.js` și elementele native pentru FAQ și meniul mobil rămân responsabile de comportament, astfel că UIkit JavaScript nu este încărcat în paralel.

Paleta vizuală folosește maro clasic (`#4b3428`), maro închis (`#30221b`) și accentele aurii existente. Aceleași culori sunt folosite în bara browserului și imaginea de partajare.

## Structură

- Acasă, Despre noi, Servicii, Blog și Contact.
- Nouă pagini cu descrierile complete ale domeniilor de practică, salvate în `src/service-content.json`.
- Trei articole complete, preluate din interfața publică WordPress a cabinetului și salvate în `src/blog-posts.json`.
- Datele cabinetului, serviciile, valorile, întrebările frecvente și lista articolelor se află în `src/content.mjs`.

Descrierile serviciilor pot fi sincronizate din sursa publică prin `python scripts/sync-service-content.py` (necesită `requests` și `beautifulsoup4`). Buildul nu accesează rețeaua.

## Dezvoltare

Necesită Node.js 20 sau mai nou. Nu există dependențe npm.

```sh
npm run dev
```

Site-ul local este disponibil la `http://127.0.0.1:4173/`. Pentru generarea și verificarea fișierelor:

```sh
npm run build
npm run check
```

Fișierele publicabile sunt în `dist/`. Setează `SITE_URL` la domeniul final și `NOINDEX=false` la buildul pentru publicare. Implicit, site-ul este marcat `noindex`.

## Contact

Formularul validează câmpurile și acordul, apoi deschide WhatsApp la `+40 785 869 247` cu numele, emailul, telefonul și mesajul precompletate. Vizitatorul apasă „Trimite” în WhatsApp pentru expediere. Datele publice de contact sunt telefonul `+40 785 869 247`, adresa `avocat.pantelimon@gmail.com` și Bulevardul Pipera, nr. 1.

Un clic pe adresa de email deschide un mesaj nou prin `mailto:`. Dacă vizitatorul nu are o aplicație de email configurată, pe pagină apar opțiuni pentru Gmail, Outlook și copierea adresei. Aceste opțiuni sunt separate de formularul WhatsApp.

Pagina Contact include o hartă Google Maps cu punctul cabinetului la coordonatele `44.4838785, 26.1089708` și un link către fișa Google Maps furnizată pentru cabinet.

## Imagini

Fotografiile din `src/assets/photos/` sunt imagini generate anterior pornind de la portretul furnizat în proiect. Înainte de publicare, cabinetul trebuie să confirme că asemănarea și utilizarea lor sunt potrivite.
# site_Avocat-Radoi-Pantelimon
