from pathlib import Path


class MySqlite3:
    conn = 0
    cursor = 0
    db_filename =''
    row = []

    def __init__(self, db_filename_):         
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
                    
    def update_db (self, json_file):
        
        self.__json_load(json_file)
        for i in self.row:
            nr_date_=list(i)[0]    
            nr_date=re.search("(\d*) (.*)",nr_date_).groups() #->tablica
            section = list(dict(i[nr_date_]).keys())[0]
            title = list(dict(i[nr_date_]).values())[0]
            
        self.cursor.execute("INSERT OR IGNORE INTO magazines (id,date,section,title,types_of_game, page_numbers, score, url, reviewer) VALUES(?,?,?,?,?,?,?,?,?)",\
                            (nr_date[0],nr_date[1],section,title,"NULL","NULL","NULL","NULL","NULL"))
        self.conn.commit()                        
    
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
