# Paula Silva exterior — LOTE de 4 (prompt no-invention + palete real). Caminho A.
import os, json, base64, urllib.request, sys, winreg
from PIL import Image, ImageDraw, ImageFont

MODEL="gemini-3-pro-image"
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\Teste . Paula Silva.jpg"
PREFIX=r"C:\Users\José Ferreira\Nanobana\renders\paulasilva_lote"
N=4

key=os.environ.get("GEMINI_API_KEY")
if not key:
    h=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment"); key=winreg.QueryValueEx(h,"GEMINI_API_KEY")[0]

USER=("Convert this 3D model into a realistic exterior photograph of the same house. Keep the exact same building "
 "geometry, roof, windows, wood-slat cladding, walls and layout - change nothing structural and add NO new elements. "
 "Do not invent or add anything that is not in the original: no extra buildings, no neighbouring houses, no added "
 "trees, no extra fences or gates, no people, no cars, no garden furniture. Keep the boundary walls and fences "
 "exactly as in the model. Keep the surroundings simple and empty. A plain natural sky is allowed. "
 "Only make it photorealistic: realistic render-plaster, wood and concrete textures, natural daylight with soft "
 "shadows, real grass, realistic materials. Photographic, slightly imperfect, not a perfect render. No text, no watermark.")
ANCHOR=(" Keep these real project finishes faithful (do not change their colour): exterior walls in medium grey "
 "mineral render; the roof in matte ANTHRACITE FLAT CERAMIC tiles (telha plana) - NOT metal sheet, no standing "
 "seams, no large overhanging eaves; the wood-slat cladding in light natural wood; metalwork and gates in matte "
 "black; side retaining walls in exposed concrete.")
PROMPT=USER+ANCHOR

src=Image.open(SRC).convert("RGB"); print("SRC",src.size,flush=True)
b64=base64.b64encode(open(SRC,"rb").read()).decode()
r=src.size[0]/src.size[1]; cset={"1:1":1.0,"5:4":1.25,"4:3":1.333,"3:2":1.5,"16:9":1.778}
ar=min(cset,key=lambda k:abs(cset[k]-r))
url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
body={"contents":[{"parts":[{"text":PROMPT},{"inline_data":{"mime_type":"image/jpeg","data":b64}}]}],
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
