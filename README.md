# Examensarbete - ObjektIdentifiering med användargränssnitt
Examensarbete - YH 30 - Campus Varberg

# Verktyg

PyCharm Community Edition\
Visual Studio Code\
PyQt Designer

# Kodspråk
Python 3 (64-bitar)

# Bibliotek
PyQt5\
OpenCv 3/4\
pywin32\
keyboard

# Paketinstallerare
pip/pip3

# Funktionalitet
Användaren kan välja mellan två lägen. Default som har \
stöd för egen användarinput där användaren själv\
kan lägga in en egen bild och med hjälp av den kunna\
hitta liknande objekt på skärmen eller angiven ruta.
Threshold styr hur likt objektet ska vara, 1 är 100%, medan 0.4 är 40%.\

Användaren kan även ta hjälp av HSV för att
"svarta ner" allt som inte anknyts till objektet.
Observera att programmet måste vara inställt i samma HSV
som bilden är tagen i. Detta görs möjligt genom att välja en tillfällig bild,
sätta thresholden till 1 och start/stoppa körningen. Då kommer en skärmdump upp som användaren
kan screenshota.

FPS är tränad med OpenCV:s cascade classifier inom CSGO i banan
Dust 2 mot Terrorister. Programmet försöker då ringa in i terroristerna
i en ruta. Detta är dock inte helt korrekt, då den ibland
anger Anti-Terrorister som matchningar och även annan omgivning i spelet.

Resultaten av matchningarna kan ses i PyQt menyn och även 
det justerbara kantfönstret. Programmet anpassar sig även 
efter enhetens upplösning, men fungerar bäst i 16:9 (1920:1080)

# Källor
https://stackoverflow.com/ \
https://www.youtube.com/playlist?list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI \
https://opencv.org/ \
https://pypi.org/

# Exempelbilder
<img src="https://github.com/lindgrenkamali/Examensarbete-ObjectDetection-with-UI/blob/main/README-IMAGES/objectdetection.png?raw=true" />
I exemplet har jag använt klippt ut en av solrosorna från bilden. Med 54% (0.54) säkerhet kunde programmet identifiera 4 solrosor från bilden som ringas in med 
gröna fyrkanter.
