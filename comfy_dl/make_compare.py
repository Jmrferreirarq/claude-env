from PIL import Image, ImageDraw, ImageFont
import os
R=r"C:\Users\José Ferreira\Nanobana\renders"

panels=[
 ("cozinha_gptimage.png","ORIGEM (gpt-image)"),
 ("cozinha_ultimate.png","v2 (base: puxadores latao, bancos beige, cortinas verdes)"),
 ("cozinha_v3_finishes.png","v3 (puxadores pretos, bancos carvalho, cortinas brancas)"),
]
TH=620   # target panel height
gap=18; lab=46
imgs=[]
for f,_ in panels:
    im=Image.open(os.path.join(R,f)).convert("RGB")
    w=int(TH*im.size[0]/im.size[1])
    imgs.append(im.resize((w,TH),Image.LANCZOS))
totw=sum(i.size[0] for i in imgs)+gap*(len(imgs)-1)
canvas=Image.new("RGB",(totw,TH+lab),(20,20,22))
d=ImageDraw.Draw(canvas)
try: font=ImageFont.truetype("arialbd.ttf",18); font2=ImageFont.truetype("arial.ttf",14)
except: font=ImageFont.load_default(); font2=font
x=0
for (f,label),im in zip(panels,imgs):
    canvas.paste(im,(x,lab))
    # label text (wrap if long)
    words=label.split(); lines=[""];
    for w_ in words:
        if d.textlength((lines[-1]+" "+w_).strip(),font=font2)< im.size[0]-12: lines[-1]=(lines[-1]+" "+w_).strip()
        else: lines.append(w_)
    ty=6
    for ln in lines[:2]:
        d.text((x+8,ty),ln,fill=(240,240,240),font=font2); ty+=17
    x+=im.size[0]+gap
OUT=os.path.join(R,"cozinha_comparacao_origem_v2_v3.png")
canvas.save(OUT)
print("SAVED",OUT,canvas.size)
canvas.resize((min(1500,canvas.size[0]),int(canvas.size[1]*min(1500,canvas.size[0])/canvas.size[0]))).save(r"C:\comfy_dl\_compare_view.png")
