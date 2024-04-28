#!/bin/bash
#python3 import_semgrep_to_defect_dojo.py --host "http://localhost:8080" --product "WebGoat App" --engagement "Initial Security test" --scan "Gitleaks Scan" --report ./report/gitleak-report/report.json
python3 import_semgrep_to_defect_dojo.py --host "http://localhost:8080" --product "WebGoat App" --engagement "Scan 2" --scan "Gitleaks Scan" --report ./report/gitleak-report/report.json