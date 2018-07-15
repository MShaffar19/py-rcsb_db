##
# File:    SchemaDefAccessTests.py
# Author:  J. Westbrook
# Date:    15-Jun-2018
# Version: 0.001
#
# Update:
#
##
"""
Tests the accessor methods for schema meta data.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
import os
import sys
import time
import unittest

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from rcsb_db import __version__
except Exception as e:
    sys.path.insert(0, TOPDIR)
    from rcsb_db import __version__

from rcsb_db.define.SchemaDefAccess import SchemaDefAccess
from rcsb_db.define.SchemaDefBuild import SchemaDefBuild
#
from rcsb_db.helpers.DictInfoHelper import DictInfoHelper
from rcsb_db.helpers.SchemaDefHelper import SchemaDefHelper
from rcsb_db.helpers.SchemaDocumentHelper import SchemaDocumentHelper
from rcsb_db.io.IoUtil import IoUtil

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SchemaDefAccessTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        self.__pathPdbxDictionaryFile = os.path.join(TOPDIR, 'rcsb_db', 'data', 'dictionaries', 'mmcif_pdbx_v5_next.dic')
        self.__pathRcsbDictionaryFile = os.path.join(TOPDIR, 'rcsb_db', 'data', 'dictionaries', 'rcsb_mmcif_ext_v1.dic')

        self.__startTime = time.time()
        logger.debug("Running tests on version %s" % __version__)
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)" % (self.id(),
                                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                            endTime - self.__startTime))

    def testAccess(self):
        schemaNames = ['pdbx', 'chem_comp', 'bird', 'bird_family', 'bird_chem_comp']
        applicationNames = ['ANY', 'SQL']
        for schemaName in schemaNames:
            for applicationName in applicationNames:
                self.__testAccess(schemaName, applicationName)

    def __testBuild(self, schemaName, applicationName):
        try:
            instDataTypeFilePath = os.path.join(TOPDIR, 'rcsb_db', 'data', 'data_type_info', 'scan-%s-type-map.json' % schemaName)
            appDataTypeFilePath = os.path.join(TOPDIR, 'rcsb_db', 'data', 'data_type_info', 'app_data_type_mapping.cif')
            #
            pathSchemaDefJson = os.path.join(HERE, 'test-output', 'schema_def-%s-%s.json' % (schemaName, applicationName))
            #
            dictInfoHelper = DictInfoHelper()
            defHelper = SchemaDefHelper()
            docHelper = SchemaDocumentHelper()
            #
            smb = SchemaDefBuild(schemaName,
                                 dictLocators=[self.__pathPdbxDictionaryFile, self.__pathRcsbDictionaryFile],
                                 instDataTypeFilePath=instDataTypeFilePath,
                                 appDataTypeFilePath=appDataTypeFilePath,
                                 dictHelper=dictInfoHelper,
                                 schemaDefHelper=defHelper,
                                 documentDefHelper=docHelper,
                                 applicationName=applicationName,
                                 includeContentClasses=['ADMIN_CATEGORY'])
            sD = smb.build()
            #
            logger.debug("Schema dictionary category length %d" % len(sD['SCHEMA_DICT']))
            self.assertGreaterEqual(len(sD['SCHEMA_DICT']), 5)
            #
            ioU = IoUtil()
            ioU.serialize(pathSchemaDefJson, sD, format='json', indent=3)
            return sD

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()
        return {}

    def __testAccess(self, schemaName, applicationName):
        try:
            sD = self.__testBuild(schemaName, applicationName)
            ok = self.__testAccessors(sD)
            self.assertTrue(ok)
            #
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()
        return {}

    def __testAccessors(self, schemaDef):
        """  Verify data and accessor mapping -

        """

        sd = SchemaDefAccess(schemaDef)
        logger.debug("Schema name %s" % sd.getName())
        logger.debug("Schema name %s" % sd.getAppName())

        logger.debug("Database name %s" % sd.getDatabaseName())
        logger.debug("Versioned database name %s" % sd.getVersionedDatabaseName())

        logger.debug("Collections %r" % sd.getContentTypeCollections(sd.getName()))

        for dS in sd.getDataSelectorNames():
            logger.debug("Selector %s %r" % (dS, sd.getDataSelectors(dS)))

        collectionNames = sd.getContentTypeCollections(sd.getName())
        for collectionName in collectionNames:

            logger.debug("Collection excluded %r" % sd.getCollectionExcluded(collectionName))
            logger.debug("Collection included %r" % sd.getCollectionSelected(collectionName))
            logger.debug("Collection document key attribute name %r" % sd.getDocumentKeyAttributeName(collectionName))

        schemaIdList = sd.getSchemaIdList()
        for schemaId in schemaIdList:
            #
            aIdL = sd.getAttributeIdList(schemaId)
            tObj = sd.getSchemaObject(schemaId)
            attributeIdList = tObj.getAttributeIdList()
            self.assertEqual(len(aIdL), len(attributeIdList))
            attributeNameList = tObj.getAttributeNameList()
            logger.debug("Ordered attribute Id   list %s" % (str(attributeIdList)))
            logger.debug("Ordered attribute name list %s" % (str(attributeNameList)))
            #
            mAL = tObj.getMapAttributeNameList()
            logger.debug("Ordered mapped attribute name list %s" % (str(mAL)))

            mAL = tObj.getMapAttributeIdList()
            logger.debug("Ordered mapped attribute id   list %s" % (str(mAL)))

            cL = tObj.getMapInstanceCategoryList()
            logger.debug("Mapped category list %s" % (str(cL)))
            ccL = tObj.getContentClasses()
            logger.debug("Content classes %r" % ccL)
            if 'ADMIN_CATEGORY' in ccL:
                self.assertGreaterEqual(len(cL), 0)
            else:
                self.assertGreater(len(cL), 0)
            for c in cL:
                aL = tObj.getMapInstanceAttributeList(c)
                logger.debug("Mapped attribute list in %s :  %s" % (c, str(aL)))
        return True


def schemaAccessSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(SchemaDefAccessTests("testAccess"))
    return suiteSelect


if __name__ == '__main__':
    #
    if True:
        mySuite = schemaAccessSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
