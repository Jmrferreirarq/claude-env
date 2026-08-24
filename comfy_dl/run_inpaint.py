import json, urllib.request, urllib.parse, time, sys
from PIL import Image

SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
TAG    = sys.argv[1]
DENOISE= float(sys.argv[2])
POS    = sys.argv[3]
NEG    = sys.argv[4]
SEED   = int(sys.argv[5]) if len(sys.argv)>5 else 12345
BASE_IN= sys.argv[6] if len(sys.argv)>6 else "cozinha_v2_handles.png"   # in ComfyUI/input
OUT_NAME=sys.argv[7] if len(sys.argv)>7 else None

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())

region_img = TAG+"_region_up.png"
mask_img   = TAG+"_region_mask_up.png"
g={
 "1":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
 "2":{"class_type":"LoadImage","inputs":{"image":region_img}},
 "3":{"class_type":"LoadImage","inputs":{"image":mask_img}},
 "4":{"class_type":"ImageToMask","inputs":{"image":["3",0],"channel":"red"}},
 "5":{"class_type":"VAEEncode","inputs":{"pixels":["2",0],"vae":["1",2]}},
 "6":{"class_type":"SetLatentNoiseMask","inputs":{"samples":["5",0],"mask":["4",0]}},
 "7":{"class_type":"CLIPTextEncode","inputs":{"text":POS,"clip":["1",1]}},
 "8":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["1",1]}},
 "9":{"class_type":"KSampler","inputs":{"model":["1",0],"positive":["7",0],"negative":["8",0],
       "latent_image":["6",0],"seed":SEED,"steps":30,"cfg":6.0,
       "sampler_name":"dpmpp_2m","scheduler":"karras","denoise":DENOISE}},
 "10":{"class_type":"VAEDecode","inputs":{"samples":["9",0],"vae":["1",2]}},
 "11":{"class_type":"SaveImage","inputs":{"images":["10",0],"filename_prefix":TAG+"_inpaint"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,flush=True)
out=None
for _ in range(900):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{})
        if "11" in h[pid].get("outputs",{}) and h[pid]["outputs"]["11"].get("images"):
            out=h[pid]["outputs"]["11"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not out: print("TIMEOUT"); sys.exit(1)
q=urllib.parse.urlencode({"filename":out["filename"],"subfolder":out.get("subfolder",""),"type":out.get("type","output")})
data=urllib.request.urlopen(SRV+"/view?"+q).read()
RES=r"C:\comfy_dl\_"+TAG+"_result_up.png"; open(RES,"wb").write(data)
print("result",RES,len(data),flush=True)

meta=json.load(open(r"C:\comfy_dl\\"+TAG+"_meta.json"))
xs0,ys0,rw,rh=meta["xs0"],meta["ys0"],meta["rw"],meta["rh"]
full=Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\\"+BASE_IN).convert("RGB")
gen=Image.open(RES).convert("RGB").resize((rw,rh),Image.LANCZOS)
mask=Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\\"+mask_img).convert("L").resize((rw,rh),Image.LANCZOS)
region_orig=full.crop((xs0,ys0,xs0+rw,ys0+rh))
comp=Image.composite(gen,region_orig,mask)
full.paste(comp,(xs0,ys0))

if OUT_NAME:
    o1=r"C:\Users\José Ferreira\Nanobana\renders\\"+OUT_NAME
    o2=r"C:\ComfyUI_windows_portable\ComfyUI\input\\"+OUT_NAME
    full.save(o1); full.save(o2); print("SAVED",o1,flush=True)

pad=30
bx0=max(0,xs0-pad);by0=max(0,ys0-pad);bx1=min(full.width,xs0+rw+pad);by1=min(full.height,ys0+rh+pad)
Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\\"+BASE_IN).convert("RGB").crop((bx0,by0,bx1,by1)).save(r"C:\comfy_dl\_"+TAG+"_before.png")
full.crop((bx0,by0,bx1,by1)).save(r"C:\comfy_dl\_"+TAG+"_after.png")
print("DONE",full.size,flush=True)
