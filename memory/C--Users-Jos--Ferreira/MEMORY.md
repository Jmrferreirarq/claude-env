# Memory Index

- [project_fa_template_rjue.md](project_fa_template_rjue.md) — FA_Template_RJUE_v1: estado do trabalho de melhoria do template Archicad para prática RJUE portuguesa
- [project_susana_migration.md](project_susana_migration.md) — Migração projeto SusanaSantos para template PT: BMs/composites/camadas/surfaces/zone categories
- [project_barracao_lic_branco.md](project_barracao_lic_branco.md) — Projeto Barracao LIC Branco: 94 camadas em 20 folders, 6 composites, 18 BMs, 15 zone categories PT; pendente rename de fills/surfaces
- [user_profile.md](user_profile.md) — Perfil do utilizador: arquiteto português, trabalha com Archicad e BIM para prática RJUE
- [feedback_no_acentos.md](feedback_no_acentos.md) — Sem acentos nos nomes Archicad (navigator, schedules, atributos, etc.)
- [feedback_tapir_delete_attributes_unsafe.md](feedback_tapir_delete_attributes_unsafe.md) — Tapir attributes_delete_attributes não protege atributos em uso; success:true não é fiável
- [feedback_tapir_set_details_unsupported.md](feedback_tapir_set_details_unsupported.md) — Tapir set_details_of_elements ignora silenciosamente mutações em tipos "Not yet supported" (Railing, etc.) apesar do success:true
- [feedback_tapir_navigator_projectmap_readonly.md](feedback_tapir_navigator_projectmap_readonly.md) — Tapir navigator_rename_navigator_item retorna 7403 em itens do Project Map (Sections etc.); só View Map é mutável
- [feedback_tapir_set_stories_broken.md](feedback_tapir_set_stories_broken.md) — Tapir project_set_stories falha com 'result' e não aplica nada; mutação de stories tem de ser manual GUI
- [feedback_tapir_create_bm_cutsurface_ignored.md](feedback_tapir_create_bm_cutsurface_ignored.md) — Tapir CreateBuildingMaterials ignora cutSurfaceIndex; BM fica criado mas com cutSurface vazio, requer ajuste manual GUI
- [feedback_tapir_create_bm_batch_silent_no_op.md](feedback_tapir_create_bm_batch_silent_no_op.md) — Tapir create_building_materials batch pode falhar silenciosamente (success retornado, nada aplicado); validar sempre via re-leitura
- [feedback_tapir_create_surfaces_reflection_ignored.md](feedback_tapir_create_surfaces_reflection_ignored.md) — Tapir create_surfaces ignora ambient/diffuse/specularReflection; surface fica preta ate ajuste manual GUI
- [feedback_tapir_no_create_fills.md](feedback_tapir_no_create_fills.md) — Tapir nao tem CreateFills/rename/delete; pedir ao utilizador criar Fills no GUI primeiro
- [reference_rjue_zone_classification.md](reference_rjue_zone_classification.md) — Guia de classificação de zonas para RJUE (compartimento → categoria)
- [reference_fa_building_materials_system_v1.md](reference_fa_building_materials_system_v1.md) — Regras FA System v1: nomenclatura+priority de BMs/Fills/Composites; validar antes de criar/alterar
- [reference_tapir_mcp_setup.md](reference_tapir_mcp_setup.md) — MCP ArchicadTapir (user scope) lançado via C:\tapir_home\start_tapir.bat
