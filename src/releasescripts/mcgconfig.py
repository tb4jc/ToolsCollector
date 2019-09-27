#
# Script for updating MCG Master configurations to new given version.
#
# Version 1.0.1.0
#

import fileinput
import sys
import os
from filesearch import find_files, dos_2_unix


def update_master_xml(work_dir, version_dic):
    result = True
    err_msg = 'No Error'
    master_files = find_files(work_dir, '.*mcg_(stand|master).*\.xml')
    search_list = ['0000-mcg_base', '0000-mcg_framewrk', '0000-mcg_services']
    for file_path, file_name in master_files:
        file_input_obj = fileinput.input([file_path], inplace=1, mode='rb')
        for line_ba in file_input_obj:
            # for each mcg master, search line with DLU name matching any of search_list
            line = line_ba.decode()
            for key in search_list:
                idx = line.find(key)
                if idx > 0:
                    sys.stdout.write(line)
                    # write next four lines to file then replace with new release, update and evolution
                    for counter in range(0, 3, 1):
                        line = file_input_obj.readline().decode()
                        sys.stdout.write(line)
                    file_input_obj.readline()
                    sys.stdout.write('                <Release>%s</Release>\n' % version_dic['release'])
                    file_input_obj.readline()
                    sys.stdout.write('                <Update>%s</Update>\n' % version_dic['update'])
                    file_input_obj.readline()
                    sys.stdout.write('                <Evolution>%s</Evolution>\n' % version_dic['evolution'])
                    line = file_input_obj.readline().decode()
                    break
            sys.stdout.write(line)
        file_input_obj.close()
        dos_2_unix(file_path)
    return result, err_msg


def update_platform_xml(work_dir, version_dic):
    result = True
    err_msg = 'No Error'
    version_rub = '.%s.%s.%s' % (version_dic['release'], version_dic['update'], version_dic['evolution'])

    # update mcg platform files
    search_data = {'mcg_platform_BT.xml': '3', 'mcg2_platform_BT.xml': '4', 'mcg4_platform_BT.xml': '5', 'mcg4x86_platform_BT.xml': '6'}
    platform_files = find_files(work_dir, '.*mcg.?_platform.*\.xml')
    for file_path, file_name in platform_files:
        # for each platform master, search version line
        full_version = search_data[file_name] + version_rub
        platform_files_input_obj = fileinput.input([file_path], inplace=1)
        for line_ba in platform_files_input_obj:
            # line = line_ba.decode()
            line = line_ba
            idx_in_line = line.find('<SciMdluName>0000-mcg_stand_nrt')
            if idx_in_line > 0:
                # write current line then get next line
                sys.stdout.write(line)
                # line = platform_files_input_obj.readline().decode()
                line = platform_files_input_obj.readline()
                new_line_start = line[:line.find('>')+1]
                new_line_end = line[line.rfind('<'):]
                line = new_line_start + full_version + new_line_end
            sys.stdout.write(line)
    return result, err_msg


def update_mcg_master_files(top_dir, new_version):
    result = True
    err_msg = "No error"
    mcg_master_dir = os.path.join(top_dir, '06_mcg_firmware_cfg/mcg_master_cfg')
    version_vrue = new_version.split('.')
    version_dic = {'release': version_vrue[1],
                   'update': version_vrue[2],
                   'evolution': version_vrue[3]}
    result, err_msg = update_master_xml(str(mcg_master_dir), version_dic)
    if result:
        result, err_msg = update_platform_xml(mcg_master_dir, version_dic)
    return result, err_msg


if __name__ == "__main__":
    update_platform_xml('3.22.1.0')





