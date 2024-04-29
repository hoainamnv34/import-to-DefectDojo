FROM python:3.9-bullseye

COPY import_to_defect_dojo.py /import_to_defect_dojo.py

ENTRYPOINT ["python3", "/import_to_defect_dojo.py"]
