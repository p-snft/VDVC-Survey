#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import dateutil.parser as dparser
import io
import re
import string
import sys
import unicodecsv

reload(sys)  
sys.setdefaultencoding('utf8')

# SPSS-Export
rohdaten='./rohdaten/rohdaten2014.dat'

duplikatsliste='./daten/schreibweisen.tsv'
zuordnungsliste='./daten/zuordnung.tsv'
ogdbgames='./rohdaten/ogdbexport20161024_211122.csv'
moregames='./daten/no-ogdb.tsv'

# Dateien für Ergebnisse
feedback = io.open("./rohdaten/feedback2014.dat", "w", encoding="utf8")
results = io.open("./rohdaten/daten2014.dat", "w", encoding="utf8")
versteck = io.open("./rohdaten/versteck2014.dat", "w", encoding="utf8")
zensurinfo = io.open("./rohdaten/zensurinfo2014.dat", "w", encoding="utf8")
nennungen = io.open("./daten/2014/nennungen.tsv", "w", encoding="utf8")
f_unbekannt = io.open("./daten/2014/unbekannte-titel.tsv", "w", encoding="utf8") 

def freigabe(string):
	parts = string.replace(',','_').split('_')
	kandidat=21
	for part in parts:
		if part.isnumeric():
			kandidat = min(kandidat,int(part))
		elif u"OA" in part:
			return u"USK0"
		elif u"KJ" in part:
			kandidat = min(kandidat,18)
	if kandidat == 21:
		return u""
	else:
		return u'USK'+unicode(kandidat)

freigabeordnung = {u'BPjM' : -1, u'StGB' : -1, u'USK0' : 0, u'USK6' : 1, u'USK12' : 2, u'USK16' : 3, u'USK18' : 4, u'' : 100, u'.' : 100}

d_unbekannt = {}

# Dieses Dictionary ordnet Spieltitel eine Releasejahr und eine USK-Friegabe zu
# Zuordnung von Genres wäre möglich.
with io.open(ogdbgames, encoding='utf8') as ogdb_file:
	ogdb_reader = unicodecsv.reader(ogdb_file,delimiter=";")
	ogdb_list=[]
	lastentry=""
	for ogdb_entry in ogdb_reader:
		if ogdb_entry[0].lower() == lastentry:
			if freigabe(ogdb_entry[3]) != u'':
				if ogdb_list[-1][2] == u'':
					ogdb_list[-1][2]=freigabe(ogdb_entry[3])
				elif freigabeordnung[freigabe(ogdb_entry[3])] < freigabeordnung[ogdb_list[-1][2]]:
					ogdb_list[-1][2]=freigabe(ogdb_entry[3])
		else:
			ogdb_list.append([ogdb_entry[0].lower(),ogdb_entry[9],freigabe(ogdb_entry[3])])
			lastentry=ogdb_entry[0].lower()

	ogdblookup={ogdb_entry[0]:(ogdb_entry[1],ogdb_entry[2]) for ogdb_entry in ogdb_list}

def freigabe(string):
    parts = string.replace(',','_').split('_')
    kandidat=21
    for part in parts:
        if part.isnumeric():
            kandidat = min(kandidat,int(part))
        elif u"OA" in part:
            return u"USK0"
        elif u"KJ" in part:
            kandidat = min(kandidat,18)
    if kandidat == 21:
        return u""
    else:
        return u'USK'+unicode(kandidat)

freigabeordnung = {u'BPjM' : -1, u'StGB' : -1, u'USK0' : 0, u'USK6' : 1, u'USK12' : 2, u'USK16' : 3, u'USK18' : 4, u'' : 100, u'.' : 100}

d_unbekannt = {}

