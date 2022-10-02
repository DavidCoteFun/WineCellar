#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""

import pandas as pd
from os import listdir
from datetime import date

df_original=None
gDF=None
theEncoding='utf-8'

def get_default_values():
    dVal={}
    dVal['ProductInfo']=""
    dVal['Prix']=0.0
    dVal['Pays']=""
    dVal['Region']=""
    dVal['Appellation']=""
    dVal['Designation']=""     #'Désignation réglementée': '(AOC/AOP) Appellation origine controlée/protégée'
    dVal['Classification']=""  #"Grand cru classe"
    dVal['Alcool']=0.0               
    dVal['Sucre']=0.0
    dVal['Couleur']="Rouge"
    dVal['Cepages']=""
    dVal['Format']=750
    dVal['Producteur']=""
    dVal['Agent']=""
    dVal['CodeSAQ']=""
    dVal['CodeCUP']=""
    dVal['Millesime']=0
    dVal['BoireMin']=0
    dVal['BoireMax']=0
    dVal['Bue']="non"
    dVal['AcquiseOu']=""
    dVal['Notes']=""
    dVal['Particularite']="" #vin Bio
    return dVal


def init_global_df(fDir="../WineCellarData",fName="MaCave.csv"):
    global gDF, df_original
    if gDF is None:
        gDF=load_df(fDir,fName)
    if df_original is None:
        df_original=gDF.copy(deep=True)
    return gDF

def load_df(fDir,fName="MaCave.csv"):
    try:
        ffName="%s/%s"%(fDir,fName)
        print("Loading DataFrame %s ..."%ffName)
        df = pd.read_csv(ffName, index_col=None, header=0, encoding=theEncoding, dtype={'CodeCUP': str, 'CodeSAQ':str}, sep="|")
        df=df.fillna('')
    except:
        print("Erreur avec %s"%ffName)
        print("Retourne un DataFrame vide...")
        df=pd.DataFrame(columns=get_default_values().keys())
    return df

def resume_de_la_cave(df,verbose=1):
    cInfo={}
    cInfo['nPleines']=len(df.loc[df['Bue']=="non"])
    cInfo['nTotal']=len(df)
    if verbose>0:
        print("Bouteilles pleines: %i"%cInfo['nPleines'])
        print("Historique: %i"%cInfo['nTotal'])
        pass
    return cInfo

def write_df(fDir="../WineCellarData",fDirBack="fichiers_csv",fName="MaCave.csv",doBackup=True):
    global gDF
    if doBackup:
        global df_original
        if df_original is None:
            print("Erreur: impossible de faire un backup!!")
        else:
            allFiles=listdir(fDir)
            myDay=date.today()
            bfName=fName.replace(".csv","_backup_%s.%s.%s.csv"%(myDay.year,myDay.month,myDay.day))
            if not (bfName in allFiles):
                fbfName="%s/%s"%(fDirBack,bfName)
                print("Backup: %s"%fbfName)
                df_original.to_csv(fbfName, encoding=theEncoding,index=False)
                pass
            pass
        pass
    
    ffName="%s/%s"%(fDir,fName)
    gDF.to_csv(ffName, encoding=theEncoding,index=False,sep="|")
    #gDF.to_excel(ffName.replace(".csv",".xslx"))
    print("Mise à jour du fichier: %s"%ffName)
    return


