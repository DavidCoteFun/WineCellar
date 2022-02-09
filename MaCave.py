#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""
theVersion="1.1.0"

import sys
import libDataframe as lDF
import libWeb as lWeb
import libUI as lUI
from libBtleInfo import BtleInfo

#import pandas as pd
#import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
#from matplotlib.backends.backend_pdf import PdfPages

print("Ma Cave - Version %s \n"%theVersion)

myCUP=None
Test=False
Debug=False
Ajouter=False
Enlever=False
Editer=False
Info=True
nBtles=1
args=sys.argv[1:]
for arg in args:
    if arg=='-d':
        Debug=True    
    elif arg=='-t':
        Test=True
    elif arg.startswith('x'):
        nBtles=int(arg.split('x')[1])
    elif arg.startswith('Aj'):
        Ajouter=True
        print("  *** AJOUTER ***")
    elif (arg.startswith('Bo') or arg.startswith('En')):
        Enlever=True
        print("  *** BOIRE ***")
    elif arg.startswith('Ed'):
        Editer=True
        print("  *** EDITER ***")
    elif arg.startswith('In'):
        Info=True    
        print("  *** INFO ***")
    elif arg.startswith("cup:"):
        myCUP=arg.split("cup:")[1]
        print("  *** SET CUP : %s ***"%myCUP)
    elif arg=="-h" or arg=="help":
        print("*** HELP CENTER ***")
        print("#test or debug")
        print("python MaCave.py -t -d cup:3760091910011")
        print("")
        print("#normal usage")
        print("python MaCave.py Ajouter")
        print("python MaCave.py Ajouter x5")
        print("python MaCave.py Ajouter cup:1234524")
        print("python MaCave.py Boire")
        print("python MaCave.py Editer")
        print(" ")
        sys.exit()
    else:
        print("WARNING argument: %s inconnu"%arg)


getDB=(Enlever or Editer or Info or Ajouter)
getWeb=(Ajouter or Info) and not (Enlever or Editer)
#if myCUP:
#    getWeb=False

print(" ")
bInfo=BtleInfo()
bInfo.debug=Debug
df=lDF.init_global_df()
cInfo_initial=lDF.resume_de_la_cave(df,verbose=1)

if myCUP is None:
    myCUP=lUI.getCUP(debug=Debug)

if myCUP:
    if getDB:
        print("*** Getting DB info ***")
        dbInfo=lDF.getInfoFromDB(myCUP,PleineSeulement=Enlever)
        bInfo.add(dbInfo)
        pass
    
    if getWeb:
        print("*** Getting Web info ***")
        webInfo=lWeb.getInfoFromSAQ(myCUP,debug=Debug)
        webInfo=lDF.webSaqToStandardSchema(webInfo)
        bInfo.add(webInfo)
        pass
    
    bInfo.resolve()
            
    if Ajouter or Editer:
        bInfo.edit_btle()
    else:
        bInfo.Print(True)


if bInfo.is_ready():    
    if Ajouter:
        lDF.ajouter_bouteille(bInfo,nBtles)
    
    if Enlever:
        lDF.boire_bouteille(bInfo)
    
    if Editer:
        lDF.modifier_bouteille(bInfo)
    
    if (Ajouter or Editer or Enlever):
        if Ajouter:
            rep=input("Modifier la base de données pour Ajouter? <y> \n")
        elif Enlever:
            rep=input("Modifier la base de données pour Boire? <y> \n")
        else:
            rep=input("Modifier la base de données pour Editer? <y> \n")

        if (rep == "") or (rep == "y"):
            lDF.write_df(doBackup=True)
            print("INTIAL:")
            lDF.resume_de_la_cave(lDF.df_original,verbose=1)
            print("FINAL:")
            cInfo_final=lDF.resume_de_la_cave(lDF.gDF,verbose=1)
            pass
        pass
    pass
else:
    print("Erreur - bInfo not ready")

