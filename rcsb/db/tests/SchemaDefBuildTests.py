##
# File:    SchemaDefBuildTests.py
# Author:  J. Westbrook
# Date:    9-Jun-2018
# Version: 0.001
#
# Update:
#      7-Sep-2018 jdw Update JSON/BSON schema generation tests
#      7-Oct-2018 jdw update with repository_holdings and  sequence_cluster tests
#     29-Nov-2018 jdw add selected build tests
##
"""
Tests for utilities employed to construct local and json schema defintions from
dictionary metadata and user preference data.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
import os
import time
import unittest

from rcsb.db.define.SchemaDefAccess import SchemaDefAccess
from rcsb.db.utils.SchemaDefUtil import SchemaDefUtil
from rcsb.utils.config.ConfigUtil import ConfigUtil

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class SchemaDefBuildTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        mockTopPath = os.path.join(TOPDIR, 'rcsb', 'mock-data')
        pathConfig = os.path.join(mockTopPath, 'config', 'dbload-setup-example.yml')
        configName = 'site_info'
        self.__cfgOb = ConfigUtil(configPath=pathConfig, defaultSectionName=configName, mockTopPath=mockTopPath)
        #
        self.__sdu = SchemaDefUtil(cfgOb=self.__cfgOb)
        self.__workPath = os.path.join(HERE, 'test-output')
        self.__schemaLevels = self.__cfgOb.getList('SCHEMA_LEVELS_TEST', sectionName='schema_catalog_info')
        self.__schemaTypes = self.__cfgOb.getList('SCHEMA_TYPES_TEST', sectionName='schema_catalog_info')
        #
        self.__schemaNameList = self.__cfgOb.getList('SCHEMA_NAMES_TEST', sectionName='schema_catalog_info')
        self.__dataTypingList = self.__cfgOb.getList('DATATYPING_TEST', sectionName='schema_catalog_info')
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)" % (self.id(),
                                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                            endTime - self.__startTime))

    def testBuildSchemaDefs(self):
        for schemaName in self.__schemaNameList:
            for dataTyping in self.__dataTypingList:
                self.__sdu.makeSchemaDef(schemaName, dataTyping=dataTyping, saveSchema=True, altDirPath=self.__workPath)
    #

    def testBuildCollectionSchema(self):
        for schemaName in self.__schemaNameList:
            d = self.__sdu.makeSchemaDef(schemaName, dataTyping='ANY', saveSchema=False, altDirPath=None)
            sD = SchemaDefAccess(d)
            for cd in sD.getCollectionInfo():
                collectionName = cd['NAME']
                for schemaType in self.__schemaTypes:
                    if schemaType.lower() == 'rcsb':
                        continue
                    for level in self.__schemaLevels:
                        self.__sdu.makeSchema(schemaName, collectionName, schemaType=schemaType, level=level, saveSchema=True, altDirPath=self.__workPath)


def schemaBuildSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(SchemaDefBuildTests("testBuildSchemaDefs"))
    suiteSelect.addTest(SchemaDefBuildTests("testBuildCollectionSchema"))
    return suiteSelect


if __name__ == '__main__':
    #
    if True:
        mySuite = schemaBuildSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
