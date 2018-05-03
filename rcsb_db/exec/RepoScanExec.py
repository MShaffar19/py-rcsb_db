##
# File: RepoScanExec.py
#
#  Execution wrapper  --  repository scanning utilities --
#  Updates:
#
#
##
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import os
import sys
import argparse

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from rcsb_db import __version__
except Exception as e:
    sys.path.insert(0, TOPDIR)
    from rcsb_db import __version__


from rcsb_db.utils.ConfigUtil import ConfigUtil
from rcsb_db.utils.ScanRepoUtil import ScanRepoUtil


def readPathList(fileListPath):
    pathList = []
    try:
        with open(fileListPath, 'r') as ifh:
            for line in ifh:
                pth = str(line[:-1]).strip()
                if len(pth) and not pth.startswith("#"):
                    pathList.append(pth)
    except Exception as e:
        pass
    logger.debug("Reading path list length %d" % len(pathList))
    return pathList


def scanRepo(cfgOb, contentType, scanDataFilePath, dictFilePath, numProc, chunkSize, fileLimit, mockTopPath,
             inputPathList=None, pathListFilePath=None, dataCoverageFilePath=None, dataTypeFilePath=None, failedFilePath=None):
    """ Utility method to scan repo for the input content type.
    """
    try:
        #
        sr = ScanRepoUtil(cfgOb, dictPath=dictFilePath, numProc=numProc, chunkSize=chunkSize, fileLimit=fileLimit, mockTopPath=mockTopPath)
        ok = sr.scanContentType(contentType, scanType='full', inputPathList=inputPathList, outputFilePath=scanDataFilePath,
                                failedFilePath=failedFilePath, saveInputFileListPath=pathListFilePath)
        if dataTypeFilePath:
            ok = sr.evalScan(scanDataFilePath, dataTypeFilePath, evalType='data_type')
        if dataCoverageFilePath:
            ok = sr.evalScan(scanDataFilePath, dataCoverageFilePath, evalType='data_coverage')

        return ok
    except Exception as e:
        logger.exception("Failing with %s" % str(e))


def main():
    parser = argparse.ArgumentParser()
    #
    parser.add_argument("--dict_file_path", default=None, help="PDBx/mmCIF dictionary file path")
    #
    #parser.add_argument("--full", default=False, action='store_true', help="Full scan of repository")
    #parser.add_argument("--incr", default=False, action='store_true', help="Incr scan of repository")
    #
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--scan_chem_comp_ref", default=False, action='store_true', help="Scan Chemical Component reference definitions (public subset)")
    group.add_argument("--scan_bird_chem_comp_ref", default=False, action='store_true', help="Scan Bird Chemical Component reference definitions (public subset)")
    group.add_argument("--scan_bird_ref", default=False, action='store_true', help="Scan Bird reference definitions (public subset)")
    group.add_argument("--scan_bird_family_ref", default=False, action='store_true', help="Scan Bird Family reference definitions (public subset)")
    group.add_argument("--scan_entry_data", default=False, action='store_true', help="Scan PDB entry data (current released subset)")
    #
    parser.add_argument("--config_path", default=None, help="Path to configuration options file")
    parser.add_argument("--config_name", default="DEFAULT", help="Configuration section name")

    parser.add_argument("--input_file_list_path", default=None, help="Input file containing file paths to scan")
    parser.add_argument("--output_file_list_path", default=None, help="Output file containing file paths scanned")
    parser.add_argument("--fail_file_list_path", default=None, help="Output file containing file paths that fail scan")
    parser.add_argument("--scan_data_file_path", default=None, help="Output working file storing scan data (Pickle)")
    parser.add_argument("--coverage_file_path", default=None, help="Coverage map (JSON) output path")
    parser.add_argument("--type_map_file_path", default=None, help="Type map (JSON) output path")

    parser.add_argument("--num_proc", default=2, help="Number of processes to execute (default=2)")
    parser.add_argument("--chunk_size", default=10, help="Number of files loaded per process")
    parser.add_argument("--file_limit", default=None, help="Load file limit for testing")
    parser.add_argument("--debug", default=False, action='store_true', help="Turn on verbose logging")
    parser.add_argument("--mock", default=False, action='store_true', help="Use MOCK repository configuration for testing")
    args = parser.parse_args()
    #
    debugFlag = args.debug
    if debugFlag:
        logger.setLevel(logging.DEBUG)
        logger.debug("Using software version %s" % __version__)
    # ----------------------- - ----------------------- - ----------------------- - ----------------------- - ----------------------- -
    #                                       Configuration Details
    configPath = args.config_path
    configName = args.config_name
    if not configPath:
        configPath = os.getenv('DBLOAD_CONFIG_PATH', None)
    try:
        if os.access(configPath, os.R_OK):
            os.environ['DBLOAD_CONFIG_PATH'] = configPath
            logger.info("Using configuation path %s (%s)" % (configPath, configName))
        else:
            logger.error("Missing or access issue with config file %r" % configPath)
            exit(1)

        cfgOb = ConfigUtil(configPath=configPath, sectionName=configName)
    except Exception as e:
        logger.error("Missing or access issue with config file %r" % configPath)
        exit(1)

    #
    try:
        numProc = int(args.num_proc)
        chunkSize = int(args.chunk_size)
        fileLimit = int(args.file_limit) if args.file_limit else None
        #
        failedFilePath = args.fail_file_list_path

        #loadType = 'full' if args.full else 'replace'
        #loadType = 'replace' if args.replace else 'full'
        #
        inputFileListPath = args.input_file_list_path
        outputFileListPath = args.output_file_list_path
        scanDataFilePath = args.scan_data_file_path
        dataCoverageFilePath = args.coverage_file_path
        dataTypeFilePath = args.type_map_file_path
        mockTopPath = os.path.join(TOPDIR, "rcsb_db", "data") if args.mock else None
        dictFilePath = args.dict_file_path if args.dict_file_path else os.path.join(TOPDIR, 'rcsb_db', 'data', 'mmcif_pdbx_v5_next.dic')
    except Exception as e:
        logger.exception("Argument processing problem %s" % str(e))
        parser.print_help(sys.stderr)
        exit(1)
    # ----------------------- - ----------------------- - ----------------------- - ----------------------- - ----------------------- -
    #
    # Read any input path lists -
    #
    inputPathList = None
    if inputFileListPath:
        inputPathList = readPathList(inputFileListPath)
    #
    ##

    if args.scan_chem_comp_ref:
        contentType = 'chem_comp'

    elif args.scan_bird_chem_comp_ref:
        contentType = 'bird_chem_comp'

    elif args.scan_bird_ref:
        contentType = 'bird_chem_comp'

    elif args.scan_bird_family_ref:
        contentType = 'bird_family'

    elif args.scan_entry_data:
        contentType = 'pdbx'

    ok = scanRepo(cfgOb, contentType, scanDataFilePath, dictFilePath, numProc, chunkSize, fileLimit, mockTopPath,
                  inputPathList=inputPathList, pathListFilePath=outputFileListPath, dataCoverageFilePath=dataCoverageFilePath,
                  dataTypeFilePath=dataTypeFilePath, failedFilePath=failedFilePath)

    logger.info("Operation completed with status %r " % ok)


if __name__ == '__main__':
    main()