strikeout=[" (Steam)"," (GOG)"," (Early Access)"]
# Dieses Dictionary ordnet Spieltitel eine Releasejahr und eine USK-Friegabe zu
# Zuordnung von Genres wäre möglich.
with io.open(ogdbgames, encoding='utf8') as ogdb_file:
    ogdb_reader = unicodecsv.reader(ogdb_file,delimiter=";")
    ogdb_list=[]
    lastentry=""
    for ogdb_entry in ogdb_reader:
        for so in strikeout:
            ogdb_entry[0] = ogdb_entry[0].replace(so, "" )
        if ogdb_entry[0].lower() == lastentry:
            if ogdb_entry[9] != u'' and ogdb_list[-1][1] == u'':
                ogdb_list[-1][1] = ogdb_entry[9]
            if freigabe(ogdb_entry[3]) != u'':
                if ogdb_list[-1][2] == u'':
                    ogdb_list[-1][2]=freigabe(ogdb_entry[3])
                elif freigabeordnung[freigabe(ogdb_entry[3])] < freigabeordnung[ogdb_list[-1][2]]:
                    ogdb_list[-1][2]=freigabe(ogdb_entry[3])
            if ogdb_entry[9] != "" and ogdb_list[-1][1] == "":
                ogdb_list[-1][1] = ogdb_entry[9]
        else:
            ogdb_list.append([ogdb_entry[0].lower(),ogdb_entry[9],freigabe(ogdb_entry[3]),ogdb_entry[0]])
            lastentry=ogdb_entry[0].lower()
    ogdblookup={ogdb_entry[0]:(ogdb_entry[1] if ogdb_entry[1] != "" else "0",ogdb_entry[2],ogdb_entry[3]) for ogdb_entry in ogdb_list}

# Dieses Dictionary ordnet Spieltitel eine Releasejahr und eine USK-Friegabe zu
with io.open(moregames, encoding='utf8') as extra_file:
    extra_reader = unicodecsv.reader(extra_file,delimiter="\t")
    vdvclookup={extra_entry[0].lower():(extra_entry[1],extra_entry[2],extra_entry[0]) for extra_entry in extra_reader}

# Dieses Dictionary ordnet genannten Spieltiteln die bekannte Schreibweise zu
with io.open(duplikatsliste, encoding='utf8') as nl_file:
    nl_reader = unicodecsv.reader(nl_file,delimiter="\t")
    namelookup={nl_entry[1].lower():nl_entry[0] for nl_entry in nl_reader}

# Dieses Set enthält alle erfassten Schreibweisen
with io.open(duplikatsliste, encoding='utf8') as nl_file:
    nl_reader = unicodecsv.reader(nl_file,delimiter="\t")
    knowngames ={nl_entry[0].lower() for nl_entry in nl_reader}

# Dieses Dictionary ordnet Spielen einen speziellen ODGB-Eintrag zu
with io.open(zuordnungsliste, encoding='utf8') as ol_file:
    ol_reader = unicodecsv.reader(ol_file,delimiter="\t")
    ogdbtitles={ol_entry[0].lower():ol_entry[1].lower() for ol_entry in ol_reader}

def find_gameinfo(title): # search data of the game
    lowtitle = title.lower()
    year = u""
    freigabe = u""
    
    if lowtitle in namelookup:
        lowtitle = namelookup[lowtitle].lower()
    if lowtitle in ogdbtitles:
       ogdbtitle = ogdbtitles[lowtitle].lower()
    else:
       ogdbtitle = lowtitle

    if ogdbtitle in ogdblookup:
        year = ogdblookup[ogdbtitle][0].encode('utf-8')
        freigabe = ogdblookup[ogdbtitle][1]
        if lowtitle not in knowngames:
            if lowtitle == ogdbtitle:
                title = ogdblookup[ogdbtitle][2]
            else:
                title = lowtitle
    elif lowtitle in vdvclookup:
        year = vdvclookup[lowtitle][0].encode('utf-8')
        freigabe = vdvclookup[lowtitle][1].encode('utf-8')
        if lowtitle not in knowngames:
            title = vdvclookup[lowtitle][2]
    else:
        if len(lowtitle) > 0 and lowtitle not in knowngames:
            if title in d_unbekannt:
            	d_unbekannt[title] = d_unbekannt[title] + 1
            else:
            	d_unbekannt[title] = 1

    # make a return value out of the result
    return [title,year,freigabe]

