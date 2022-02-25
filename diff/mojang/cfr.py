
import os
import sys
import inspect
import requests

# Allow importing from parent module
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir) 

from common import files

def decompile_jar(jar_path, output_path):
    print(f"Decompiling {jar_path}")
    result = os.system(f"java -jar cfr.jar {jar_path} --silent true --clobber true --showversion false --outputpath {output_path}")
    return result == 0

def download_latest():
    # releases_result = requests.get('https://api.github.com/repos/leibnitz27/cfr/releases?per_page=1', 
    #                                headers={'Accept': 'application/vnd.github.v3+json'})
    # if releases_result.status_code != 200:
    #     print(f"Error: Unable to fetch release list (status code: {releases_result.status_code})")
    #     return None
    
    # assets_url = releases_result.json()[0]['assets_url']

    # assets_result = requests.get(assets_url, headers={'Accept': 'application/vnd.github.v3+json'})
    # if assets_result.status_code != 200:
    #     print(f"Error: Unable to fetch assets (status code: {assets_result.status_code})")
    #     return False
    
    
    # cfr_jar_url = next(x['browser_download_url'] for x in assets_result.json() if x['name'].startswith('cfr') and x['name'].endswith('.jar') and not 'javadoc' in x['name'])
    cfr_jar_url = 'https://www.benf.org/other/cfr/cfr-0.152.jar'
    files.download_file(cfr_jar_url, 'cfr.jar')

    return True

if __name__ == '__main__':
    download_latest()
