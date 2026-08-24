---
name: FA-360 plataforma Ferreira Arquitetos
description: Monorepo pnpm (Node 24, React+Vite, Express 5, Postgres/Drizzle) self-hosted. Plataforma de gestão operacional da Ferreira Arquitetos.
type: project
originSessionId: 8e0a8004-12ea-42eb-b7b6-5330215eb07b
lastUpdated: 2026-04-14
---

## Localização

```
C:\Users\José Ferreira\OneDrive\Desktop\Platform-Evolution\Platform-Evolution\
```

GitHub: `https://github.com/Jmrferreirarq/FA-360-01` (branch `master`)

## Como arrancar

### Opção A — BAT (duplo clique)
```
start-fa360.bat   ← lê credenciais do .env, abre browser automaticamente
stop-fa360.bat    ← termina o processo node
```

### Opção B — Bash (terminal Claude Code)
```bash
REPO="C:/Users/José Ferreira/OneDrive/Desktop/Platform-Evolution/Platform-Evolution"
DATABASE_URL="postgresql://neondb_owner:npg_YiFrzE8JlW0n@ep-noisy-boat-alswvni1.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require" \
NODE_ENV=production PORT=5000 \
AI_INTEGRATIONS_OPENAI_BASE_URL="https://api.openai.com/v1" \
AI_INTEGRATIONS_OPENAI_API_KEY="sk-not-configured" \
ANTHROPIC_API_KEY="<key do .env>" \
node "$REPO/artifacts/api-server/dist/index.cjs" &
```

URL: **http://localhost:5000**

### Build (após alterações de código)
```bash
# API server
cd artifacts/api-server && npx tsx build.ts

# Frontend
pnpm --filter @workspace/fa360 run build
```

> ⚠️ Nunca usar `pnpm run build` no root — typecheck estrito falha em ~25 rotas.

## Credenciais e variáveis de ambiente

Ficheiro `.env` na raiz do repo (gitignored):
- `DATABASE_URL` — Neon Postgres Frankfurt
- `ANTHROPIC_API_KEY` — Claude API (Maria AI)
- `NODE_ENV=production`, `PORT=5000`
- `AI_INTEGRATIONS_OPENAI_BASE_URL` + `AI_INTEGRATIONS_OPENAI_API_KEY` — mantidos por compatibilidade mas não usados

## Base de dados

Neon Postgres (Frankfurt): `ep-noisy-boat-alswvni1.c-3.eu-central-1.aws.neon.tech`
- **453** clientes · **620** propostas · **60** projetos · **392** billing_phases · **318** invoices
- **127** accounting_accounts · **8** suppliers · **3** specialists · **1** team member

## Stack técnica

| Camada | Tecnologia |
|--------|-----------|
| Runtime | Node 24 |
| API | Express 5 + TypeScript (tsx / esbuild) |
| ORM | Drizzle ORM |
| Frontend | React 18 + Vite + TailwindCSS + shadcn/ui |
| AI | Anthropic Claude claude-sonnet-4-6 (SDK `@anthropic-ai/sdk`) |
| DB | Neon Postgres (serverless) |
| Build dist | `artifacts/api-server/dist/index.cjs` (bundle único 2.7MB) |
| Static | Frontend buildado em `artifacts/fa360/dist/public/`, servido pelo Express |

## Ficheiros críticos — não modificar sem motivo

- `artifacts/fa360/public/` — logos e assets estáticos
- `artifacts/fa360/src/index.css` — estilos globais (no-scrollbar, etc.)
- `artifacts/fa360/src/lib/comercialRules.ts` — regras comerciais FA

## Módulos e estado

| Módulo | Estado |
|--------|--------|
| Dashboard | ✅ Operacional |
| Clientes | ✅ Com badge e filtro "Portal Activo" |
| Propostas | ✅ Operacional |
| Projetos | ✅ Operacional |
| Obras | ✅ Operacional |
| Faturação / Financials | ✅ Operacional |
| Maria AI | ✅ Claude Vision — progresso, social, documento |
| Portal Cliente | ✅ Funcional (slug por cliente) |
| Inbox (Outlook) | ❌ Inoperante — precisa OAuth Microsoft Graph |
| Tarefas | ✅ Operacional |
| Agenda | ✅ Operacional |
| Calculadoras | ✅ Operacionais |

## Maria AI — como funciona

Endpoint: `POST /api/maria/analyze-doc`

Fluxo por tipo de conteúdo:

- **`progresso`** (imagem) → Claude Vision diretamente na foto → registo de obra formatado em Markdown (fase, trabalhos, materiais, observações técnicas)
- **`social`** (imagem) → Claude Vision → caption Instagram + versão LinkedIn + hashtags
- **`documento`** / **`outro`** → OCR (pdf-parse ou Vision) → extração JSON estruturada → card com botão "Criar cliente e proposta"

Modal de contexto aparece automaticamente ao selecionar ficheiros:
- Tipo: Progresso / Redes Sociais / Documento / Outro
- Cliente (pesquisa) + Projeto

O botão "Criar cliente na plataforma" só aparece para tipo `documento` E sem cliente pré-selecionado.

Chat streaming: `POST /api/maria/chat` com SSE usando `anthropic.messages.stream()`.

## Teste de regressão

Token `Gb_7DtAJ` (Hotel Santa Ana) → 1083 m², IVA 23%, 7 fases, arq 34 250 €.

## Bloqueios conhecidos

- **Outlook/Inbox**: precisa de `REPLIT_CONNECTORS_HOSTNAME` — módulo inoperante até reescrever com OAuth Microsoft Graph
- **Processo node em Windows**: usar bash com env vars explícitos (PowerShell tem problemas com `$env:` no contexto Claude Code). O `start-fa360.bat` funciona de forma autónoma.