results.write(u'"id";"token";"submitdate";"startlanguage";"startdate";"datestamp";"ipaddr";"refurl";"Geburtsjahr";"Geschlecht";"WohnortDeutschland";"Breitbandzugang";"COAXSpeed";"DSLSpeed";"FunkSpeed";"Videospieler";"ExSpieler";"ExWann";"Ablehnung_1";"Ablehnung_2";"Ablehnung_3";"Ablehnung_4";"Ablehnung_5";"VersteckJN";"VersteckArt_1";"VersteckArt_2";"VersteckArt_3";"VersteckArt_4";"Multiplayer";"Erfahrung";"Plattform_PCMac";"Plattform_PCWin";"Plattform_PCLnx";"Plattform_Plystn";"Plattform_Wii";"Plattform_XBox";"Plattform_DS";"Plattform_Android";"Plattform_iPhone";"Plattform_WinPhone";"Spiel1";"Release1";"Freigabe1";"Spiel2";"Release2";"Freigabe2";"Spiel3";"Release3";"Freigabe3";"Spiel4";"Release4";"Freigabe4";"Spiel5";"Release5";"Freigabe5";"Nutzungsdauer_SQ1";"Nutzungsdauer_SQ2";"Nutzungsdauer_SQ3";"Nutzungsdauer_SQ4";"Nutzungsdauer_SQ5";"Nutzungsumfang4";"Bezugsweg_SQ1";"Bezugsweg_SQ2";"Bezugsweg_SQ3";"Bezugsweg_SQ4";"Bezugsweg_SQ5";"Plattformen_SQ1";"Plattformen_SQ2";"Plattformen_SQ3";"Plattformen_SQ4";"Plattformen_SQ5";"AusgabenHardware";"AusgabenSpieleKauf";"AusgabenSpieleAbos";"AusgabenAddonsDLCs";"AusgabenGameserver";"Endmotivation_1";"Endmotivation_2";"Endmotivation_3";"Endmotivation_4";"Endmotivation_5";"Endmotivation_7";"Endmotivation_9";"Endzwang_SQ001";"Endzwang_SQ002";"Endverstndnis_1";"Endverstndnis_2";"Endverstndnis_3";"Endverstndnis_4";"Endverstndnis_5";"Endverstndnis_7";"Endverstndnis_9";"Startmotivation_1";"Startmotivation_2";"Startmotivation_3";"Startmotivation_4";"Startmotivation_5";"Illegalmotivation_1#0";"Illegalmotivation_1#1";"Illegalmotivation_2#0";"Illegalmotivation_2#1";"Illegalmotivation_3#0";"Illegalmotivation_3#1";"Illegalmotivation_4#0";"Illegalmotivation_4#1";"Illegalmotivation_5#0";"Illegalmotivation_5#1";"Illegalmotivation_6#0";"Illegalmotivation_6#1";"Illegalmotivation_7#0";"Illegalmotivation_7#1";"Illegalmotivation_8#0";"Illegalmotivation_8#1";"IllegalVerstaendnis_1";"IllegalVerstaendnis_2";"IllegalVerstaendnis_3";"IllegalVerstaendnis_4";"IllegalVerstaendnis_5";"IllegalVerstaendnis_6";"IllegalVerstaendnis_7";"IllegalVerstaendnis_8";"Kennzeichenkenntnis_SQ001";"Kennzeichenkenntnis_SQ002";"Kennzeichenkenntnis_SQ003";"Kennzeichenkenntnis_SQ004";"Kennzeichenkenntnis_SQ005";"Schnittkenntnis";"Zensurmeinung";"Zensurinformation";"Zensurinfowege_1";"Zensurinfowege_2";"Zensurinfowege_3";"Zensurinfowege_4";"Zensurinfowege_5";"Zensurinfowege_6";"UncutBezug";"UncutBezugErfolg";"UncutBezugWegKErf_SQ001";"UncutBezugWegKErf_SQ002";"UncutBezugWegKErf_SQ003";"UncutBezugWegKErf_SQ004";"UncutBezugWegKErf_SQ005";"UncutBezugWegKErf_SQ006";"UncutBezugWegKErf_SQ007";"UncutBezugWegKErf_SQ008";"UncutBezugWegKErf_SQ009";"UncutBezugWegKErf_SQ010";"UncutBezugWegErf_SQ001#0";"UncutBezugWegErf_SQ001#1";"UncutBezugWegErf_SQ002#0";"UncutBezugWegErf_SQ002#1";"UncutBezugWegErf_SQ003#0";"UncutBezugWegErf_SQ003#1";"UncutBezugWegErf_SQ004#0";"UncutBezugWegErf_SQ004#1";"UncutBezugWegErf_SQ005#0";"UncutBezugWegErf_SQ005#1";"UncutBezugWegErf_SQ006#0";"UncutBezugWegErf_SQ006#1";"UncutBezugWegErf_SQ007#0";"UncutBezugWegErf_SQ007#1";"UncutBezugWegErf_SQ008#0";"UncutBezugWegErf_SQ008#1";"UncutBezugWegErf_SQ009#0";"UncutBezugWegErf_SQ009#1";"UncutBezugWegErf_SQ010#0";"UncutBezugWegErf_SQ010#1";"Onlineaktivierung";"Onlinezwang";"Kontingent";"Kopierschutz";"Sicherheitskopie";"Datenschutz";"Geolock";"Informationsinteress_1#0";"Informationsinteress_1#1";"Informationsinteress_2#0";"Informationsinteress_2#1";"Informationsinteress_3#0";"Informationsinteress_3#1";"Informationsinteress_4#0";"Informationsinteress_4#1";"Informationsinteress_5#0";"Informationsinteress_5#1";"SexSelbstbew_SQ001#0";"SexSelbstbew_SQ001#1";"SexSelbstbew_SQ002#0";"SexSelbstbew_SQ002#1";"SexSelbstbew_SQ003#0";"SexSelbstbew_SQ003#1";"SexSelbstbew_SQ004#0";"SexSelbstbew_SQ004#1";"SexSelbstbew_SQ005#0";"SexSelbstbew_SQ005#1";"SexSelbstbew_SQ006#0";"SexSelbstbew_SQ006#1";"SexWehrlos_SQ001#0";"SexWehrlos_SQ001#1";"SexWehrlos_SQ002#0";"SexWehrlos_SQ002#1";"SexWehrlos_SQ003#0";"SexWehrlos_SQ003#1";"SexWehrlos_SQ004#0";"SexWehrlos_SQ004#1";"SexWehrlos_SQ005#0";"SexWehrlos_SQ005#1";"SexWehrlos_SQ006#0";"SexWehrlos_SQ006#1";"SexKoerper_SQ001#0";"SexKoerper_SQ001#1";"SexKoerper_SQ002#0";"SexKoerper_SQ002#1";"SexKoerper_SQ003#0";"SexKoerper_SQ003#1";"SexKoerper_SQ004#0";"SexKoerper_SQ004#1";"SexKoerper_SQ005#0";"SexKoerper_SQ005#1";"SexKoerper_SQ006#0";"SexKoerper_SQ006#1";"SexKoerper_SQ007#0";"SexKoerper_SQ007#1";"SexKoerper_SQ008#0";"SexKoerper_SQ008#1";"SexProblem";"SexMehr_Korper#0";"SexMehr_Korper#1";"SexMehr_Selbstbew#0";"SexMehr_Selbstbew#1";"SexMehr_Stereotype#0";"SexMehr_Stereotype#1"')

