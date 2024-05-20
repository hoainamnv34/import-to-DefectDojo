import requests
import sys
import json
import os

URL_DEFECT_DOJO = "http://localhost:8080"

def get_product_id(product_name):
    headers = {"Accept": "application/json", "Authorization": "Token " + DEFECT_DOJO_API_TOKEN}

    r = requests.get(URL_DEFECT_DOJO + '/api/v2/products',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for product in data['results']:
        if product['name'] == product_name:
            return product['id']
        
def get_engagement_id(product_id, engagement_name):
    headers = {"Accept": "application/json", "Authorization": "Token " + DEFECT_DOJO_API_TOKEN}

    r = requests.get(URL_DEFECT_DOJO + '/api/v2/engagements',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for engagement in data['results']:
        if engagement['name'] == engagement_name:
            if engagement['product'] == product_id:
                return engagement['id']
            
def get_test_id(engagement_id, test_title):
    headers = {"Accept": "application/json", "Authorization": "Token " + DEFECT_DOJO_API_TOKEN}

    r = requests.get(URL_DEFECT_DOJO + '/api/v2/tests',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for test in data['results']:
        if test['engagement'] == engagement_id:
            if test['title'] == test_title:
                return test['id']

if __name__ == "__main__":
    try:
        DEFECT_DOJO_API_TOKEN = os.getenv("DEFECT_DOJO_API_TOKEN")
    except KeyError: 
        print("Please set the environment variable DEFECT_DOJO_API_TOKEN") 
        sys.exit(1)
    # uploadToDefectDojo("report.json", False)
    # get_engagements()
    product_id = get_product_id("WebGoat App")
    if not product_id:
        print('[ERROR] Not found product')
    else:
        print('[INFO] Product ID:', product_id)

    engagement_id = get_engagement_id(product_id, "Test CD")

    if not engagement_id:
        print('[ERROR] Not found Engagement')
    else:
        print('[INFO] Engagement ID:', product_id)

    test_id = get_test_id(engagement_id, 'Security API Scanning')
    if not test_id:
        print('[ERROR] Not found Test')
    else:
        print('[INFO] Test ID:', product_id)

    

