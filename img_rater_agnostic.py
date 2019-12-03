import pandas as pd
from pathlib import Path
import os
from PIL import Image
from copy import deepcopy

"""<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<ASSUMING BODY_25>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
ALSO CHECK: if the hand keypoints are referencing their own wrist not the opposite"""

#Makes a dict with keys named after the keypoint columns. 76 keys (rating + 25 keypoints) for body. 126 more for both hands (21 keypoints per hand).

kpdict={"rating":[]}

for i in range(1,68):
    if i<26:
        count=str(i)
        x="x"+count
        kpdict[x]=[]
        y="y"+count
        kpdict[y]=[]
        c="c"+count
        kpdict[c]=[]

    elif i<47:
        count=str(i-25)
        x="rh_x"+count
        kpdict[x]=[]
        y="rh_y"+count
        kpdict[y]=[]
        c="rh_c"+count
        kpdict[c]=[]

    elif i>46:
        count=str(i-46)
        x="lh_x"+count
        kpdict[x]=[]
        y="lh_y"+count
        kpdict[y]=[]
        c="lh_c"+count
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


    kp=df["people"] # Navigating through the Json layers
    keyp=kp[0]
    keypoints=keyp["pose_keypoints_2d"]
    keypoints_righthand = keyp["hand_right_keypoints_2d"]
    keypoints_lefthand = keyp["hand_left_keypoints_2d"]
    print("Length of keypoints:", len(keypoints))

    """Add rating. Thus, indexes match when we start enumerate from position 1.
    Moving this down. Rating will be added at end."""




    """Keypoints for the position of the midhip and the wrists. As per Openpose/output docs. Positions 8,4,7"""
    midhip_x = keypoints[24]
    midhip_y = keypoints[25]

    rwrist_x = keypoints[12]
    rwrist_y = keypoints[13]

    lwrist_x = keypoints[21]
    lwrist_y = keypoints[22]

    """Start at 1 only means labelling the indexes thus. It does not skip 0. keypoints[1] (in here) is the first x value."""
    """This is the body agnostic maker."""
    for index, value in enumerate(keypoints):

        if index % 3 == 0:
            """These are the x's. 0,3,6,9..."""
            print(index, value)
            keypoints[index] = value - midhip_x
            # print("x",index,", which is: ",value,"minus middle hip x which is: ",x,"equals: ",value-x)
            print("Inside X:", index)


        elif index % 3 == 1:
            print(index, value)
            keypoints[index] = value - midhip_y
            # print("y", index, ", which is: ", value, "minus middle hip x which is: ", y, "equals: ", value - y)
            print("Inside Y:", index)

    for index, value in enumerate(keypoints_righthand):
        if index % 3 == 0:
            print("THESE ARE X's: ", index, value)
            keypoints_righthand[index] = value - rwrist_x

        if index % 3 == 1:
            print("THESE ARE Y's: ", index, value)
            keypoints_righthand[index] = value - rwrist_y

    for index, value in enumerate(keypoints_lefthand):
        if index % 3 == 0:
            print("THESE ARE X's: ", index, value)
            keypoints_lefthand[index] = value - lwrist_x

        if index % 3 == 1:
            print("THESE ARE Y's: ", index, value)
            keypoints_lefthand[index] = value - lwrist_y

    print("BODY AG KEYPOINTS: ",keypoints)
    print("Length of agnostic body keypoints: ", len(keypoints))
    print("RIGHTHAND KEYPOINTS: ",keypoints_righthand)
    print("LEFTHAND KEYPOINTS: ", keypoints_lefthand)
    #input("OK?")


    """except:
            print("WARNING. Tried extracting keypoints. Empty file")"""
    keypoints=keypoints+keypoints_righthand+keypoints_lefthand

    keypoints.insert(0, rating)
    print("ALL INCLUSIVE KEYPOINTS: ",keypoints)

    return keypoints

inputlist=["0","1","2","3","4","5","6","7","8","9"]

imgfolder=Path("C:/Users/tiedbranches/openpose/store/imagesfulllow/")
jsonpath=Path("C:/Users/tiedbranches/openpose/store/keypointsfulllow/")

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
        kpdataframe=dfmaker(slimkeypointdict)
        savepath="C:/Users/tiedbranches/openpose/store/outputs/" + str(input("Please name the .csv (no suffix needed): ")) + ".csv"
        pd.DataFrame.to_csv(kpdataframe, savepath)
        print("DATAFRAME: ", kpdataframe)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(kpdataframe)
        exit()

    if prerate not in inputlist:
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<PRINT NUMBER>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        prerate = input("Rate tension in image from 0 to 10: ")
        rating = int(prerate) / 10
    else:
        rating = int(prerate) / 10

    keypoints=json_extractor(jfile.path,rating) # calling function that extracts keypoints from json and adds rating in [0]

    #finalkeypointdict=pourer(kpdict,keypoints)
    slimkeypointdict=slimpourer(slimkpdict,keypoints)

    print("KPDICT: ", kpdict)
    #print("FINALKEYPOINTDICT: ",finalkeypointdict)
    print("SLIMKPDICT: ",slimkpdict)
    print("SLIMKEYPOINTDICT: ", slimkeypointdict)
    print("")
    print("Stage end")
    print("")

kpdataframe = dfmaker(slimkeypointdict)
savepath = "C:/Users/tiedbranches/openpose/store/outputs/" + str(input("Please name the .csv: ")) + ".csv"
pd.DataFrame.to_csv(kpdataframe, savepath)
print("DATAFRAME: ", kpdataframe)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(kpdataframe)

