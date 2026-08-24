from PIL import Image, ImageDraw
im=Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png").convert("RGB")
boxes=[(488,996,512,1052),(524,1124,550,1180),(632,1088,660,1144),
       (950,1006,970,1054),(982,996,1004,1048)]
ov=im.copy(); d=ImageDraw.Draw(ov)
for b in boxes: d.rectangle(b, outline=(255,0,0), width=2)
ov.crop((430,950,1130,1250)).resize((1400,600)).save(r"C:\comfy_dl\_boxcheck.png")
print("ok")
