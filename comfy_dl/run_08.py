import json, urllib.request, urllib.parse, time, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

SRV="http://127.0.0.1:8188"
SEED=80818
DEPTH=0.70; CANNY=0.45; DENOISE=0.65
SRC=r"C:\ComfyUI_windows_portable\ComfyUI\input\08.png"
RENDERS=r"C:\Users\José Ferreira\Nanobana\renders"
INP=r"C:\ComfyUI_windows_portable\ComfyUI\input"
print("PARAMS depth",DEPTH,"canny",CANNY,"denoise",DENOISE,"seed",SEED,flush=True)

POS=("high-end photoreal interior photograph, magazine quality, full-frame 35mm; keep architecture, layout, "
 "the staircase, openings and proportions EXACTLY as in the source, move/remove nothing, change no colour or "
 "material. Open-plan dining-living area. Light oak plank floor, warm off-white matte walls, white ceiling with "
 "recessed downlights. Left wall: full-height sliding glass doors with pale sheer translucent curtains drawn, soft "
 "afternoon daylight, green garden and perimeter wall outside. Centre: light wood dining table with cream "
 "upholstered chairs. Right wall: low media console with a black flat TV and a tall navy-blue open bookshelf. "
 "Far right: open floating staircase with black steel stringer, light oak treads and a glass railing against a white "
 "wall, and an interior planter garden of greenery and orange flowers on white gravel below it; a flush white wall "
 "panel beside it. Realistic soft shadows, natural light falloff, rich micro-textures.")
NEG=("cartoon, cgi, plastic, 3d render look, lowres, blurry, deformed, distorted perspective, changed layout, "
 "changed staircase, extra stairs, distorted railing, changed materials, recoloured surfaces, extra windows, "
 "added doors, oversaturated, watermark, text, people")

src=Image.open(SRC).convert("RGB")
W=1536; H=round(W*src.size[1]/src.size[0]/8)*8
src.resize((W,H),Image.LANCZOS).save(INP+r"\p08_1536.png")
src.save(INP+r"\p08_full.png")
print("base",W,H,flush=True)

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())
def fetch(o,dest):
    q=urllib.parse.urlencode({"filename":o["filename"],"subfolder":o.get("subfolder",""),"type":o.get("type","output")})
    open(dest,"wb").write(urllib.request.urlopen(SRV+"/view?"+q).read())

