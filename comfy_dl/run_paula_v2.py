# Paula Silva exterior v2 — prompt do utilizador (no-invention) + ancora de palete real. 1 teste.
import os, json, base64, urllib.request, sys, winreg
from PIL import Image, ImageDraw, ImageFont

MODEL="gemini-3-pro-image"
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\Teste . Paula Silva.jpg"
OUT=r"C:\Users\José Ferreira\Nanobana\renders\paulasilva_v2_test.png"

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
# ancora de acabamentos REAIS (confirmados no modelo 19723) — factos, nao invencao
ANCHOR=(" Keep these real project finishes faithful (do not change their colour): exterior walls in medium grey "
 "mineral render; the roof in matte ANTHRACITE FLAT CERAMIC tiles (telha plana) - NOT metal sheet, no standing "
 "seams, no large overhanging eaves; the wood-slat cladding in light natural wood; metalwork and gates in matte "
 "black; side retaining walls in exposed concrete.")
PROMPT=USER+ANCHOR

src=Image.open(SRC).convert("RGB"); print("SRC",src.size,flush=True)
b64=base64.b64encode(open(SRC,"rb").read()).decode()
r=src.size[0]/src.size[1]; cand={"1:1":1.0,"5:4":1.25,"4:3":1.333,"3:2":1.5,"16:9":1.778}
ar=min(cand,key=lambda k:abs(cand[k]-r))
body={"contents":[{"parts":[{"text":PROMPT},{"inline_data":{"mime_type":"image/jpeg","data":b64}}]}],
 "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":ar,"imageSize":"2K"}}}
url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
try: resp=json.loads(urllib.request.urlopen(req,timeout=300).read())
except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode()[:1500]); sys.exit(2)
c=resp.get("candidates",[]); saved=False
for p in c[0].get("content",{}).get("parts",[]):
    d=p.get("inlineData") or p.get("inline_data")
    if d: open(OUT,"wb").write(base64.b64decode(d["data"])); saved=True
    elif "text" in p: print("TEXT:",p["text"][:300])
if not saved: print("NO IMG",json.dumps(resp)[:1200]); sys.exit(4)
res=Image.open(OUT); print("SAVED",OUT,res.size,"ar",ar,flush=True)
CMP=OUT.rsplit(".",1)[0]+"_compare.png"; TW=1180
try: font=ImageFont.truetype("arial.ttf",20)
except: font=ImageFont.load_default()
def rs(im): return im.resize((TW,int(TW*im.size[1]/im.size[0])),Image.LANCZOS)
a,b=rs(src),rs(res); lab=28; gap=22
cv=Image.new("RGB",(TW,a.size[1]+b.size[1]+lab*2+gap),(18,18,20)); dr=ImageDraw.Draw(cv)
dr.text((6,4),"ORIGEM — clay (Paula Silva)",fill=(235,235,235),font=font); cv.paste(a,(0,lab))
y=lab+a.size[1]+gap; dr.text((6,y-22),"RESULTADO v2 — prompt no-invention + palete real",fill=(210,255,210),font=font); cv.paste(b,(0,y))
cv.save(CMP); print("COMPARE",CMP,flush=True)
