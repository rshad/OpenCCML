#!C:\Users\rashz\PycharmProjects\Openstack-Virtualization-TFG\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'client==0.0.1','console_scripts','client'
__requires__ = 'client==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('client==0.0.1', 'console_scripts', 'client')()
    )
