from __future__ import print_function

import sys
import os
from pathlib import Path
import subprocess

batch_files = str()

def init_globals():
    global batch_files
    root_dir, head = os.path.split(os.path.dirname(__file__))
    batch_files = os.path.join(root_dir, 'batch_files')


def handle_subprocess(checkout_params):
    result = 0
    err_msg = 'No error'
    try:
        err_msg = subprocess.check_output(checkout_params)
    except subprocess.CalledProcessError as e:
        print("Batch file execution failed with error %d, output = '%s'", e.returncode, e.output)
        result = e.returncode
        err_msg = e.output
    return result, err_msg


def create_pack_tags_from_branch(branch_version, tag_version):
    # root_dir, head = os.path.split(os.path.dirname(__file__))
    # batch_files = os.path.join(root_dir, 'batch_files')
    global batch_files
    batch_file = os.path.join(batch_files, 'create_pack_tag_from_branch.cmd')
    return handle_subprocess([batch_file, branch_version, tag_version])


def copy_fw_to_install_dir(repo_version, inst_version, inst_dir):
    # could use shutil.copytree function or call batch file
    # copy_batch_file = 'c:/Users/Thomas/Development/python/ToolsCollector/src/batch_files/copy_fw_to_inst.cmd '
    # root_dir, head = os.path.split(os.path.dirname(__file__))
    # batch_files = os.path.join(root_dir, 'batch_files')
    global batch_files
    batch_file = os.path.join(batch_files, 'copy_fw_to_inst.cmd')
    return handle_subprocess([batch_file,  repo_version, inst_version, inst_dir])


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
