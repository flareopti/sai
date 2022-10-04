#!/bin/python3

import requests
import re
import subprocess
import json
import os
import tarfile
import pprint
import argparse
import shutil

def patch(links,link):
    if len(links[link]['patches']) != 0:
        for patch in links[link]['patches']:
            filename = re.split(r'/', patch)[-1]
            if os.path.exists(patch):
                shutil.copyfile(patch, f'{os.getcwd()}/{filename}')
            else:
                response = requests.get(patch)
                open(filename, 'wb').write(response.content)
            subprocess.check_call(['sh', '-c', f'patch < {filename}'])

def download(links,link):
        filename = re.split(r'/',links[link]['programme'])[-1]
        extension = re.split(r'\.',filename)[-1]

        os.mkdir(link)
        os.chdir(link)
        
        if os.path.exists(links[link]['programme']):
            os.replace(link,f'{maindir}/{filename}')
        if extension != 'gz':
            print(link,os.getcwd())
            subprocess.check_call(['git','clone',links[link]['programme']])
        else:
            response = requests.get(links[link]['programme'])
            open(filename,"wb").write(response.content)
            with tarfile.open(filename) as tar:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar)


def setup(links, action):

    if action == 'print':
        pprint.pprint(links)


    for link in links:
        os.chdir(maindir)

        if action == 'download' or action == 'setup':
            download(links,link)
        else:
            os.chdir(link)

        directory = os.listdir()
        directory = [i for i in directory if os.path.isdir(i)]
        os.chdir(directory[0])
        
        if action == 'install_patches' or action == 'setup':
            patch(links,link)

        if action == 'build':
            subprocess.call(['make'])

        if action == 'install' or action == 'setup':
            subprocess.call(['sudo', 'make', 'install'])

        if action == 'uninstall':
            subprocess.call(['make', 'uninstall'])

        if action == 'full_remove':
            os.chdir(maindir)
            shutil.rmtree(link)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'Success at {action}!')



if __name__ == '__main__':
    with open('links.json', 'r') as file:
        links = json.load(file)

    maindir = os.getcwd()

    parser = argparse.ArgumentParser(description="Auto-build and install suckless software")
    parser.add_argument('-d','--download', action='store_true', help='Only Download')
    parser.add_argument('-b','--build', action='store_true', help='Only build')
    parser.add_argument('-iP','--install-patches', action='store_true', help='Only apply patches')
    parser.add_argument('-i','--install', action='store_true', help='Build and install')
    parser.add_argument('-S','--setup', action='store_true', help='Download and install everything')
    parser.add_argument('-u','--uninstall', action='store_true', help='Remove installed programmes from system')
    parser.add_argument('-fR', '--full-remove', action='store_true', help='Remove all downloaded files')
    parser.add_argument('-p','--print', action='store_true', help='Print all links')
    args = parser.parse_args()

    action = [i[0] for i in args._get_kwargs() if i[1]][0]
    
    setup(links,action) 

