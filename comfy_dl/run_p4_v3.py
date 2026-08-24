import json, urllib.request, urllib.parse, time, sys, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRV="http://127.0.0.1:8188"
SEED=70414
DEPTH=0.70; CANNY=0.45; DENOISE=0.65
SRC=r"C:\Users\José Ferreira\Nanobana\renders\06_cozinha_p4.png"
RENDERS=r"C:\Users\José Ferreira\Nanobana\renders"
INP=r"C:\ComfyUI_windows_portable\ComfyUI\input"
print("PARAMS depth",DEPTH,"canny",CANNY,"denoise",DENOISE,"seed",SEED,flush=True)

POS=("high-end photoreal interior photograph, keep architecture, openings, layout, the staircase "
 "and tile sizes exactly; move/remove nothing; rich realistic materials, magazine quality, full-frame 35mm. "
 "Open-plan kitchen-living. Warm off-white matte walls and sloped ceiling with recessed downlights. "
 "White kitchen island with a pale light-stone quartz worktop, black induction hob and a wood chopping board; "
 "brushed stainless steel sink and tap on the near side. Three pale cream conical pendant lamps on thin black cords "
 "over the island. Back wall: wall-mounted black flat TV above a long low light-oak media console. Oatmeal fabric "
 "sofa and one terracotta armchair. Light oak dining table with light oak chairs; a leafy green plant. Large sliding "
 "glass wall to a green garden, with pale sheer translucent curtains drawn to the sides. Staircase on the right: "
 "solid oak treads with white structure and white wall, closed steps. Greige large-format porcelain floor tiles; "
 "keep existing skirting. Bright soft even natural daylight, airy, gentle soft shadows.")
NEG=("cartoon, cgi, plastic, 3d render look, lowres, blurry, deformed, distorted perspective, extra windows, "
 "extra stairs, added doors, changed layout, green curtains, green chairs, bar stools, slatted tv wall, watermark, text, people")

src=Image.open(SRC).convert("RGB")
W=1536; H=round(W*src.size[1]/src.size[0]/8)*8
src.resize((W,H),Image.LANCZOS).save(INP+r"\enscape_p4_1536.png")
src.save(INP+r"\enscape_p4_full.png")   # full-res copy for clean protection upscale
print("base input",W,H,flush=True)

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
 "10":{"class_type":"LoadImage","inputs":{"image":"enscape_p4_1536.png"}},
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
        "upscale_by":2.0,"seed":SEED,"steps":18,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras",
        "denoise":0.20,"upscale_model":["30",0],"mode_type":"Linear","tile_width":1024,"tile_height":1024,
        "mask_blur":8,"tile_padding":32,"seam_fix_mode":"None","seam_fix_denoise":1.0,"seam_fix_width":64,
        "seam_fix_mask_blur":8,"seam_fix_padding":16,"force_uniform_tiles":True,"tiled_decode":True,"batch_size":1}},
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"p4v3_final"}},
 # clean (non-generative) upscale of the ORIGINAL, for staircase protection
 "40":{"class_type":"LoadImage","inputs":{"image":"enscape_p4_full.png"}},
 "41":{"class_type":"ImageUpscaleWithModel","inputs":{"upscale_model":["30",0],"image":["40",0]}},
 "42":{"class_type":"SaveImage","inputs":{"images":["41",0],"filename_prefix":"p4v3_protsrc"}},
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
fetch(fin, r"C:\comfy_dl\_p4v3_real.png")
fetch(prot, r"C:\comfy_dl\_p4v3_protsrc.png")
real=Image.open(r"C:\comfy_dl\_p4v3_real.png").convert("RGB")
prot=Image.open(r"C:\comfy_dl\_p4v3_protsrc.png").convert("RGB")
print("REALISM FINAL",real.size,"  PROT SRC",prot.size,flush=True)
real.save(RENDERS+r"\cozinha_p4v3_nostair.png")  # realism only, before protection

# ---- HARD STAIRCASE PROTECTION (right side) ----
if prot.size!=real.size: prot=prot.resize(real.size,Image.LANCZOS)
W2,H2=real.size
# staircase + white structure on the right (fractions of full image)
x0=int(0.62*W2); y0=int(0.27*H2); x1=W2; y1=int(0.87*H2)
mask=Image.new("L",real.size,0)
ImageDraw.Draw(mask).rectangle((x0,y0,x1,y1),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(90))
protected=Image.composite(prot,real,mask)
protected.save(RENDERS+r"\cozinha_p4v3_final.png")
protected.save(INP+r"\cozinha_p4v3_final.png")
print("PROTECTED",protected.size,flush=True)

# ---- staircase proof: original(clean) vs result ----
cx0,cy0,cx1,cy1=int(0.64*W2),int(0.29*H2),int(0.99*W2),int(0.86*H2)
co=prot.crop((cx0,cy0,cx1,cy1)); cp=protected.crop((cx0,cy0,cx1,cy1))
BW=520
def rs(im): return im.resize((BW,int(BW*im.size[1]/im.size[0])),Image.LANCZOS)
co2,cp2=rs(co),rs(cp)
try: font=ImageFont.truetype("arial.ttf",16)
except: font=ImageFont.load_default()
lab=24; gap=18
cv=Image.new("RGB",(BW*2+gap,max(co2.size[1],cp2.size[1])+lab),(18,18,20)); dr=ImageDraw.Draw(cv)
dr.text((6,4),"ESCADA original (limpa)",fill=(230,230,230),font=font)
dr.text((BW+gap+6,4),"ESCADA no resultado (protegida)",fill=(210,255,210),font=font)
cv.paste(co2,(0,lab)); cv.paste(cp2,(BW+gap,lab))
cv.save(RENDERS+r"\cozinha_p4v3_stair_proof.png")

# ---- before / after (original vs final) ----
TW=940
rows=[(src,"ORIGINAL Enscape p4"),(protected,"COZINHA p4 v3 — realismo + escada protegida")]
disp=[(im.resize((TW,int(TW*im.size[1]/im.size[0])),Image.LANCZOS),l) for im,l in rows]
gap=26; lab=26; Ht=sum(d.size[1] for d,_ in disp)+(gap+lab)*len(disp)
cv2=Image.new("RGB",(TW,Ht),(18,18,20)); dr2=ImageDraw.Draw(cv2); y=0
for d,l in disp:
    dr2.text((6,y+4),l,fill=(240,240,240),font=font); cv2.paste(d,(0,y+lab)); y+=d.size[1]+lab+gap
cv2.save(RENDERS+r"\cozinha_p4v3_compare.png")
print("proofs saved",flush=True)
