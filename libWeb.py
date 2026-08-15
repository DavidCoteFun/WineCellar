#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""

from requests_html import HTMLSession
import json
import urllib.request
import libSelenium as lSelenium


def getInfoFromWeb(cupCode,debug=False):
    saqInfo={}
    saqCode=None
    productURL=None

    try:
        productURL = lSelenium.getProductURL(cupCode)

    except:
        print("Incapable de trouver le code SAQ a partir du CUP: %s"%cupCode)
        saqInfo['Code SAQ']="Inexistant"
        saqInfo['Code CUP']=cupCode
        rep=input("Entrer le code SAQ or l'URL manuellement, ou <enter> continuer sans code\n")
        if ".com" in rep:
            productURL = rep
        elif len(rep)>3:
            print(" ")
            saqCode=rep
            productURL="https://www.saq.com/fr/%s"%saqCode
        else:
            return saqInfo

    if "saq.com" in productURL:
        saqCode = productURL.split('/')[-1]

        try:
            saqInfo=getInfoFromSaqCode(saqCode,debug)
            saqInfo['Code SAQ']=saqCode
        except:
            print("Incapable de trouver l'info pour le code SAQ: %s"%saqCode)
            print("https://www.saq.com/fr/%s"%saqCode)

    elif "lcbo.com" in productURL:
        try:
            saqInfo=getInfoFromLCBOWeb(productURL,debug)
        except:
            print("Incapable de trouver l'info pour la LCBO")
            print(productURL)

    
    #Easier to stick to original formats, not webpage info, for these codes
    saqInfo['Code CUP']=cupCode
    saqInfo['Bue']="saq_web"
    return saqInfo
    
def getSAQCode_fromCUP_old_obsolete(cupCode):
    # Historic function working with SAQ website up to 2024.
    # No longer works since a website update some time in 2025.
    # Replaced by lSelenium.getProductURL(cupCode)
    
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


def getSaqCode_obsolete(cupCode):
    #tmpURL2 = getSAQCode_fromCUP_old_obsolete(cupCode)
    productURL = lSelenium.getProductURL(cupCode)
    saqCode = productURL.split('/')[-1]
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



def getInfoFromLCBOWeb(myURL,debug=False):
    myInfo={}
    if debug:
        print("WEB INFO:")
        print(myURL)

    session = HTMLSession()
    r2 = session.get(myURL)
    rawHTML=r2.html.text

    try:
        prix=float(rawHTML.split('final_price":')[1].split(',')[0])
        myInfo['Prix']=float(rawHTML.split('final_price":')[1].split(',')[0])
        if debug:
            print("Prix: %.2f $"%prix)
    except:
        print("Prix inconnu")


    myInfo['CodeSAQ']=""
    if "lcbo.com/fr/" in myURL:
        if myInfo['CodeSAQ']=="":
            try:
                myInfo['CodeSAQ']=rawHTML.split('LCBO n° :\n')[1].split('\n')[0]
            except:
                myInfo['CodeSAQ']=""

        if myInfo['CodeSAQ']=="":
            try:
                myInfo['CodeSAQ']=rawHTML.split('VINTAGES\xa0:\n')[1].split('\n')[0]
            except:
                myInfo['CodeSAQ']=""

    else:
        if myInfo['CodeSAQ']=="":
            try:
                myInfo['CodeSAQ']=rawHTML.split('LCBO#:\n')[1].split('\n')[0]
            except:
                myInfo['CodeSAQ']=""

        if myInfo['CodeSAQ']=="":
            try:
                myInfo['CodeSAQ']=rawHTML.split('VINTAGES#:\n')[1].split('\n')[0]
            except:
                myInfo['CodeSAQ']=""

        
    if "Plus de détails" in rawHTML:
        details=rawHTML.split('Plus de détails')[1].split('\n')
    elif "More Details" in rawHTML:
        details=rawHTML.split('More Details')[1].split('\n')
    else:
        print("Incapable de trouver les détails du produit LCBO")
        details=[]

    allKeys=["Date de la livraison","Degré d'alcool","Origine","Appellation","Par","Teneur en sucre","Style","Cépage"]
    allKeys+=["Release Date","Alcohol/Vol","Made In","By","Sugar Content","Style","Varietal"]

    i=0
    while i<len(details):
        key=details[i]
        if key in allKeys:
            value = details[i+1]
            if debug:
                print("%s: %s"%(key,value))
            if key=="Degré d'alcool" or key=="Alcohol/Vol":
                alcool=float(value.split('%')[0])
                myInfo['Alcool']=alcool
            elif key=="Origine" or key=="Made In":
                myInfo['Region']=value
            elif key=="Appellation":
                myInfo['Appellation']=value
            elif key=="Par" or key=="By":
                myInfo['Producteur']=value
            elif key=="Teneur en sucre" or key=="Sugar Content":
                sucre=float(value.split('\xa0')[0])
                myInfo['Sucre']=sucre
            elif key=="Cépage" or key=="Varietal":
                myInfo['Cepages']=value
            #elif key=="" or key=="":
            #    myInfo['']=value
        i+=1

    myInfo['ProductInfo']=""
    myInfo['Millesime']=0

    if debug:
        print(myInfo)
    return myInfo

