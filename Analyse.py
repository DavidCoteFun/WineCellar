import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

nTot=df['Millesime'].loc[df['Bue']=='non'].count()
n2020_plus=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']>=2020].count()
n2015_2019=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']>=2015].loc[df['Millesime']<2020].count()
n2010_2014=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']>=2010].loc[df['Millesime']<2015].count()
n2005_2009=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']>=2005].loc[df['Millesime']<2010].count()
n2000_2004=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']>=2000].loc[df['Millesime']<2005].count()
n1990_1999=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']>=1990].loc[df['Millesime']<2000].count()
n1980_1989=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']>=1980].loc[df['Millesime']<1990].count()
n1979_moins=df['Millesime'].loc[df['Bue']=='non'].loc[df['Millesime']<=1979].count()

print("Total    : %i"%nTot)
print("2020+    : %i"%n2020_plus)
print("2015-2019: %i"%n2015_2019)
print("2010-2014: %i"%n2010_2014)
print("2005-2009: %i"%n2005_2009)
print("2000-2004: %i"%n2000_2004)
print("1990-1999: %i"%n1990_1999)
print("1980-1989: %i"%n1980_1989)
print("1979-    : %i"%n1979_moins)

tmp=(n2015_2019+n2020_plus)/nTot*100
print("2015+ : %.1f%% "%tmp)
tmp=(n2000_2004+n2005_2009+n2010_2014)/nTot*100
print("2000-2014 : %.1f%% "%tmp)
tmp=(n1990_1999+n1980_1989+n1979_moins)/nTot*100
print("1999-  : %.1f%% "%tmp)


dd=df['Millesime'].loc[df['Bue']=="non"].loc[df['Millesime']>0]
#dd.value_counts()
nbins=dd.max()-dd.min()
ax = dd.plot.hist(bins=nbins,ylabel="",title="Nombre de bouteilles par millésime")
ax.set_ylabel(' ')
ax.set_xlabel('Millésime')
plt.show()



"""
Total    : 536
2020+    : 170
2015-2019: 203
2010-2014: 66
2005-2009: 29
2000-2004: 22
1990-1999: 19
1980-1989: 12
1979-    : 15


2015+ : 69.6% 
2000-2014 : 21.8% 
1999-  : 8.6% 


La Côte d'Or "By The Book"

./MaCave.py Bo date:2026-3-25 cup:3337694116104 
Bouchard Père & Fils Volnay Premier Cru Caillerets Ancienne Cuvée Carnot 2020

./MaCave.py Bo date:2026-3-25 cup:3337694116111 
Bouchard Père & Fils Pommard Premier Cru 2020

./MaCave.py Bo date:2026-3-25 cup:3260980024039
Morin Père & Fils Pommard 2005

./MaCave.py Bo date:2026-3-25 cup:TaupenotRiotte2009
Domaine Taupenot-Merme Morey-Saint-Denis Premier Cru La Riotte 2009

./MaCave.py Bo date:2026-3-25 cup:TaupenotOrveau2011 
Domaine Taupenot-Merme Chambolle-Musigny Premier Cru La Combe d'Orveau 2011

TBD Domaine Jean Tardy Vosne-Romanée 1er Cru Les Chaumes 2006

./MaCave.py Bo date:2026-3-25 cup:3340778001647 
Domaine Nuiton-Beaunoy Clos de la Roche Grand Cru 2011

./MaCave.py Bo date:2026-3-25 cup:RionChambolleMusigny1995 -d 
Domaine Patrice Rion Chambolle-Musigny Les Cras 1995

./MaCave.py Bo date:2026-3-25 cup:3463260065955 -d
Domaine A-F Gros Vosne-Romanée Premier Cru Clos des Réas 1995

./MaCave.py Bo date:2026-3-25 cup:BeauneTollotBeau1993 -d  
Domaine Tollot-Beaut Beaune Clos du Roi Premier Cru 1993

2026-3-25
AVO La Bourgogne By The Book. Avril 2026.

./MaCave.py Bo date:2026-3-25 cup:
"""


