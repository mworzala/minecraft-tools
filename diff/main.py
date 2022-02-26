
import os
import sys
import inspect
import requests

# Allow importing from parent module
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from common import files
from mojang import reconstruct, cfr

def main():
    if not os.path.exists('temp'):
        os.mkdir('temp')
    os.chdir('temp')

    source_version = None
    target_version = None

    if len(sys.argv) > 1:
        source_version = sys.argv[1]
    else: 
        print("Error: No source version specified")
        return 1
    if source_version == None: return 1
    print(f"Source...{source_version}")

    if len(sys.argv) > 2:
        target_version = sys.argv[2]
    else:
        print("Error: No target version specified")
        return 1
    if target_version == None: return 1
    print(f"Target...{target_version}")

    result = download_client(target_version)
    if not result: return 1

    result = reconstruct.download_latest()
    if not result: return 1
    result = cfr.download_latest()
    if not result: return 1

    print("Deobfuscating Minecraft...")
    result = reconstruct.deobfuscate_jar('server.jar', 'server.txt', 'server_deobfuscated.jar')
    if not result: return 1

    print("Decompiling Minecraft...")
    result = cfr.decompile_jar('server_deobfuscated.jar', 'server_decompiled')
    if not result: return 1

    print("Done!")

    if source_version != "none":
        # os.system(f"git checkout {source_version}")
        return 0
    else:
        os.system(f"git checkout -b {target_version}_moj_all")

    os.system(f"cp -r temp/server_decompiled/** .")
    os.system(f"git add .")
    os.system(f"git commit -m \"{target_version}\"")
    os.system(f"git push origin {target_version}_moj_all")

    return 0

def determine_latest_version():
    return "1.18.1"

def download_client(version):
    manifest_result = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    if manifest_result.status_code != 200:
        print(f"Error: Unable to fetch version manifest (status code: {manifest_result.status_code})")
        return False
    
    version_url = next(x['url'] for x in manifest_result.json()['versions'] if x['id'] == version)
    print(f"Downloading {version_url}")

    version_json_result = requests.get(version_url)
    if version_json_result.status_code != 200:
        print(f"Error: Unable to fetch version json (status code: {version_json_result.status_code})")
        return False
    
    version_json = version_json_result.json()

    server_jar_url = version_json['downloads']['server']['url']
    print(f"Downloading {server_jar_url}")
    files.download_file(server_jar_url, f"server.jar")

    server_mappings_url = version_json['downloads']['server_mappings']['url']
    print(f"Downloading {server_mappings_url}")
    files.download_file(server_mappings_url, f"server.txt")

    return True
    

if __name__ == '__main__':
    sys.exit(main())
