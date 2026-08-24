import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
RENDERS=r"C:\Users\José Ferreira\Nanobana\renders"
clean=Image.open(RENDERS+r"\06_upscaled_clean.png").convert("RGB")

a=np.asarray(clean).astype(np.float32)/255.0
# near-neutral white balance (barely any warmth - user found previous grade too warm)
a[...,0]*=1.005; a[...,2]*=0.997
# airy shadow lift (interiors-magazine bright/airy feel)
a=a*0.985+0.015
# very gentle S-curve contrast
a=(a-0.5)*1.04+0.5
# soft highlight rolloff to tame blown glass / bright walls
hi=0.85
a=np.where(a>hi, hi+(a-hi)*0.65, a)
a=np.clip(a,0,1)
g=Image.fromarray((a*255).astype(np.uint8),"RGB")
# gentle saturation + clarity (NO grain, NO heavy sharpen)
g=ImageEnhance.Color(g).enhance(1.04)
g=g.filter(ImageFilter.UnsharpMask(radius=55,percent=9,threshold=3))   # clarity (local contrast)
g=g.filter(ImageFilter.UnsharpMask(radius=1.4,percent=35,threshold=3)) # whisper of crispness
# very subtle vignette (no grain)
b=np.asarray(g).astype(np.float32)/255.0
H,W=b.shape[:2]
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)/np.sqrt(2)
vig=1.0-0.05*np.clip(d,0,1)**2.4   # corners only ~ -5%
b=np.clip(b*vig[...,None],0,1)
graded=Image.fromarray((b*255).astype(np.uint8),"RGB")
graded.save(RENDERS+r"\06_graded.png")
graded.save(r"C:\ComfyUI_windows_portable\ComfyUI\input\06_graded.png")
print("GRADED",graded.size)

# side-by-side: clean (no grade) vs graded
TW=900
try: font=ImageFont.truetype("arial.ttf",17)
except: font=ImageFont.load_default()
rows=[(clean,"SEM grade (upscale limpo)"),(graded,"COM grade subtil (sem grao)")]
disp=[(im.resize((TW,int(TW*im.size[1]/im.size[0])),Image.LANCZOS),lab) for im,lab in rows]
gap=28; lab=26; Ht=sum(d.size[1] for d,_ in disp)+(gap+lab)*len(disp)
canvas=Image.new("RGB",(TW,Ht),(18,18,20)); dr=ImageDraw.Draw(canvas); y=0
for dimg,l in disp:
    dr.text((6,y+4),l,fill=(240,240,240),font=font); canvas.paste(dimg,(0,y+lab)); y+=dimg.size[1]+lab+gap
canvas.save(RENDERS+r"\06_grade_compare.png")
print("saved compare")
