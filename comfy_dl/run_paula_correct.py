# Exterior Paula Silva — palete REAL confirmado (modelo 19723) + cobertura do source. 1 teste.
import os, json, base64, urllib.request, sys, winreg
from PIL import Image, ImageDraw, ImageFont

MODEL="gemini-3-pro-image"
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\Teste . Paula Silva.jpg"
OUT=r"C:\Users\José Ferreira\Nanobana\renders\paulasilva_correct_test.png"

key=os.environ.get("GEMINI_API_KEY")
if not key:
    h=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment"); key=winreg.QueryValueEx(h,"GEMINI_API_KEY")[0]

PROMPT=("Transform this crude 3D architectural massing render into a realistic exterior real-estate photograph "
 "of the same house. Keep the EXACT same building geometry, massing, roof shape, slope and orientation, facade, "
 "window and sliding-door positions, garden layout, boundary walls and fence as in the render - change nothing in "
 "the design or proportions. "
 "CRITICAL ROOF: keep the exact same roof shape, pitch and orientation as in the source render. Do NOT add large "
 "overhanging eaves, do NOT change the roof into a different shape. Roof finish: matte ANTHRACITE / graphite grey "
 "FLAT ceramic roof tiles (telha plana), dark grey. "
 "Apply these REAL project materials (confirmed from the BIM model): exterior walls in smooth matte MEDIUM GREY "
 "mineral render (reboco cinza); large glazing reveals, timber wall panels and the slatted screens/fence in LIGHT "
 "natural WOOD slats (ripado, light pine tone); side retaining walls in exposed concrete; metalwork, gates and "
 "railings in BLACK matte wrought iron; a real mown green lawn; light grey concrete paving on the access path; "
 "anthracite window frames. "
 "Only re-light, re-texture and replace the flat placeholder blue sky with a realistic sky. Do NOT add any object, "
 "extra vegetation, furniture, car, person, pool or decor not present in the original. "
 "Natural daylight, partly-cloudy real sky, soft realistic shadows consistent with the sun, slightly warm white "
 "balance, subtle film grain, natural atmospheric depth. Real estate architectural photograph, photographic and "
 "slightly imperfect, not a perfect render. No people, no cars, no text, no watermark, no new elements, no changes "
 "to the layout or proportions.")

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
y=lab+a.size[1]+gap; dr.text((6,y-22),"RESULTADO — palete REAL (reboco cinza + telha plana antracite + ripado claro + metal preto)",fill=(210,255,210),font=font); cv.paste(b,(0,y))
cv.save(CMP); print("COMPARE",CMP,flush=True)
