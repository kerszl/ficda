from bs4 import BeautifulSoup as bs
#import urllib
from urllib.request import urlopen
import re
import json
from time import sleep
from random import randint

#MAIN_LINK = 'https://www.cdaction.pl/magazyn/'
MAIN_LINK_1NR = 'https://www.cdaction.pl/magazyn/numer-2-30.html'
MAIN_LINK_241NR = 'https://www.cdaction.pl/magazyn/numer-241-1.html'
#https://www.cdaction.pl/magazyn/numer-241-1.html
#przykładowy numer
#https://www.cdaction.pl/magazyn/numer-4-30.html
#CALY_LINK='https://www.cdaction.pl/magazyn/numer-4-14.html'
CALY_LINK = 'file:///mnt/d/moje programy i inne/GNU/ficda/przykladowa_strona.html'




class MyScrap:
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

    MAIN_LINK = 'https://www.cdaction.pl/magazyn/'

    site =''
    page =''    
    section_title=[]
    nr = ''
    scraped = False


    def __init__ (self, curr_nr:int, biggest_nr=244):
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
                        self.section_title.append({self.nr:{chapter_names:j.text}})

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



#a=MyScrap(CALY_LINK)


#---zgrywamy numery do formatu json

for i in range(244,245):
    a=MyScrap(i)
    a.scrap()
    a.json_dumping()    
    sleep (randint(1,2))




