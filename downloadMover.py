import os
import zipfile
import datetime
import shutil
import hashlib
from collections import defaultdict


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def rm_dup(path):
    """relies on the md5 function above to remove duplicate files"""
    if not os.path.isdir(path):  # make sure the given directory exists
        print('specified directory does not exist!')
        return

    md5_dict = defaultdict(list)
    for root, dirs, files in os.walk(path):  # the os.walk function allows checking subdirectories too...
        for filename in files:
            print('\rReading: ' + filename, sep=' ', end='', flush=True)
            filepath = os.path.join(root, filename)
            file_md5 = md5(filename)
            md5_dict[file_md5].append(filepath)

    for key in md5_dict:
        file_list = md5_dict[key]
        while len(file_list) > 1:
            item = file_list.pop()
            os.remove(item)
            print('\rRemoved: ' + item, sep=' ', end='', flush=True)
    print()


def pack_zip(path):
    #print(os.getcwd())
    zipFileName = 'downloadsYYY_' + datetime.datetime.now().strftime('%d-%m-%Y_%H_%M') + '.zip'
    print('Zipfilename: ' +zipFileName)
    os.chdir(downloadpath_yyy)
    #print(os.getcwd())
    for files in os.listdir(downloadpath_yyy):
        # print(files)
        # files = os.path.join(downloadpath_yyy, files)
        # print(files)
        with zipfile.ZipFile(zipFileName, 'a', compression=zipfile.ZIP_DEFLATED) as down_zip:
            if 'downloadsYYY_' not in files:
                print('\rPack to zip: '+files , sep=' ', end='', flush=True)
                down_zip.write(files)
                os.remove(files)
    print()



if __name__ == '__main__':
    #path for start/download_dir
    downloadpath_yyy = os.path.abspath(r'Y:\downloads')
    #path for target dir
    targetpath_zzz = os.path.abspath(r'Z:\downloadsBackup')
    os.chdir(downloadpath_yyy) #changed cwd to download_dir
    rm_dup(downloadpath_yyy)  # removes duplicates in download
    print('DONE REMOVING DUPLICATES')

    #print(os.listdir(downloadpath_yyy))
    pack_zip(downloadpath_yyy) # packs remaining files in zip
    #print(os.getcwd())
    print('DONE PACKING TO ZIP')

    print('files to be moved to zzz: ' + str(os.listdir(downloadpath_yyy))) #lists to be moved files
    for file in os.listdir(downloadpath_yyy):
        shutil.move(file, os.path.join(targetpath_zzz, file)) #moves zip and remaining files to backup
    print('DONE!')
