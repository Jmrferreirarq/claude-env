# Teste honesto: Gemini consegue manter a RAMPA com instrucao explicita? (1 imagem, sobre o clay)
import os, json, base64, urllib.request, sys, winreg
from PIL import Image, ImageDraw, ImageFont

MODEL="gemini-3-pro-image"
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\Teste . Paula Silva.jpg"
OUT=r"C:\Users\José Ferreira\Nanobana\renders\paulasilva_ramp_test.png"
key=os.environ.get("GEMINI_API_KEY")
if not key:
    h=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment"); key=winreg.QueryValueEx(h,"GEMINI_API_KEY")[0]

PROMPT=("Convert this 3D model into a realistic exterior photograph of the same house. Keep the exact same building "
 "geometry, roof, windows, wood-slat cladding, walls and layout - change nothing structural and add NO new elements. "
 "Do not invent or add anything: no extra buildings, no neighbouring houses, no added trees, no extra fences or gates, "
 "no people, no cars, no garden furniture. Keep boundary walls and fences exactly as in the model. Surroundings simple "
 "and empty. A plain natural sky is allowed. "
 "CRITICAL GEOMETRY — THE RAMP: the paved access strip on the RIGHT side of the house, between the house and the right "
 "boundary wall, is a RAMP that slopes DOWNWARD from the foreground toward the back, going down to a lower level, "
 "bordered by a low retaining edge. Render it as a real INCLINED concrete ramp descending - do NOT flatten it into a "
 "level patio or flat path; preserve the downward slope and the change in height. "
 "Real project finishes: medium grey mineral render walls; matte anthracite flat ceramic roof tiles; light natural "
 "wood slat cladding; matte black metalwork and gates; exposed concrete side/retaining walls; real green lawn; light "
 "grey concrete on the ramp. Photorealistic, natural daylight, soft shadows, slightly imperfect, not a perfect render. "
 "No text, no watermark.")

src=Image.open(SRC).convert("RGB")
b64=base64.b64encode(open(SRC,"rb").read()).decode()
r=src.size[0]/src.size[1]; cset={"1:1":1.0,"5:4":1.25,"4:3":1.333,"3:2":1.5,"16:9":1.778}
ar=min(cset,key=lambda k:abs(cset[k]-r))
body={"contents":[{"parts":[{"text":PROMPT},{"inline_data":{"mime_type":"image/jpeg","data":b64}}]}],
 "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":ar,"imageSize":"2K"}}}
url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
try: resp=json.loads(urllib.request.urlopen(req,timeout=300).read())
except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode()[:1000]); sys.exit(2)
c=resp.get("candidates",[]); saved=False
for p in c[0].get("content",{}).get("parts",[]):
    d=p.get("inlineData") or p.get("inline_data")
    if d: open(OUT,"wb").write(base64.b64decode(d["data"])); saved=True
if not saved: print("NO IMG"); sys.exit(4)
print("SAVED",OUT,Image.open(OUT).size,flush=True)
# crop da rampa p/ verificar
res=Image.open(OUT).convert("RGB")
def crop(im,a,b,c2,d2):
    w,h=im.size; return im.crop((int(a*w),int(b*h),int(c2*w),int(d2*h)))
sc=crop(src,0.55,0.42,1.0,1.0); rc=crop(res,0.55,0.42,1.0,1.0)
BW=560
def rs(im): return im.resize((BW,int(BW*im.size[1]/im.size[0])),Image.LANCZOS)
sc2,rc2=rs(sc),rs(rc); lab=26; gap=16
try: font=ImageFont.truetype("arial.ttf",18)
except: font=ImageFont.load_default()
cv=Image.new("RGB",(BW*2+gap,max(sc2.size[1],rc2.size[1])+lab),(18,18,20)); dr=ImageDraw.Draw(cv)
dr.text((6,4),"SOURCE rampa (clay)",fill=(235,235,235),font=font)
dr.text((BW+gap+6,4),"Gemini c/ instrucao explicita",fill=(210,255,210),font=font)
cv.paste(sc2,(0,lab)); cv.paste(rc2,(BW+gap,lab))
cv.save(r"C:\Users\José Ferreira\Nanobana\renders\paulasilva_ramp_test_check.png")
print("check saved",flush=True)
