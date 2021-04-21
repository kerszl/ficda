#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import json
from time import sleep
from random import randint
import sqlite3
from pathlib import Path

LAST_NUMBER = 244 #last nr of cd action
BASE_NAME = "cdaction.db" #name of cd action base with games

#MAIN_LINK = 'https://www.cdaction.pl/magazyn/'
#MAIN_LINK_1NR = 'https://www.cdaction.pl/magazyn/numer-2-30.html'
#MAIN_LINK_241NR = 'https://www.cdaction.pl/magazyn/numer-241-1.html'
#https://www.cdaction.pl/magazyn/numer-241-1.html
#przykładowy numer
#https://www.cdaction.pl/magazyn/numer-4-30.html
#CALY_LINK='https://www.cdaction.pl/magazyn/numer-4-14.html'
#CALY_LINK = 'file:///mnt/d/moje programy i inne/GNU/ficda/przykladowa_strona.html'



class MyCdActionScrap:
    CHAPTERS = {
    'CHAPTER_GAME1':'ZA PIĘĆ DWUNASTA',
    'CHAPTER_GAME2':'ZA 5 12',
    'CHAPTER_GAME3':'W PRODUKCJI',
    'CHAPTER_GAME4':'RECENZJE',
    'CHAPTER_GAME5':'KASZANKA ZONE',
    'CHAPTER_GAME6':'KASZANKA',
    'CHAPTER_GAME7':'JUŻ GRALIŚMY',
    
    }

    H2_TAG="h2"
    DIV_TAG="div"
    CLASS_TAG1={"class":"blok_info"}
    CLASS_TAG2={"class":"tytul"}

    #CLASS_TAG3={"class":"okladka"}
    CLASS_TAG3={"class":"przegladarka"}

    MAIN_LINK = 'https://www.cdaction.pl/magazyn/'

    site =''
    page =''    
    section_title=[]
    nr = ''
    date =''
    scraped = False
    


    def __init__ (self, curr_nr:int, biggest_nr=LAST_NUMBER):
        if curr_nr>biggest_nr:
            print ("Za duzy numer - ",curr_nr)
            exit()
        section_title=[]
        nr_page=(biggest_nr/8)+1-(curr_nr/8)
        link=self.MAIN_LINK+'numer-'+str(curr_nr)+'-'+str(int(nr_page))+'.html'              
        self.site=link
        body = urlopen(self.site) 
        soup = bs(body,'html.parser')
        self.page = soup.find_all(self.DIV_TAG,self.CLASS_TAG1)
        try:
            self.date = soup.find(self.DIV_TAG,self.CLASS_TAG3).find("h1").text
        except:
            print ("Jakis blad")            
        self.scrap_nr()
    
    def scrap_nr (self):
        self.nr = re.search('(https://)(www.cdaction.pl/)(magazyn/)(numer-[0-9]*)(-.*)(.html)',self.site)[4]
            

    def scrap (self):        
        self.section_title=[]
        for chapter_names in self.CHAPTERS.values():
            for i in self.page:
                a=i.find(self.H2_TAG).text.strip()                                
                if (a==chapter_names):
                    b=i.find_all(self.DIV_TAG,self.CLASS_TAG2)
                    for j in b:
                        nr_and_date=self.nr.replace("numer-","") +" "+self.date                        
                        self.section_title.append({nr_and_date:{chapter_names:j.text}})

        self.scraped=True
        return self.section_title



    def json_dumping (self):
        if self.scraped:
            file = 'numery/'+self.nr + '.json'
            try:
                with open(file, 'w') as f:
                    json.dump(self.section_title,f)             
                status="ok"
                if len(self.section_title)==0:
                    status="pusty"
                print ("Zgralem: "+file+" "+status)   
            except ValueError as e:                
                print ("Problem z plikiem "+file+" lub formatem json")
                print (e)        
                exit()

class MySqlite3:
    conn = 0
    cursor = 0
    db_filename =''
    row = []

    def __init__(self, db_filename_,truncate=False):         
        my_file = Path(db_filename_)
        if not my_file.exists():
            print ("Nie ma pliku:",db_filename_)
            exit ()
        else:
            self.db_filename=db_filename_

        try:                
            self.conn = sqlite3.connect(self.db_filename)            
        except sqlite3.Error as e:
            print (e)
            exit ()
        
        try:                
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print (e)
            exit ()
        if truncate:
            self.__truncate_db()
                    
    def __truncate_db (self):
                self.cursor.execute("DELETE FROM magazines")
                self.cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='magazines'")                
                self.conn.commit()


    def update_db (self, json_file):        
        self.row = []
        self.__json_load(json_file)
        pure_numer=re.search("(numery/numer-)(\d*)(.json)",json_file).groups()[1]

        if len(self.row)>0:
            for i in self.row:
                nr_date_=list(i)[0]    
                nr_date=re.search("(\d*) (.*)",nr_date_).groups() #->tablica
                section = list(dict(i[nr_date_]).keys())[0]
                title = list(dict(i[nr_date_]).values())[0]
                self.cursor.execute("INSERT OR IGNORE INTO magazines (nr_magazine,date,section,title,types_of_game, page_numbers, score, url, reviewer, platform) VALUES(?,?,?,?,?,?,?,?,?,?)",\
                            (nr_date[0],nr_date[1],section,title,"NULL","NULL","NULL","NULL","NULL","NULL"))
                self.conn.commit()
        else:   
                nr_date = [0,0]                                                
                nr_date[0]=pure_numer                
                nr_date[1]= "NULL"
                section = "NULL"
                title = "NULL"
                self.cursor.execute("INSERT OR IGNORE INTO magazines (id,date,section,title,types_of_game, page_numbers, score, url, reviewer, platform) VALUES(?,?,?,?,?,?,?,?,?,?)",\
                            (nr_date[0],nr_date[1],section,title,"NULL","NULL","NULL","NULL","NULL","NULL"))
                self.conn.commit()                       
            
        print ("Cd action nr "+str(pure_numer)+" wrzucony do bazy") 
            

   
    def search_title(self,title):
        self.cursor.execute("SELECT * FROM magazines WHERE title LIKE "+"'%"+title+"%'")
        title_found = self.cursor.fetchall()
        return title_found

                
        #self.conn.commit()                       




    def __json_load (self, json_file):        
        try:
            with open(json_file, 'r') as f:
                self.row=json.load(f)
        except ValueError as e:
            print (e)
            exit ()
                                
    def close_db (self):        
        self.cursor.close()
        self.conn.close()                        


#---zgrywamy numery ze strony cdaction do formatu json
# for i in range(1,245):
#     a=MyCdActionScrap(i)
#     a.scrap()
#     a.json_dumping()    
#     sleep (randint(1,3))

#
#--- Zczytujemy pliki json i wrzucamy wszystko do bazy sqlite

####baza = MySqlite3 (BASE_NAME,truncate=True)
# baza = MySqlite3 (BASE_NAME)
# for i in range(1,LAST_NUMBER):
#     json_iter="numery/numer-"+str(i)+".json"
#     baza.update_db(json_iter)
# baza.close_db()

#-----------
#zrobic ladne wyswietlanie i z linii polece

baza = MySqlite3 (BASE_NAME)
result=baza.search_title("carrion")

for i,j in enumerate(result):
    print (str(i+1)+" "+str(j[1])+" "+str(j[2])+" "+str(j[3])+" "+str(j[4]))

baza.close_db()











