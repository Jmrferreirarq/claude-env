---
name: Tapir Archicad API
description: How to connect and use the Tapir addon API to automate Archicad via JSON/HTTP
type: reference
originSessionId: acc2c8fa-6a72-4639-b0ca-8e43e6466c1a
---
Tapir addon (ENZYME-APD/tapir-archicad-automation) exposes Archicad JSON API on `http://localhost:19723`.

**Two types of commands:**
- Built-in Archicad: `{"command": "API.GetProductInfo"}` (direct)
- Tapir addon: wrapped via `API.ExecuteAddOnCommand` with `commandNamespace: "TapirCommand"`

**Tapir command format:**
```json
{
  "command": "API.ExecuteAddOnCommand",
  "parameters": {
    "addOnCommandId": {"commandNamespace": "TapirCommand", "commandName": "CommandName"},
    "addOnCommandParameters": {}
  }
}
```

**Key commands tested and working:**
- GetStories / SetStories (names shift by 1 in array — array[0]→story 0, story -1 immutable)
- GetProjectInfo / GetProjectInfoFields / SetProjectInfoField
- GetGeoLocation / SetGeoLocation
- GetAttributesByType (Layer, Composite, BuildingMaterial, Surface, Fill, Profile, LayerCombination, ZoneCategory, PenTable, MEPSystem, Line)
- CreateLayers, CreateLayerCombinations, CreateBuildingMaterials, CreateComposites, CreateSurfaces
- CreatePropertyGroups, CreatePropertyDefinitions, DeletePropertyDefinitions
- GetAllProperties, GetAllElements, GetElementsByType
- GetFavoritesByType
- GetModelViewOptions, GetLibraries

**Important gotchas:**
- CreatePropertyDefinitions requires `defaultValue` field (not documented as required)
- CreateComposites requires `separators` array (count = skins + 1), each skin needs `type/buildingMaterialId/framePen/thickness`
- CreateSurfaces requires all 12 fields (materialType, ambientReflection, diffuseReflection, specularReflection, transparency, shine, transparencyAttenuation, emissionAttenuation, surfaceColor, specularColor, emissionColor)
- AttributeId format is always `{"attributeId": {"guid": "..."}}`
- UTF-8 encoding issues with curl on Windows — use Python subprocess with `encoding="utf-8", errors="replace"`
- Modal dialogs in Archicad block all API calls (error 4001)
- Cannot: rename views/layouts, create publisher sets, create zone categories, edit layout book, translate MEP systems

**Composite/attribute rename in place — IMPORTANT trick (verified 2026-05-11):**
- The API has no dedicated `rename attribute` for Composite/Layer/BM. `overwriteExisting=true` on `CreateComposites` does **NOT** rename in place by default — it creates a duplicate.
- **To rename in place**, send `attributeId={existing GUID}` + `name={existing name, identical}` + `overwriteExisting=true` + the FULL skin/separator payload. Then you can ALSO change other fields (skins, separators, useWith) in the same call. The GUID is preserved → elements that reference this composite stay intact.
- Sending `attributeId` + DIFFERENT name does NOT rename — creates a new entry. Use this only to actually create new composites, not to rename.
- Lesson learned: I tried rename via attributeId+new-name and got 2 duplicate composites (idx 2 and 3) which I had to delete with `attributes_delete_attributes`.

**Read limitations on specific element types:**
- `GetDetailsOfElements` and `Get2DBoundingBoxes` for Elevation/Section/InteriorElevation/Detail return `"Not yet supported element type"`. Same for Text. Coordinates of section markers are not exposed via Tapir.
- `GetGDLParametersOfElements` on Wall/Slab returns 0 params (only Objects/Doors/Windows/Lamps have GDL params exposed).
- Some Pydantic validator bugs in the MCP middleware: Object's `GetDetailsOfElements` may fail validation but the data IS in the error message. Workaround: call raw HTTP via PowerShell directly on localhost:19723.

**Navigator items (rename/clone):**
- Project Map navigator items (Stories, Elevations, Sections, etc.) are **read-only** for `RenameNavigatorItem` (error 7403). Cannot rename Elevations/Sections in Project Map via API.
- Workflow: use `view_clone_project_map_item_to_view_map` to clone an Elevation/Section into a View Map folder. The cloned View IS renameable via `RenameNavigatorItem` (set newName + newId).
- `view_create_view_map_folder` creates folders in View Map root or under a parent.
- `navigator_set_view_settings` works on Views in View Map (not Project Map). Fields: `layerCombination`, `penSetName`, `modelViewOptions`, `dimensionStyle`, `graphicOverrideCombination`. NO scale field — scale must be set in GUI.

**Cannot create via Tapir (only GUI):**
- Dimensions (linear, level, angle, radial) — no `CreateDimension` exposed
- Elevation/Section markers — no `CreateElevation` / `CreateSection`
- New Library Parts (GDL Objects from scratch) — `library_add_files_to_embedded_library` requires a pre-existing `.gsm` file; `LP_XMLConverter.exe` exists at `C:\Program Files\GRAPHISOFT\Archicad 28\` and can convert XML↔GSM, but generating valid placeable Object XML from scratch is high-risk without reference templates
- Stair tool — no Tapir command
- Show on Stories / Floor Plan Display options of Walls — not exposed as GDL or property; only GUI
- System layers like the default "ARCHICAD Layer" (index 1) are read-only — cannot delete OR rename via API (error 6104/7403)

**LayerCombination details limitation:**
- `GetLayerCombinationAttributes` returns `layerAttributeIds` (full list of layers in the LC) but NOT the per-layer hidden/locked state. Can't tell from the API which layers are visible in a given LC. Use GUI.

**Material continuity / cutFill alignment:**
- BMs sharing the same `cutFillId` will look visually identical in section. Default generic cutFill is `a7d74135-f8c6-45d1-a32c-73416f06976e`. Tijolo Cerâmico 11/22 use a different cutFill `5f167249-d667-456a-974a-d826eac650bf` (brick pattern).
- For wall/slab merge at corners: same BM atomically + `connectionPriority` compatible. Composite separator pens influence the line at element edges — set the relevant separator's `linePen` to 0 (transparent) for clean junctions.

**GDL Parameter set/get (Doors/Windows/Objects):**
- Use the actual `name` field (param 192's name is `gs_sunShade_bShowIn2D`), not the `displayName`. The MCP middleware's `elements_set_gdl_parameters_of_elements` requires `name` AND `index` AND `type` AND `value`. Missing name causes "both name and index are missing" error.
- "Overhead Garage Door 27" library part is designed for retractable doors and shows minimal 2D symbol in plan (just the opening). For visible plan symbol with swing arc, choose a different library part (e.g. "Door 27" with double swing).

**Element ID uniqueness:**
- Archicad allows duplicate Element IDs. Walls with ID `SW-072` can exist multiple times. Use `Document → Element ID Manager` to renumber to unique IDs before referring to elements by ID.

**Direct HTTP (raw, no Pydantic validation):**
- PowerShell `Invoke-RestMethod` on `http://localhost:19723` works around MCP middleware Pydantic validation bugs. Useful when MCP tool returns validation errors but the actual Tapir response is valid.
- `GetElementsByType` via raw HTTP returns all elements in one shot (no pagination); MCP middleware paginates to 100 per page.
