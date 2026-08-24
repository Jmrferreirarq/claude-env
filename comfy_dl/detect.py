from PIL import Image, ImageDraw
from collections import deque
im=Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png").convert("RGB")
W,H=im.size; px=im.load()
# region of cabinet doors (exclude oven column & upper)
RX0,RY0,RX1,RY1=430,1000,1140,1320
OVEN=(600,1000,770,1010)  # oven is above band; minimal
dark=set()
for x in range(RX0,RX1):
    for y in range(RY0,RY1):
        r,g,b=px[x,y]
        if (r+g+b)/3 < 120:        # dark groove/shadow of handle
            dark.add((x,y))
# connected components (4-neigh)
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
# filter: handle-sized vertical-ish components
cand=[c for c in comps if 60<=c[4]<=1500 and (c[3]-c[1])>=18 and (c[2]-c[0])<=60]
cand.sort(key=lambda c:(c[1],c[0]))
print("components:",len(comps),"candidates:",len(cand))
ov=im.copy(); d=ImageDraw.Draw(ov)
for (x0,y0,x1,y1,n) in cand:
    d.rectangle((x0-1,y0-1,x1+1,y1+1), outline=(255,0,0), width=2)
    print(f"  box=({x0},{y0},{x1},{y1}) area={n} w={x1-x0} h={y1-y0}")
ov.crop((430,950,1140,1330)).resize((1420,760)).save(r"C:\comfy_dl\_detect_ov.png")
print("saved overlay")
