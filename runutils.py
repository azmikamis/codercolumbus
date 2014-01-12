import sys
from os.path import join, abspath


def fix_sys_path():
    sys.path.insert(0, join(abspath('.'), 'lib'))