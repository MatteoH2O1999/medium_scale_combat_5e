import os
import shutil
from os.path import dirname, join
from zipfile import ZipFile

rootdir = dirname(dirname(dirname(__file__)))
uploaddir = join(rootdir, 'to_upload')
distdir = join(rootdir, 'dist')

if os.path.exists(uploaddir):
    print(f'{uploaddir} already exists')
    shutil.rmtree(uploaddir)
    print(f'{uploaddir} removed')
os.mkdir(uploaddir)

for folder in os.listdir(distdir):
    folder_path = join(distdir, folder)
    zip_path = join(uploaddir, f'{folder}.zip')
    print(f'Zipping content of folder {folder_path} to {zip_path}...')
    with ZipFile(zip_path, 'w') as zip_file:
        for path, dirnames, filenames in os.walk(folder_path):
            for file in filenames:
                filepath = join(path, file)
                archive_path = os.path.relpath(filepath, folder_path)
                print(f'Processing file {filepath} to archive path {archive_path}')
                zip_file.write(filepath, archive_path)
