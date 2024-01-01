#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""

import libDataframe as lDF
import time


def getCUP(debug=False):
    myCUP=getCUPFromCamera(debug)
    if myCUP is None:
        rep=input("Incapable de trouver le CUP: \n reessayer? < r > \n entrer manuellement < m > \n abandonner < enter > \n")
        if rep=="r":
            return getCUP()
        elif rep=="m":
            myCUP=input("Taper le CUP: ")
    print(" ")
    return myCUP

def getCUPFromCamera(debug=False):
    import imutils
    from imutils.video import VideoStream
    from pyzbar import pyzbar
    import cv2

    myCUP=None
    print("Montrez une bouteille à la camera...") 
    vs = VideoStream(src=0).start()
    tryAgain=20
    while tryAgain>0:
        if debug:
            print("Essai %i"%tryAgain)
        time.sleep(1.0)
        frame = vs.read()
        frame = imutils.resize(frame, width=1000)
        barcodes = pyzbar.decode(frame)
        if debug:
            print(barcodes)
            cv2.imwrite("images/test%i.jpg"%tryAgain, frame)
        if barcodes:
            myCUP=barcodes[0].data.decode("utf-8")
            print("*** CUP: %s ***"%myCUP)
            tryAgain=0
            pass
        tryAgain-=1
        pass
    cv2.destroyAllWindows()
    vs.stop()
    return myCUP

def updateBtleInfoFromKeyboard(bInfo,option="defaults"):
    defaults=lDF.get_default_values()
    bDic=bInfo.resolved_dict
    if len(bInfo.original_dict)<1:
        print("Warning - Modification d'une bouteille sans backup")
    
    bInfo.Print(debug=True)
    print("Voulez-vous editer certaines informations?")
    print("<cr> : non merci")
    print("1 : ['Millesime','BoireMin','BoireMax']")
    print("2 : ['AcquiseOu','Notes']")
    print("3 : all keys")
    print("Bue (yyyy-m-d)")
    myKeys=[] 
    rep=input("...or any comma-separated keys \n")
    if rep:
        if rep=="1":
            myKeys=['Millesime','BoireMin','BoireMax']
        elif rep=="2":
            myKeys=['AcquiseOu','Notes']
        elif rep=="3" or rep=="all":
            myKeys=lDF.get_default_values().keys()
        else:
            myKeys=rep.split(',')
    
    for k in myKeys:
        try:
            if bDic[k]==defaults[k]:
                if k=="BoireMin":
                    bDic[k]=bDic['Millesime']+5
                elif k=="BoireMax":
                    bDic[k]=bDic['Millesime']+10
                
            rep=input("%s: ? <%s> \n"%(k,bDic[k]))
            if rep:
                isOK=True
                if "," in rep:
                    print("pas de virgule svp")
                    
                if isOK:
                    if k in ['Millesime','BoireMin','BoireMax','Format']:
                        bDic[k]=int(rep)
                    elif k in ['Prix','Sucre','Alcool']:
                        bDic[k]=float(rep)
                    else:
                        bDic[k]=rep
        except:
            print("Probleme avec: %s"%k)

    if myKeys:
        #Verification finale
        bInfo.Print(debug=True)
        rep=input("Modifier d'autres informations? <n> \n")
        if not ((rep=="") or (rep=="n")):
            print("Nouvelles corrections ou modifications...")
            time.sleep(1)
            return updateBtleInfoFromKeyboard(bInfo,option)
    
    return bInfo

