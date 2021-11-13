import shutil
import os
from pathlib import Path
from datetime import datetime

root_dir = '/home/david/bootcamp/repos/HelloFlask'

dbaccess_dict = {
    1: 'postgres_heroku',
    2: 'sqlite'
}

db_source_id = 2

f_src = os.path.join(root_dir, 'data', 'dbaccess_' + dbaccess_dict[db_source_id] + '.py')
f_dst = os.path.join(root_dir, 'dbaccess.py')
f_bak = os.path.join(root_dir, 'local', 'dbaccess_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.py')
shutil.copy(f_dst, f_bak)
shutil.copy(f_src, f_dst)