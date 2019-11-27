
import pandas as pd
from pathlib import Path
import os
from PIL import Image
from copy import deepcopy


#Makes a dict with keys named after the keypoint columns. 76 keys (rating + 25 keypoints)

kpdict={"rating":[]}

for i in range(1,26):
    count=str(i)
    x="x"+count
    kpdict[x]=[]
    y="y"+count
    kpdict[y]=[]
    c="c"+count
    kpdict[c]=[]

print("KPDICT: ", kpdict)
print(len(kpdict))
slimkpdict=deepcopy(kpdict)

#====================================================


def slimpourer(slimkpdict,keypoints):
    """Pours list of keypoints into the lists within kpdict."""
    for (key,kplist), kp in zip(slimkpdict.items(),keypoints):

        kplist.append(kp)

    return slimkpdict


#=====================================================

def dfmaker(dict):
    kpdataframe=pd.DataFrame.from_dict(dict)

    return kpdataframe


#=====================================================
def json_extractor(path,rating):
    df=pd.read_json(path)

    try:
        kp=df["people"] # Navigating through the Json layers
        keyp=kp[0]
        keypoints=keyp["pose_keypoints_2d"]

        keypoints.insert(0,rating)

    except:
        print("WARNING. Tried extracting keypoints. Empty file")

    return keypoints


imgfolder=Path("/Users/gonzalofidalgo/Documents/bibel/openpose/images/")
jsonpath=Path("/Users/gonzalofidalgo/Documents/bibel/openpose/keypoints/")

for file,jfile in zip(os.scandir(imgfolder), os.scandir(jsonpath)):
    print(type(file)) #This is a os.DirEntry object. We call its Attribute path on the next line.
    print("IMAGE BEING OPENED: ",file.path)
    print("")

    print(type(jfile))
    print("JSON BEING OPENED: ",jfile.path) # calling its attribute "path"
    print("")

    img=Image.open(file.path)
    img.show()

    prerate=input("Rate tension in image from 0 to 10: ")

    if prerate=="ok":
        kpdataframe=dfmaker(finalkeypointdict)
        pd.DataFrame.to_csv(kpdataframe,"/Users/gonzalofidalgo/Documents/bibel/openpose/keypoints/output.csv")
        print("DATAFRAME: ", kpdataframe)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(kpdataframe)
        exit()
    else:
        rating = int(prerate) / 10

    keypoints=json_extractor(jfile.path,rating) # calling function that extracts keypoints from json and adds rating in [0]

    finalkeypointdict=pourer(kpdict,keypoints)
    slimkeypointdic=slimpourer(slimkpdict,keypoints)

    print("KPDICT: ", kpdict)
    print("FINALKEYPOINTDICT: ",finalkeypointdict)
    print("SLIMKPDICT: ",slimkpdict)
    print("")
    print("Stage end")
    print("")


