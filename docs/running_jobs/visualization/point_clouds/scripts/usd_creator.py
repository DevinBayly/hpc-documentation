from pxr import Usd,UsdGeom,Vt,Sdf
from pathlib import Path
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()
name = args.name
#ensure that the ordering of the files isn't lexicographic

pcds =sorted(Path().glob("*pcd"))
pcds

def makepcloud_pcd(pcd_name):
#     print("making cloud of ",pcd_name)
    with open(pcd_name,"rb") as phile:
        line = phile.readline()
        header = []
        limiter = 50
        while not b"DATA" in line and limiter >0:
            line = phile.readline()
            header.append(line)
            limiter-= 1
        buf = phile.read()
    parts = [[e for e in d.decode().strip().split(" ")[1:]] for d in header[1:] ]
    parts = [p for p in parts if len(p) >0]
    parts
#     print("parts are",parts)
    num_points = int(parts[7][0])
    collection = []
    for attri,e in enumerate(parts[3]):
#         print("e is ",e)
        for i in range(int(e)):
            name = parts[0][attri]
            if name =="_":
                name+=str(i)+str(attri)+"skip"
            unit = (parts[2][attri]+parts[1][attri]).lower()
            collection.append((name,unit))
    d = np.dtype(collection)
#     print("num bytes per point" , d.itemsize)
    arr = np.frombuffer(buf[:d.itemsize*num_points],dtype=d)
    
    return arr


stage = Usd.Stage.CreateNew(f"{name}.usdc")
pts = UsdGeom.Points.Define(stage,"/mypoints")

import numpy as np

points = pts.GetPointsAttr()
widths = pts.GetWidthsAttr()

stage.SetStartTimeCode(0)
stage.SetEndTimeCode(len(pcds))
for i,pcd in enumerate(pcds):
    arr = makepcloud_pcd(str(pcd))
    names = arr.dtype.names[3:]
    pvars={}
    points.Set(time=i,value=Vt.Vec3fArray.FromNumpy(np.array([arr["x"],arr["y"],arr["z"]]).T))
    for name in names:
      # skip the "_" prefaced names that stand for offset balancing in pcd binary
        if "skip" in name:
          continue
        pvar = UsdGeom.PrimvarsAPI(pts).CreatePrimvar(name,Sdf.ValueTypeNames.FloatArray,"vertex")
        pvar.Set(time=i,value= Vt.FloatArray(arr[name].astype("float64")))
        pvars[name] = pvar
    
    

stage.Save()

