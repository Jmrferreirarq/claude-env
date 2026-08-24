from PIL import Image, ImageDraw, ImageFilter
from collections import deque
SRC=r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png"
im=Image.open(SRC).convert("RGB"); W,H=im.size; px=im.load()
RX0,RY0,RX1,RY1=430,1000,1140,1320
dark=set()
for x in range(RX0,RX1):
    for y in range(RY0,RY1):
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
# build mask: within each expanded box, select non-bright (the whole bar)
mask=Image.new("L",(W,H),0); mpx=mask.load()
ML,MR,MT,MB=14,16,6,6
for (x0,y0,x1,y1,n) in cand:
    ex0,ey0,ex1,ey1=max(0,x0-ML),max(0,y0-MT),min(W,x1+MR),min(H,y1+MB)
    for x in range(ex0,ex1):
        for y in range(ey0,ey1):
            r,g,b=px[x,y]
            if (r+g+b)/3 < 205: mpx[x,y]=255
mask=mask.filter(ImageFilter.GaussianBlur(1.0)); mpx=mask.load()
out=im.copy(); opx=out.load()
for x in range(RX0-20,RX1+20):
    for y in range(RY0-20,RY1+20):
        a=mpx[x,y]/255.0
        if a<=0.02: continue
        r,g,b=px[x,y]; L=0.299*r+0.587*g+0.114*b
        t=int(max(0,min(255,14+L*0.18)))
        opx[x,y]=(int(r*(1-a)+t*a),int(g*(1-a)+t*a),int(b*(1-a)+t*a))
out.save(r"C:\Users\José Ferreira\Nanobana\renders\cozinha_v2_handles.png")
out.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_v2_handles.png")
mask.point(lambda v:255 if v>20 else 0).crop((430,950,1140,1330)).resize((1420,760)).save(r"C:\comfy_dl\_h2_mask.png")
im.crop((430,980,720,1230)).resize((580,500)).save(r"C:\comfy_dl\_h2_before_L.png")
out.crop((430,980,720,1230)).resize((580,500)).save(r"C:\comfy_dl\_h2_after_L.png")
im.crop((930,980,1040,1080)).resize((550,500)).save(r"C:\comfy_dl\_h2_before_R.png")
out.crop((930,980,1040,1080)).resize((550,500)).save(r"C:\comfy_dl\_h2_after_R.png")
print("recolored", len(cand), "handles")
