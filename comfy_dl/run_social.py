import json, urllib.request, urllib.parse, time, sys
from PIL import Image

SRV="http://127.0.0.1:8188"
SEED=30314
POS=("high-end photoreal interior photograph, keep architecture, openings, layout, the staircase "
 "and tile sizes exactly; move/remove nothing; rich realistic materials, magazine quality, full-frame 35mm. "
 "Open-plan living-dining-kitchen. Warm off-white matte walls, high white ceiling with recessed downlights. "
 "Two large pale grey conical pendant lamps hanging low over the living area. Left: long low dark walnut media "
 "console against the wall. Charcoal grey fabric sofa, round wood coffee table, one lime chartreuse tub armchair. "
 "Dining: medium-oak wood-top rectangular table with white moulded shell chairs on wood-and-metal legs. Right: "
 "kitchen with a dark vertical-slatted island base and a pale light-stone quartz worktop, black induction hob, "
 "brushed stainless steel sink; tall white cabinetry with integrated appliances behind. Open floating staircase "
 "centre with white stringer structure and medium-wood treads and glass railing; a small green planter bed at its "
 "foot. Greige large-format porcelain floor tiles; keep existing skirting. Bright soft even natural daylight, airy, "
 "gentle soft shadows.")
NEG=("cartoon, cgi, plastic, 3d render look, lowres, blurry, deformed, distorted perspective, extra windows, "
 "extra stairs, added doors, changed layout, blue island, glass dining table, cream chairs, wood plank floor, "
 "brass tap, gold tap, flowers, monstera, lavender, watermark, text, people")

# prep already done by caller, but re-prep to be safe
src=Image.open(r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\03 Zona Social.jpg").convert("RGB")
W=1536; H=round(W*src.size[1]/src.size[0]/8)*8
src.resize((W,H),Image.LANCZOS).save(r"C:\ComfyUI_windows_portable\ComfyUI\input\social03_1536.png")
print("base input",W,H,flush=True)

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())

CN="controlnet_union_sdxl_promax.safetensors"
g={
 "4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
 "10":{"class_type":"LoadImage","inputs":{"image":"social03_1536.png"}},
 "11":{"class_type":"DepthAnythingV2Preprocessor","inputs":{"ckpt_name":"depth_anything_v2_vitl.pth","resolution":1024,"image":["10",0]}},
 "16":{"class_type":"CannyEdgePreprocessor","inputs":{"high_threshold":200,"low_threshold":100,"resolution":1024,"image":["10",0]}},
 "12":{"class_type":"ControlNetLoader","inputs":{"control_net_name":CN}},
 "13":{"class_type":"SetUnionControlNetType","inputs":{"control_net":["12",0],"type":"depth"}},
 "17":{"class_type":"ControlNetLoader","inputs":{"control_net_name":CN}},
 "18":{"class_type":"SetUnionControlNetType","inputs":{"control_net":["17",0],"type":"canny/lineart/anime_lineart/mlsd"}},
 "6":{"class_type":"CLIPTextEncode","inputs":{"text":POS,"clip":["4",1]}},
 "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
 "14":{"class_type":"ControlNetApplyAdvanced","inputs":{"strength":0.6,"start_percent":0,"end_percent":1,
        "image":["11",0],"control_net":["13",0],"positive":["6",0],"negative":["7",0],"vae":["4",2]}},
 "19":{"class_type":"ControlNetApplyAdvanced","inputs":{"strength":0.85,"start_percent":0,"end_percent":0.85,
        "image":["16",0],"control_net":["18",0],"positive":["14",0],"negative":["14",1],"vae":["4",2]}},
 "15":{"class_type":"VAEEncode","inputs":{"pixels":["10",0],"vae":["4",2]}},
 "3":{"class_type":"KSampler","inputs":{"model":["4",0],"positive":["19",0],"negative":["19",1],
        "latent_image":["15",0],"seed":SEED,"steps":30,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":0.35}},
 "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
 "20":{"class_type":"SaveImage","inputs":{"images":["8",0],"filename_prefix":"social03_base"}},
 "30":{"class_type":"UpscaleModelLoader","inputs":{"model_name":"RealESRGAN_x4plus.pth"}},
 "31":{"class_type":"UltimateSDUpscale","inputs":{
        "image":["8",0],"model":["4",0],"positive":["19",0],"negative":["19",1],"vae":["4",2],
        "upscale_by":2.0,"seed":SEED,"steps":18,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras",
        "denoise":0.20,"upscale_model":["30",0],"mode_type":"Linear","tile_width":1024,"tile_height":1024,
        "mask_blur":8,"tile_padding":32,"seam_fix_mode":"None","seam_fix_denoise":1.0,"seam_fix_width":64,
        "seam_fix_mask_blur":8,"seam_fix_padding":16,"force_uniform_tiles":True,"tiled_decode":True,"batch_size":1}},
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"social03_final"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,"seed",SEED,flush=True)
base=fin=None
for _ in range(1800):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{}); outs=h[pid].get("outputs",{})
        if "32" in outs and outs["32"].get("images"):
            base=outs.get("20",{}).get("images",[None])[0]; fin=outs["32"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not fin: print("TIMEOUT"); sys.exit(1)
def fetch(o,dest):
    q=urllib.parse.urlencode({"filename":o["filename"],"subfolder":o.get("subfolder",""),"type":o.get("type","output")})
    open(dest,"wb").write(urllib.request.urlopen(SRV+"/view?"+q).read())
if base: fetch(base, r"C:\comfy_dl\_social_base.png")
fetch(fin, r"C:\comfy_dl\_social_final.png")
out1=r"C:\Users\José Ferreira\Nanobana\renders\social_zona_v1.png"
out2=r"C:\ComfyUI_windows_portable\ComfyUI\input\social_zona_v1.png"
Image.open(r"C:\comfy_dl\_social_final.png").save(out1); Image.open(r"C:\comfy_dl\_social_final.png").save(out2)
print("SAVED",out1, Image.open(out1).size,flush=True)
