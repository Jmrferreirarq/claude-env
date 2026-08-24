import json, urllib.request, urllib.parse, time, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRV="http://127.0.0.1:8188"
SEED=60606
DEPTH=0.75; CANNY=0.70; DENOISE=0.40
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\06.png"
RENDERS=r"C:\Users\José Ferreira\Nanobana\renders"
print("PARAMS depth",DEPTH,"canny",CANNY,"denoise",DENOISE,flush=True)

POS=("high-end photoreal interior photograph, magazine quality, full-frame 35mm; keep architecture, layout, the "
 "staircase, materials and finishes EXACTLY as in the source, move/remove nothing, do not change any colour or "
 "material. Open-plan social area: warm off-white matte walls, white ceiling with recessed downlights, light oak "
 "plank floor. Open floating staircase with black steel stringer, light oak treads and a full-height glass railing "
 "beside a mirror wall. Interior planter garden on white gravel (monstera, purple lavender, orange gerbera, ferns, "
 "succulents) against a vertical slatted-oak feature wall. Kitchen with white and oak cabinetry, a navy-blue island "
 "with a white quartz waterfall worktop, three white bar stools, a brass tap, Nespresso machine and fruit bowl, "
 "under-cabinet LED, black track lights and black pendant lamps. Glass-top dining table with cream upholstered "
 "chairs and a grey tray of candles. Bright soft even natural daylight, gentle soft shadows.")
NEG=("cartoon, cgi, plastic, 3d render look, lowres, blurry, deformed, distorted perspective, changed layout, "
 "changed staircase, extra stairs, distorted staircase, changed materials, recoloured surfaces, extra windows, "
 "added doors, oversaturated, watermark, text, people")

src=Image.open(SRC).convert("RGB")
W=1536; H=round(W*src.size[1]/src.size[0]/8)*8
src.resize((W,H),Image.LANCZOS).save(r"C:\ComfyUI_windows_portable\ComfyUI\input\social06_src.png")
print("base",W,H,flush=True)

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())

CN="controlnet_union_sdxl_promax.safetensors"
g={
 "4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
 "10":{"class_type":"LoadImage","inputs":{"image":"social06_src.png"}},
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
 "19":{"class_type":"ControlNetApplyAdvanced","inputs":{"strength":CANNY,"start_percent":0,"end_percent":1,
        "image":["16",0],"control_net":["18",0],"positive":["14",0],"negative":["14",1],"vae":["4",2]}},
 "15":{"class_type":"VAEEncode","inputs":{"pixels":["10",0],"vae":["4",2]}},
 "3":{"class_type":"KSampler","inputs":{"model":["4",0],"positive":["19",0],"negative":["19",1],
        "latent_image":["15",0],"seed":SEED,"steps":30,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":DENOISE}},
 "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
 "30":{"class_type":"UpscaleModelLoader","inputs":{"model_name":"RealESRGAN_x4plus.pth"}},
 "31":{"class_type":"UltimateSDUpscale","inputs":{
        "image":["8",0],"model":["4",0],"positive":["6",0],"negative":["7",0],"vae":["4",2],
        "upscale_by":2.5,"seed":SEED,"steps":18,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras",
        "denoise":0.20,"upscale_model":["30",0],"mode_type":"Linear","tile_width":1024,"tile_height":1024,
        "mask_blur":8,"tile_padding":32,"seam_fix_mode":"None","seam_fix_denoise":1.0,"seam_fix_width":64,
        "seam_fix_mask_blur":8,"seam_fix_padding":16,"force_uniform_tiles":True,"tiled_decode":True,"batch_size":1}},
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"social06_real"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,flush=True)
fin=None
for _ in range(1800):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{}); outs=h[pid].get("outputs",{})
        if "32" in outs and outs["32"].get("images"): fin=outs["32"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not fin: print("TIMEOUT"); sys.exit(1)
q=urllib.parse.urlencode({"filename":fin["filename"],"subfolder":fin.get("subfolder",""),"type":fin.get("type","output")})
open(r"C:\comfy_dl\_06_real.png","wb").write(urllib.request.urlopen(SRV+"/view?"+q).read())
real=Image.open(r"C:\comfy_dl\_06_real.png").convert("RGB")
print("REALISM FINAL",real.size,flush=True)
real.save(RENDERS+r"\06_real_nostair.png")  # before staircase protection (for inspection)

# ---- HARD STAIRCASE PROTECTION: paste original (clean-upscaled) staircase region back ----
prot=Image.open(RENDERS+r"\06_upscaled_clean.png").convert("RGB")   # original, clean 2x
if prot.size!=real.size: prot=prot.resize(real.size,Image.LANCZOS)
W2,H2=real.size; sx=W2/1920.0; sy=H2/1080.0
# staircase+mirror+glass+planter region (orig 1920x1080 coords)
x0,y0,x1,y1=330,200,995,905
box=(int(x0*sx),int(y0*sy),int(x1*sx),int(y1*sy))
mask=Image.new("L",real.size,0)
ImageDraw.Draw(mask).rectangle(box,fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(60))   # feather the seam
protected=Image.composite(prot,real,mask)        # where mask=white -> original staircase pixels
protected.save(RENDERS+r"\06_real_protected.png")
protected.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\06_real_protected.png")
print("PROTECTED saved",protected.size,flush=True)

# ---- staircase crop proof: original vs protected (must be identical) ----
cx0,cy0,cx1,cy1=int(360*sx),int(230*sy),int(820*sx),int(900*sy)
co=prot.crop((cx0,cy0,cx1,cy1)); cp=protected.crop((cx0,cy0,cx1,cy1))
BW=560
def rs(im): return im.resize((BW,int(BW*im.size[1]/im.size[0])),Image.LANCZOS)
co2,cp2=rs(co),rs(cp)
try: font=ImageFont.truetype("arial.ttf",16)
except: font=ImageFont.load_default()
lab=24; gap=18
canvas=Image.new("RGB",(BW*2+gap,max(co2.size[1],cp2.size[1])+lab),(18,18,20))
dr=ImageDraw.Draw(canvas)
dr.text((6,4),"ESCADA original",fill=(230,230,230),font=font)
dr.text((BW+gap+6,4),"ESCADA no resultado (protegida)",fill=(210,255,210),font=font)
canvas.paste(co2,(0,lab)); canvas.paste(cp2,(BW+gap,lab))
canvas.save(RENDERS+r"\06_real_stair_proof.png")
print("stair proof saved",flush=True)