CN="controlnet_union_sdxl_promax.safetensors"
g={
 "4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
 "10":{"class_type":"LoadImage","inputs":{"image":"p08_1536.png"}},
 "11":{"class_type":"DepthAnythingV2Preprocessor","inputs":{"ckpt_name":"depth_anything_v2_vitl.pth","resolution":1024,"image":["10",0]}},
 "16":{"class_type":"CannyEdgePreprocessor","inputs":{"high_threshold":200,"low_threshold":100,"resolution":1024,"image":["10",0]}},
 "12":{"class_type":"ControlNetLoader","inputs":{"control_net_name":CN}},
 "13":{"class_type":"SetUnionControlNetType","inputs":{"control_net":["12",0],"type":"depth"}},
 "17":{"class_type":"ControlNetLoader","inputs":{"control_net_name":CN}},
 "18":{"class_type":"SetUnionControlNetType","inputs":{"control_net":["17",0],"type":"canny/lineart/anime_lineart/mlsd"}},
 "6":{"class_type":"CLIPTextEncode","inputs":{"text":POS,"clip":["4",1]}},
 "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
 "14":{"class_type":"ControlNetApplyAdvanced","inputs":{"strength":DEPTH,"start_percent":0,"end_percent":1,
        "image":["11",0],"control_net":["13",0],"positive":["6",0],"negative":["7",0],"vae":["4",2]}},
 "19":{"class_type":"ControlNetApplyAdvanced","inputs":{"strength":CANNY,"start_percent":0,"end_percent":0.85,
        "image":["16",0],"control_net":["18",0],"positive":["14",0],"negative":["14",1],"vae":["4",2]}},
 "15":{"class_type":"VAEEncode","inputs":{"pixels":["10",0],"vae":["4",2]}},
 "3":{"class_type":"KSampler","inputs":{"model":["4",0],"positive":["19",0],"negative":["19",1],
        "latent_image":["15",0],"seed":SEED,"steps":30,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":DENOISE}},
 "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
 "30":{"class_type":"UpscaleModelLoader","inputs":{"model_name":"RealESRGAN_x4plus.pth"}},
 "31":{"class_type":"UltimateSDUpscale","inputs":{
        "image":["8",0],"model":["4",0],"positive":["19",0],"negative":["19",1],"vae":["4",2],
        "upscale_by":2.5,"seed":SEED,"steps":18,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras",
        "denoise":0.20,"upscale_model":["30",0],"mode_type":"Linear","tile_width":1024,"tile_height":1024,
        "mask_blur":8,"tile_padding":32,"seam_fix_mode":"None","seam_fix_denoise":1.0,"seam_fix_width":64,
        "seam_fix_mask_blur":8,"seam_fix_padding":16,"force_uniform_tiles":True,"tiled_decode":True,"batch_size":1}},
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"p08_final"}},
 "40":{"class_type":"LoadImage","inputs":{"image":"p08_full.png"}},
 "41":{"class_type":"ImageUpscaleWithModel","inputs":{"upscale_model":["30",0],"image":["40",0]}},
 "42":{"class_type":"SaveImage","inputs":{"images":["41",0],"filename_prefix":"p08_protsrc"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,flush=True)
fin=prot=None
for _ in range(2400):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{}); outs=h[pid].get("outputs",{})
        if "32" in outs and outs["32"].get("images") and "42" in outs and outs["42"].get("images"):
            fin=outs["32"]["images"][0]; prot=outs["42"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not fin: print("TIMEOUT"); sys.exit(1)
fetch(fin, r"C:\comfy_dl\_p08_real.png")
fetch(prot, r"C:\comfy_dl\_p08_protsrc.png")
real=Image.open(r"C:\comfy_dl\_p08_real.png").convert("RGB")
prot=Image.open(r"C:\comfy_dl\_p08_protsrc.png").convert("RGB")
print("REALISM",real.size,"PROTSRC",prot.size,flush=True)
real.save(RENDERS+r"\p08_realism_nostair.png")

# ---- protect staircase + planter + right panel (right block) ----
if prot.size!=real.size: prot=prot.resize(real.size,Image.LANCZOS)
W2,H2=real.size
x0=int(0.68*W2); y0=0; x1=W2; y1=H2
mask=Image.new("L",real.size,0)
ImageDraw.Draw(mask).rectangle((x0,y0,x1,y1),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(100))
protected=Image.composite(prot,real,mask)
protected.save(RENDERS+r"\p08_protected_raw.png")

# ---- photographic grade w/ shadow lift (recovers dark right side, no geometry change) ----
a=np.asarray(protected).astype(np.float32)/255.0
a=np.power(a,0.86)                 # gamma shadow lift (dark staircase/right recovers most)
a[...,0]*=1.006; a[...,2]*=0.996   # whisper warm WB
a=(a-0.5)*1.05+0.5                 # gentle S-curve
hi=0.86; a=np.where(a>hi, hi+(a-hi)*0.6, a)  # highlight rolloff (tame bright window)
a=np.clip(a,0,1)
gimg=Image.fromarray((a*255).astype(np.uint8),"RGB")
gimg=ImageEnhance.Color(gimg).enhance(1.05)
gimg=gimg.filter(ImageFilter.UnsharpMask(radius=55,percent=10,threshold=3))
gimg=gimg.filter(ImageFilter.UnsharpMask(radius=1.4,percent=35,threshold=3))
b=np.asarray(gimg).astype(np.float32)/255.0
yy,xx=np.mgrid[0:H2,0:W2].astype(np.float32)
d=np.sqrt(((xx-W2/2)/(W2/2))**2+((yy-H2/2)/(H2/2))**2)/np.sqrt(2)
b=np.clip(b*(1.0-0.05*np.clip(d,0,1)**2.4)[...,None],0,1)
final=Image.fromarray((b*255).astype(np.uint8),"RGB")
final.save(RENDERS+r"\p08_final.png")
final.save(INP+r"\p08_final.png")
print("FINAL",final.size,flush=True)

# ---- proofs ----
try: font=ImageFont.truetype("arial.ttf",16)
except: font=ImageFont.load_default()
# staircase geometry proof: original(clean) vs final (graded) in protected zone
cx0,cy0,cx1,cy1=int(0.70*W2),int(0.06*H2),int(0.99*W2),int(0.80*H2)
co=prot.crop((cx0,cy0,cx1,cy1)); cp=final.crop((cx0,cy0,cx1,cy1))
BW=460
def rs(im): return im.resize((BW,int(BW*im.size[1]/im.size[0])),Image.LANCZOS)
co2,cp2=rs(co),rs(cp); lab=24; gap=18
cv=Image.new("RGB",(BW*2+gap,max(co2.size[1],cp2.size[1])+lab),(18,18,20)); dr=ImageDraw.Draw(cv)
dr.text((6,4),"ESCADA original",fill=(230,230,230),font=font)
dr.text((BW+gap+6,4),"ESCADA no resultado (geometria igual, so luz)",fill=(210,255,210),font=font)
cv.paste(co2,(0,lab)); cv.paste(cp2,(BW+gap,lab)); cv.save(RENDERS+r"\p08_stair_proof.png")
# before/after
TW=940
rows=[(src,"08.png ORIGINAL (cru)"),(final,"08 FOTORREALISTA (escada protegida + grade)")]
disp=[(im.resize((TW,int(TW*im.size[1]/im.size[0])),Image.LANCZOS),l) for im,l in rows]
gp=26; Ht=sum(d.size[1] for d,_ in disp)+(gp+lab)*len(disp)
cv2=Image.new("RGB",(TW,Ht),(18,18,20)); dr2=ImageDraw.Draw(cv2); y=0
for d,l in disp:
    dr2.text((6,y+4),l,fill=(240,240,240),font=font); cv2.paste(d,(0,y+lab)); y+=d.size[1]+lab+gp
cv2.save(RENDERS+r"\p08_compare.png")
print("proofs saved",flush=True)
