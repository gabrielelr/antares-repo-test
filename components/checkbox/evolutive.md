---
component: Checkbox
figma_id: ""
last_updated: 2026-04-10
---

# Checkbox — Evolutive

## In roadmap

### Checkbox con immagine/thumbnail
- **Richiesta da:** team E-commerce
- **Descrizione:** variante che affianca un'immagine o icona alla label, per selezione di prodotti o categorie visive
- **Stato:** in valutazione design
- **Note:** valutare se trattarla come componente separato (CheckboxCard) per non appesantire il componente base

---

## Richieste aperte (non ancora valutate)

| Richiesta | Richiedente | Data | Note |
|---|---|---|---|
| Animazione check con micro-interazione | Design team | 2026-03-15 | Coordinare con Motion foundation |
| Variante size `sm` per uso in tabelle | Team Data | 2026-02-20 | Attuale size unica (18px) troppo ingombrante in celle compatte |

---

## Decisioni architetturali

### Perché non esiste una variante `toggle-like`
La Checkbox non include stili toggle per mantenere chiara la distinzione semantica: Checkbox = selezione in form, Toggle = attivazione di feature. Unire i due porterebbe ambiguità per l'utente e complessità inutile nel componente.

### Perché il gruppo padre/figlio è gestito dalla Checkbox stessa
La logica di stato `indeterminate` per gruppi annidati è incorporata nel componente per garantire consistenza comportamentale. Affidarla al consumer aumenterebbe il rischio di implementazioni difformi.

---

_Sincronizzato da Figma_
