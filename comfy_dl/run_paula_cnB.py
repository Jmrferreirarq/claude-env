# Paula Silva exterior — Caminho B (ControlNet depth+canny) sobre o clay. Tranca a RAMPA.
import json, urllib.request, urllib.parse, time, sys
from PIL import Image

SRV="http://127.0.0.1:8188"
SEED=51234
DEPTH=0.85; CANNY=0.60; DENOISE=0.62   # source CLAY: denoise alto p/ realismo, depth forte tranca a rampa
INP=r"C:\ComfyUI_windows_portable\ComfyUI\input"
OUT=r"C:\Users\José Ferreira\Nanobana\renders\paulasilva_cnB.png"

POS=("high-end photoreal exterior architectural photograph of a two-storey single-family house, full-frame 35mm. "
 "Keep the EXACT building geometry, roof shape and slope, window and sliding-door positions, garden layout, "
 "boundary walls and especially the SLOPED ACCESS RAMP descending on the right side next to the wall - keep the "
 "ramp inclined, do NOT flatten it to level ground. Real project finishes: walls in medium grey mineral render; "
 "roof in matte anthracite flat ceramic tiles; window/door reveals and slatted screens in light natural wood; "
 "metalwork and gates matte black; side retaining walls in exposed concrete; real green mown lawn; light grey "
 "concrete paving on the descending access ramp. Natural daylight, soft realistic shadows, partly cloudy real sky, "
 "realistic materials, slightly warm white balance.")
NEG=("flattened ramp, level ground, removed slope, horizontal driveway, distorted geometry, changed layout, "
 "extra buildings, neighbouring houses, added trees, cars, people, garden furniture, cartoon, cgi, 3d render look, "
 "plastic, lowres, blurry, oversaturated, watermark, text")

base=Image.open(INP+r"\paula_ext_1536.png"); print("base",base.size,flush=True)
def post(p,pl):
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=json.dumps(pl).encode(),headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())
def fetch(o,dest):
    q=urllib.parse.urlencode({"filename":o["filename"],"subfolder":o.get("subfolder",""),"type":o.get("type","output")})
    open(dest,"wb").write(urllib.request.urlopen(SRV+"/view?"+q).read())

CN="controlnet_union_sdxl_promax.safetensors"
g={
 "4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
 "10":{"class_type":"LoadImage","inputs":{"image":"paula_ext_1536.png"}},
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
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"paula_cnB"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,flush=True)
fin=None
for _ in range(3000):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{}); outs=h[pid].get("outputs",{})
        if "32" in outs and outs["32"].get("images"): fin=outs["32"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)[:1500]); sys.exit(2)
    time.sleep(1)
if not fin: print("TIMEOUT"); sys.exit(1)
fetch(fin,OUT); print("SAVED",OUT,Image.open(OUT).size,flush=True)
