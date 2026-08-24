# David Afonso social (render texturado) — LOTE 4, Caminho A, interior ancorado + no-invention.
import os, json, base64, urllib.request, sys, winreg
from PIL import Image, ImageDraw, ImageFont

MODEL="gemini-3-pro-image"
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\Enscape_2026-06-26-11-38-47.png"
PREFIX=r"C:\Users\José Ferreira\Nanobana\renders\da_social_lote"
N=4
key=os.environ.get("GEMINI_API_KEY")
if not key:
    h=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment"); key=winreg.QueryValueEx(h,"GEMINI_API_KEY")[0]

PROMPT=("Transform this 3D architectural render into a realistic interior photograph of the same open-plan living "
 "space. Keep the exact same layout, geometry, perspective, furniture, colours and materials - change nothing in the "
 "design, add or remove nothing; only make it look like a real photo shot with a DSLR 35mm lens. "
 "Preserve EXACTLY: the open staircase with white stringer, dark wood treads and glass railing, and the mirror wall "
 "beside it (keep it a clean flat mirror - do not invent objects in the reflection); the indoor planter garden under "
 "the stairs (potted dracaena and monstera in terracotta pots on grass); the double-height void; the two large woven "
 "cone pendant lamps; the grey sectional sofa and the lime-yellow armchair; the round wood coffee table with thin "
 "black legs; the oak dining table with white moulded chairs; the concrete kitchen island with black slatted base, "
 "white tall units and integrated appliances; the wall-mounted black TV; the large glazed wall with sheer curtains "
 "and the garden outside; large-format greige porcelain floor tiles; warm off-white walls and ceiling with recessed "
 "downlights. "
 "Do not add any new object, plant, furniture, artwork or decor not already present. "
 "Materials matte and believable, natural daylight from the glazing with soft realistic shadows and warm bounce, "
 "subtle film grain, shallow depth of field, slightly warm white balance. Real estate magazine photograph, "
 "photographic and slightly imperfect, not a perfect render. No people, no text, no watermark, no changes to the "
 "layout or objects.")

src=Image.open(SRC).convert("RGB"); print("SRC",src.size,flush=True)
b64=base64.b64encode(open(SRC,"rb").read()).decode()
r=src.size[0]/src.size[1]; cset={"1:1":1.0,"5:4":1.25,"4:3":1.333,"3:2":1.5,"16:9":1.778}
ar=min(cset,key=lambda k:abs(cset[k]-r))
url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
body={"contents":[{"parts":[{"text":PROMPT},{"inline_data":{"mime_type":"image/png","data":b64}}]}],
 "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":ar,"imageSize":"2K"}}}

outs=[]
for i in range(1,N+1):
    req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    try: resp=json.loads(urllib.request.urlopen(req,timeout=300).read())
    except urllib.error.HTTPError as e: print("HTTP",i,e.code,e.read().decode()[:500]); continue
    c=resp.get("candidates",[])
    if not c: print(i,"no cand"); continue
    sv=None
    for p in c[0].get("content",{}).get("parts",[]):
        d=p.get("inlineData") or p.get("inline_data")
        if d: sv=f"{PREFIX}_{i}.png"; open(sv,"wb").write(base64.b64decode(d["data"]))
    if sv: outs.append(sv); print("ok",i,os.path.basename(sv),Image.open(sv).size,flush=True)

if outs:
    try: font=ImageFont.truetype("arial.ttf",30)
    except: font=ImageFont.load_default()
    cw=900; ims=[Image.open(o).convert("RGB") for o in outs]
    th=[im.resize((cw,int(cw*im.size[1]/im.size[0])),Image.LANCZOS) for im in ims]
    ch=max(t.size[1] for t in th); lab=40; cols=2; rows=(len(th)+1)//2
    grid=Image.new("RGB",(cw*cols,(ch+lab)*rows),(15,15,17)); dr=ImageDraw.Draw(grid)
    for idx,t in enumerate(th):
        cx=(idx%cols)*cw; cy=(idx//cols)*(ch+lab)
        dr.text((cx+8,cy+6),"#%d  %s"%(idx+1,os.path.basename(outs[idx])),fill=(210,255,210),font=font)
        grid.paste(t,(cx,cy+lab))
    gp=f"{PREFIX}_grid.png"; grid.save(gp); print("GRID",os.path.basename(gp),grid.size,flush=True)
