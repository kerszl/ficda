#!/usr/bin/python3

#from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen


from time import sleep
from random import randint
#import sqlite3
#from pathlib import Path

#LAST_NUMBER = 244 #last nr of cd action
BASE_NAME = "cdaction.db" #name of cd action base with games

from mycdactionscrap import MyCdActionScrap
from mycdactionscrap import LAST_NUMBER
from mysqlite3 import MySqlite3



#1.---zgrywamy numery ze strony cdaction do formatu json w katalogu numery (numer-x.json)
# for i in range(1,LAST_NUMBER+1):
#     a=MyCdActionScrap(i)
#     a.scrap()
#     a.json_dumping()    
#     sleep (randint(1,2))
#

#2.--- Zczytujemy pliki json i wrzucamy wszystko do bazy sqlite

baza = MySqlite3 (BASE_NAME,truncate=True)
#baza = MySqlite3 (BASE_NAME)
for i in range(1,LAST_NUMBER):
    json_iter="numery/numer-"+str(i)+".json"
    baza.update_db(json_iter)
baza.close_db()

#-----------
#zrobic ladne wyswietlanie i z linii polece

#baza = MySqlite3 (BASE_NAME)
#result=baza.search_title("Assassin's creed valhalla")
#result=baza.search_title("Shadow of tomb raider")
#result=baza.search_title("shadow of the tomb raider")

#for i,j in enumerate(result):
#    print (str(i+1)+" "+str(j[1])+" "+str(j[2])+" "+str(j[3])+" "+str(j[4]))

#baza.close_db()











