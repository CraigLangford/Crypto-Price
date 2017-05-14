import os
from subprocess import call
import shutil

BOLD = '\033[1m'


if __name__ == '__main__':
    """
    Running `python3 setup.py` will generate a cryptoprice.zip file which can
    be uploaded to the AWS Lambda website and be used as a fully functioning
    lambda function.
    """
    # 1. Include requests folder for distribution
    call(['pip', 'install', 'requests', '-t', '.'])

    # 2. Zip cryptoprice.py, requests/ and data/ into cryptoprice.zip
    print("Adding contents to zip folder")
    os.mkdir('zip_folder')
    call(['cp', 'cryptoprice.py', 'zip_folder/'])
    call(['cp', '-rf', 'data/', 'zip_folder/data/'])
    call(['cp', '-rf', 'requests/', 'zip_folder/requests/'])
    print("Zipping contents")
    shutil.make_archive('cryptoprice', 'zip', 'zip_folder')

    # 3. Remove requests folders.
    print("Removing unneeded files")
    call(['rm', '-rf', 'zip_folder'])
    for node in os.listdir():
        if node.startswith('requests'):
            shutil.rmtree(node)

    print(BOLD + "cryptoprice.zip is now created - upload this to AWS Lambda"
          + BOLD)
