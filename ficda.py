from bs4 import BeautifulSoup as bs
#import urllib
from urllib.request import urlopen
import re


MAIN_LINK = 'https://www.cdaction.pl/magazyn/'
MAIN_LINK_1NR = 'https://www.cdaction.pl/magazyn/numer-2-30.html'
#przykładowy numer
#https://www.cdaction.pl/magazyn/numer-4-30.html
#CALY_LINK='https://www.cdaction.pl/magazyn/numer-4-30.html'
CALY_LINK = 'file:///mnt/d/moje programy i inne/GNU/ficda/przykladowa_strona.html'


body=urlopen(CALY_LINK) 
soup = bs(body,'html.parser')
strona=soup.find_all("div",{"class":"blok_info"})

#print (type(strona))

#div class="blok_info"
for i in strona:
    a=i.find("h2").text
    if (a=="RECENZJE"):
        b=i.find_all("div",{"class":"tytul"})
        for j in b:
            print (j.text)


    #main_panel=main_panel.find("div",{"class":"col-md-9 single-panel-wrapper"})
    #main_panel=main_panel.find_all("div",{"class":"mix-title"})    


#class Craw:

