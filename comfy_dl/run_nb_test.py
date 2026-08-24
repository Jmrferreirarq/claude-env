# Nano Banana Pro (gemini-3-pro-image) — TESTE de 1 imagem (cozinha)
import os, json, base64, urllib.request, sys, winreg
from PIL import Image

MODEL="gemini-3-pro-image"
SRC=r"C:\Users\José Ferreira\Nanobana\renders\06_cozinha_p4.png"
OUT=r"C:\Users\José Ferreira\Nanobana\renders\cozinha_nb_test.png"

# --- key (env, fallback registry) ---
key=os.environ.get("GEMINI_API_KEY")
if not key:
    h=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment")
    key=winreg.QueryValueEx(h,"GEMINI_API_KEY")[0]
print("key:", key[:6]+"..."+key[-3:], flush=True)

# --- fixed anti-CGI prompt (PROTOCOLO-QUALIDADE.md, verbatim) ---
PROMPT=("Transform this 3D render into a realistic amateur real-estate photograph of the same interior. "
 "Keep the exact same layout, geometry, perspective, furniture, colours and materials - change nothing in "
 "the design, only make it look like a real photo shot with a DSLR, 35mm lens. "
 "Make materials matte and believable: realistic satin wood, NOT glossy mirrors - remove strong reflections. "
 "Real, slightly imperfect plants. Natural surface texture, subtle dust, micro-detail. "
 "Lighting: one soft directional daylight source from the window with natural falloff and warm bounce, "
 "realistic soft shadows - not flat even lighting. Subtle film grain, shallow depth of field, faint "
 "atmospheric depth, slightly warm white balance. "
 "Real estate magazine photograph, photographic and slightly imperfect, not a perfect render. "
 "No people, no text, no watermark, no changes to the layout or objects.")

src=Image.open(SRC).convert("RGB")
print("SRC", src.size, flush=True)
b64=base64.b64encode(open(SRC,"rb").read()).decode()

body={
 "contents":[{"parts":[
   {"text":PROMPT},
   {"inline_data":{"mime_type":"image/png","data":b64}}
 ]}],
 "generationConfig":{
   "responseModalities":["IMAGE"],
   "imageConfig":{"aspectRatio":"3:2","imageSize":"2K"}
 }
}
url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
try:
    resp=json.loads(urllib.request.urlopen(req,timeout=300).read())
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode()[:2000]); sys.exit(2)

cand=resp.get("candidates",[])
if not cand: print("NO CANDIDATES:", json.dumps(resp)[:1500]); sys.exit(3)
parts=cand[0].get("content",{}).get("parts",[])
saved=False
for p in parts:
    if "inlineData" in p or "inline_data" in p:
        d=p.get("inlineData") or p.get("inline_data")
        open(OUT,"wb").write(base64.b64decode(d["data"]))
        saved=True
    elif "text" in p:
        print("TEXT:", p["text"][:300])
if not saved: print("NO IMAGE PART:", json.dumps(resp)[:1500]); sys.exit(4)
im=Image.open(OUT); print("SAVED", OUT, im.size, flush=True)
print("finishReason:", cand[0].get("finishReason"))
