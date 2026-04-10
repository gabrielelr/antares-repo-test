---
component: Button
figma_id: ""
status: stable
version: 2.3.0
last_updated: 2026-04-10
---

# Button

Il Button è il componente di azione primaria del sistema. Viene utilizzato per innescare azioni immediate, navigazione o invio di form.

## Varianti

| Variante | Utilizzo |
|---|---|
| `primary` | Azione principale della pagina. Una sola per contesto. |
| `secondary` | Azioni alternative o secondarie rispetto alla primaria. |
| `ghost` | Azioni terziarie, contesti a bassa enfasi (es. dentro card). |
| `danger` | Azioni distruttive o irreversibili (es. elimina, cancella). |

## Dimensioni

| Size | Utilizzo |
|---|---|
| `sm` | Contesti compatti: tabelle, toolbar, form inline. |
| `md` | Default. Form standard, modal, sezioni di contenuto. |
| `lg` | Hero, CTA ad alta visibilità, landing page. |

## Anatomia

- **Label** — testo dell'azione, sempre presente
- **Icon leading** _(opzionale)_ — icona a sinistra della label
- **Icon trailing** _(opzionale)_ — icona a destra della label
- **Icon only** — solo icona, richiede `aria-label`

## Comportamento

- Lo stato `disabled` blocca interazione e riduce opacità al 40%.
- Lo stato `loading` sostituisce la label con uno spinner e blocca click multipli.
- La larghezza è determinata dal contenuto per default; può essere forzata a `full-width`.

## Accessibilità

- Usa il tag `<button>` nativo, non `<div>` o `<a>`.
- Se icon-only, fornire sempre `aria-label` descrittivo.
- Il focus ring è sempre visibile in modalità keyboard navigation.
- Contrasto minimo garantito su tutti i background di sistema.

## Da non fare

- Non usare più di un Button `primary` per contesto visivo.
- Non troncare la label: ridimensionare il contenitore o usare size più piccola.
- Non usare `danger` per azioni reversibili.

---

_Sincronizzato da Figma — [changelog](./changelog.md) · [evolutive](./evolutive.md)_
