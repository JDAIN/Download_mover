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
            # skips currently downloading files
            if filename.endswith(".crdownload"):
                continue

            filepath = os.path.join(root, filename)
            print('\rReading: ' + filename, sep=' ', end='\t\t\t\t\t\t\t', flush=True)

            file_md5 = md5(filepath)
            md5_dict[file_md5].append(filepath)

    for key in md5_dict:
        file_list = md5_dict[key]
        while len(file_list) > 1:
            item = file_list.pop()
            os.remove(item)
            print('\rRemoved: ' + item, sep=' ', end='\t\t\t\t\t\t\t', flush=True)
    print()


def pack_zip(path):
    # print(os.getcwd())
    zip_file_name = 'downloadsYYY_' + datetime.datetime.now().strftime('%d-%m-%Y_%H_%M') + '.zip'
    print('Zipfilename: ' + zip_file_name + "\n")
    os.chdir(downloadpath_yyy)
    # print(os.getcwd())
    for files in os.listdir(downloadpath_yyy):
        # skips currently downloading files
        if files.endswith(".crdownload"):
            continue
        # print(files)
        files = os.path.join(downloadpath_yyy, files)
        # print(files)
        with zipfile.ZipFile(zip_file_name, 'a', compression=zipfile.ZIP_DEFLATED) as down_zip:
            if 'downloadsYYY_' not in files:
                print('\rPack to zip: ' + files, sep=' ', end='\t\t\t\t\t', flush=True)

                if os.path.isdir(files):
                    for f in os.listdir(files):
                        down_zip.write(os.path.join(files, f))
                        os.remove(os.path.join(files, f))

                    os.rmdir(files)  # deletes empty folder after files have been removed
                else:
                    down_zip.write(files)
                    os.remove(files)


if __name__ == '__main__':
    # path for start/download_dir
    downloadpath_yyy = os.path.abspath(r'Y:\downloads')
    # path for target dir
    targetpath_zzz = os.path.abspath(r'Z:\Backup\downloadsBackup')
    os.chdir(downloadpath_yyy)  # changed cwd to download_dir
    rm_dup(downloadpath_yyy)  # removes duplicates in download
    print('DONE REMOVING DUPLICATES')

    # print(os.listdir(downloadpath_yyy))
    pack_zip(downloadpath_yyy)  # packs remaining files in zip
    # print(os.getcwd())
    print('\nDONE PACKING TO ZIP')

    print('files to be moved to zzz: ' + ', '.join(os.listdir(downloadpath_yyy)))  # lists to be moved files
    for file in os.listdir(downloadpath_yyy):
        shutil.move(file, os.path.join(targetpath_zzz, file))  # moves zip and remaining files to backup
    print('DONE!')
