#!/usr/bin/python3
__version__ = "0.2"

#from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen


from time import sleep
from random import randint
import argparse
import re
#import sqlite3
#from pathlib import Path


BASE_NAME = "cdaction.db" #name of cd action base with games

from mycdactionscrap import MyCdActionScrap
from mysqlite3 import MySqlite3

LAST_NUMBER = 0
HIGHEST_SAVED_NUMBER = 0

#---UPDATE---
def update ():
#1.---zgrywamy numery ze strony cdaction do formatu json w katalogu numery (numer-x.json)
    scrap = MyCdActionScrap()
    LAST_NUMBER=scrap.last_number+1
    HIGHEST_SAVED_NUMBER=scrap.highest_saved_number+1
    if (HIGHEST_SAVED_NUMBER!=LAST_NUMBER):
        for i in range(HIGHEST_SAVED_NUMBER,LAST_NUMBER):
            scrap.scrap_nr(i)
            scrap.json_dumping()
            sleep (randint(1,2))
    else:
        print ("Wydania w katalugu numery są aktualne")

#2.--- Zczytujemy pliki json i wrzucamy wszystko do bazy sqlite

    #baza = MySqlite3 (BASE_NAME,truncate=True) #uwaga, tworzy baze od zera!!!
    baza = MySqlite3 (BASE_NAME)
    for i in range(HIGHEST_SAVED_NUMBER,LAST_NUMBER):
        json_iter="numery/numer-"+str(i)+".json"
        baza.update_db(json_iter)
    baza.close_db()


def przeszukaj_baze (tytul):
#-Dziwolągi typu "luty 2003" zamienia na "02/2003"
    miesiace={
              "styczeń":"01",
              "luty":"02",
              "marzec":"01",
              "kwiecień":"01",
              "maj":"01",
              "czerwiec":"01",
              "lipiec":"01",
              "sierpień":"08",
              "wrzesień":"09",
              "październik":"10",
              "listopad":"11",
              "grudzień":"12"
    }

    def przerob_nazwe_miesiaca(do_zamiany):
        if re.search("^[a-z].*",do_zamiany):
            tekst_przerob = do_zamiany.split()
            try:
                ret_string=miesiace[tekst_przerob[0]]+"/"+tekst_przerob[1]            
            except:
                ret_string="Error"
            return ret_string
        else:
            return do_zamiany
        
    baza = MySqlite3 (BASE_NAME)
    znaleziony_tytul=baza.search_title(tytul) 

    print("{:<3}{:<5}{:<9}{:<17}{}".format("ID","NR","DATA","SEKCJA","NAZWA"))

    for j,i in enumerate(znaleziony_tytul,1):
        print("{:<3}{:<5}{:<9}{:<17}{}".format(str(j),i[1],przerob_nazwe_miesiaca(i[2]),i[3],i[4]))

    baza.close_db()


parser = argparse.ArgumentParser(description="""Ficda to program, który zgrywa nazwy gier do bazy, 
które zostały opisane w numerach cdaction. Dane są zgrywane ze strony cdaction.pl.
""", formatter_class=argparse.RawTextHelpFormatter,add_help=False
                                 )
parser._optionals.title = 'Argumenty opcjonalne'

parser.add_argument('-u', '--update', help='aktualizuje gry ze strony i wrzuca do bazy',action='store_true' )
parser.add_argument('-s', '--search', metavar='[nazwa gry]', help='wyszukuje gre z bazy' )
parser.add_argument('-h', '--help', help='pokazuje help',action='help', default=argparse.SUPPRESS )                    

parser.add_argument('-v', '--version', action='version', help='pokazuje wersje programu i wychodzi',
                    version='%(prog)s '+__version__
                    )

args = parser.parse_args()

if args.update:
    update()
    exit()

if args.search:    
    przeszukaj_baze(args.search)
    exit()












