#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""


from requests_html import HTMLSession
import json
import urllib.request


def getInfoFromSAQ(cupCode,debug=False):
    saqInfo={}
    try:
        saqCode=getSaqCode(cupCode)
    except:
        print("Incapable de trouver le code SAQ a partir du CUP: %s"%cupCode)
        saqInfo['Code SAQ']="Inexistant"
        saqInfo['Code CUP']=cupCode
        rep=input("Entrer le code SAQ manuellement ou <enter> continuer sans code\n")
        if len(rep)>3:
            print(" ")
            saqCode=rep
        else:
            return saqInfo

    try:
        saqInfo=getInfoFromSaqCode(saqCode,debug)
    except:
        print("Incapable de trouver l'info pour le code SAQ: %s"%saqCode)
        print("https://www.saq.com/fr/%s"%saqCode)
    
    #Easier to stick to original formats, not webpage info, for these codes
    saqInfo['Code SAQ']=saqCode
    saqInfo['Code CUP']=cupCode
    saqInfo['Bue']="saq_web"
    return saqInfo
    

def getSaqCode(cupCode):
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

    #bug fix July 28th 2021 after an upgrade of SAQ website
    if not saqCode.isnumeric():
        saqCode=saqCode.split('\n')[0]
    return saqCode


def getInfoFromSaqCode(saqCode,debug=False):
    myInfo={}
    myURL="https://www.saq.com/fr/%s"%saqCode
    if debug:
        print("WEB INFO:")
        print(myURL)
    session = HTMLSession()
    r2 = session.get(myURL)
    productInfo=r2.html.find(".product.info.main .page-title-wrapper")[0].text.split('\n')[0]
    myInfo['ProductInfo']=productInfo
    if debug:
        print(productInfo)

    try:
        prix=r2.html.find(".wrapper-price-promotions .product-info-price")[0].text
        prix2=prix.replace(u'\xa0$','').replace(',','.')
        prix3=prix2.split('\n')[0]
        prix4=float(prix3)
        myInfo['Prix']=prix4
        if debug:
            print("Prix: %.2f $"%prix4)
    except:
        print("Prix inconnu")
        
    xtraInfo=r2.html.find(".product.data.items .product-data-item-additional .additional-attributes-wrapper .col-8-moins-1 ul.list-attributs li")
    for xx in xtraInfo:
        i=xx.find("strong",first=True)
        key=i.attrs['data-th']
        val=i.text.split('\n')[0]
        val=val.replace('\xa0',' ')
        myInfo[key]=val
        if debug:
            print(" %s: %s"%(key,val))

    myInfo['Millesime']=0
    tmp=myInfo['ProductInfo'].split(' ')[-1]
    if tmp.isnumeric():
        myInfo['Millesime']=int(tmp)
        tmp2=myInfo['ProductInfo']
        myInfo['ProductInfo']=tmp2.replace(tmp,'')
        pass
    
    tmp=myInfo['Format']
    if "ml" in myInfo['Format']:
        myInfo['Format']=int(tmp.replace('ml',''))
    elif "L" in myInfo['Format']:
        tmp=float(tmp.replace('L','').replace(',','.'))
        myInfo['Format']=int(1000*tmp)
        
    return myInfo

