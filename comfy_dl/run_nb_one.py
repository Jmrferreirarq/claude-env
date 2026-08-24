# Nano Banana Pro (gemini-3-pro-image) — 1 imagem. Uso: python run_nb_one.py "<SRC>" "<OUT>" "<LABEL>"
import os, json, base64, urllib.request, sys, winreg
from PIL import Image, ImageDraw, ImageFont

MODEL="gemini-3-pro-image"
SRC=sys.argv[1]; OUT=sys.argv[2]; LABEL=sys.argv[3] if len(sys.argv)>3 else "Nano Banana Pro (2K)"
MODE=sys.argv[4] if len(sys.argv)>4 else "default"   # "default" | "strict" (cena vazia/crua)

key=os.environ.get("GEMINI_API_KEY")
if not key:
    h=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment"); key=winreg.QueryValueEx(h,"GEMINI_API_KEY")[0]
print("key:",key[:6]+"..."+key[-3:],"| mode:",MODE,flush=True)

PROMPT_DEFAULT=("Transform this 3D render into a realistic amateur real-estate photograph of the same interior. "
 "Keep the exact same layout, geometry, perspective, furniture, colours and materials - change nothing in "
 "the design, only make it look like a real photo shot with a DSLR, 35mm lens. "
 "Make materials matte and believable: realistic satin wood, NOT glossy mirrors - remove strong reflections. "
 "Real, slightly imperfect plants. Natural surface texture, subtle dust, micro-detail. "
 "Lighting: one soft directional daylight source from the window with natural falloff and warm bounce, "
 "realistic soft shadows - not flat even lighting. Subtle film grain, shallow depth of field, faint "
 "atmospheric depth, slightly warm white balance. "
 "Real estate magazine photograph, photographic and slightly imperfect, not a perfect render. "
 "No people, no text, no watermark, no changes to the layout or objects.")

# variante CENA VAZIA/CRUA: re-iluminar e re-texturizar SEM acrescentar nada
PROMPT_STRICT=("Transform this 3D render into a realistic amateur real-estate photograph of the same interior. "
 "Keep the exact same layout, geometry, perspective, openings, doors, walls, colours and materials - change "
 "nothing in the design, only make it look like a real photo shot with a DSLR, 35mm lens. "
 "CRITICAL: do NOT add any object, plant, decor, furniture, curtain, rug, artwork, switch or fixture that is "
 "not already present in the original render. Only re-light and re-texture what already exists. If the scene "
 "is empty, keep it empty. "
 "Make materials matte and believable: realistic satin wood and plaster, NOT glossy mirrors - remove strong "
 "reflections. Natural surface texture, subtle dust, micro-detail on walls, floor tiles and the door. "
 "Lighting: soft natural daylight with gentle falloff and warm bounce, realistic soft shadows - not flat even "
 "lighting. Subtle film grain, shallow depth of field, faint atmospheric depth, slightly warm white balance. "
 "Real estate magazine photograph, photographic and slightly imperfect, not a perfect render. "
 "No people, no text, no watermark, no new elements, no changes to the layout or objects.")

# variante EXTERIOR (strict): converter massa clay em foto de arquitetura exterior, sem inventar
PROMPT_EXT=("Transform this crude 3D architectural massing render into a realistic exterior real-estate "
 "photograph of the same house. Keep the exact same building geometry, massing, roof shape, facade, window "
 "and sliding-door positions, garden layout, boundary walls and slatted fence - change nothing in the design "
 "or proportions; only make it look like a real photo shot with a DSLR, 35mm lens. "
 "CRITICAL: do NOT add any object, extra vegetation, furniture, car, person, pool or decor not present in the "
 "original. Only re-light, re-texture, and replace the flat placeholder sky with a realistic sky. "
 "Realistic matte plaster/render walls, natural roof material, real glass with subtle reflections, wood-slat "
 "fence, concrete side walls, real mown lawn with natural texture. "
 "Natural daylight, clear to partly-cloudy real sky, soft realistic shadows consistent with the sun, slightly "
 "warm white balance, subtle film grain, natural atmospheric depth. "
 "Real estate architectural photograph, photographic and slightly imperfect, not a perfect render. "
 "No people, no cars, no text, no watermark, no new elements, no changes to the layout.")

PROMPT = {"strict":PROMPT_STRICT,"exterior":PROMPT_EXT}.get(MODE, PROMPT_DEFAULT)

src=Image.open(SRC).convert("RGB"); print("SRC",src.size,flush=True)
b64=base64.b64encode(open(SRC,"rb").read()).decode()
# aspect ratio para o mais próximo do source
r=src.size[0]/src.size[1]
cand={"1:1":1.0,"5:4":1.25,"4:3":1.333,"3:2":1.5,"16:9":1.778}
ar=min(cand,key=lambda k:abs(cand[k]-r))
body={"contents":[{"parts":[{"text":PROMPT},{"inline_data":{"mime_type":"image/jpeg","data":b64}}]}],
 "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":ar,"imageSize":"2K"}}}
url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
try: resp=json.loads(urllib.request.urlopen(req,timeout=300).read())
except urllib.error.HTTPError as e: print("HTTP",e.code); print(e.read().decode()[:2000]); sys.exit(2)
cand=resp.get("candidates",[])
if not cand: print("NO CAND:",json.dumps(resp)[:1500]); sys.exit(3)
saved=False
for p in cand[0].get("content",{}).get("parts",[]):
    d=p.get("inlineData") or p.get("inline_data")
    if d: open(OUT,"wb").write(base64.b64decode(d["data"])); saved=True
    elif "text" in p: print("TEXT:",p["text"][:300])
if not saved: print("NO IMG:",json.dumps(resp)[:1500]); sys.exit(4)
res=Image.open(OUT); print("SAVED",OUT,res.size,"ar",ar,flush=True)

# compare origem vs resultado
CMP=OUT.rsplit(".",1)[0]+"_compare.png"
TW=1180
try: font=ImageFont.truetype("arial.ttf",20)
except: font=ImageFont.load_default()
def rs(im): return im.resize((TW,int(TW*im.size[1]/im.size[0])),Image.LANCZOS)
a,b=rs(src),rs(res); lab=28; gap=22
cv=Image.new("RGB",(TW,a.size[1]+b.size[1]+lab*2+gap),(18,18,20)); dr=ImageDraw.Draw(cv)
dr.text((6,4),"ORIGEM — render Enscape",fill=(235,235,235),font=font); cv.paste(a,(0,lab))
y=lab+a.size[1]+gap; dr.text((6,y-22),"RESULTADO — "+LABEL,fill=(210,255,210),font=font); cv.paste(b,(0,y))
cv.save(CMP); print("COMPARE",CMP,flush=True)
