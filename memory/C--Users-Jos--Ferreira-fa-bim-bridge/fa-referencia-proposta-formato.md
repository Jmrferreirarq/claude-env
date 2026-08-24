---
name: fa-referencia-proposta-formato
description: "Formato da referência de proposta do atelier FA — FA-[INICIAIS]-[LOCAL3]-[YY][IDproposta]"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5ee310dd-5ac7-4c66-9935-fd9101a51a72
  modified: 2026-07-27T14:46:14.608Z
---

Referência de proposta no atelier Ferreira Arquitetos:
**`FA-[iniciais do cliente]-[local 3 letras]-[YY][ID da proposta]`**

Exemplos confirmados pelo utilizador:
- `FA-AN-GAF-26707` → proposta **707**
- `FA-AH-VAG-26703` → proposta **703** (Vagos)
- `FA-HN-MAT-26708` → proposta **708** (Humberto Nogueira, Mataduços)

Decompõe: `FA` · iniciais do cliente (2 letras) · localidade (3 primeiras letras) · ano a 2 dígitos (`26` = 2026) · **ID da proposta no fim**.

**Não** é `FA-YYYY-NNN` sequencial — o ID vem colado ao ano no último bloco. Já gerei uma referência errada (`FA-HU-MAT-2607`) por assumir formato sequencial; confirmar sempre iniciais + local + ID.

Relacionado: [[fa360-pr-workflow]].
