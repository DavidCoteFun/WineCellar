from requests_html import HTMLSession
import json
import urllib.request
import libSelenium as lSelenium


myURL="https://www.lcbo.com/fr/brut-vqa-trius-284539"
#myURL="https://www.lcbo.com/en/trius-brut-ros-c-sparkling-17690"
#myURL="https://www.lcbo.com/en/trius-red-303800"
#myURL="https://www.lcbo.com/fr/chateau-la-lagune-2024-46850"
debug=True

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

if "Plus de détails" in rawHTML:
    details=rawHTML.split('Plus de détails')[1].split('\n')
elif "More Details" in rawHTML:
    details=rawHTML.split('More Details')[1].split('\n')
else:
    print("Incapable de trouver les détails du produit")
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

myInfo['ProductInfo']=rawHTML.split('|')[0]
myInfo['Millesime']=0

myInfo['CodeSAQ']=""
if "lcbo.com/fr/" in myURL:
    if myInfo['CodeSAQ']=="":
        try:
            myInfo['CodeSAQ']=rawHTML.split('LCBO n° :\n')[1].split('\n')[0]
            print(myInfo['CodeSAQ'])
        except:
            myInfo['CodeSAQ']=""

    if myInfo['CodeSAQ']=="":
        try:
            myInfo['CodeSAQ']=rawHTML.split('VINTAGES\xa0:\n')[1].split('\n')[0]
            print(myInfo['CodeSAQ'])
        except:
            myInfo['CodeSAQ']=""

else:
    if myInfo['CodeSAQ']=="":
        try:
            myInfo['CodeSAQ']=rawHTML.split('LCBO#:\n')[1].split('\n')[0]
            print(myInfo['CodeSAQ'])
        except:
            myInfo['CodeSAQ']=""

    if myInfo['CodeSAQ']=="":
        try:
            myInfo['CodeSAQ']=rawHTML.split('VINTAGES#:\n')[1].split('\n')[0]
            print(myInfo['CodeSAQ'])
        except:
            myInfo['CodeSAQ']=""

print(myInfo)

#rawHTML.split('VINTAGES')[1][:10]
#rawHTML.split('Passer à la fin de la galerie')
