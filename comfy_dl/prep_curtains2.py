import numpy as np, json
from PIL import Image, ImageFilter
from collections import deque

BASE=r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_v2b_stools.png"
SAM=r"C:\comfy_dl\_mask_curtains.png"
im=Image.open(BASE).convert("RGB"); W,H=im.size
m=np.array(Image.open(SAM).convert("L"))>127
vis=np.zeros((H,W),bool); keep=np.zeros((H,W),bool)
ys,xs=np.where(m)
for sy,sx in zip(ys,xs):
    if vis[sy,sx]:continue
    q=deque([(sy,sx)]);vis[sy,sx]=True;px=[]
    while q:
        cy,cx=q.popleft();px.append((cy,cx))
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=cy+dy,cx+dx
            if 0<=ny<H and 0<=nx<W and m[ny,nx] and not vis[ny,nx]:
                vis[ny,nx]=True;q.append((ny,nx))
    if len(px)<1000: continue
    cx_=sum(p[1] for p in px)//len(px)
    if cx_ < 2520:                      # keep curtain panels, drop TV wall blob (cx~2757)
        for py,pxx in px: keep[py,pxx]=True
print("kept px",int(keep.sum()))

mimg=Image.fromarray((keep*255).astype(np.uint8))
mimg=mimg.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(6))
arr=np.array(mimg)
ys,xs=np.where(arr>40); ry0,ry1,rx0,rx1=ys.min(),ys.max(),xs.min(),xs.max()
pad=40
xs0=max(0,rx0-pad);ys0=max(0,ry0-pad);xs1=min(W,rx1+pad);ys1=min(H,ry1+pad)
rw=xs1-xs0;rh=ys1-ys0;Z=2
im.crop((xs0,ys0,xs1,ys1)).resize((rw*Z,rh*Z),Image.LANCZOS).save(r"C:\ComfyUI_windows_portable\ComfyUI\input\c_region_up.png")
mimg.crop((xs0,ys0,xs1,ys1)).resize((rw*Z,rh*Z),Image.LANCZOS).convert("RGB").save(r"C:\ComfyUI_windows_portable\ComfyUI\input\c_region_mask_up.png")
json.dump({"xs0":int(xs0),"ys0":int(ys0),"rw":int(rw),"rh":int(rh),"Z":Z},open(r"C:\comfy_dl\c_meta.json","w"))
reg=im.crop((xs0,ys0,xs1,ys1));ov=np.array(reg).copy();mm=np.array(mimg.crop((xs0,ys0,xs1,ys1)))>50
ov[mm]=(ov[mm]*0.4+np.array([255,40,40])*0.6).astype(np.uint8)
Image.fromarray(ov).save(r"C:\comfy_dl\_c_mask_overlay.png")
print("region",(xs0,ys0,rw,rh))
