get file='./rohdaten/daten2014.sav'.
COMPUTE Jahrgang1=MAX(1999,MIN(2015,Release1)).
SORT CASES BY Jahrgang1.
SPLIT FILE BY Jahrgang1.
FREQUENCIES
  /VARIABLES=Spiel1
  /FORMAT=TABLE
  /STATISTICS=NONE.
SPLIT FILE OFF.
COMPUTE Jahrgang2=MAX(1999,MIN(2015,Release2)).
SORT CASES BY Jahrgang2.
SPLIT FILE BY Jahrgang2.
FREQUENCIES
  /VARIABLES=Spiel2
  /FORMAT=TABLE
  /STATISTICS=NONE.
SPLIT FILE OFF.
COMPUTE Jahrgang3=MAX(1999,MIN(2015,Release3)).
SORT CASES BY Jahrgang3.
SPLIT FILE BY Jahrgang3.
FREQUENCIES
  /VARIABLES=Spiel3
  /FORMAT=TABLE
  /STATISTICS=NONE.
SPLIT FILE OFF.
COMPUTE Jahrgang4=MAX(1999,MIN(2015,Release4)).
SORT CASES BY Jahrgang4.
SPLIT FILE BY Jahrgang4.
FREQUENCIES
  /VARIABLES=Spiel4
  /FORMAT=TABLE
  /STATISTICS=NONE.
SPLIT FILE OFF.
COMPUTE Jahrgang5=MAX(1999,MIN(2015,Release5)).
SORT CASES BY Jahrgang5.
SPLIT FILE BY Jahrgang5.
FREQUENCIES
  /VARIABLES=Spiel5
  /FORMAT=TABLE
  /STATISTICS=NONE.
SPLIT FILE OFF.
EXIT.

