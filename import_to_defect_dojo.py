import string
import requests
import sys
import argparse
import os


def uploadToDefectDojo(is_new_import, token, url, product_name, engagement_name, scan_type, filename):

    if filename == '':
        multipart_form_data = {
            'scan_type': (None, scan_type),
            'product_name': (None, product_name),
            'engagement_name': (None, engagement_name),
        }

    else:
        multipart_form_data = {
            'file': (filename, open(filename, 'rb')),
            'scan_type': (None, scan_type),
            'product_name': (None, product_name),
            'engagement_name': (None, engagement_name),

        }

    endpoint = '/api/v2/import-scan/' if is_new_import else '/api/v2/reimport-scan/'
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
    parse.add_argument('--is-new', dest='is_new_import', type=bool)
    parse.add_argument('--token', dest='token')
    
    return parse.parse_args()   
    


if __name__ == "__main__":
    args = fetchArguments()

    uploadToDefectDojo(args.is_new_import, args.token, args.host, args.product_name, args.engagement_name, args.scan_type, args.report)

    # try:
    #     token = os.getenv("DEFECT_DOJO_API_TOKEN")
    # except KeyError: 
    #     print("Please set the environment variable DEFECT_DOJO_API_TOKEN") 
    #     sys.exit(1)
    # print(sys.argv)
    # if len(sys.argv) == 15:
    #     url = sys.argv[2]
    #     product_name = sys.argv[4]
    #     engagement_name = sys.argv[6]
    #     scan_type = sys.argv[8]
    #     report = sys.argv[10]
    #     is_new_import = sys.argv[12]
    #     token=sys.argv[14]

    #     is_new_import = True if is_new_import=="True" else False

    #     print("token ", token, "host: ", url, " product_name", product_name, " engagement_name", engagement_name, " scan_type", scan_type)
        
    #     uploadToDefectDojo(is_new_import, token, url, product_name, engagement_name, scan_type, report)
    # else:
    #     print(
    #         'Usage: python3 import_to_defect_dojo.py --host DOJO_URL --product PRODUCT_NAME --engagement ENGAGEMENT_NAME --report REPORT_FILE --new-import True/False --token TOKEN')
    
    