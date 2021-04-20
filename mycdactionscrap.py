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
