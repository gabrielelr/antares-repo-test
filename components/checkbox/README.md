---
component: Checkbox
figma_id: ""
status: stable
version: 1.1.0
last_updated: 2026-04-10
---

# Checkbox

La Checkbox permette all'utente di selezionare una o più opzioni da un insieme. È usata in form, filtri e liste di selezione multipla.

## Varianti

| Variante | Utilizzo |
|---|---|
| `default` | Singola checkbox standalone o in gruppo |
| `indeterminate` | Stato parziale: alcuni elementi di un gruppo figlio sono selezionati |

## Stati

| Stato | Descrizione |
|---|---|
| `unchecked` | Nessuna selezione |
| `checked` | Selezionato |
| `indeterminate` | Selezione parziale (solo per checkbox padre di un gruppo) |
| `disabled` | Non interagibile, stato preservato visivamente |
| `error` | Validazione fallita, abbinato a messaggio di errore |

## Anatomia

- **Control** — il quadrato interattivo
- **Label** _(opzionale)_ — testo descrittivo a destra del control
- **Helper text** _(opzionale)_ — testo secondario sotto la label
- **Error message** _(opzionale)_ — visibile solo in stato `error`

## Comportamento

- In un gruppo di checkbox, lo stato delle singole non influenza le altre (a differenza del RadioButton).
- La checkbox padre con stato `indeterminate` seleziona/deseleziona tutte le figlie al click.
- Il click sull'area della label attiva/disattiva la checkbox.

## Quando usarla

- Selezione multipla tra opzioni indipendenti
- Accettazione di termini e condizioni (singola)
- Filtri applicabili in combinazione

## Quando non usarla

- Selezione esclusiva tra opzioni: usare `RadioButton`
- Attivazione/disattivazione di una funzionalità: usare `Toggle`
- Selezione da liste lunghe (> 7 opzioni): valutare `MultiSelect`

## Accessibilità

- Usa `<input type="checkbox">` nativo.
- Label sempre associata via `for`/`id` o come elemento wrapper.
- Stato `indeterminate` impostato via JS (`indeterminate = true`), non tramite attributo HTML.
- Gruppo di checkbox correlate racchiuso in `<fieldset>` con `<legend>`.

---

_Sincronizzato da Figma — [changelog](./changelog.md) · [evolutive](./evolutive.md)_
