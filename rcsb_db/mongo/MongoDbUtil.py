##
# File:  MongoDbUtil.py
# Date:  12-Mar-2018 J. Westbrook
#
# Update:
#      17-Mar-2018. jdw add replace and index ops
##
"""
Base class for simple essential database operations for MongoDb.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
logger = logging.getLogger(__name__)
#
#


class MongoDbUtil(object):

    def __init__(self, mongoClientObj, verbose=False):
        self.__verbose = verbose
        self.__mgObj = mongoClientObj

    def databaseExists(self, databaseName):
        try:
            dbNameList = self.__mgObj.list_database_names()
            if databaseName in dbNameList:
                return True
            else:
                return False
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def getDatabaseNames(self):
        return self.__mgObj.list_database_names()

    def createDatabase(self, databaseName, overWrite=True):
        try:
            if overWrite and self.databaseExists(databaseName):
                logger.debug("Dropping existing database %s" % databaseName)
                self.__mgObj.drop_database(databaseName)
            db = self.__mgObj[databaseName]
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))

        return False

    def dropDatabase(self, databaseName):
        try:
            self.__mgObj.drop_database(databaseName)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def collectionExists(self, databaseName, collectionName):
        try:
            if self.databaseExists(databaseName) and (collectionName in self.__mgObj[databaseName].collection_names()):
                return True
            else:
                return False
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def getCollectionNames(self, databaseName):
        return self.__mgObj[databaseName].collection_names()

    def createCollection(self, databaseName, collectionName, overWrite=True):
        try:
            if overWrite and self.collectionExists(databaseName, collectionName):
                self.__mgObj[databaseName].drop_collection(collectionName)
            #
            ok = self.__mgObj[databaseName].create_collection(collectionName)
            logger.debug("Return from create collection %r " % ok)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def dropCollection(self, databaseName, collectionName):
        try:
            ok = self.__mgObj[databaseName].drop_collection(collectionName)
            logger.debug("Return from drop collection %r " % ok)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def insert(self, databaseName, collectionName, dObj):
        try:
            c = self.__mgObj[databaseName].get_collection(collectionName)
            r = c.insert_one(dObj)
            try:
                rId = r.inserted_id
                return rId
            except Exception as e:
                logger.debug("Failing with %s" % str(e))
                return None
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return None

    def insertList(self, databaseName, collectionName, dList):
        rIdL = []
        try:
            c = self.__mgObj[databaseName].get_collection(collectionName)
            r = c.insert_many(dList)
            try:
                rIdL = r.inserted_ids
                return rIdL
            except Exception as e:
                logger.debug("Insert ID recovery failing with %s" % str(e))
                return rIdL
        except Exception as e:
            logger.exception("Insert operation failing with %s" % str(e))
        return rIdL

    def fetchOne(self, databaseName, collectionName, ky, val):
        try:
            c = self.__mgObj[databaseName].get_collection(collectionName)
            dObj = c.find_one({ky: val})
            return dObj
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return None

    def replace(self, databaseName, collectionName, dObj, selectD, upsertFlag=True):
        try:
            c = self.__mgObj[databaseName].get_collection(collectionName)
            r = c.replace_one(selectD, dObj, upsert=upsertFlag)
            logger.debug("Replace returns  %r" % r)
            try:
                rId = r.upserted_id
                numMatched = r.matched_count
                numModified = r.modified_count
                logger.debug("Replacement mathed %d modified %d with _id %s" % (numMatched, numModified, rId))
                return rId
            except Exception as e:
                logger.exception("Failing %s and %s selectD %r with %s" % (databaseName, collectionName, selectD, str(e)))
                return None
        except Exception as e:
            logger.exception("Failing %s and %s selectD %r with %s" % (databaseName, collectionName, selectD, str(e)))
        return None

    def replaceList(self, databaseName, collectionName, dList, keyName, upsertFlag=True):
        try:
            rIdL = []
            c = self.__mgObj[databaseName].get_collection(collectionName)
            for d in dList:
                selectD = {keyName: d[keyName]}
                r = c.replace_one(selectD, d, upsert=upsertFlag)
                try:
                    rIdL.append(r.upserted_id)
                except Exception as e:
                    logger.error("Failing %s and %s selectD %r with %s" % (databaseName, collectionName, keyName, str(e)))
        except Exception as e:
            logger.exception("Failing %s and %s selectD %r with %s" % (databaseName, collectionName, keyName, str(e)))
        #
        return rIdL

    def createIndex(self, databaseName, collectionName, keyList, indexName="primary", indexType="DESCENDING", uniqueFlag=False):
        try:
            iTupL = [(ky, indexType) for ky in keyList]
            c = self.__mgObj[databaseName].get_collection(collectionName)
            c.create_index(iTupL, name=indexName, background=True, unique=uniqueFlag)
            return True
        except Exception as e:
            logger.exception("Failing %s and %s keyList %r with %s" % (databaseName, collectionName, keyList, str(e)))
        return False

    def dropIndex(self, databaseName, collectionName, indexName="primary"):
        try:
            c = self.__mgObj[databaseName].get_collection(collectionName)
            c.drop_index(indexName)
            return True
        except Exception as e:
            logger.exception("Failing %s and %s with %s" % (databaseName, collectionName, str(e)))
        return False

    def reIndex(self, databaseName, collectionName):
        try:
            c = self.__mgObj[databaseName].get_collection(collectionName)
            c.reindex()
            return True
        except Exception as e:
            logger.exception("Failing %s and %s with %s" % (databaseName, collectionName, str(e)))
        return False
