import json, urllib.request, urllib.parse, time, os, sys

SRV = "http://127.0.0.1:8188"
CKPT = "RealVisXL_V5.0_fp16.safetensors"

def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(SRV+path, data=data, headers={"Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(req).read())

def get(path):
    return json.loads(urllib.request.urlopen(SRV+path).read())

# ---- build inpaint graph (region crop, low-ish denoise recolor) ----
POS = "matte black metal bar handle on cabinet, dark anthracite hardware, satin black finish"
NEG = "brass, gold, chrome, silver, yellow, shiny gold, reflective metal"
g = {
 "1": {"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
 "2": {"class_type":"LoadImage","inputs":{"image":"h_region_up.png"}},
 "3": {"class_type":"LoadImage","inputs":{"image":"h_region_mask_up.png"}},
 "4": {"class_type":"ImageToMask","inputs":{"image":["3",0],"channel":"red"}},
 "5": {"class_type":"VAEEncode","inputs":{"pixels":["2",0],"vae":["1",2]}},
 "6": {"class_type":"SetLatentNoiseMask","inputs":{"samples":["5",0],"mask":["4",0]}},
 "7": {"class_type":"CLIPTextEncode","inputs":{"text":POS,"clip":["1",1]}},
 "8": {"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["1",1]}},
 "9": {"class_type":"KSampler","inputs":{
        "model":["1",0],"positive":["7",0],"negative":["8",0],"latent_image":["6",0],
        "seed":777001,"steps":28,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":0.55}},
 "10":{"class_type":"VAEDecode","inputs":{"samples":["9",0],"vae":["1",2]}},
 "11":{"class_type":"SaveImage","inputs":{"images":["10",0],"filename_prefix":"h_inpaint_out"}},
}
r = post("/prompt", {"prompt": g})
pid = r["prompt_id"]
print("submitted", pid, flush=True)

# ---- poll ----
out_img = None
for _ in range(600):
    h = get("/history/"+pid)
    if pid in h:
        outs = h[pid].get("outputs", {})
        if "11" in outs and outs["11"].get("images"):
            out_img = outs["11"]["images"][0]
            break
        if h[pid].get("status",{}).get("status_str")=="error":
            print("ERROR", json.dumps(h[pid].get("status"))); sys.exit(1)
    time.sleep(1)
if not out_img:
    print("TIMEOUT"); sys.exit(1)
print("done", out_img, flush=True)

# ---- fetch result bytes ----
q = urllib.parse.urlencode({"filename":out_img["filename"],"subfolder":out_img.get("subfolder",""),"type":out_img.get("type","output")})
res = urllib.request.urlopen(SRV+"/view?"+q).read()
RES_PATH = r"C:\comfy_dl\_h_inpaint_result_up.png"
open(RES_PATH,"wb").write(res)
print("saved result", RES_PATH, len(res), flush=True)

# ---- composite back onto full-res original ----
from PIL import Image, ImageFilter
meta = json.load(open(r"C:\comfy_dl\h_meta.json"))
xs0,ys0,rw,rh,Z = meta["xs0"],meta["ys0"],meta["rw"],meta["rh"],meta["Z"]

full = Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png").convert("RGB")
gen_up = Image.open(RES_PATH).convert("RGB").resize((rw,rh), Image.LANCZOS)   # back to region size
# region-size mask (use the small mask we saved, or rebuild from up mask)
mask_up = Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\h_region_mask_up.png").convert("L").resize((rw,rh), Image.LANCZOS)

region_orig = full.crop((xs0,ys0,xs0+rw,ys0+rh))
comp = Image.composite(gen_up, region_orig, mask_up)
full.paste(comp, (xs0,ys0))

OUT1 = r"C:\Users\José Ferreira\Nanobana\renders\cozinha_v2_handles.png"
OUT2 = r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_v2_handles.png"
full.save(OUT1); full.save(OUT2)
print("COMPOSITED", OUT1, full.size, flush=True)

# ---- before/after crops of the handle zone for display ----
pad=30
bx0=max(0,xs0-pad); by0=max(0,ys0-pad); bx1=min(full.width,xs0+rw+pad); by1=min(full.height,ys0+rh+pad)
before = Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png").convert("RGB").crop((bx0,by0,bx1,by1))
after  = full.crop((bx0,by0,bx1,by1))
before.save(r"C:\comfy_dl\_h_before.png"); after.save(r"C:\comfy_dl\_h_after.png")
print("BA", before.size, flush=True)
