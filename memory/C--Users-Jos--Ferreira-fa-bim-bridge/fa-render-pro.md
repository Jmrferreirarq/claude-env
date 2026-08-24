---
name: fa-render-pro
description: Pipeline de render BIM fotorrealista (IFC→Bonsai/Blender→Cycles) em construção no fa-bim-bridge
metadata: 
  node_type: memory
  type: project
  originSessionId: 052b665b-c336-4161-9ad5-a86961cb8e21
---

`fa-render-pro` — pipeline de render fotorrealista de interiores da Ferreira Arquitetos, em `fa-bim-bridge/fa-render-pro/`. Caminho escolhido (Fase 2, 2026-06-24): **IFC → Bonsai/BlenderBIM → Cycles GPU**, depois de a IA generativa (Replicate SD1.5 e Nano Banana/Gemini) ter sido rejeitada por **não preservar a geometria** — recria sempre a imagem. Ver [[ia-render-nao-preserva-geometria]].

**Setup operacional:**
- Blender **5.0.1** em `C:\Program Files\Blender Foundation\Blender 5.0\blender.exe` → Python **3.11**.
- Bonsai **0.8.5-post1** build **py311** instalado/ativo (`bl_ext.user_default.bonsai`). Regra: o build do Bonsai tem de bater certo com o Python do Blender (5.0=py311; 5.1=py313).
- Cycles em GPU via **OPTIX** (RTX 3070 8 GB). Aviso "HIPEW failed" é inofensivo.

**Arquitetura:** `fa_render_pro.py` (orquestrador host) lança `_engine.py` (headless no Blender). Presets em JSON: `materials.json` (material IFC + classe → PBR), `views.json` (câmaras), `lighting.json`, `render.json` (preview/standard/final/plan). `capture_view.py` corre no GUI para capturar enquadramentos do viewport para `views.json`.

**Estado:** pipeline corre ponta-a-ponta (import→materiais→isolar piso→luz→Cycles→PNG). **Por fazer:** afinar câmaras interiores (melhor no GUI via capture_view — fazer às cegas em headless é ineficiente), acabamentos por móvel, luz de luminárias.

**Modelo de teste:** David Afonso, IFC `2026.05.18_DavidAfonso - Imagens.ifc` (em `.@ David Afonso\1 . Modelação\JPEG\...\Imagens Interiores\`). IFC2X3, 3 pisos (0 / 3.0 / 5.8 m), 681 meshes, 7 materiais. Zona social piso 0: x≈95–112, y≈46–54.
