#!/usr/bin/python3

import os
import shutil
import subprocess
import sys


TEST_IMAGE = 'sample_image.jffs2'
TEST_DIR = 'test'

FILES = {'a': b'1\n',
         'b': b'2\n',
         'output': b'\xff' * 5000}

DIRS = ['f']


def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(base_dir)
    shutil.rmtree(TEST_DIR, ignore_errors=True)
    ret = 0
    try:
        runcmd = ['./jffs2extract', '-f', TEST_IMAGE, '-d', TEST_DIR]
        print(*runcmd)
        retcode = subprocess.call(runcmd)
        if retcode:
            print(f'jffs2extract failed with return code {retcode} !')
            ret = 1

        if not os.path.isdir(TEST_DIR):
            print(f'Output directory "{TEST_DIR}" was not created!')
            return 1

        os.chdir(TEST_DIR)

        for fn, content in FILES.items():
            if not os.path.isfile(fn):
                ret = 1
                print(f'File "{fn} does not exist!')
                continue

            with open(fn, 'rb') as f:
                if f.read() != content:
                    ret = 1
                    print(f'Content of "{fn}" is wrong!')

        for d in DIRS:
            if not os.path.isdir(d):
                ret = 1
                print(f'Directory "{d}" does not exist!')

        dirlist = set(FILES).union(DIRS)
        for fn in os.listdir():
            if fn not in dirlist:
                ret = 1
                print(f'Unknown file/dir "{fn}"!')
    except Exception as e:
        print(f'Exception in test! {e.__class__.__name__}: {e}')
        ret = 1
    finally:
        os.chdir(base_dir)
        shutil.rmtree(TEST_DIR, ignore_errors=True)

    if not ret:
        print(f'All tests passed!')

    return ret


if __name__ == '__main__':
    sys.exit(main())
