import os
import zipfile
import datetime
import shutil
import hashlib
from collections import defaultdict
from tkinter import Tk
from tkinter.filedialog import askdirectory


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
    # the os.walk function allows checking subdirectories too...
    for root, dirs, files in os.walk(path):
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
    os.chdir(path)  # just to be sure
    folder_name = os.path.basename(path)
    zipFileName = folder_name + '_' + datetime.datetime.now().strftime('%d-%m-%Y_%H-%M') + '.zip'
    print('Zipfilename: ' + zipFileName)
    os.chdir(downloadpath_yyy)

    for files in os.listdir(downloadpath_yyy):
        with zipfile.ZipFile(zipFileName, 'a', compression=zipfile.ZIP_DEFLATED) as down_zip:
            if folder_name+'_' not in files:
                print('\rPack to zip: ' + files, sep=' ', end='', flush=True)
                down_zip.write(files)
                os.remove(files)
    print()


if __name__ == '__main__':
    # path for start/download_dir
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    # show an "Open" dialog box and return the path to the selected file
    file_dir = askdirectory(title='Choose Downloadfolder')

    downloadpath_yyy = os.path.abspath(file_dir)
    os.chdir(downloadpath_yyy)

    rm_dup(downloadpath_yyy)  # removes duplicates in download
    print('DONE REMOVING DUPLICATES')

    pack_zip(downloadpath_yyy)  # packs remaining files in zip

    print('DONE PACKING TO ZIP')

    file_dir2 = askdirectory(title='Choose Backupfolder')
    targetpath_zzz = os.path.abspath(file_dir2)

    # lists to be moved files
    print('files to be moved to zzz: ' + str(os.listdir(downloadpath_yyy)))
    for file in os.listdir(downloadpath_yyy):
        # moves zip and remaining files to backup
        shutil.move(file, os.path.join(targetpath_zzz, file))
    print('DONE!')
