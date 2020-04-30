import pandas as pd
import numpy as np
from pathlib import Path
import os
from fastai.tabular import *
from tkinter import *
import serial
import time


#Makes a dict with keys named after the keypoint columns. 202 keys (rating + 25 keypoints)
def kpdictmaker():
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

    #print("KPDICT IN MAKER: ", kpdict)
    print(len(kpdict))
    return kpdict


def json_extractor(path, kpdict):
    df = pd.read_json(path)

    kp = df["people"]  # Navigating through the Json layers
    keyp = kp[0]
    keypoints = keyp["pose_keypoints_2d"]
    keypoints_righthand = keyp["hand_right_keypoints_2d"]
    keypoints_lefthand = keyp["hand_left_keypoints_2d"]
    #print("Length of keypoints:", len(keypoints))

    """Add rating. Thus, indexes match when we start enumerate from position 1.
    Moving this down. Rating will be added at end."""

    """Keypoints for the position of the midhip and the wrists. As per Openpose/output docs. Positions 8,4,7"""
    midhip_x = keypoints[24]
    midhip_y = keypoints[25]

    rwrist_x = keypoints[12]
    rwrist_y = keypoints[13]

    lwrist_x = keypoints[21]
    lwrist_y = keypoints[22]

    """NECK and MIDHIP. POS 1 & 8"""
    neck_y = keypoints[4]
    midhip_y = keypoints[25]
    torso_delta = 100 * (neck_y - midhip_y)


    """RIGHT SHOULDER and ELBOW. POS 2 & 3"""
    rshoulder_x = keypoints[6]
    rshoulder_y = keypoints[7]

    relbow_x = keypoints[9]
    relbow_y = keypoints[10]

    rshoulder_delta = 1.9 * multiplier * (rshoulder_y - relbow_y) / torso_delta

    """LEFT SHOULDER and ELBOW. POS 5 & 6"""
    lshoulder_x = keypoints[15]
    lshoulder_y = keypoints[16]

    lelbow_x = keypoints[18]
    lelbow_y = keypoints[19]

    lshoulder_delta = 1.9 * multiplier * (lshoulder_y - lelbow_y) / torso_delta

    """RIGHT HIP  and KNEE. POS 9 & 10"""
    rhip_x = keypoints[27]
    rhip_y = keypoints[28]

    rknee_x = keypoints[30]
    rknee_y = keypoints[31]

    rleg_delta = 0.7 * multiplier * (rhip_y - rknee_y) / torso_delta

    """LEFT HIP  and KNEE. POS 12 & 13"""
    lhip_x = keypoints[36]
    lhip_y = keypoints[37]

    lknee_x = keypoints[39]
    lknee_y = keypoints[40]

    lleg_delta = 0.7 * multiplier * (lhip_y - lknee_y) / torso_delta

    """NOSE and NECK. POS 0 & 1"""
    nose_x = keypoints[0]

    neck_x = keypoints[3]

    face_delta = 2 * multiplier * (nose_x - midhip_x) / torso_delta

    """LHEEL 21 RHEEL 24"""

    for index, value in enumerate(keypoints):

        if index % 3 == 0:
            """These are the x's. 0,3,6,9..."""
            #print(index, value)
            keypoints[index] = value - midhip_x
            # print("x",index,", which is: ",value,"minus middle hip x which is: ",x,"equals: ",value-x)
            #print("Inside X:", index)


        elif index % 3 == 1:
            #print(index, value)
            keypoints[index] = value - midhip_y
            # print("y", index, ", which is: ", value, "minus middle hip x which is: ", y, "equals: ", value - y)
            #print("Inside Y:", index)

    for index, value in enumerate(keypoints_righthand):
        if index % 3 == 0:
            #print("THESE ARE X's: ", index, value)
            keypoints_righthand[index] = value - rwrist_x

        if index % 3 == 1:
            #print("THESE ARE Y's: ", index, value)
            keypoints_righthand[index] = value - rwrist_y

    for index, value in enumerate(keypoints_lefthand):
        if index % 3 == 0:
            #print("THESE ARE X's: ", index, value)
            keypoints_lefthand[index] = value - lwrist_x

        if index % 3 == 1:
            #print("THESE ARE Y's: ", index, value)
            keypoints_lefthand[index] = value - lwrist_y

    #print("BODY AG KEYPOINTS: ", keypoints)
    #print("Length of agnostic body keypoints: ", len(keypoints))
    #print("RIGHTHAND KEYPOINTS: ", keypoints_righthand)
    #print("LEFTHAND KEYPOINTS: ", keypoints_lefthand)
    # input("OK?")

    """except:
            print("WARNING. Tried extracting keypoints. Empty file")"""
    keypoints = keypoints + keypoints_righthand + keypoints_lefthand

    keypoints.insert(0, 0.5)  # Do i really want to add rating ?
    #print("ALL INCLUSIVE KEYPOINTS: ", keypoints)

    kpdict = slimpourer(kpdict, keypoints)
    kpdataframe = dfmaker(kpdict)

    return kpdataframe, rshoulder_delta, lshoulder_delta, rleg_delta, lleg_delta, face_delta


