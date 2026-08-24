from PIL import Image
import colorsys
im = Image.open(r"C:\ComfyUI_windows_portable\ComfyUI\input\cozinha_ultimate.png").convert("RGB")
px = im.load()
pts = {
 "tall_left_handle": (528,1008),
 "tall_right_handle": (652,1020),
 "low_handle_1": (560,1170),
 "low_handle_2": (965,1115),
 "white_door": (520,800),
 "oak_niche": (980,1060),
 "oak_upper": (820,560),
}
for name,(x,y) in pts.items():
    # average a 7x7 patch
    rs=gs=bs=0;n=0
    for dx in range(-3,4):
        for dy in range(-3,4):
            r,g,b=px[x+dx,y+dy]; rs+=r;gs+=g;bs+=b;n+=1
    r,g,b=rs//n,gs//n,bs//n
    h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
    print(f"{name:18} RGB=({r:3},{g:3},{b:3})  H={h*360:5.1f} S={s:.2f} V={v:.2f}")
