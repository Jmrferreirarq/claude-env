---
name: fa360-test-runner-ts-imports
description: fa360 — imports relativos em src/lib precisam de extensão .ts por causa do runner de testes (Node type-stripping)
metadata: 
  node_type: memory
  type: project
  originSessionId: 205e9e7d-698a-497b-947e-ae8f7e194725
---

No `fa360-platform` (artifacts/fa360), os testes (`*.test.mjs`) correm os `.ts` diretamente via type-stripping do Node 24, que NÃO resolve imports relativos sem extensão (`ERR_MODULE_NOT_FOUND`). O Vite resolve, mas o test-runner não.

**Why:** convenção do projeto — os testes importam o source COM extensão (`from "./publicProposal.ts"`); o `tsconfig` tem `allowImportingTsExtensions: true` + `moduleResolution: bundler`, por isso o `.ts` no import é válido para o tsc.

**How to apply:** qualquer import relativo novo em `src/lib/*.ts` deve levar `.ts` (ex.: `"./contacto.ts"`), senão parte a cadeia de testes (`pnpm --filter @workspace/fa360 test`). O `build` é só `vite build` e não corre tsc; o `pnpm typecheck` está pré-existentemente vermelho (~296 erros, sobretudo `implicit any` TS7006 e TS6305 da `api-client-react` não buildada) — não confundir com regressões.
