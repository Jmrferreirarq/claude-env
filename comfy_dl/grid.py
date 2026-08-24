from PIL import Image, ImageDraw, ImageFont
im = Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png").convert("RGB")
x0,y0,x1,y1 = 430,500,1150,1350
crop = im.crop((x0,y0,x1,y1))
Z=2
crop = crop.resize((crop.width*Z, crop.height*Z))
d = ImageDraw.Draw(crop)
try: font = ImageFont.truetype("arial.ttf", 16)
except: font = ImageFont.load_default()
# vertical grid every 50 orig px
for ox in range(x0 - (x0%50)+50, x1, 50):
    sx=(ox-x0)*Z
    d.line([(sx,0),(sx,crop.height)], fill=(255,0,0), width=1)
    d.text((sx+2,2), str(ox), fill=(255,0,0), font=font)
for oy in range(y0 - (y0%50)+50, y1, 50):
    sy=(oy-y0)*Z
    d.line([(0,sy),(crop.width,sy)], fill=(255,0,0), width=1)
    d.text((2,sy+1), str(oy), fill=(255,0,0), font=font)
crop.save(r"C:\comfy_dl\_grid_cab.png")
print("saved", crop.size)
