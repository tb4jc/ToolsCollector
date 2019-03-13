#
# Script for updating MCG Pack configurations to new given versions.
#

from __future__ import print_function

import fileinput
import sys
import os
from pathlib import *


def update_device_pack_inc_file(file_path, fw_version_dic):
    result = True
    err_msg = 'No Error'
    version_rub = '%s.%s.%s\n' % (fw_version_dic['revision'], fw_version_dic['update'], fw_version_dic['build'])
    counter = 0
    for line in fileinput.input([file_path], inplace=1):
        counter += 1
        idx_in_line = line.find('SCI1VERSION')
        if idx_in_line >= 0:
            new_line_start = line[:line.find('.')+1]
            line = new_line_start + version_rub
        sys.stdout.write(line)
    if counter == 0:
        result = False
        err_msg = "Empty file"
    return result, err_msg


def update_versions_inc_file(file_path, version_dic):
    result = True
    err_msg = 'No Error'
    counter = 0
    for line in fileinput.input([file_path], inplace=1):
        counter += 1
        idx_in_line = line.find('nrtos_prod_base')
        if idx_in_line >= 0:
            line = 'nrtos_prod_base/' + version_dic['prod_base']['full'] + '\n'
        else:
            idx_in_line = line.find('mcg_firmware')
            if idx_in_line >= 0:
                line = 'mcg_firmware/' + version_dic['fw']['full'] + '\n'
            else:
                idx_in_line = line.find('mcg_config/')
                if idx_in_line >= 0:
                    line = 'mcg_config/' + version_dic['cfg']['full'] + '\n'
        sys.stdout.write(line)
    if counter == 0:
        result = False
        err_msg = "Empty file"
    return result, err_msg


def update_target(target_dir, versions_dic):
    result = True
    err_msg = 'No error'
    for root_dir, dirs, files in os.walk(target_dir, topdown=True):
        for name in files:
            if name == 'versions.inc':
                file_path = os.path.join(root_dir, name)
                result, err_msg = update_versions_inc_file(file_path, versions_dic)
                pass
            elif name == 'device_pack.inc':
                file_path = os.path.join(root_dir, name)
                result, err_msg = update_device_pack_inc_file(file_path, versions_dic['fw'])
            if not result:
                break
        if not result:
            break
    return result, err_msg

def update_pack_files(package_dir, version_dic):
    result = True
    err_msg = "No error"

    fw_split = version_dic['fw'].split('.')
    fw_dic = {'full': version_dic['fw'], 'version': fw_split[0], 'revision': fw_split[1], 'update': fw_split[2], 'build': fw_split[3]}
    cfg_split = version_dic['cfg'].split('.')
    cfg_dic = {'full': version_dic['cfg'], 'version': cfg_split[0], 'revision': cfg_split[1], 'update': cfg_split[2], 'build': cfg_split[3]}
    prod_base_version_split = version_dic['prod_base'].split('.')
    prod_base_dic = {'full': version_dic['prod_base'], 'version': prod_base_version_split[0], 'revision': fw_split[1], 'update': fw_split[2], 'build': prod_base_version_split[3]}
    versions_dic = {'fw': fw_dic, 'cfg': cfg_dic, 'prod_base': prod_base_dic}

    mcg_base_dir = os.path.join(package_dir, 'mcg')
    result, err_msg = update_target(mcg_base_dir, versions_dic)
    if result:
        mcg2_base_dir = os.path.join(package_dir, 'mcg2')
        result, err_msg = update_target(mcg2_base_dir, versions_dic)
        if result:
            nrtos4_base_dir = os.path.join(package_dir, 'nrtos4')
            result, err_msg = update_target(nrtos4_base_dir, versions_dic)

    return result, err_msg


if __name__ == "__main__":
    pack_dir = Path('c:\\Users\Thomas\Development\python\ToolsCollector\src\__mcg_pack')
    version_dic = {'fw': '3.22.0.1', 'cfg': '3.22.0.0', 'prod_base': '3.22.0.3'}
    result, err_msg = update_pack_files(str(pack_dir), version_dic)
    print(result)
    print(err_msg)







