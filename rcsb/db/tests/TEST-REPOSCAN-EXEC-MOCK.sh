#!/bin/bash
# File: TEST-REPOSCAN-EXEC-MOCK.sh
#
# Test of ScanRepo CLI
#
repo_scan_cli   --mock  --scan_chem_comp_ref      --working_path ./test-output --scan_data_file_path ./test-output/scan-cc-data.pic --coverage_file_path ./test-output/scan-cc-coverage.json --type_map_file_path ./test-output/scan-cc-type-map.json  --config_path ../../mock-data/config/dbload-setup-example.yml --config_name site_info --fail_file_list_path ./test-output/scan-failed-cc-path-list.txt  >& ./test-output/LOGCHEMCOMPFULL
repo_scan_cli   --mock  --scan_bird_chem_comp_ref --working_path ./test-output --scan_data_file_path ./test-output/scan-bird-cc-data.pic --coverage_file_path ./test-output/scan-bird-cc-coverage.json --type_map_file_path ./test-output/scan-bird-cc-type-map.json  --config_path ../../mock-data/config/dbload-setup-example.yml --config_name site_info --fail_file_list_path ./test-output/scan-failed-bird-cc-path-list.txt  >& ./test-output/LOGBIRDCHEMCOMPFULL
repo_scan_cli   --mock  --scan_bird_ref           --working_path ./test-output --scan_data_file_path ./test-output/scan-bird-data.pic --coverage_file_path ./test-output/scan-bird-coverage.json --type_map_file_path ./test-output/scan-bird-type-map.json  --config_path ../../mock-data/config/dbload-setup-example.yml --config_name site_info --fail_file_list_path ./test-output/scan-failed-bird-path-list.txt  >& ./test-output/LOGBIRDFULL
repo_scan_cli   --mock  --scan_bird_family_ref    --working_path ./test-output --scan_data_file_path ./test-output/scan-bird-family-data.pic --coverage_file_path ./test-output/scan-bird-family-coverage.json --type_map_file_path ./test-output/scan-bird-family-type-map.json  --config_path ../../mock-data/config/dbload-setup-example.yml --config_name site_info --fail_file_list_path ./test-output/scan-failed-family-path-list.txt  >& ./test-output/LOGBIRDFAMILY
repo_scan_cli   --mock  --scan_entry_data         --working_path ./test-output --scan_data_file_path ./test-output/scan-entry-data.pic --coverage_file_path ./test-output/scan-entry-coverage.json --type_map_file_path ./test-output/scan-entry-type-map.json  --config_path ../../mock-data/config/dbload-setup-example.yml --config_name site_info --fail_file_list_path ./test-output/scan-failed-entry-path-list.txt >& ./test-output/LOGENTRYFULL
repo_scan_cli   --mock  --scan_ihm_dev            --working_path ./test-output --scan_data_file_path ./test-output/scan-ihm_dev-data.pic --coverage_file_path ./test-output/scan-ihm_dev-coverage.json --type_map_file_path ./test-output/scan-ihm_dev-type-map.json  --config_path ../../mock-data/config/dbload-setup-example.yml --config_name site_info --fail_file_list_path ./test-output/scan-failed-ihm-path-list.txt >& ./test-output/LOGIHMFULL
#