gameshist=[0,0,0,0,0,0]
#for pspp_entry in pspp_data:
with io.open(rohdaten, encoding='utf8') as f:
	reader = unicodecsv.reader(f,delimiter=';')
	for spss_entry in reader:
		ngames=0
		if len(spss_entry) == 223 or len(spss_entry) == 224:
			game = spss_entry[41:46]
		else:
			print("Error in Entry:")
			print(spss_entry)

		# write data before items to insert
		for item in spss_entry[:28]:
			results.write(u'"'+item+u'";')
		if (len(spss_entry[28]) > 0):
			versteck.write(spss_entry[28]+u'\n\n')
		for item in spss_entry[29:41]:
			results.write(u'"'+item+u'";')
		for g in range(0,5): # 5 games (hardcoded)
			if (len(game[g]) > 1):
				ngames=ngames+1
			gameinfo = find_gameinfo(game[g])
			results.write(u'"'+gameinfo[0]+u' ('+gameinfo[1]+u')";')
			for i in range(1,3):
				results.write(u'\"'+gameinfo[i]+u'\";')
		for item in spss_entry[46:126]:
			results.write(u'"'+item+u'";')
		if(len(spss_entry[126]) > 0):
			zensurinfo.write(spss_entry[126]+u'\n\n')
		for item in spss_entry[127:222]:
			results.write(u'"'+item+u'";')
		results.write(u'"'+spss_entry[222]+u'"\n')
		if (len(spss_entry) > 223):
			if (len(spss_entry[223]) > 0):
				feedback.write(spss_entry[223]+u'\n\n')
		gameshist[ngames] = gameshist[ngames]+1

nennungen.write(u'"Genannte Titel"\t"Häufigkeit"\n')
for nr in range(0,6):
	nennungen.write(unicode(nr)+u'\t'+unicode(gameshist[nr])+u'\n')
	
f_unbekannt.write(u'"Unbekannter Titel"\t"Nennungen"\n')
for item in sorted(d_unbekannt.items(),key=lambda x: x[1], reverse=True):
	f_unbekannt.write(u'"'+unicode(item[0])+u'"\t'+unicode(item[1])+u'\n')

