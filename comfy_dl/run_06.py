import json, urllib.request, urllib.parse, time, sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

SRV="http://127.0.0.1:8188"
SEED=60606
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\06.png"
RENDERS=r"C:\Users\José Ferreira\Nanobana\renders"

POS=("high-end photoreal interior photograph, magazine quality, sharp realistic micro-textures; keep architecture, "
 "layout, materials and finishes EXACTLY as in the source, do not change any colour or material. Open-plan social "
 "area: warm off-white matte walls, white ceiling with recessed downlights, light oak plank floor. Open floating "
 "staircase with black steel stringer, light oak treads and a full-height glass railing beside a mirror wall. "
 "Interior planter garden on white gravel (monstera, purple lavender, orange gerbera, ferns, succulents) against a "
 "vertical slatted-oak feature wall. Kitchen with white and oak cabinetry, a navy-blue island with a white quartz "
 "waterfall worktop, three white bar stools, a brass tap, Nespresso machine and fruit bowl, under-cabinet LED strip, "
 "black track lights and black pendant lamps. Glass-top dining table with cream upholstered chairs and a grey tray "
 "of candles. Bright soft even natural daylight, gentle soft shadows.")
NEG=("cartoon, cgi, plastic, 3d render look, lowres, blurry, deformed, distorted perspective, changed layout, "
 "changed materials, recoloured surfaces, extra windows, extra stairs, added doors, oversaturated, watermark, text, people")

# copy source into ASCII input
im=Image.open(SRC).convert("RGB")
print("SRC",im.size,flush=True)
im.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\social06_src.png")

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())

g={
 "4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
 "10":{"class_type":"LoadImage","inputs":{"image":"social06_src.png"}},
 "6":{"class_type":"CLIPTextEncode","inputs":{"text":POS,"clip":["4",1]}},
 "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
 "30":{"class_type":"UpscaleModelLoader","inputs":{"model_name":"RealESRGAN_x4plus.pth"}},
 "31":{"class_type":"UltimateSDUpscale","inputs":{
        "image":["10",0],"model":["4",0],"positive":["6",0],"negative":["7",0],"vae":["4",2],
        "upscale_by":2.0,"seed":SEED,"steps":20,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras",
        "denoise":0.20,"upscale_model":["30",0],"mode_type":"Linear","tile_width":1024,"tile_height":1024,
        "mask_blur":8,"tile_padding":32,"seam_fix_mode":"Band Pass","seam_fix_denoise":0.20,"seam_fix_width":64,
        "seam_fix_mask_blur":8,"seam_fix_padding":16,"force_uniform_tiles":True,"tiled_decode":True,"batch_size":1}},
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"social06_enh"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,"seed",SEED,flush=True)
fin=None
for _ in range(1800):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{}); outs=h[pid].get("outputs",{})
        if "32" in outs and outs["32"].get("images"):
            fin=outs["32"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not fin: print("TIMEOUT"); sys.exit(1)
q=urllib.parse.urlencode({"filename":fin["filename"],"subfolder":fin.get("subfolder",""),"type":fin.get("type","output")})
open(r"C:\comfy_dl\_06_enh.png","wb").write(urllib.request.urlopen(SRV+"/view?"+q).read())
enh=Image.open(r"C:\comfy_dl\_06_enh.png").convert("RGB")
enh.save(RENDERS+r"\06_enhanced.png")
print("ENHANCED",enh.size,flush=True)

# ---------- post-production grade (non-destructive look only) ----------
a=np.asarray(enh).astype(np.float32)/255.0
# subtle warm white balance
a[...,0]*=1.015; a[...,2]*=0.985
# gentle S-curve contrast around mid
a=(a-0.5)*1.07+0.5
# soft highlight rolloff (recover blown glass-table / bright walls)
hi=0.80
a=np.where(a>hi, hi+(a-hi)*0.6, a)
a=np.clip(a,0,1)
g_img=Image.fromarray((a*255).astype(np.uint8),"RGB")
# saturation
g_img=ImageEnhance.Color(g_img).enhance(1.06)
# clarity (large-radius low-amount local contrast) + crisp micro-sharpen
g_img=g_img.filter(ImageFilter.UnsharpMask(radius=40,percent=18,threshold=2))
g_img=g_img.filter(ImageFilter.UnsharpMask(radius=2,percent=70,threshold=2))
# vignette + fine grain
b=np.asarray(g_img).astype(np.float32)/255.0
H,W=b.shape[:2]
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
cx,cy=W/2,H/2
d=np.sqrt(((xx-cx)/cx)**2+((yy-cy)/cy)**2)/np.sqrt(2)
vig=1.0-0.14*np.clip(d,0,1)**2.2          # corners ~ -14%
b=b*vig[...,None]
rng=np.random.default_rng(606)
b=b+rng.normal(0,0.008,b.shape).astype(np.float32)  # subtle film grain
b=np.clip(b,0,1)
final=Image.fromarray((b*255).astype(np.uint8),"RGB")
final.save(RENDERS+r"\06_final.png")
final.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\06_final.png")
print("FINAL",final.size,flush=True)

# ---------- before/after comparison ----------
TH=520; gap=16; lab=34
panels=[(im,"06.png ORIGINAL (1920x1080)"),(final,"06_final ENHANCED + GRADE ("+str(final.size[0])+"x"+str(final.size[1])+")")]
ims=[]
for p,_ in panels:
    w=int(TH*p.size[0]/p.size[1]); ims.append(p.resize((w,TH),Image.LANCZOS))
from PIL import ImageDraw,ImageFont
totw=max(i.size[0] for i in ims)
canvas=Image.new("RGB",(totw,(TH+lab)*2),(18,18,20))
d2=ImageDraw.Draw(canvas)
try: font=ImageFont.truetype("arial.ttf",16)
except: font=ImageFont.load_default()
y=0
for (p,label),i2 in zip(panels,ims):
    d2.text((8,y+8),label,fill=(235,235,235),font=font)
    canvas.paste(i2,(0,y+lab)); y+=TH+lab
canvas.save(RENDERS+r"\06_comparacao.png")
print("SAVED compare",flush=True)
