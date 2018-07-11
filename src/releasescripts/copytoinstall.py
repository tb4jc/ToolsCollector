from __future__ import print_function

import sys
import os
from pathlib import Path
import subprocess


def copy_fw_to_install_dir(repo_version, inst_version, inst_dir):
    # could use shutil.copytree function or call batch file
    result = 0
    err_msg = 'No error'
    copy_batch_file = 'c:/Users/Thomas/Development/python/ToolsCollector/src/batch_files/copy_fw_to_inst.cmd '
    try:
        err_msg = subprocess.check_output([copy_batch_file, repo_version, inst_version, inst_dir])
    except subprocess.CalledProcessError as e:
        print("Batch file execution failed with error %d, output = '%s'", e.returncode, e.output)
        result = e.returncode
        err_msg = e.output
    return result, err_msg


if __name__ == "__main__":
    install_dir = Path('c:/Users/Thomas/Development/python/ToolsCollector/src/__mcg_inst_dir')
    mcgfw_repo_version = '3.23.0.99'
    mcgfw_repo_version = '1.2.3.4'
    mcgfw_inst_version = '3.23.0'
    result, err_msg = copy_fw_to_install_dir(mcgfw_repo_version, mcgfw_inst_version, str(install_dir))
    if result == 0:
        print("Batch file finished with result '%s'" % err_msg)
    else:
        print("Batch file failed with error %d and err_msg '%s'" % (result, err_msg))
