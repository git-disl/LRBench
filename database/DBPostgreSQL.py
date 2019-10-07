import psycopg2
from DBDriver import DBDriver


class DBPostgreSQL(DBDriver):
    def __init__(self, _dbName, _dbUser, _dbAddr, _dbPasswd):
        super(DBPostgreSQL, self).__init__(_dbName, _dbUser, _dbAddr, _dbPasswd)
        self.__connectStr__ = r"dbname="+r"'"+self.__dbName__+r"' " + r"user="+r"'"+self.__dbUser__+r"' " \
                            + r"host=" + r"'"+self.__dbAddr__+r"' " + r"password="+r"'"+self.__dbPasswd__+"'"

    def connect(self):
        try:
            self.__conn__ = psycopg2.connect(self.__connectStr__)
            self.__dbStatus__ = "connected"
        except Exception as e:
            print(e)
    def getCursor(self): # Shared Cursor for the Database
        if self.__dbCursor__ != None:
            return self.__dbCursor__
        if self.__dbStatus__ == "connected":
            try:
                self.__dbCursor__ = self.__conn__.cursor()
            except Exception as e:
                print(e)
        else:
            try:
                self.connect()
                self.__dbCursor__ = self.__conn__.cursor()
            except Exception as e:
                print(e)
        return self.__dbCursor__

    def execute(self, _sqlStateMent):
        try:
            tmpCursor = self.getCursor()
            tmpCursor.execute(_sqlStateMent)
            return tmpCursor
        except Exception as e:
            print(e)
            
    #LRBench APIs
    def insertLR(self, dataset, network, lrPolicy):
        raise NotImplementedError
        tmpCursor = self.execute("SELECT EXISTS(SELECT * FROM " + lrPolicy + ")")
        if not tmpCursor.fetchone()[0]:
            tmpCursor.execute("CREATE TABLE")
        tmpCursor.execute("INSERT)
                          
    def queryLRs(self, dataset, network, lrPolicy):
        raise NotImplementedError


# Module Test
if __name__ == "__main__":
    db = DBPostgreSQL('lrbench', 'yanzhaowu', 'localhost', '123456')
    print(db.execute("""CREATE TABLE MODULETEST (name char(40));"""))
    print(db.execute("""SELECT * FROM MODULETEST""").fetchall())
    print(db.execute("""INSERT INTO MODULETEST (name) VALUES ('lrbench')"""))
    print(db.execute("""SELECT * FROM MODULETEST""").fetchall())
    print(db.execute("""DROP TABLE MODULETEST"""))
