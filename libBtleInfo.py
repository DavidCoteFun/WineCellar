#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:48:33 2021

@author: dcote
"""

import pandas
import time
import copy
import libUI as lUI

from itertools import groupby
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


class BtleInfo():
    def __init__(self):
        self.raw_inputs=[]
        self.consolidated_dict={}
        self.resolved_dict={}
        self.original_dict={}
        self.debug=False
        return

    def is_ready(self):
        return len(self.resolved_dict.keys())>1
    
    def Print(self,debug=False):
        if not self.is_ready():
            print("Warning - BtleInfo.resolved_dict is not ready")
            print("Consolidated_dict:")
            print(self.consolidated_dict)
            return
        
        important_keys=['ProductInfo','Prix','Pays','Region','Appellation','Cepages','Alcool','Sucre','Millesime','BoireMin','BoireMax','AcquiseOu','Notes']
        for k in important_keys:
            try:
                print("%s: %s"%(k,self.resolved_dict[k]))
            except KeyError:
                print("%s: ???"%k)
            
        if debug:
            print(" ")
            for k in self.resolved_dict.keys():
                if not (k in important_keys):
                    try:
                        print("%s: %s"%(k,self.resolved_dict[k]))                    
                    except KeyError:
                        print("%s: ???"%k)
        print(" ")
        return
    
    def add(self,info):
        self.raw_inputs.append(info)
        if isinstance(info,dict):
            self.add_dict(info)
        elif isinstance(info,pandas.core.frame.DataFrame):
            self.add_df(info)
        else:
            print("BtleInfo: Unsupported type %s"%(type(info)))
        
        return

    def add_dict(self,info):
        for key in info.keys():
            if not (key in self.consolidated_dict):
                self.consolidated_dict[key]=[]
                pass
            self.consolidated_dict[key].append(info[key])
        return
    
    def add_df(self,info):
        for key in info.keys():
            if not (key in self.consolidated_dict):
                self.consolidated_dict[key]=[]

            for val in info[key]:
                #if not (val in self.consolidated_dict[key]):
                self.consolidated_dict[key].append(val)
        return
    
    def resolve(self):
        #this function goes from vList to val
        cd=self.consolidated_dict
        keysToResolve=[]
        for key in cd.keys():
            vList=cd[key]
            if not isinstance(vList,list):
                print("Error consolidated_dic vList is not a list?? --> %s : %s"%(key,vList))
                return False
            
            if len(vList)<1:
                print("Warning - Pas d'info sur cette bouteille")
                break
            elif all_equal(vList):
                self.resolved_dict[key]=vList[0]
            else:
                keysToResolve.append(key)
            pass

        if self.debug:
            print("keysToResolve: %s"%keysToResolve)
        if keysToResolve:
            kGroup=[]
            i=0
            maxNVals=len(self.consolidated_dict[keysToResolve[0]])
            while i<maxNVals:
                dTmp={}
                kGroup.append(dTmp)
                i+=1

            for k in keysToResolve:
                i=0
                while i<maxNVals:
                    kGroup[i][k]=self.consolidated_dict[k][i]
                    i+=1
            
            if maxNVals<1:
                print("WARNING - Aucune info sur cette bouteille")
                return False
            
            isAmbiguous=True
            if len(keysToResolve)==1 and keysToResolve[0]=="Bue" and maxNVals==2:
                if kGroup[0]["Bue"]=="saq_web":
                    self.resolved_dict["Bue"]=kGroup[1]["Bue"]
                    isAmbiguous=False
                elif kGroup[1]["Bue"]=="saq_web":
                    self.resolved_dict["Bue"]=kGroup[0]["Bue"]
                    isAmbiguous=False

            if isAmbiguous:
                self.Print(debug=True)
                print("Ambiguité entre %i bouteilles:"%maxNVals)
                i=0
                while i<maxNVals:
                    print("%i"%(i+1))
                    dTmp=kGroup[i]
                    for iK in dTmp:
                        if self.debug:
                            print("%s: %s (%s)"%(iK,dTmp[iK],type(dTmp[iK])))
                        else:
                            print("%s: %s"%(iK,dTmp[iK]))
                            pass
                        pass
                    i+=1
    
                rep=input("Quelle bouteille voulez-vous? \n")
                try:
                    iRep=int(rep)-1
                    dTmp=kGroup[iRep]
                    for k in keysToResolve:
                        self.resolved_dict[k]=dTmp[k]
                except:
                    print("Erreur - Entrer un chiffre entre 1 et %i"%maxNVals)
                    time.sleep(2)
                    return self.resolve()
        
        if len(self.original_dict)<1:
            self.original_dict=copy.deepcopy(self.resolved_dict)

        return True

    def edit_btle(self,dateBue=""):
        lUI.updateBtleInfoFromKeyboard(self,dateBue)
        return

    def set_date_bue(self,theDate):
        if isinstance(theDate,str):
            self.resolved_dict['Bue']=theDate
        else:
            print("Warning - wrong format date %s"%theDate)
        return
