get file='./rohdaten/daten2014.sav'.
SORT CASES BY Geburtsjahr.
COMPUTE Altersstufe=  MAX(10,MIN(60,5*TRUNC((2014-Geburtsjahr)/5))).
SPLIT FILE BY Altersstufe.
FREQUENCIES
  /VARIABLES=AusgabenHardware
  /FORMAT=TABLE
  /STATISTICS=NONE.
FREQUENCIES
  /VARIABLES=AusgabenSpieleKauf
  /FORMAT=TABLE
  /STATISTICS=NONE.
FREQUENCIES
  /VARIABLES=AusgabenSpieleAbos
  /FORMAT=TABLE
  /STATISTICS=NONE.
FREQUENCIES
  /VARIABLES=AusgabenAddonsDLCs
  /FORMAT=TABLE
  /STATISTICS=NONE.
FREQUENCIES
  /VARIABLES=AusgabenGameserver
  /FORMAT=TABLE
  /STATISTICS=NONE.
SPLIT FILE OFF.
EXIT.

