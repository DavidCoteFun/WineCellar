#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""

import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar
import cv2
import argparse
from requests_html import HTMLSession
import time
import json
import urllib.request

debug=False

def trouver_bouteille(saqCode):
    myURL="https://www.saq.com/fr/%s"%saqCode
    if debug:
        print(myURL)
    session = HTMLSession()
    r2 = session.get(myURL)
    productInfo=r2.html.find(".product.info.main .page-title-wrapper")[0].text
    print(productInfo)
    prix=r2.html.find(".wrapper-price-promotions .product-info-price")[0].text
    prix.replace(u'\xa0',' ')
    print("Prix: %s"%prix)
    
    xtraInfo=r2.html.find(".product.data.items .product-data-item-additional .additional-attributes-wrapper .col-8-moins-1 ul.list-attributs li")
    print("Details:")
    for i in xtraInfo:
        print(" %s"%i.text)
    return

def cupToSaqCode(cupCode):
    #step 1
    tmpURL="https://www.saq.com/fr/search/ajax/suggest/?q=0%s"%cupCode
    r3=urllib.request.urlopen(tmpURL)
    saqObj=json.load(r3)
    tmpURL2=saqObj[1]['url']
    #step 2
    session = HTMLSession()
    r1 = session.get(tmpURL2)
    saqObj=r1.html.find(".product-item-details .content-wrapper .saq-code, .product-item-grid-details .content-wrapper .saq-code")[0]
    saqCode=saqObj.text.split(' ')[2]
    return saqCode


print("[INFO] starting video stream...")

vs = VideoStream(src=0).start()
tryAgain=20
while tryAgain>0:
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
        print("\n * * * * * * * ")
        if debug:
            print("Code barre: %s"%myCUP)
        try:
            mySAQ=cupToSaqCode(myCUP)
            trouver_bouteille(mySAQ)
        except:
            print("Pas d'info pour le code CUP: %s"%myCUP)
        print(" * * * * * * * ")
        tryAgain=0
        pass
    tryAgain-=1
    if tryAgain==0:
        rep=input("Incapable de déterminer le code CUP. Entrer manuellement? \n")

if tryAgain>0:
    #rep=input("Millésime: ? \n")
    rep=input("Année minimale pour boire: ? \n")
    rep=input("Année maximale pour boire: ? \n")
    #rep=input("Notes: ? \n")
    rep=input("Info correcte? <y/n> \n")

cv2.destroyAllWindows()
vs.stop()

