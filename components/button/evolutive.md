---
component: Button
figma_id: ""
last_updated: 2026-04-10
---

# Button — Evolutive

Questa sezione traccia le richieste di evoluzione del componente, le decisioni prese e la roadmap futura.

## In roadmap

### Supporto split button
- **Richiesta da:** team Product (Q1 2026)
- **Descrizione:** variante con area click divisa tra azione principale e dropdown secondario
- **Stato:** in valutazione design
- **Note:** verificare compatibilità con pattern esistenti di menu e dropdown

### Animazione stato loading
- **Richiesta da:** team Mobile Web
- **Descrizione:** transizione più fluida tra stato default e loading, con micro-animazione sull'icona spinner
- **Stato:** approvato, in attesa di slot nel backlog
- **Note:** usare token di durata da Motion foundation

---

## Richieste aperte (non ancora valutate)

| Richiesta | Richiedente | Data | Note |
|---|---|---|---|
| Variante outline con bordo tratteggiato | Design team Checkout | 2026-03-01 | Solo per contesti form opzionali |
| Prop `countdown` per blocco temporaneo post-click | Team Sicurezza | 2026-02-14 | Es. "Riprova tra 30s" |

---

## Decisioni architetturali

### Perché non esiste una variante `link`
Il Button non include una variante link-style per evitare ambiguità semantica tra azione e navigazione. Per link testuali usare il componente `TextLink`. Decisione presa in design review del 2025-05-10.

### Perché `full-width` è una prop e non una variante
La larghezza è una proprietà di layout, non di stile. Tenerla separata dalle varianti permette di combinare qualsiasi variante con comportamento full-width senza moltiplicare i casi in Figma.

---

_Sincronizzato da Figma_
