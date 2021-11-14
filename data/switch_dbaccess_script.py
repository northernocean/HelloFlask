import shutil
import os
from datetime import datetime

# this is a utility script that can be run directly as a python
# file for copying a given dbaccess file into the project root
# as dbaccess.py. In order to avoid losing any changes that might
# have been made directly in the current dbacccess.py file, it
# also is set up to create backups of that file before replacing
# it with the new version from this folder.

# Setup
root_dir = '/home/david/bootcamp/repos/HelloFlask'
backup_current_dbaccess = True
dbaccess_option = 4

# dbaccess file options
dbaccess_options = {
    1: 'postgres',
    2: 'sqlite',
    3: 'github_content_csv',
    4: 'github_content_json'
}

# Copy desired dbaccess file to root of directory. Optionally, backup the current one in use 
src = os.path.join(root_dir, 'data', 'dbaccess_' + dbaccess_options[dbaccess_option] + '.py')
dst = os.path.join(root_dir, 'dbaccess.py')
bak = os.path.join(root_dir, 'local', 'dbaccess_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.py')
if backup_current_dbaccess:
    shutil.copy(dst, bak)
shutil.copy(src, dst)