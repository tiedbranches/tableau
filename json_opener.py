import pandas as pd
from pathlib import Path

datafolder=Path("C:/Users/tiedbranches/openpose/")
jsonpath=datafolder / "store/keypoints/kp.json"

df=pd.read_json(jsonpath)
kp=df["people"]
keyp=kp[0]
keypoints=keyp["pose_keypoints_2d"]
print(keypoints)