# =====================================================

def slimpourer(slimkpdict, keypoints):
    """Pours list of keypoints into the lists within kpdict. It´s a one-element dict in inference right?"""
    for (key, kplist), kp in zip(slimkpdict.items(), keypoints):
        kplist.append(kp)

    return slimkpdict


# =====================================================

def dfmaker(dict):
    kpdataframe = pd.DataFrame.from_dict(dict)

    return kpdataframe

# =====================================================

def constrain (val):
    return round(min(1200, max(0,val)))

# =====================================================

# =====================================================
initpos=0
multiplier=60000

serPort = "COM4"
baudRate = 115200
ser = serial.Serial(serPort, baudRate)
print("Serial port " + serPort + " opened  Baudrate " + str(baudRate))




jsonpath=Path("C:/Users/tiedbranches/openpose/store/inferencekp/")
deletelist = list(os.scandir(jsonpath))
for i in deletelist:
    os.remove(i)
    #This I think is an automatic folder clearer


root = Tk()
var = StringVar()
var2 = StringVar()



l = Label(root, textvariable = var,font=("Courier",404))
l.pack()



while True:
    try:
        filelist = list(os.scandir(jsonpath))
        last = filelist.pop()
        print("PATH OF JSON BEING OPENED: ", last.path)


        kpdict = kpdictmaker()

        try:
            kpdataframe,rshoulder_delta, lshoulder_delta, rleg_delta, lleg_delta, face_delta= json_extractor(last.path, kpdict)
            print(rshoulder_delta, lshoulder_delta, rleg_delta, lleg_delta, face_delta)

        except Exception as errormessage:
            stepperpos = 0
            stepperposition = "<" + str(stepperpos) + ">"
            ser.write(stepperposition.encode('utf-8'))
            print("JSON_EXTRACTOR IN LOOP ERROR: ", errormessage)
            print("No person in frame perhaps.")

            stepperposition = "<" + str(0) + "," + str(0) + "," + str(0) + "," + str(0) + "," + str(0) + ">"
            print("STEPPERPOSITION: ", stepperposition)
            ser.write(stepperposition.encode('utf-8'))


        try:
            os.remove(todelete)  #We should delete the file-5 or so, because it seems to fall back on a previous if it reads too fast?

        except Exception as errormessage:
            print(errormessage)

        todelete = str(last.path) #Sets current json to be deleted on next loop, once next is opened

        var.set(str(round(rshoulder_delta)))
        time.sleep(0.1)


        if rshoulder_delta>-1200 and rshoulder_delta<1200:
            stepperpos = constrain(face_delta)
            stepperpos2 = constrain(lshoulder_delta)
            stepperpos3 = constrain(lleg_delta)
            stepperpos4 = constrain(rleg_delta)
            stepperpos5 = constrain( rshoulder_delta)

            stepperposition = "<" + str(stepperpos) + "," + str(stepperpos2) + "," + str(stepperpos3) + "," + str(stepperpos4) + "," + str(stepperpos5) + ","   ">"
            print("STEPPERPOSITION: ",stepperposition)
            ser.write(stepperposition.encode('utf-8'))
            time.sleep(0.01)
        else:
            pass



        root.update()

    except Exception as errormessage:
        print("BROKEN MAIN LOOP. OK IN FIRST LOOP: ", errormessage)
        stepperpos=initpos
        stepperposition = "<" + str(stepperpos) + ">"
        ser.write(stepperposition.encode('utf-8'))



        #A full serial buffer might be causing delays--it was the fact that Arduino was replying to PC and nothing was reading it.
        #Need to find a way to launch program with no person in frame. Either a further try/except or an initial populated json.
