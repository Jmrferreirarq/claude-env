import json, urllib.request, urllib.parse, time, sys
from PIL import Image

SRV="http://127.0.0.1:8188"
SEED=70414
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

# prep 1536-wide input
src=Image.open(r"C:\Users\José Ferreira\Nanobana\renders\06_cozinha_p4.png").convert("RGB")
W=1536; H=round(W*src.size[1]/src.size[0]/8)*8
src.resize((W,H),Image.LANCZOS).save(r"C:\ComfyUI_windows_portable\ComfyUI\input\enscape_p4_1536.png")
print("base input",W,H,flush=True)

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())

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
 "14":{"class_type":"ControlNetApplyAdvanced","inputs":{"strength":0.6,"start_percent":0,"end_percent":1,
        "image":["11",0],"control_net":["13",0],"positive":["6",0],"negative":["7",0],"vae":["4",2]}},
 "19":{"class_type":"ControlNetApplyAdvanced","inputs":{"strength":0.85,"start_percent":0,"end_percent":0.85,
        "image":["16",0],"control_net":["18",0],"positive":["14",0],"negative":["14",1],"vae":["4",2]}},
 "15":{"class_type":"VAEEncode","inputs":{"pixels":["10",0],"vae":["4",2]}},
 "3":{"class_type":"KSampler","inputs":{"model":["4",0],"positive":["19",0],"negative":["19",1],
        "latent_image":["15",0],"seed":SEED,"steps":30,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":0.35}},
 "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
 "20":{"class_type":"SaveImage","inputs":{"images":["8",0],"filename_prefix":"enscape_p4_base"}},
 "30":{"class_type":"UpscaleModelLoader","inputs":{"model_name":"RealESRGAN_x4plus.pth"}},
 "31":{"class_type":"UltimateSDUpscale","inputs":{
        "image":["8",0],"model":["4",0],"positive":["19",0],"negative":["19",1],"vae":["4",2],
        "upscale_by":2.0,"seed":SEED,"steps":18,"cfg":6.0,"sampler_name":"dpmpp_2m","scheduler":"karras",
        "denoise":0.20,"upscale_model":["30",0],"mode_type":"Linear","tile_width":1024,"tile_height":1024,
        "mask_blur":8,"tile_padding":32,"seam_fix_mode":"None","seam_fix_denoise":1.0,"seam_fix_width":64,
        "seam_fix_mask_blur":8,"seam_fix_padding":16,"force_uniform_tiles":True,"tiled_decode":True,"batch_size":1}},
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"enscape_p4_final"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,"seed",SEED,flush=True)
base=fin=None
for _ in range(1200):
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
if base: fetch(base, r"C:\comfy_dl\_p4_base.png")
fetch(fin, r"C:\comfy_dl\_p4_final.png")
out1=r"C:\Users\José Ferreira\Nanobana\renders\cozinha_enscape_v1.png"
out2=r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_enscape_v1.png"
Image.open(r"C:\comfy_dl\_p4_final.png").save(out1); Image.open(r"C:\comfy_dl\_p4_final.png").save(out2)
print("SAVED",out1, Image.open(out1).size,flush=True)
