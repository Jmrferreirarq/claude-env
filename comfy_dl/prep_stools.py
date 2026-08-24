import numpy as np, json
from PIL import Image, ImageFilter
from collections import deque

BASE = r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_v2_handles.png"
SAM  = r"C:\comfy_dl\_mask_stools.png"

m = np.array(Image.open(SAM).convert("L"))
H,W = m.shape
b = m>127

# connected components (4-neigh) to split the 3 stools
lab = np.zeros((H,W),np.int32); cur=0; comps=[]
for y in range(H):
    for x in range(W):
        if b[y,x] and lab[y,x]==0:
            cur+=1; q=deque([(y,x)]); lab[y,x]=cur; px=[]
            while q:
                cy,cx=q.popleft(); px.append((cy,cx))
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<H and 0<=nx<W and b[ny,nx] and lab[ny,nx]==0:
                        lab[ny,nx]=cur; q.append((ny,nx))
            if len(px)>800: comps.append((cur,px))
print("components kept:",len(comps))

seat = np.zeros((H,W),bool)
for cid,px in comps:
    ys=[p[0] for p in px]; xs=[p[1] for p in px]
    y0,y1=min(ys),max(ys); x0,x1=min(xs),max(xs)
    cw=x1-x0+1; ch=y1-y0+1
    # per-row white count within this comp
    rows={}
    for (yy,xx) in px: rows[yy]=rows.get(yy,0)+1
    # seat = top contiguous run of rows whose fill >= 55% of comp width
    seat_rows=[]
    for yy in range(y0, y0+int(ch*0.6)):
        if rows.get(yy,0) >= 0.55*cw:
            seat_rows.append(yy)
        elif seat_rows:
            break  # stop at first gap after seat starts
    if not seat_rows:
        # fallback: top 22% band
        seat_rows=list(range(y0, y0+int(ch*0.22)))
    sy0,sy1=min(seat_rows),max(seat_rows)
    # fill solid rectangle per seat rows using comp's x-extent at those rows
    for yy in seat_rows:
        xr=[p[1] for p in px if p[0]==yy]
        if xr:
            seat[yy, min(xr):max(xr)+1]=True
    print(f"stool {cid}: box=({x0},{y0},{x1},{y1}) seat y {sy0}-{sy1} h={sy1-sy0}")

# build region bbox around seats with pad, for crop-stitch
ys,xs=np.where(seat)
ry0,ry1=ys.min(),ys.max(); rx0,rx1=xs.min(),xs.max()
pad=50
xs0=max(0,rx0-pad); ys0=max(0,ry0-pad); xs1=min(W,rx1+pad); ys1=min(H,ry1+pad)
rw=xs1-xs0; rh=ys1-ys0

# mask image grow +6, blur 4 (full size first)
mask_full = Image.fromarray((seat*255).astype(np.uint8))
mask_full = mask_full.filter(ImageFilter.MaxFilter(13))   # ~+6px each side
mask_full = mask_full.filter(ImageFilter.GaussianBlur(4))

base = Image.open(BASE).convert("RGB")
region = base.crop((xs0,ys0,xs1,ys1))
region_mask = mask_full.crop((xs0,ys0,xs1,ys1))

# upscale 2x for SDXL
Z=2
region_up = region.resize((rw*Z,rh*Z), Image.LANCZOS)
region_mask_up = region_mask.resize((rw*Z,rh*Z), Image.LANCZOS).convert("RGB")

region_up.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\s_region_up.png")
region_mask_up.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\s_region_mask_up.png")
json.dump({"xs0":int(xs0),"ys0":int(ys0),"rw":int(rw),"rh":int(rh),"Z":Z}, open(r"C:\comfy_dl\s_meta.json","w"))

# display mask: overlay
disp = region.copy()
import numpy as _np
ov=_np.array(disp); mm=_np.array(region_mask.resize(region.size))>60
ov[mm]=(ov[mm]*0.4+_np.array([255,40,40])*0.6).astype(_np.uint8)
Image.fromarray(ov).save(r"C:\comfy_dl\_s_mask_overlay.png")
mask_full.crop((xs0,ys0,xs1,ys1)).save(r"C:\comfy_dl\_s_mask.png")
print("region",(xs0,ys0,rw,rh),"up",region_up.size)
