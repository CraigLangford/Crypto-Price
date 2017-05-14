import os
from subprocess import call
import shutil

BOLD = '\033[1m'


if __name__ == '__main__':
    """
    Running `python setup.py` will generate a cryptoprice.zip file which can
    be uploaded to the AWS Lambda website and be used as a fully functioning
    lambda function.
    """
    # Include requests folder for distribution
    call(['pip', 'install', 'requests', '-t', '.'])

    # Place cryptoprice.py, data and requests into zip_folder
    print("Adding contents to zip folder")
    os.mkdir('zip_folder')
    call(['cp', 'cryptoprice.py', 'zip_folder/'])
    call(['cp', '-rf', 'data/', 'zip_folder/data/'])
    call(['cp', '-rf', 'requests/', 'zip_folder/requests/'])

    # Zip contents of zip_folder
    print("Zipping contents")
    shutil.make_archive('cryptoprice', 'zip', 'zip_folder')

    # Remove folders used to create zip
    print("Removing unneeded files")
    call(['rm', '-rf', 'zip_folder'])
    for node in os.listdir():
        if node.startswith('requests') or node == 'zip_folder':
            shutil.rmtree(node)

    print(BOLD + "cryptoprice.zip is now created - upload this to AWS Lambda"
          + BOLD)
