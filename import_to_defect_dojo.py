import json
import string
import requests
import sys
import argparse
import os


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def uploadToDefectDojo(is_new_import, token, url, product_name, engagement_name, scan_type, filename, active, verified, test_title, close_old_findings, close_old_findings_product_scope, branch_tag, commit_hash):

    multipart_form_data = {
        'scan_type': (None, scan_type),
        'product_name': (None, product_name),
        'engagement_name': (None, engagement_name),
        'active': (None, str(active)),
        'verified': (None, str(verified)),
        'test_title': (None, test_title),
        'close_old_findings': (None, str(close_old_findings)),
        'close_old_findings_product_scope': (None, str(close_old_findings_product_scope)),
        'branch_tag': (None, branch_tag),
        'commit_hash': (None, commit_hash),
    }

    if filename:
        multipart_form_data['file'] = (filename, open(filename, 'rb'))

    endpoint = '/api/v2/import-scan/' if is_new_import else '/api/v2/reimport-scan/'

    print(endpoint)
    r = requests.post(
        url + endpoint,
        files=multipart_form_data,
        headers={
            'Authorization': 'Token ' + token,
        }
    )
    if r.status_code != 200 and r.status_code != 201:
        sys.exit(f'Post failed: {r.text}')
    print(r.text)

def fetchArguments():
    parse = argparse.ArgumentParser(description='Import scan results to DefectDojo')
    parse.add_argument('--host', dest='host')
    parse.add_argument('--product', dest='product_name')
    parse.add_argument('--engagement', dest='engagement_name')
    parse.add_argument('--scan', dest='scan_type')
    parse.add_argument('--report', dest='report')
    parse.add_argument('--is_new_import', dest='is_new_import', type=str2bool, required=False, default=None)
    parse.add_argument('--token', dest='token')


    parse.add_argument('--active', dest='active' , type=str2bool)
    parse.add_argument('--verified', dest='verified' , type=str2bool)
    parse.add_argument('--test_title', dest='test_title',)
    parse.add_argument('--close_old_findings', dest='close_old_findings', type=str2bool)
    parse.add_argument('--close_old_findings_product_scope', dest='close_old_findings_product_scope', type=str2bool)
    parse.add_argument('--branch_tag', dest='branch_tag')
    parse.add_argument('--commit_hash', dest='commit_hash')
    
    return parse.parse_args()   



def get_product_id(product_name, token, url):
    headers = {"Accept": "application/json", "Authorization": "Token " + token}

    r = requests.get(url + '/api/v2/products',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for product in data['results']:
        if product['name'] == product_name:
            return product['id']
        
def get_engagement_id(product_id, engagement_name, token, url):
    headers = {"Accept": "application/json", "Authorization": "Token " + token}

    r = requests.get(url + '/api/v2/engagements',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for engagement in data['results']:
        if engagement['name'] == engagement_name:
            if engagement['product'] == product_id:
                return engagement['id']
            
def get_test_id(engagement_id, test_title, token, url):
    headers = {"Accept": "application/json", "Authorization": "Token " + token}

    r = requests.get(url + '/api/v2/tests',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for test in data['results']:
        if test['engagement'] == engagement_id:
            if test['title'] == test_title:
                return test['id']

def is_new_import(product_name, engagement_name, test_title, token, url):
    product_id = get_product_id(product_name, token, url)
    if not product_id:
        sys.exit('[ERROR] Not found product')
    else:
        print('[INFO] Product ID:', product_id)

    engagement_id = get_engagement_id(product_id, engagement_name, token, url)

    if not engagement_id:
        sys.exit('[ERROR] Not found Engagement')
    else:
        print('[INFO] Engagement ID:', product_id)

    test_id = get_test_id(engagement_id, test_title, token, url)
    if not test_id:
        return True
    else:
        print('[INFO] Test ID:', product_id)
        return False




if __name__ == "__main__":
    args = fetchArguments()
    print(args)

    

    if args.is_new_import:
        is_new = args.is_new_import
    else:
        is_new = is_new_import(args.product_name, args.engagement_name, args.test_title,args.token, args.host )

    print("is_new_import: ", is_new)

    uploadToDefectDojo(
        is_new, 
        args.token, 
        args.host, 
        args.product_name, 
        args.engagement_name, 
        args.scan_type, 
        args.report, 
        args.active, 
        args.verified, 
        args.test_title, 
        args.close_old_findings, 
        args.close_old_findings_product_scope, 
        args.branch_tag, 
        args.commit_hash
    )