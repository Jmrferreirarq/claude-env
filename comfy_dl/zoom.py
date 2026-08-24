from PIL import Image
im = Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png")
print("FULL", im.size)
crops = {
  "zoomL_tall": (430, 520, 780, 1200),
  "zoomL_oven": (560, 650, 950, 1180),
  "zoomL_low":  (430, 980, 1100, 1340),
}
for name,(x0,y0,x1,y1) in crops.items():
    c = im.crop((x0,y0,x1,y1))
    c = c.resize((c.width*2, c.height*2))
    p = rf"C:\comfy_dl\_{name}.png"
    c.save(p); print(name, (x0,y0,x1,y1), "->", p)