def webSaqToStandardSchema(webInfo):
    #first default values
    stdInfo=get_default_values()
    #then fill standard keys if present
    for kk in stdInfo.keys():
        if kk in webInfo:
            stdInfo[kk]=webInfo.pop(kk)

    #now deal with known special cases
    if "Région" in webInfo:
        stdInfo['Region']=webInfo.pop('Région')
    if "Appellation d'origine" in webInfo:
        stdInfo['Appellation']=webInfo.pop("Appellation d'origine")
    if "Désignation réglementée" in webInfo:
        stdInfo['Designation']=webInfo.pop('Désignation réglementée')
    if "Degré d'alcool" in webInfo:
        # 14,5 % --> 14.5
        tmp=webInfo.pop("Degré d'alcool")
        stdInfo['Alcool']=float(tmp.replace('%','').replace(',','.'))
    if "Taux de sucre" in webInfo:
        # 1,9 g/L  --> 1.9
        tmp=webInfo.pop('Taux de sucre')
        stdInfo['Sucre']=float(tmp.replace("g/L","").replace(",",".").replace("<",""))
    if "Code SAQ" in webInfo:
        stdInfo['CodeSAQ']=webInfo.pop('Code SAQ')
    if "Code CUP" in webInfo:
        stdInfo['CodeCUP']=webInfo.pop('Code CUP')
    if "Agent promotionnel" in webInfo:
        stdInfo['Agent']=webInfo.pop('Agent promotionnel')
    if "Cépages" in webInfo:
        stdInfo['Cepages']=webInfo.pop('Cépages')
    if "Cépage" in webInfo:
        stdInfo['Cepages']=webInfo.pop('Cépage')
    if "Particularité" in webInfo:
        stdInfo['Particularite']=webInfo.pop('Particularité')
    
    #Anything left? Should not...
    if len(webInfo)>0:
        print("WARNING: ignoring keys %s"%webInfo.keys())
    return stdInfo

def getInfoFromDB(myCUP,aDF=None,PleineSeulement=False):
    if aDF is None:
        global gDF
        aDF=gDF
    d1=aDF.loc[aDF['CodeCUP']==myCUP]
    d1=d1.drop_duplicates()
    if PleineSeulement:
        d1=d1.loc[d1['Bue']=="non"]
    return d1


def get_df_index(btleInfo,btle_pleine):
    global gDF
    #Note: unique id is CUP + Millesime + Notes
    myCUP=btleInfo.original_dict['CodeCUP']
    myYear=btleInfo.original_dict['Millesime']
    myNote=btleInfo.original_dict['Notes']
    if btle_pleine:
        myInd=gDF.loc[(gDF['CodeCUP']==myCUP) & (gDF['Millesime']==myYear) & (gDF['Notes']==myNote) & (gDF['Bue']=="non")].index
    else:
        dateBue=btleInfo.original_dict['Bue']
        myInd=gDF.loc[(gDF['CodeCUP']==myCUP) & (gDF['Millesime']==myYear) & (gDF['Notes']==myNote) & (gDF['Bue']==dateBue)].index

    if len(myInd)>0:
        if len(myInd)>1:
            print("Warning - Non-unique index")
            pass
        return myInd[0]
    return None


def efface_bouteille(btleInfo):
    #df3.drop(index=3)
    return

def ajouter_bouteille(btleInfo,nBtles=1):
    global gDF
    k1=list(btleInfo.resolved_dict.keys()).sort()
    k2=list(gDF.keys()).sort()
    if k1==k2:
        btleInfo.resolved_dict['Bue']="non"
        i=0
        while i<nBtles:
            gDF=gDF.append(btleInfo.resolved_dict,ignore_index=True)
            i+=1
            pass
    else:
        print("Erreur: impossible d'ajouter la bouteille car le schema est inchoherent")
        print("%i keys: %s"%(len(k1),k1))
        print("%i keys: %s"%(len(k2),k2))
    return


def boire_bouteille(btleInfo):
    global gDF
    theIndex=get_df_index(btleInfo,btle_pleine=True)
    if theIndex is None:
        print("Warning - Pas de bouteille disponible pour boire!")
    else:
        myDay=date.today()
        gDF['Bue'].at[theIndex]="%s-%s-%s"%(myDay.year,myDay.month,myDay.day)
    return

def modifier_bouteille(btleInfo):
    theIndex=get_df_index(btleInfo,btle_pleine=False)
    if theIndex is None:
        print("Warning - Pas d'index pour modifier")
    else:
        for k in btleInfo.resolved_dict:
            gDF[k].at[theIndex]=btleInfo.resolved_dict[k]
    return

