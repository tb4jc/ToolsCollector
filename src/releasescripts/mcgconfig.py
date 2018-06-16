#
# Script for updating MCG Master configurations to new gien version.
#

import fileinput
import string
import sys
from pathlib import *
from filesearch import replace_in_files, find_files


def update_master_xml(file_name, old_firmware_version, new_firmware_version):
    old_fw_version_vrue = old_firmware_version.split('.')
    new_fw_version_vrue = new_firmware_version.split('.')
    search_string = '''<Release>%s</Release>
                <Update>%s</Update>
                <Evolution>%s</Evolution>''' % (old_fw_version_vrue[1], old_fw_version_vrue[2], old_fw_version_vrue[3])
    replace_string = '''<Release>22</Release>
                <Update>0</Update>
                <Evolution>2</Evolution>''' % (new_fw_version_vrue[1], new_fw_version_vrue[2], new_fw_version_vrue[3])
    changed_files = replace_in_files(search_string, replace_string, 'mcg_master.*\.xml')
    pass


def update_platform_xml(top_dir, new_firmware_version):
    result = True
    err_msg = 'No Error'
    root_dir = Path(top_dir)
    rel_master_dir = Path('06_mcg_firmware/mcg_master_cfg')
    work_dir = root_dir.joinpath(rel_master_dir)

    version_nrtos1 = new_firmware_version
    version_vrue = version_nrtos1.split('.')
    release_val = version_vrue[1]
    update_val = version_vrue[2]
    evolution_val = version_vrue[3]
    version_nrtos2 = '4.%s.%s.%s' % (release_val, update_val, evolution_val)
    version_nrtos4 = '4.%s.%s.%s' % (release_val, update_val, evolution_val)
    version_rub = version_nrtos1[version_nrtos1.find('.'):]

    # update mcg platform files
    search_data = { 'mcg_platform_BT.xml' : '3', 'mcg2_platform_BT.xml' : '4', 'mcg4_platform_BT.xml' : '5'}
    platform_files = find_files(str(work_dir), '.*mcg.?_platform.*\.xml')
    for file_path, file_name in platform_files:
        print "File = %s\n" % file_name
        # for each platform master, search version line
        full_version = search_data[file_name] + version_rub
        platform_files_input_obj = fileinput.input([file_path], inplace=1)
        for line in platform_files_input_obj:
            lineno = string.find(line, '<SciMdluName>0000-mcg_stand_nrt')
            if lineno > 0:
                # write current line then get next line
                sys.stdout.write(line)
                line = platform_files_input_obj.readline()
                new_line_start = line[:line.find('>')+1]
                new_line_end = line[line.rfind('<'):]
                line = new_line_start + full_version + new_line_end
            sys.stdout.write(line)

    master_files = find_files(str(work_dir), '.*mcg_(stand|master).*\.xml')
    search_list = ['0000-mcg_base', '0000-mcg_framewrk', '0000-mcg_services']
    for file_path, file_name in master_files:
        print "File = %s\n" % file_name
        file_input_obj = fileinput.input([file_path], inplace=1)
        for line in file_input_obj:
            # for each mcg master, search line with DLU name matching any of search_list
            for key in search_list:
                idx = string.find(line, key)
                if idx > 0:
                    sys.stdout.write(line)
                    # write next four lines to file then replace with new release, update and evolution
                    for counter in range(0, 3, 1):
                        sys.stdout.write(file_input_obj.readline())
                    file_input_obj.readline()
                    sys.stdout.write('                <Release>%s</Release>\n' % release_val)
                    file_input_obj.readline()
                    sys.stdout.write('                <Update>%s</Update>\n' % update_val)
                    file_input_obj.readline()
                    sys.stdout.write('                <Evolution>%s</Evolution>\n' % evolution_val)
                    line = file_input_obj.readline()
                    break
            sys.stdout.write(line)

    # files_master = list(work_dir.glob('**/mcg_master*.xml'))
    # files_stand = list(work_dir.glob('**/0000-mcg_stand*.xml'))
    # files = [files_master, files_stand]

    return result, err_msg


def update_mcg_master_files(top_dir, new_version):
    result = True
    err_msg = "No error"
    # result, errMsg = update_master_xml()
    result, err_msg = update_platform_xml(top_dir, new_version)
    return result, err_msg


if __name__ == "__main__":
    update_platform_xml('3.22.1.0')





