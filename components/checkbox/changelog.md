---
component: Checkbox
figma_id: ""
last_updated: 2026-04-10
---

# Checkbox — Changelog

## [1.1.0] — 2026-04-10

### Aggiunto
- Stato `error` con messaggio di validazione integrato
- Helper text sotto la label per descrizioni aggiuntive

### Modificato
- Dimensione del control aumentata da 16px a 18px per miglior target touch
- Token bordo aggiornato: `checkbox-border` ora usa `color-border-strong` invece di `color-border-default`

### Corretto
- Fix: stato `indeterminate` non veniva preservato correttamente dopo re-render in React
- Fix: click su label non attivava il toggle in alcuni browser mobile

---

## [1.0.0] — 2025-09-01

### Rilascio iniziale
- Varianti: `default`, `indeterminate`
- Stati: `unchecked`, `checked`, `indeterminate`, `disabled`
- Supporto label e helper text
- Gruppo checkbox con gestione stato padre/figlio

---

_Sincronizzato da Figma_
