from PIL import Image, ImageFilter
import statistics
SRC=r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png"
im=Image.open(SRC).convert("RGB")
W,H=im.size
px=im.load()
boxes=[(480,993,514,1054),(518,1120,554,1182),(630,1084,666,1148),
       (946,1004,974,1058),(980,994,1008,1050)]
mask=Image.new("L",(W,H),0); mpx=mask.load()
out=im.copy(); opx=out.load()
for (x0,y0,x1,y1) in boxes:
    # background = median of brightest 40% pixels in box
    vals=[]
    for x in range(x0,x1):
        for y in range(y0,y1):
            r,g,b=px[x,y]; vals.append((r+g+b,r,g,b))
    vals.sort(reverse=True)
    top=vals[:max(1,int(len(vals)*0.4))]
    bgr=statistics.median(t[1] for t in top); bgg=statistics.median(t[2] for t in top); bgb=statistics.median(t[3] for t in top)
    for x in range(x0,x1):
        for y in range(y0,y1):
            r,g,b=px[x,y]
            dist=abs(r-bgr)+abs(g-bgg)+abs(b-bgb)
            if dist>34:                      # bar pixel
                mpx[x,y]=255
# feather mask 1.2px then recolor using feathered alpha
mask=mask.filter(ImageFilter.GaussianBlur(1.2))
mpx=mask.load()
for (x0,y0,x1,y1) in boxes:
    for x in range(max(0,x0-2),min(W,x1+2)):
        for y in range(max(0,y0-2),min(H,y1+2)):
            a=mpx[x,y]/255.0
            if a<=0.02: continue
            r,g,b=px[x,y]
            L=0.299*r+0.587*g+0.114*b
            t=int(max(0,min(255, 16 + L*0.20)))   # matte black, keep subtle sheen
            nr=int(r*(1-a)+t*a); ng=int(g*(1-a)+t*a); nb=int(b*(1-a)+t*a)
            opx[x,y]=(nr,ng,nb)
out.save(r"C:\Users\José Ferreira\Nanobana\renders\cozinha_v2_handles.png")
out.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_v2_handles.png")
# binary mask for display
mask.point(lambda v:255 if v>20 else 0).save(r"C:\comfy_dl\_handles_mask.png")
# overlay red where masked
ov=im.copy(); ovp=ov.load()
for x in range(W):
    pass
mm=mask.load()
for (x0,y0,x1,y1) in boxes:
    for x in range(max(0,x0-2),min(W,x1+2)):
        for y in range(max(0,y0-2),min(H,y1+2)):
            if mm[x,y]>40:
                r,g,b=ov.getpixel((x,y)); ov.putpixel((x,y),(255,40,40))
ov.crop((430,950,1130,1250)).resize((1400,600)).save(r"C:\comfy_dl\_handles_overlay.png")
# before/after zoom (tall band + right band)
im.crop((430,980,720,1200)).resize((580,440)).save(r"C:\comfy_dl\_before_L.png")
out.crop((430,980,720,1200)).resize((580,440)).save(r"C:\comfy_dl\_after_L.png")
im.crop((900,980,1040,1080)).resize((560,400)).save(r"C:\comfy_dl\_before_R.png")
out.crop((900,980,1040,1080)).resize((560,400)).save(r"C:\comfy_dl\_after_R.png")
print("done")
