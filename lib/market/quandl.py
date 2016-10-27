import config.GlobalConfig
import quandl

config = config.GlobalConfig.Config()

class Api(object):
    def __init__(self):
        quandl.ApiConfig.api_key = 'T4u_qrsCC8RAEWAHKmi8'
        return

    def getSingleNameHistoricalEod(self,ticker):
        pathString = config.ticker2QuandlPathMap[ticker]
        pd = quandl.get(pathString)
        pd["Ticker"] = ticker
        #print(pd)
        return pd

    def downloadDatabase(self,dbName,fileLocation):
        print("Downloading Quandl %s database to:%s" % (dbName,fileLocation))
        quandl.Database(dbName).bulk_download_to_file(fileLocation)
        print("Download complete.")

    def readDatabaseFromCSV(self,dbName,fileLocation):
        print("Reading Quandl %s database from:%s" % (dbName,fileLocation))

        print("Load complete.")

    def getSingleQuandlTsByKey(self, pathString):
        pd = quandl.get(pathString)
        pd["QuandlPathString"] = pathString
        # print(pd)
        return pd

    def getMultipleQuandlTsByKey(self, pathStringlist):
        print(pathStringlist)
        pd = quandl.get(pathStringlist)
        #pd["QuandlPathString"] = pathString
        # print(pd)
        return pd



