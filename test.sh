#!/bin/bash
#python3 import_semgrep_to_defect_dojo.py --host "http://localhost:8080" --product "WebGoat App" --engagement "Initial Security test" --scan "Gitleaks Scan" --report ./report/gitleak-report/report.json
#python3 import_to_defect_dojo.py --host "http://localhost:8080" --product "WebGoat App" --engagement "Scan 2" --scan "SonarQube API Import" --report '' --new True --token 0026e57d77b876b033736e9644e4e54ed41aa7f7

# python3 import_to_defect_dojo.py --host "http://localhost:8080" --product "WebGoat App" --engagement "Test CI" --scan "SonarQube API Import" --report "./report/gitleak-report/report.json" --is_new_import=False --token "0026e57d77b876b033736e9644e4e54ed41aa7f7" --active=false
python3 import_to_defect_dojo.py --host "http://localhost:8080" --product "WebGoat App" --engagement "Test CI" --scan "SonarQube API Import" --report "./report/gitleak-report/report.json" --token "1313c9e54a7ab10774a92ccfb448884aebbcc93f" --active="True" --test_title="Static Application Security Testing"
