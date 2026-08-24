import numpy as np, json
from PIL import Image, ImageFilter
from collections import deque

BASE=r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_v2b_stools.png"
im=Image.open(BASE).convert("RGB")
W,H=im.size
a=np.array(im).astype(np.int16)
R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]

# green/sage curtain: green dominant, not too dark, not the deep-green dining chairs region
green = (G> R+8) & (G> B+8) & (G>70) & (G<230)

# restrict to window band (right side, upper-mid) to avoid chairs/plants/floor
band=np.zeros((H,W),bool)
band[560:1230, 1950:2980]=True   # window/curtain zone only
mask = green & band

# clean: remove tiny specks via connected components, keep big blobs
m=mask.copy()
lab=np.zeros((H,W),np.int32);cur=0;keep=np.zeros((H,W),bool)
ys,xs=np.where(m)
visited=np.zeros((H,W),bool)
for (sy,sx) in zip(ys,xs):
    if visited[sy,sx]:continue
    q=deque([(sy,sx)]);visited[sy,sx]=True;px=[]
    while q:
        cy,cx=q.popleft();px.append((cy,cx))
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=cy+dy,cx+dx
            if 0<=ny<H and 0<=nx<W and m[ny,nx] and not visited[ny,nx]:
                visited[ny,nx]=True;q.append((ny,nx))
    if len(px)>1500:
        for (py,pxx) in px: keep[py,pxx]=True
mask=keep
print("curtain px",int(mask.sum()),"frac %.4f"%(mask.sum()/(W*H)))

mimg=Image.fromarray((mask*255).astype(np.uint8))
mimg=mimg.filter(ImageFilter.MaxFilter(17))   # grow ~+8
mimg=mimg.filter(ImageFilter.GaussianBlur(6))

ys,xs=np.where(np.array(mimg)>40)
ry0,ry1,rx0,rx1=ys.min(),ys.max(),xs.min(),xs.max()
pad=40
xs0=max(0,rx0-pad);ys0=max(0,ry0-pad);xs1=min(W,rx1+pad);ys1=min(H,ry1+pad)
rw=xs1-xs0;rh=ys1-ys0
Z=2
region=im.crop((xs0,ys0,xs1,ys1))
rmask=mimg.crop((xs0,ys0,xs1,ys1))
region.resize((rw*Z,rh*Z),Image.LANCZOS).save(r"C:\ComfyUI_windows_portable\ComfyUI\input\c_region_up.png")
rmask.resize((rw*Z,rh*Z),Image.LANCZOS).convert("RGB").save(r"C:\ComfyUI_windows_portable\ComfyUI\input\c_region_mask_up.png")
json.dump({"xs0":int(xs0),"ys0":int(ys0),"rw":int(rw),"rh":int(rh),"Z":Z},open(r"C:\comfy_dl\c_meta.json","w"))

ov=np.array(region).copy();mm=np.array(rmask.resize(region.size))>50
ov[mm]=(ov[mm]*0.4+np.array([255,40,40])*0.6).astype(np.uint8)
Image.fromarray(ov).save(r"C:\comfy_dl\_c_mask_overlay.png")
print("region",(xs0,ys0,rw,rh))
