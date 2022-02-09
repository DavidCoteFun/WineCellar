#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""

from pyzbar import pyzbar
import argparse
import cv2
from requests_html import HTMLSession
import json
import urllib.request


#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to input image")
#args = vars(ap.parse_args())

image = cv2.imread("images/Untitled.jpg")
barcodes = pyzbar.decode(image)
cupCode=barcodes[0].data.decode("utf-8")
print("Code barre: %s"%cupCode)

#CUP to SAQ
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

#Wine info
myURL="https://www.saq.com/fr/%s"%saqCode
r2 = session.get(myURL)
productInfo=r2.html.find(".product.info.main .page-title-wrapper")[0].text
print(productInfo)
prix=r2.html.find(".wrapper-price-promotions .product-info-price")[0].text
prix2=prix.replace(u'\xa0$','').replace(',','.')
prix3=float(prix2)
print("Prix: %.2f $"%prix3)

xtraInfo=r2.html.find(".product.data.items .product-data-item-additional .additional-attributes-wrapper .col-8-moins-1 ul.list-attributs li")
print("Details:")
for i in xtraInfo:
    print(" %s"%i.text)
    print(" %s: %s"%(i.find("span")[0].text,i.find("strong")[0].text))


