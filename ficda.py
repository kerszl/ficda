from bs4 import BeautifulSoup as bs
#import urllib
from urllib.request import urlopen
import re
import json


MAIN_LINK = 'https://www.cdaction.pl/magazyn/'
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
    'CHAPTER_GAME2':'W PRODUKCJI',
    'CHAPTER_GAME3':'RECENZJE',
    'CHAPTER_GAME4':'KASZANKA ZONE'
    }

    H2_TAG="h2"
    DIV_TAG="div"
    CLASS_TAG1={"class":"blok_info"}
    CLASS_TAG2={"class":"tytul"}
    

    site =''
    page =''    
    section_title=[]
    nr = ''


    def __init__ (self, link):
        self.site=link
        body = urlopen(self.site) 
        soup = bs(body,'html.parser')
        self.page = soup.find_all(self.DIV_TAG,self.CLASS_TAG1)
        self.scrap_nr()
    
    def scrap_nr (self):
        self.nr = re.search('(https://)(www.cdaction.pl/)(magazyn/)(numer-[0-9]*)(-.*)(.html)',self.site)[4]
        


    def scrap (self):        
        for chapter_names in self.CHAPTERS.values():
            for i in self.page:
                a=i.find(self.H2_TAG).text
                if (a==chapter_names):
                    b=i.find_all(self.DIV_TAG,self.CLASS_TAG2)
                    for j in b:
                        self.section_title.append({self.nr:{chapter_names:j.text}})

        return self.section_title
    
    def json_dumping (self):
        #sprawdzic czy bylo zgrane do pamieci        
        file = self.nr + '.json'
        try:
            with open(file, 'w') as f:
                json.dump(self.section_title,f)
        except ValueError as e:                
            print ("Problem z plikiem "+file+" lub formatem json")
            print (e)        
            exit()



#a=MyScrap(CALY_LINK)
a=MyScrap(MAIN_LINK_241NR)

a.scrap()
a.json_dumping()

exit ()
print (b)
a="numer-141"
b=a+'.json'

print (b)


#a='https://www.cdaction.pl/magazyn/numer-1-30.html'


#print (re.search('(https://)(www.cdaction.pl/)(magazyn/)(numer-[0-9]?)(-.*)(.html)',a)[4])
#numer-131-1.html

#section_title=[{"nr":{"chap1":"nr"}},{"nr":{"chap1":"nr"}}]


#print (section_title)
#json.dump()        




