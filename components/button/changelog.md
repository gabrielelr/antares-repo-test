---
component: Button
figma_id: ""
last_updated: 2026-04-10
---

# Button — Changelog

## [2.3.0] — 2026-04-10

### Aggiunto
- Variante `ghost` per contesti a bassa enfasi
- Supporto prop `icon-only` con validazione `aria-label` obbligatoria

### Modificato
- Token colore `button-primary-bg` aggiornato al nuovo valore brand (#1A73E8 → #0057D9)
- Migliorato contrasto stato `hover` su variante `secondary`

### Corretto
- Fix: stato `loading` non bloccava il click in Firefox
- Fix: focus ring non visibile su sfondo scuro in Safari

---

## [2.2.0] — 2026-01-15

### Aggiunto
- Size `lg` per uso in hero section e CTA ad alta visibilità
- Prop `full-width` per layout a larghezza piena

### Modificato
- Border radius aggiornato da 4px a 6px per allineamento con nuovo foundation token `radius-md`

---

## [2.1.0] — 2025-10-03

### Aggiunto
- Stato `loading` con spinner integrato

### Rimosso
- Variante `flat` deprecata — sostituita da `ghost`

---

## [2.0.0] — 2025-06-20

### Breaking change
- Rinominata prop `type` in `variant` per evitare conflitto con attributo HTML nativo
- Rimossa prop `block` — usare `full-width`

### Aggiunto
- Variante `danger` per azioni distruttive
- Supporto icon leading e trailing via slot

---

_Sincronizzato da Figma_
