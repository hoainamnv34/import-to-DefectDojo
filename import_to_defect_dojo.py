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
    parse.add_argument('--is_new_import', dest='is_new_import', type=str2bool)
    parse.add_argument('--token', dest='token')


    parse.add_argument('--active', dest='active' , type=bool)
    parse.add_argument('--verified', dest='verified' , type=bool)
    parse.add_argument('--test_title', dest='test_title',)
    parse.add_argument('--close_old_findings', dest='close_old_findings', type=bool)
    parse.add_argument('--close_old_findings_product_scope', dest='close_old_findings_product_scope', type=bool)
    parse.add_argument('--branch_tag', dest='branch_tag')
    parse.add_argument('--commit_hash', dest='commit_hash')
    
    return parse.parse_args()   
    


if __name__ == "__main__":
    args = fetchArguments()
    print(args)

    uploadToDefectDojo(
        args.is_new_import, 
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