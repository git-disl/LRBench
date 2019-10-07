# DeepLR Database Module

class DBDriver(object):
    def __init__(self, _dbName, _dbUser, _dbAddr, _dbPasswd):
        self.__dbName__ = _dbName
        self.__dbUser__ = _dbUser
        self.__dbAddr__ = _dbAddr
        self.__dbPasswd__ = _dbPasswd
        self.__dbStatus__ = 'init'
        self.__dbCursor__ = None

    def connect(self):
        raise NotImplementedError

    def getCursor(self):
        raise NotImplementedError

    def execute(self, _sqlStateMent):
        raise NotImplementedError
    
    # LRBench APIs    
    def insertLR(self, dataset, network, lrPolicy):
        raise NotImplementedError
        
    def queryLRs(self, dataset, network, lrPolicy):
        raise NotImplementedError
