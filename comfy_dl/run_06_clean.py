import json, urllib.request, urllib.parse, time, sys
from PIL import Image, ImageDraw, ImageFont

SRV="http://127.0.0.1:8188"
SRC=r"C:\Users\José Ferreira\.@ David Afonso\1 . Modelação\JPEG\2026\06.22.2026\Moradia Unifamiliar — David Afonso\Imagens Interiores\06.png"
RENDERS=r"C:\Users\José Ferreira\Nanobana\renders"

orig=Image.open(SRC).convert("RGB")
orig.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\social06_src.png")
print("SRC",orig.size,flush=True)

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())

# PURE RealESRGAN upscale (no diffusion, no grain, no grade)
g={
 "10":{"class_type":"LoadImage","inputs":{"image":"social06_src.png"}},
 "30":{"class_type":"UpscaleModelLoader","inputs":{"model_name":"RealESRGAN_x4plus.pth"}},
 "31":{"class_type":"ImageUpscaleWithModel","inputs":{"upscale_model":["30",0],"image":["10",0]}},
 "32":{"class_type":"SaveImage","inputs":{"images":["31",0],"filename_prefix":"social06_clean4x"}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,flush=True)
fin=None
for _ in range(900):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{}); outs=h[pid].get("outputs",{})
        if "32" in outs and outs["32"].get("images"): fin=outs["32"]["images"][0]; break
        if st.get("status_str")=="error": print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not fin: print("TIMEOUT"); sys.exit(1)
q=urllib.parse.urlencode({"filename":fin["filename"],"subfolder":fin.get("subfolder",""),"type":fin.get("type","output")})
open(r"C:\comfy_dl\_06_clean4x.png","wb").write(urllib.request.urlopen(SRV+"/view?"+q).read())
up4=Image.open(r"C:\comfy_dl\_06_clean4x.png").convert("RGB")
print("RealESRGAN 4x ->",up4.size,flush=True)
# downscale 4x -> 2x (3840x2160), Lanczos = clean, crisp, no grain
clean=up4.resize((orig.size[0]*2,orig.size[1]*2),Image.LANCZOS)
clean.save(RENDERS+r"\06_upscaled_clean.png")
clean.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\06_upscaled_clean.png")
print("CLEAN 2x ->",clean.size,flush=True)

# 100% crop comparison: original vs clean (same region), both shown at same display width
x0,y0,x1,y1=1180,300,1620,560
co=orig.crop((x0,y0,x1,y1))
cc=clean.crop((x0*2,y0*2,x1*2,y1*2))
TW=900
try: font=ImageFont.truetype("arial.ttf",18)
except: font=ImageFont.load_default()
rows=[(co,"ORIGINAL 06.png (1920x1080)"),(cc,"CLEAN UPSCALE (3840x2160) - RealESRGAN puro, sem grao")]
disp=[(im.resize((TW,int(TW*im.size[1]/im.size[0])),Image.LANCZOS),lab) for im,lab in rows]
gap=30; H=sum(d.size[1] for d,_ in disp)+gap*len(disp)
canvas=Image.new("RGB",(TW,H),(18,18,20)); dr=ImageDraw.Draw(canvas); y=0
for d,lab in disp:
    dr.text((6,y+4),lab,fill=(240,240,240),font=font); canvas.paste(d,(0,y+26)); y+=d.size[1]+gap
canvas.save(RENDERS+r"\06_clean_compare.png")
print("saved compare",flush=True)
