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
        err_msg = subprocess.check_output(checkout_params, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("Batch file execution failed with error %d, output = '%s'" % (e.returncode, e.output))
        result = e.returncode
        err_msg = e.output
    return result, err_msg.decode()


def create_pack_tags_from_branch(branch_version, tag_version):
    global batch_files
    if batch_files == "":
        init_globals()
    batch_file = os.path.join(batch_files, 'create_pack_tag_from_branch.cmd')
    ret_value = handle_subprocess([batch_file, "-b", branch_version, "-t", tag_version])
    return ret_value


def copy_fw_to_install_dir(repo_version, inst_version, inst_dir):
    # could use shutil.copytree function or call batch file
    global batch_files
    if batch_files == "":
        init_globals()
    batch_file = os.path.join(batch_files, 'copy_fw_to_inst.cmd')
    cmd_list = [batch_file, "-s", repo_version, "-d", inst_version]
    if inst_dir != "":
        cmd_list.append("-p")
        cmd_list.append(inst_dir)
    ret_value = handle_subprocess(cmd_list)
    return ret_value


if __name__ == "__main__":
    init_globals()
    print("batch_files = %s" % batch_files)
    install_dir = Path('c:/Users/Thomas/Development/python/ToolsCollector/src/__mcg_inst_dir')
    mcgfw_repo_version = '3.23.0.99'
    mcgfw_repo_version = '1.2.3.4'
    mcgfw_inst_version = '3.23.0'
    l_result, l_err_msg = copy_fw_to_install_dir(mcgfw_repo_version, mcgfw_inst_version, str(install_dir))
    if l_result == 0:
        print("Batch file finished with result '%s'" % l_err_msg)
    # error already printed in handle_subprocess() function
