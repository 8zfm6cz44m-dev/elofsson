# Släktträd – Martin Elofsson

Statisk webbplats med interaktivt släktträd och hela forskningsunderlaget (Master, Forskningslogg och Bildregister, version 2026-08-25). Sammanställd för Jan Källne.

Ingen inloggning, databas eller byggsteg. Ren HTML, CSS och JavaScript.

## Publicera med GitHub Pages

1. Lägg alla filer i roten av `main` i `8zfm6cz44m-dev/elofsson` och ersätt den gamla `index.html`.
2. Gå till **Settings → Pages**.
3. Välj **Deploy from a branch**, gren `main`, mapp `/ (root)` och spara.
4. Sidan publiceras på `https://8zfm6cz44m-dev.github.io/elofsson/` efter någon minut.

## Förhandsgranska lokalt

Datan läses med `fetch`, så sidan måste köras via en webbserver:

```
python3 -m http.server
```

Öppna sedan `http://localhost:8000`. Att dubbelklicka på `index.html` fungerar inte.

## Struktur

| Fil | Innehåll |
|---|---|
| `index.html` | Sidans skal |
| `assets/app.js` | Träd, personkort, sökning, vyer |
| `assets/style.css` | Utseende |
| `data/persons.json` | Personer: namn, datum, platser, identitetsstatus, anteckningar, källor, sökord |
| `data/relations.json` | Relationer, var och en med egen status och grund |
| `data/views.json` | Trädens placering (kolumn, rad) och gruppramar |
| `data/images.json` | Bildregistrets poster med länkar och kopplade personer |
| `data/notes.json` | Master, Forskningslogg och Bildregister, oförkortat |
| `data/flags.json` | Olösta frågor, motsägelser, uteslutet och bevisregler |
| `arkiv/` | Den ursprungliga HTML-exporten |
| `tools/` | Extraherings- och kontrollskript |

## Statusnivåer

`verified` (Verifierad), `family` (Familjebekräftad), `strong` (Mycket stark kandidat), `candidate` (Kandidat), `lead` (Lead) och `excluded` (Utesluten).

Personens `status` gäller identiteten. Relationens `status` gäller själva släktbandet och styr linjens färg och streck. En verifierad person kan alltså ha en osäker föräldrarelation.

## Underhåll

**Ny person.** Lägg till ett objekt i `persons.json` och placera personen i en vy i `views.json` med `[kolumn, rad]`. Halva kolumner fungerar. Partner står bredvid varandra och barn placeras under parets mittpunkt.

**Ny eller ändrad relation.** Lägg till eller ändra i `relations.json`. Typerna är `child` (`parents` + `child`), `partner` (`a` + `b`) och `sibling` (`a` + `b`). Skriv alltid källgrunden i `basis`.

**Nya versioner av Master, Forskningslogg och Bildregister.** Exportera dokumenten till HTML i samma format som filen i `arkiv/`, lägg den där och uppdatera filnamnet i `tools/extract_notes.py` och `tools/verify_notes.py`. Kör sedan:

```
pip install beautifulsoup4
python3 tools/extract_notes.py
python3 tools/verify_notes.py
python3 tools/validate.py
```

`verify_notes.py` kontrollerar att ingen text har försvunnit. `validate.py` kontrollerar att alla id:n hänger ihop och stoppar om Elofs föräldrar markeras som säkra.

## Integritet

Sidan innehåller uppgifter om levande personer. `robots.txt` och `noindex` hindrar sökmotorer, men sidan är ändå publik för den som har länken.
