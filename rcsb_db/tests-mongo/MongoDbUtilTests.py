##
#
# File:    MongoDbUtilTests.py
# Author:  J. Westbrook
# Date:    12-Mar-2018
# Version: 0.001
#
# Updates:
##
"""
Test cases for simple MongoDb client opeations .

Adjust environment setup  -

        . set-test-env.sh


"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import os
import sys
import unittest
import time
import pprint
import dateutil.parser

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from rcsb_db import __version__
except Exception as e:
    sys.path.insert(0, TOPDIR)
    from rcsb_db import __version__

from rcsb_db.mongo.ConnectionBase import ConnectionBase
from rcsb_db.mongo.MongoDbUtil import MongoDbUtil


class MongoDbUtilTests(unittest.TestCase):

    def setUp(self):
        self.__dbName = 'test_database'
        self.__collectionName = 'test_collection'
        self.__lfh = sys.stderr
        self.__verbose = True
        self.__myC = None
        dbUserId = os.getenv("MONGO_DB_USER_NAME")
        dbUserPwd = os.getenv("MONGO_DB_PASSWORD")
        dbName = os.getenv("MONGO_DB_NAME")
        dbHost = os.getenv("MONGO_DB_HOST")
        dbPort = os.getenv("MONGO_DB_PORT")
        dbAdminDb = os.getenv("MONGO_DB_ADMIN_DB_NAME")
        ok = self.open(dbUserId=dbUserId, dbUserPwd=dbUserPwd, dbHost=dbHost, dbName=dbName, dbPort=dbPort, dbAdminDb=dbAdminDb)
        self.assertTrue(ok)
        self.__startTime = time.time()
        logger.debug("Running tests on version %s" % __version__)
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        self.close()
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def open(self, dbUserId=None, dbUserPwd=None, dbHost=None, dbName=None, dbPort=None, dbAdminDb=None):
        prefD = {"DB_HOST": dbHost, 'DB_USER': dbUserId, 'DB_PW': dbUserPwd, 'DB_NAME': dbName, "DB_PORT": dbPort, 'DB_ADMIN_DB_NAME': dbAdminDb}
        self.__myC = ConnectionBase()
        self.__myC.setPreferences(prefD)
        ok = self.__myC.openConnection()
        if ok:
            return True
        else:
            return False

    def close(self):
        if self.__myC is not None:
            self.__myC.closeConnection()
            self.__myC = None
            return True
        else:
            return False

    def getClientConnection(self):
        return self.__myC.getClientConnection()

    def __makeDataObj(self, nCats, Nattribs, Nrows):
        rD = {}
        for cat in range(nCats):
            catName = "category_%d" % cat
            rD[catName] = []
            for row in range(Nrows):
                d = {}
                for attrib in range(Nattribs):
                    val = "val_%d_%d" % (row, attrib)
                    attribName = "attrib_%d" % attrib
                    d[attribName] = val
                rD[catName].append(d)
            d = {}
            for attrib in range(Nattribs):
                val = "2018-01-30 12:01"
                attribName = "attrib_%d" % attrib
                d[attribName] = dateutil.parser.parse(val)
            rD[catName].append(d)

        return rD

    def testCreateDatabase(self):
        """Test case -  create database -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createDatabase(self.__dbName)
            self.assertTrue(ok)
            ok = mg.createDatabase(self.__dbName)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testCreateCollection(self):
        """Test case -  create collection -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            #
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testCreateDropDatabase(self):
        """Test case -  create/drop database -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createDatabase(self.__dbName)
            self.assertTrue(ok)
            ok = mg.dropDatabase(self.__dbName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertFalse(ok)
            #
            ok = mg.createDatabase(self.__dbName)
            self.assertTrue(ok)
            ok = mg.dropDatabase(self.__dbName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertFalse(ok)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testCreateCollectionDropDatabase(self):
        """Test case -  create/drop collection -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            #
            ok = mg.dropDatabase(self.__dbName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertFalse(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertFalse(ok)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testCreateDropCollection(self):
        """Test case -  create/drop collection -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            #
            logger.debug("Databases = %r" % mg.getDatabaseNames())
            logger.debug("Collections = %r" % mg.getCollectionNames(self.__dbName))
            ok = mg.dropCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            logger.debug("Databases = %r" % mg.getDatabaseNames())
            logger.debug("Collections = %r" % mg.getCollectionNames(self.__dbName))
            # Removing the last collection will remove the database (results appear differ between mac and linux - )
            ok = mg.databaseExists(self.__dbName)
            # self.assertFalse(ok)
            #
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertFalse(ok)
            logger.debug("Collections = %r" % mg.getCollectionNames(self.__dbName))
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testInsertSingle(self):
        """Test case -  create collection and insert data -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            #
            dObj = self.__makeDataObj(2, 5, 5)
            rId = mg.insert(self.__dbName, self.__collectionName, dObj)
            self.assertTrue(rId is not None)
            # Note that dObj is mutated by additional key '_id' that is added on insert -
            #
            rObj = mg.fetchOne(self.__dbName, self.__collectionName, '_id', rId)
            logger.debug("Return Object %s" % pprint.pformat(rObj))
            self.assertEqual(len(dObj), len(rObj))
            self.assertEqual(dObj, rObj)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testInsertList(self):
        """Test case -  create collection and insert data -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            #
            dList = []
            for ii in range(100):
                dList.append(self.__makeDataObj(2, 5, 5))
            #
            rIdL = mg.insertList(self.__dbName, self.__collectionName, dList)
            self.assertTrue(len(rIdL), len(dList))
            # Note that dObj is mutated by additional key '_id' that is added on insert -
            #
            for ii, rId in enumerate(rIdL):
                rObj = mg.fetchOne(self.__dbName, self.__collectionName, '_id', rId)
                logger.debug("Return Object %s" % pprint.pformat(rObj))
                self.assertEqual(len(dList[ii]), len(rObj))
                self.assertEqual(dList[ii], rObj)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReplaceSingle(self):
        """Test case -  create collection and insert document  and then replace document -

        Environment setup --

        . set-test-env.sh

        """
        try:
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            #
            dObj = self.__makeDataObj(2, 5, 5)
            dObj['THE_KEY'] = 'ONE'
            rId = mg.insert(self.__dbName, self.__collectionName, dObj)
            self.assertTrue(rId is not None)
            # Note that dObj is mutated by additional key '_id' that is added on insert -
            #
            rObj = mg.fetchOne(self.__dbName, self.__collectionName, '_id', rId)
            logger.debug("Return Object %s" % pprint.pformat(rObj))
            self.assertEqual(len(dObj), len(rObj))
            self.assertEqual(dObj, rObj)
            #
            # Now replace with a new document
            dObj = self.__makeDataObj(3, 2, 2)
            dObj['THE_KEY'] = 'ONE'
            logger.debug("Replace Object %s" % pprint.pformat(dObj))
            rId = mg.replace(self.__dbName, self.__collectionName, dObj, {'THE_KEY': 'ONE'}, upsertFlag=True)
            # self.assertTrue(rId is not None)
            rObj = mg.fetchOne(self.__dbName, self.__collectionName, 'THE_KEY', 'ONE')
            rObj.pop('_id', None)
            dObj.pop('_id', None)
            logger.debug("Return Object %s" % pprint.pformat(rObj))
            self.assertEqual(len(dObj), len(rObj))
            self.assertEqual(dObj, rObj)
            #
            # Now replace with a new document with a different key
            dObj2 = self.__makeDataObj(5, 5, 5)
            dObj2['THE_KEY'] = 'TWO'
            logger.debug("Replace Object %s" % pprint.pformat(dObj))
            #
            rId = mg.replace(self.__dbName, self.__collectionName, dObj2, {'THE_KEY': 'TWO'}, upsertFlag=True)
            rObj = mg.fetchOne(self.__dbName, self.__collectionName, 'THE_KEY', 'TWO')
            rObj.pop('_id', None)
            dObj2.pop('_id', None)
            logger.debug("Return Object %s" % pprint.pformat(rObj))
            self.assertEqual(len(dObj2), len(rObj))
            self.assertEqual(dObj2, rObj)
            #
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReplaceList(self):
        """Test case -  create collection and insert document list - replace document list

        """
        try:
            nDocs = 10
            client = self.getClientConnection()
            mg = MongoDbUtil(client)
            ok = mg.createCollection(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            ok = mg.databaseExists(self.__dbName)
            self.assertTrue(ok)
            ok = mg.collectionExists(self.__dbName, self.__collectionName)
            self.assertTrue(ok)
            #
            dList = []
            for ii in range(nDocs):
                dObj = self.__makeDataObj(2, 5, 5)
                dObj['THE_KEY'] = 'KVAL_%d' % ii
                dList.append(dObj)
            #
            rIdL = mg.insertList(self.__dbName, self.__collectionName, dList)
            self.assertTrue(len(rIdL), len(dList))
            # Note that dObj is mutated by additional key '_id' that is added on insert -
            #
            for ii, rId in enumerate(rIdL):
                rObj = mg.fetchOne(self.__dbName, self.__collectionName, '_id', rId)
                logger.debug("Return Object %s" % pprint.pformat(rObj))
                self.assertEqual(len(dList[ii]), len(rObj))
                self.assertEqual(dList[ii], rObj)
            #
            dList = []
            for ii in range(nDocs):
                dObj = self.__makeDataObj(2, 5, 5)
                dObj['THE_KEY'] = 'KVAL_%d' % ii
                dList.append(dObj)
            #
            dList = []
            for ii in range(nDocs + nDocs):
                dObj = self.__makeDataObj(4, 10, 10)
                dObj['THE_KEY'] = 'KVAL_%d' % ii
                dList.append(dObj)
            #
            updL = mg.replaceList(self.__dbName, self.__collectionName, dList, 'THE_KEY', upsertFlag=True)
            logger.debug("Upserted id list length %d" % len(updL))
            for ii in range(nDocs + nDocs):
                kVal = 'KVAL_%d' % ii
                rObj = mg.fetchOne(self.__dbName, self.__collectionName, 'THE_KEY', kVal)
                logger.debug("Return Object %s" % pprint.pformat(rObj))
                rObj.pop('_id', None)
                dList[ii].pop('_id', None)
                self.assertEqual(len(dList[ii]), len(rObj))
                self.assertEqual(dList[ii], rObj)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suiteOps():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(MongoDbUtilTests("testCreateDatabase"))
    suiteSelect.addTest(MongoDbUtilTests("testCreateDropDatabase"))
    suiteSelect.addTest(MongoDbUtilTests("testCreateCollection"))
    suiteSelect.addTest(MongoDbUtilTests("testCreateCollectionDropDatabase"))
    suiteSelect.addTest(MongoDbUtilTests("testCreateDropCollection"))
    return suiteSelect


def suiteInsert():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(MongoDbUtilTests("testInsertSingle"))
    suiteSelect.addTest(MongoDbUtilTests("testInsertList"))
    return suiteSelect


def suiteReplace():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(MongoDbUtilTests("testReplaceSingle"))
    suiteSelect.addTest(MongoDbUtilTests("testReplaceList"))
    return suiteSelect


if __name__ == '__main__':
    if (True):
        mySuite = suiteOps()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteInsert()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteReplace()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
