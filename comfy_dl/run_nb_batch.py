# Nano Banana Pro — LOTE de N variacoes. Uso: python run_nb_batch.py "<SRC>" "<PREFIX>" <N> <mode>
import os, json, base64, urllib.request, sys, winreg
from PIL import Image, ImageDraw, ImageFont

MODEL="gemini-3-pro-image"
SRC=sys.argv[1]; PREFIX=sys.argv[2]
N=int(sys.argv[3]) if len(sys.argv)>3 else 4
MODE=sys.argv[4] if len(sys.argv)>4 else "default"

key=os.environ.get("GEMINI_API_KEY")
if not key:
    h=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment"); key=winreg.QueryValueEx(h,"GEMINI_API_KEY")[0]
print("key",key[:6]+"...","| mode",MODE,"| N",N,flush=True)

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
PROMPT = PROMPT_STRICT if MODE=="strict" else PROMPT_DEFAULT

src=Image.open(SRC).convert("RGB"); print("SRC",src.size,flush=True)
b64=base64.b64encode(open(SRC,"rb").read()).decode()
r=src.size[0]/src.size[1]; ar="3:2" if abs(r-1.5)<abs(r-1.777) else "16:9"
url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
body={"contents":[{"parts":[{"text":PROMPT},{"inline_data":{"mime_type":"image/jpeg","data":b64}}]}],
 "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":ar,"imageSize":"2K"}}}

outs=[]
for i in range(1,N+1):
    req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    try: resp=json.loads(urllib.request.urlopen(req,timeout=300).read())
    except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode()[:600]); continue
    cand=resp.get("candidates",[])
    if not cand: print(i,"no cand"); continue
    sv=None
    for p in cand[0].get("content",{}).get("parts",[]):
        d=p.get("inlineData") or p.get("inline_data")
        if d:
            sv=f"{PREFIX}_{i}.png"; open(sv,"wb").write(base64.b64decode(d["data"]))
    if sv: outs.append(sv); print("ok",i,sv,Image.open(sv).size,flush=True)

# grelha 2x2 etiquetada
if outs:
    try: font=ImageFont.truetype("arial.ttf",30)
    except: font=ImageFont.load_default()
    cw=900; ims=[Image.open(o).convert("RGB") for o in outs]
    th=[im.resize((cw,int(cw*im.size[1]/im.size[0])),Image.LANCZOS) for im in ims]
    ch=max(t.size[1] for t in th); lab=40; cols=2; rows=(len(th)+1)//2
    grid=Image.new("RGB",(cw*cols,(ch+lab)*rows),(15,15,17)); dr=ImageDraw.Draw(grid)
    for idx,t in enumerate(th):
        cx=(idx%cols)*cw; cy=(idx//cols)*(ch+lab)
        dr.text((cx+8,cy+6),"#%d  %s"%(idx+1,os.path.basename(outs[idx]),),fill=(210,255,210),font=font)
        grid.paste(t,(cx,cy+lab))
    gp=f"{PREFIX}_grid.png"; grid.save(gp); print("GRID",gp,grid.size,flush=True)
