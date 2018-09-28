##
# File:    DictMethodRunnerHelper.py
# Author:  J. Westbrook
# Date:    18-Aug-2018
# Version: 0.001 Initial version
#
# Updates:
#  4-Sep-2018 jdw add methods to construct entry and entity identier categories.
# 10-Sep-2018 jdw add method for citation author aggregation
# 22-Sep-2018 jdw add method assignAssemblyCandidates()
#
##
"""
This helper class implements external method references in the RCSB dictionary extension.

All data accessors and structures here refer to dictionary category and attribute names.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import datetime
import logging

from mmcif.api.DataCategory import DataCategory

from rcsb.db.helpers.DictMethodRunnerHelperBase import DictMethodRunnerHelperBase

logger = logging.getLogger(__name__)


class DictMethodRunnerHelper(DictMethodRunnerHelperBase):
    """ Helper class implements external method references in the RCSB dictionary extension.

    """

    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: (dict)  Placeholder for future key-value arguments

        """
        super(DictMethodRunnerHelper, self).__init__(**kwargs)
        self._thing = kwargs.get("thing", None)
        logger.debug("Dictionary method helper init")
        #

    def echo(self, msg):
        logger.info(msg)

    def setDatablockId(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getName()
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setLoadDateTime(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getProp('load_date')
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setLocator(self, dataContainer, catName, atName, **kwargs):
        try:
            val = dataContainer.getProp('locator')
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii in range(numRows):
                cObj.setValue(val, atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def setRowIndex(self, dataContainer, catName, atName, **kwargs):
        try:
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=[atName]))
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            #
            rc = cObj.getRowCount()
            numRows = rc if rc else 1
            for ii, iRow in enumerate(range(numRows), 1):
                # Note - we set the integer value as a string  -
                cObj.setValue(str(ii), atName, iRow)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def aggregateCitationAuthors(self, dataContainer, catName, atName, **kwargs):
        try:
            if not dataContainer.exists(catName) or not dataContainer.exists('citation_author'):
                return False
            #
            cObj = dataContainer.getObj(catName)
            if not cObj.hasAttribute(atName):
                cObj.appendAttribute(atName)
            citIdL = cObj.getAttributeValueList('id')
            #
            tObj = dataContainer.getObj('citation_author')
            #
            citIdL = list(set(citIdL))
            tD = {}
            for ii, citId in enumerate(citIdL):
                tD[citId] = tObj.selectValuesWhere('name', citId, 'citation_id')
            for ii in range(cObj.getRowCount()):
                citId = cObj.getValue('id', ii)
                cObj.setValue(';'.join(tD[citId]), atName, ii)
            return True
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
        return False

    def buildContainerEntryIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_entry_container_identifiers.entry_id
        _rcsb_entry_container_identifiers.entity_ids
        _rcsb_entry_container_identifiers.polymer_entity_ids_polymer
        _rcsb_entry_container_identifiers.non-polymer_entity_ids
        _rcsb_entry_container_identifiers.assembly_ids
        ...
        """
        try:
            if not dataContainer.exists('entry'):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'entity_ids', 'polymer_entity_ids',
                                                                              'non-polymer_entity_ids', 'assembly_ids']))
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('entity')
            entityIdL = tObj.getAttributeValueList('id')
            cObj.setValue(','.join(entityIdL), 'entity_ids', 0)
            #
            #
            pIdL = tObj.selectValuesWhere('id', 'polymer', 'type')
            tV = ','.join(pIdL) if pIdL else '?'
            cObj.setValue(tV, 'polymer_entity_ids', 0)

            npIdL = tObj.selectValuesWhere('id', 'non-polymer', 'type')
            tV = ','.join(npIdL) if npIdL else '?'
            cObj.setValue(tV, 'non-polymer_entity_ids', 0)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            assemblyIdL = tObj.getAttributeValueList('id') if tObj else []
            tV = ','.join(assemblyIdL) if assemblyIdL else '?'
            cObj.setValue(tV, 'assembly_ids', 0)

            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def buildContainerEntityIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_entity_container_identifiers.entry_id
        _rcsb_entity_container_identifiers.entity_id
        ...
        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('entity')):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'entity_id']))
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('entity')
            entityIdL = tObj.getAttributeValueList('id')
            for ii, entityId in enumerate(entityIdL):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(entityId, 'entity_id', ii)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def buildContainerAssemblyIds(self, dataContainer, catName, **kwargs):
        """
        Build:

        loop_
        _rcsb_assembly_container_identifiers.entry_id
        _rcsb_assembly_container_identifiers.assembly_id
        ...
        """
        try:
            if not (dataContainer.exists('entry') and dataContainer.exists('pdbx_struct_assembly')):
                return False
            if not dataContainer.exists(catName):
                dataContainer.append(DataCategory(catName, attributeNameList=['entry_id', 'assembly_id']))
            #
            cObj = dataContainer.getObj(catName)

            tObj = dataContainer.getObj('entry')
            entryId = tObj.getValue('id', 0)
            cObj.setValue(entryId, 'entry_id', 0)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            assemblyIdL = tObj.getAttributeValueList('id')
            for ii, assemblyId in enumerate(assemblyIdL):
                cObj.setValue(entryId, 'entry_id', ii)
                cObj.setValue(assemblyId, 'assembly_id', ii)
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def addDepositedAssembly(self, dataContainer, catName, **kwargs):
        """ Add the deposited coordinates as a separate assembly labeled as 'deposited'.

        """
        try:
            if not dataContainer.exists('struct_asym'):
                return False
            if not dataContainer.exists('pdbx_struct_assembly'):
                dataContainer.append(DataCategory('pdbx_struct_assembly', attributeNameList=['id', 'details', 'method_details',
                                                                                             'oligomeric_details', 'oligomeric_count',
                                                                                             'rcsb_details', 'rcsb_candidate_assembly']))
            if not dataContainer.exists('pdbx_struct_assembly_gen'):
                dataContainer.append(DataCategory('pdbx_struct_assembly_gen', attributeNameList=['assembly_id', 'oper_expression', 'asym_id_list', 'ordinal']))

            if not dataContainer.exists('pdbx_struct_oper_list'):
                row = ['1', 'identity operation', '1_555', 'x, y, z', '1.0000000000', '0.0000000000', '0.0000000000',
                       '0.0000000000', '0.0000000000', '1.0000000000', '0.0000000000', '0.0000000000',
                       '0.0000000000', '0.0000000000', '1.0000000000', '0.0000000000']
                atList = ['id', 'type', 'name', 'symmetry_operation', 'matrix[1][1]', 'matrix[1][2]', 'matrix[1][3]',
                          'vector[1]', 'matrix[2][1]', 'matrix[2][2]', 'matrix[2][3]', 'vector[2]',
                          'matrix[3][1]', 'matrix[3][2]', 'matrix[3][3]', 'vector[3]']
                dataContainer.append(DataCategory('pdbx_struct_oper_list', attributeNameList=atList, rowList=[row]))

            #
            logger.debug("Add deposited assembly for %s" % dataContainer.getName())
            cObj = dataContainer.getObj('struct_asym')
            asymIdL = cObj.getAttributeValueList('id')
            logger.debug("AsymIdL %r" % asymIdL)
            #
            # Ordinal is added by subsequent attribure-level method.
            tObj = dataContainer.getObj('pdbx_struct_assembly_gen')
            rowIdx = tObj.getRowCount()
            tObj.setValue('deposited', 'assembly_id', rowIdx)
            tObj.setValue('1', 'oper_expression', rowIdx)
            tObj.setValue(','.join(asymIdL), 'asym_id_list', rowIdx)
            #
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            rowIdx = tObj.getRowCount()
            tObj.setValue('deposited', 'id', rowIdx)
            tObj.setValue('deposited_coordinates', 'details', rowIdx)
            logger.debug("Full row is %r" % tObj.getRow(rowIdx))
            #
            return True
        except Exception as e:
            logger.exception("For %s failing with %s" % (catName, str(e)))
        return False

    def filterAssemblyDetails(self, dataContainer, catName, atName, **kwargs):
        """ Filter _pdbx_struct_assembly.details -> _pdbx_struct_assembly.rcsb_details
            with a more limited vocabulary -

                'author_and_software_defined_assembly'
                'author_defined_assembly'
                'software_defined_assembly'

        """
        mD = {'author_and_software_defined_assembly': 'author_and_software_defined_assembly',
              'author_defined_assembly': 'author_defined_assembly',
              'complete icosahedral assembly': 'author_and_software_defined_assembly',
              'complete point assembly': 'author_and_software_defined_assembly',
              'crystal asymmetric unit': 'software_defined_assembly',
              'crystal asymmetric unit, crystal frame': 'software_defined_assembly',
              'details': 'software_defined_assembly',
              'helical asymmetric unit': 'software_defined_assembly',
              'helical asymmetric unit, std helical frame': 'software_defined_assembly',
              'icosahedral 23 hexamer': 'software_defined_assembly',
              'icosahedral asymmetric unit': 'software_defined_assembly',
              'icosahedral asymmetric unit, std point frame': 'software_defined_assembly',
              'icosahedral pentamer': 'software_defined_assembly',
              'pentasymmetron capsid unit': 'software_defined_assembly',
              'point asymmetric unit': 'software_defined_assembly',
              'point asymmetric unit, std point frame': 'software_defined_assembly',
              'representative helical assembly': 'author_and_software_defined_assembly',
              'software_defined_assembly': 'software_defined_assembly',
              'trisymmetron capsid unit': 'software_defined_assembly',
              'deposited_coordinates': 'software_defined_assembly'}
        #
        try:
            if not dataContainer.exists('pdbx_struct_assembly'):
                return False

            logger.debug("Filter assembly details for %s" % dataContainer.getName())
            tObj = dataContainer.getObj('pdbx_struct_assembly')
            if not tObj.hasAttribute(atName):
                tObj.appendAttribute(atName)
            #
            for iRow in range(tObj.getRowCount()):
                details = tObj.getValue('details', iRow)
                if details in mD:
                    tObj.setValue(mD[details], 'rcsb_details', iRow)
                else:
                    tObj.setValue('software_defined_assembly', 'rcsb_details', iRow)
                logger.debug("Full row is %r" % tObj.getRow(iRow))
            return True
        except Exception as e:
            logger.exception("For %s %s failing with %s" % (catName, atName, str(e)))
        return False

    def assignAssemblyCandidates(self, dataContainer, catName, atName, **kwargs):
        """ Flag candidate biological assemblies as 'author_defined_assembly' ad author_and_software_defined_assembly'

        """
        mD = {'author_and_software_defined_assembly': 'author_and_software_defined_assembly',
              'author_defined_assembly': 'author_defined_assembly',
              'complete icosahedral assembly': 'author_and_software_defined_assembly',
              'complete point assembly': 'author_and_software_defined_assembly',
              'crystal asymmetric unit': 'software_defined_assembly',
              'crystal asymmetric unit, crystal frame': 'software_defined_assembly',
              'details': 'software_defined_assembly',
              'helical asymmetric unit': 'software_defined_assembly',
              'helical asymmetric unit, std helical frame': 'software_defined_assembly',
              'icosahedral 23 hexamer': 'software_defined_assembly',
              'icosahedral asymmetric unit': 'software_defined_assembly',
              'icosahedral asymmetric unit, std point frame': 'software_defined_assembly',
              'icosahedral pentamer': 'software_defined_assembly',
              'pentasymmetron capsid unit': 'software_defined_assembly',
              'point asymmetric unit': 'software_defined_assembly',
              'point asymmetric unit, std point frame': 'software_defined_assembly',
              'representative helical assembly': 'author_and_software_defined_assembly',
              'software_defined_assembly': 'software_defined_assembly',
              'trisymmetron capsid unit': 'software_defined_assembly',
              'deposited_coordinates': 'software_defined_assembly'}
        #
        try:
            if not dataContainer.exists('pdbx_struct_assembly'):
                return False

            tObj = dataContainer.getObj('pdbx_struct_assembly')
            if not tObj.hasAttribute(atName):
                tObj.appendAttribute(atName)
            #
            for iRow in range(tObj.getRowCount()):
                details = tObj.getValue('details', iRow)
                if details in mD and mD[details] in ['author_and_software_defined_assembly', 'author_defined_assembly']:
                    tObj.setValue('Y', 'rcsb_candidate_assembly', iRow)
                else:
                    tObj.setValue('N', 'rcsb_candidate_assembly', iRow)
                logger.debug("Full row is %r" % tObj.getRow(iRow))
            return True
        except Exception as e:
            logger.exception("For %s %s failing with %s" % (catName, atName, str(e)))
        return False

    def __getTimeStamp(self):
        utcnow = datetime.datetime.utcnow()
        ts = utcnow.strftime("%Y-%m-%d:%H:%M:%S")
        return ts