import json, urllib.request, urllib.parse, time, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRV="http://127.0.0.1:8188"
SEED=60606
DEPTH=0.60; CANNY=0.85; DENOISE=0.35     # CONSERVATIVE recipe (proven faithful on kitchen + 08)
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\06.png"
RENDERS=r"C:\Users\José Ferreira\Nanobana\renders"
INP=r"C:\ComfyUI_windows_portable\ComfyUI\input"
print("PARAMS depth",DEPTH,"canny",CANNY,"denoise",DENOISE,"seed",SEED,flush=True)

# user's own faithful prompt (verbatim intent)
POS=("real professional interior architecture photograph, absolute fidelity to the original camera angle, framing "
 "and perspective; do not change the architecture, layout, staircase, kitchen, cabinetry or proportions. Daytime "
 "scene with abundant natural light from the right and through the central void, clear sky, soft well-defined natural "
 "shadows across floor, dining table and island, plus the existing recessed lighting. DSLR RAW photography look, high "
 "sharpness, natural depth of field, balanced colors, extreme realism, natural micro-contrast, real PBR textures, "
 "zero CGI appearance. Exact materials from the source: light wood plank flooring, vertical wood slat paneling, black "
 "metal staircase with light wood treads and glass railing beside a mirror wall, white cabinetry with brass handles, "
 "light stone countertop and backsplash, navy-blue island base with three white bar stools and a brass tap, Nespresso "
 "machine and fruit bowl, black track lights and black pendants, light curtains, indoor garden under the stairs with "
 "white pebbles, lavender, orange gerbera and tropical foliage, glass-top dining table with cream chairs and a grey "
 "tray. Subtle elegant styling, clean surfaces, warm contemporary atmosphere, editorial interior photography, no "
 "halos, no oversharpening, no artificial look.")
NEG=("cartoon, cgi, plastic, 3d render look, lowres, blurry, deformed, distorted perspective, changed layout, "
 "changed staircase, extra stairs, distorted railing, warped mirror, changed materials, recoloured surfaces, "
 "extra windows, added doors, oversaturated, watermark, text, people")

src=Image.open(SRC).convert("RGB")
print("SRC",src.size,flush=True)
W=1536; H=round(W*src.size[1]/src.size[0]/8)*8
src.resize((W,H),Image.LANCZOS).save(INP+r"\p06_1536.png")
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
 "10":{"class_type":"LoadImage","inputs":{"image":"p06_1536.png"}},
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
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"p06f_final"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,flush=True)
fin=None
for _ in range(2400):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{}); outs=h[pid].get("outputs",{})
        if "32" in outs and outs["32"].get("images"): fin=outs["32"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not fin: print("TIMEOUT"); sys.exit(1)
fetch(fin, r"C:\comfy_dl\_p06f.png")
res=Image.open(r"C:\comfy_dl\_p06f.png").convert("RGB")
print("RESULT",res.size,flush=True)

# ultra-subtle clarity only (no tone/colour change) — 06 is already well lit
res=res.filter(ImageFilter.UnsharpMask(radius=50,percent=6,threshold=3))
res.save(RENDERS+r"\p06_faithful.png")
res.save(INP+r"\p06_faithful.png")
print("SAVED",res.size,flush=True)

# ---- VERIFY: staircase + mirror region (center-left), original vs result ----
try: font=ImageFont.truetype("arial.ttf",16)
except: font=ImageFont.load_default()
ow,oh=src.size; rw,rh=res.size
fx0,fy0,fx1,fy1=0.16,0.10,0.45,0.82
oc=src.crop((int(fx0*ow),int(fy0*oh),int(fx1*ow),int(fy1*oh)))
rc=res.crop((int(fx0*rw),int(fy0*rh),int(fx1*rw),int(fy1*rh)))
BW=470
def rs(im): return im.resize((BW,int(BW*im.size[1]/im.size[0])),Image.LANCZOS)
oc2,rc2=rs(oc),rs(rc); lab=24; gap=18
cv=Image.new("RGB",(BW*2+gap,max(oc2.size[1],rc2.size[1])+lab),(18,18,20)); dr=ImageDraw.Draw(cv)
dr.text((6,4),"ESCADA+ESPELHO original",fill=(230,230,230),font=font)
dr.text((BW+gap+6,4),"resultado (denoise 0.35)",fill=(210,255,210),font=font)
cv.paste(oc2,(0,lab)); cv.paste(rc2,(BW+gap,lab)); cv.save(RENDERS+r"\p06_faithful_stair_check.png")
# before/after
TW=940
rows=[(src,"06 ORIGINAL"),(res,"06 FIEL — receita conservadora 0.35 + prompt do utilizador")]
disp=[(im.resize((TW,int(TW*im.size[1]/im.size[0])),Image.LANCZOS),l) for im,l in rows]
gp=26; Ht=sum(d.size[1] for d,_ in disp)+(gp+lab)*len(disp)
cv2=Image.new("RGB",(TW,Ht),(18,18,20)); dr2=ImageDraw.Draw(cv2); y=0
for d,l in disp:
    dr2.text((6,y+4),l,fill=(240,240,240),font=font); cv2.paste(d,(0,y+lab)); y+=d.size[1]+lab+gp
cv2.save(RENDERS+r"\p06_faithful_compare.png")
print("proofs saved",flush=True)
