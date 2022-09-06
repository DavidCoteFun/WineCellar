# WineCellar

https://github.com/DavidCoteFun/WineCellar

## Instructions pour installer le soft
```
*) Install Anaconda3

*) Install HomeBrew and zbar

#On new Mac architecture arm64 (M1)
/usr/sbin/softwareupdate --install-rosetta --agree-to-license
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install zbar

#On old Mac architecture x86_64 (Intel)
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
arch -x86_64 /usr/local/bin/brew install zbar 

*) Additional python libraries:
pip install pyzbar
pip install opencv-python
pip install requests-html
pip install imutils

*) Resources:
https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
```

## Historique
```
Version 1.0.0 --> 21 mars 2021. Pas de bug connu.
Version 1.0.1 --> Option d'ajouter plusieurs bouteilles d'un coup (28.03.2021)
Version 1.0.2 --> Option d'ajouter un CUP manuellement et fonction d'aide (02.04.2021)
Version 1.0.3 --> Option d'ajouter code SAQ manuellement, fonction resume_de_la_cave (18.04.2021)
23 avil 2021: premier inventaire complet de la cave (utilisant v1.0.3)
Version 1.0.4 --> Minor bug fix avec getWebInfo avec cup "custom"
Version 1.1.0: mise à jour de libWeb.py pour suivre le nouveau site de la SAQ (28.07.2021)
```

## Usage:
```
1) Start PhotoBooth (optionel)
2) Start command shell

#test or debug
python MaCave.py -t -d

#normal usage
python MaCave.py Ajouter
python MaCave.py Ajouter x5
python MaCave.py Boire
python MaCave.py Editer
```

### Details
```
En plus de l'info standard de la SAQ, option d'ajouter manuellement:
-millesime
-annees min et max recommandees pour boire
-lieu d'achat (SAQ, Ampuis, IEGOR, cadeau, ...)
-notes supplementaires as free text
```

### Custom Edits avec Excel
```
Start Excel create new empty Book
File --> Import --> CSV File  --> MaCave.csv
 Step 1 --> Delimted, File origin: Unicode (UTF-8) --> Next
 Step 2 --> Delimiters: comma --> Next
 Step 3 --> Cliquer sur colonnes CodeSAQ et CodeCUP --> format text --> Finish
Faire les modifications
File --> SaveAs --> Format CSV UTF-8
```

### Custom CUPs pour bouteilles non-SAQ
```
cup:BelleHelene2009
cup:xyz
```
