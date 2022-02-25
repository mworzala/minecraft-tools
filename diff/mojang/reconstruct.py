
import os
import sys
import inspect
import requests

# Allow importing from parent module
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir) 

from common import files

def deobfuscate_jar(jar_path, mapping_path, output_path):
    print(f"Deobfuscating {jar_path}")
    result = os.system(f"java -jar reconstruct.jar --agree --jar {jar_path} --mapping {mapping_path} --output {output_path}")
    return result == 0

def download_latest():
    releases_result = requests.get('https://api.github.com/repos/LXGaming/Reconstruct/releases?per_page=1', 
                                   headers={'Accept': 'application/vnd.github.v3+json'})
    if releases_result.status_code != 200:
        print(f"Error: Unable to fetch release list (status code: {releases_result.status_code})")
        return None
    
    assets_url = releases_result.json()[0]['assets_url']

    assets_result = requests.get(assets_url, headers={'Accept': 'application/vnd.github.v3+json'})
    if assets_result.status_code != 200:
        print(f"Error: Unable to fetch assets (status code: {assets_result.status_code})")
        return False
    
    reconstruct_jar_url = next(x['browser_download_url'] for x in assets_result.json() if x['name'].startswith('reconstruct') and x['name'].endswith('.jar'))
    files.download_file(reconstruct_jar_url, 'reconstruct.jar')

    return True

if __name__ == '__main__':
    download_latest()
