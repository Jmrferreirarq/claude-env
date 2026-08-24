from PIL import Image, ImageDraw, ImageFont
im = Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png").convert("RGB")
def grid(x0,y0,x1,y1,Z,step,out):
    crop = im.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z))
    d=ImageDraw.Draw(crop)
    try: f=ImageFont.truetype("arial.ttf",14)
    except: f=ImageFont.load_default()
    for ox in range(x0-(x0%step)+step,x1,step):
        sx=(ox-x0)*Z; d.line([(sx,0),(sx,crop.height)],fill=(255,0,0),width=1); d.text((sx+1,1),str(ox),fill=(255,0,0),font=f)
    for oy in range(y0-(y0%step)+step,y1,step):
        sy=(oy-y0)*Z; d.line([(0,sy),(crop.width,sy)],fill=(255,0,0),width=1); d.text((1,sy+1),str(oy),fill=(255,0,0),font=f)
    crop.save(out); print(out, crop.size)
grid(430,980,720,1300,3,20,r"C:\comfy_dl\_g_left.png")
grid(820,980,1130,1120,3,20,r"C:\comfy_dl\_g_right.png")
