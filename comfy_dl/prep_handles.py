from PIL import Image, ImageFilter, ImageDraw
from collections import deque
import json
SRC=r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png"
im=Image.open(SRC).convert("RGB"); W,H=im.size; px=im.load()
# detect dark grooves -> handle boxes
dark=set()
for x in range(430,1140):
    for y in range(1000,1320):
        r,g,b=px[x,y]
        if (r+g+b)/3<120: dark.add((x,y))
seen=set(); comps=[]
for p in dark:
    if p in seen: continue
    q=deque([p]); seen.add(p); cells=[]
    while q:
        cx,cy=q.popleft(); cells.append((cx,cy))
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            n=(cx+dx,cy+dy)
            if n in dark and n not in seen: seen.add(n); q.append(n)
    xs=[c[0] for c in cells]; ys=[c[1] for c in cells]
    comps.append((min(xs),min(ys),max(xs),max(ys),len(cells)))
cand=[c for c in comps if 60<=c[4]<=1500 and (c[3]-c[1])>=18 and (c[2]-c[0])<=60]
# full mask: each box expanded then grow+blur
mask=Image.new("L",(W,H),0); d=ImageDraw.Draw(mask)
for (x0,y0,x1,y1,n) in cand:
    d.rectangle((x0-10,y0-6,x1+14,y1+6), fill=255)
mask=mask.filter(ImageFilter.MaxFilter(9))      # grow ~+8
mask=mask.filter(ImageFilter.GaussianBlur(4))    # blur 4
# region bbox
xs0=min(c[0] for c in cand)-40; ys0=min(c[1] for c in cand)-40
xs1=max(c[2] for c in cand)+40; ys1=max(c[3] for c in cand)+40
xs0=max(0,xs0); ys0=max(0,ys0); xs1=min(W,xs1); ys1=min(H,ys1)
# snap to even
rw=xs1-xs0; rh=ys1-ys0
region=im.crop((xs0,ys0,xs1,ys1))
mreg=mask.crop((xs0,ys0,xs1,ys1))
Z=2
region.resize((rw*Z,rh*Z)).save(r"C:\ComfyUI_windows_portable\ComfyUI\input\h_region_up.png")
mreg.resize((rw*Z,rh*Z)).convert("RGB").save(r"C:\ComfyUI_windows_portable\ComfyUI\input\h_region_mask_up.png")
mreg.save(r"C:\comfy_dl\_h_region_mask_small.png")
json.dump({"xs0":xs0,"ys0":ys0,"rw":rw,"rh":rh,"Z":Z,"boxes":[list(c) for c in cand]}, open(r"C:\comfy_dl\h_meta.json","w"))
# show mask over full for the user
mask.point(lambda v:255 if v>30 else 0).crop((430,950,1140,1330)).resize((1420,760)).save(r"C:\comfy_dl\_h_inpaint_mask.png")
print("region",(xs0,ys0,rw,rh),"upscaled",(rw*Z,rh*Z),"handles",len(cand))
