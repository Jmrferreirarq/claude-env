import json, urllib.request, urllib.parse, time, sys

SRV="http://127.0.0.1:8188"
PROMPT = sys.argv[1] if len(sys.argv)>1 else "bar stool seat tops"
THR    = float(sys.argv[2]) if len(sys.argv)>2 else 0.3
IMG    = sys.argv[3] if len(sys.argv)>3 else "cozinha_v2_handles.png"
TAG    = sys.argv[4] if len(sys.argv)>4 else "sammask"

def post(p,pl):
    d=json.dumps(pl).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(SRV+p,data=d,headers={"Content-Type":"application/json"})).read())
def get(p): return json.loads(urllib.request.urlopen(SRV+p).read())

g={
 "1":{"class_type":"LoadImage","inputs":{"image":IMG}},
 "2":{"class_type":"SAMModelLoader (segment anything)","inputs":{"model_name":"sam_vit_b (375MB)"}},
 "3":{"class_type":"GroundingDinoModelLoader (segment anything)","inputs":{"model_name":"GroundingDINO_SwinT_OGC (694MB)"}},
 "4":{"class_type":"GroundingDinoSAMSegment (segment anything)","inputs":{
        "sam_model":["2",0],"grounding_dino_model":["3",0],"image":["1",0],
        "prompt":PROMPT,"threshold":THR}},
 "5":{"class_type":"MaskToImage","inputs":{"mask":["4",1]}},
 "6":{"class_type":"SaveImage","inputs":{"images":["5",0],"filename_prefix":"mask_"+TAG}},
}
r=post("/prompt",{"prompt":g}); pid=r["prompt_id"]; print("submitted",pid,flush=True)
out=None
for _ in range(600):
    h=get("/history/"+pid)
    if pid in h:
        st=h[pid].get("status",{})
        if "6" in h[pid].get("outputs",{}) and h[pid]["outputs"]["6"].get("images"):
            out=h[pid]["outputs"]["6"]["images"][0]; break
        if st.get("status_str")=="error":
            print("ERROR",json.dumps(st)); sys.exit(2)
    time.sleep(1)
if not out: print("TIMEOUT"); sys.exit(1)
q=urllib.parse.urlencode({"filename":out["filename"],"subfolder":out.get("subfolder",""),"type":out.get("type","output")})
data=urllib.request.urlopen(SRV+"/view?"+q).read()
P=r"C:\comfy_dl\_mask_"+TAG+".png"; open(P,"wb").write(data)
# stats
from PIL import Image
import numpy as np
m=np.array(Image.open(P).convert("L"))
print("MASK",P,"white_frac=%.4f"%((m>127).mean()),"shape",m.shape,flush=True)
