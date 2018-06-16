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
    # root_dir = Path('/workspace/TWCS/03_mcg-dev/5_mcg-config/branches/RTC_CR_197559_TCNService_disabling')
    root_dir = Path(top_dir)
    rel_master_dir = Path('06_mcg_firmware/mcg_master_cfg')
    # rel_master_dir = Path("__testdir\mcg_master_cfg")

    work_dir = root_dir.joinpath(rel_master_dir)

    # version_nrtos1 = '3.22.2.0'
    version_nrtos1 = new_firmware_version
    version_vrue = version_nrtos1.split('.')
    version_nrtos2 = '4.%s.%s.%s' % (version_vrue[1], version_vrue[1], version_vrue[3])
    version_nrtos4 = '4.%s.%s.%s' % (version_vrue[1], version_vrue[1], version_vrue[3])
    version_rub = version_nrtos1[version_nrtos1.find('.'):]

    # replace mcg platform version
    search_data = { 'mcg_platform_BT.xml' : '3', 'mcg2_platform_BT.xml' : '4', 'mcg4_platform_BT.xml' : '5'}
    files_found = find_files(str(work_dir), '.*mcg.?_platform.*\.xml')
    for file_path, file_name in files_found:
        print "File = %s\n" % file_name
        # for each platform master, search version line
        full_version = search_data[file_name] + version_rub
        replace_in_next_line = False
        for line in fileinput.input([file_path], inplace=1):
            lineno = string.find(line, '<SciMdluName>0000-mcg_stand_nrt')
            if lineno > 0:
                replace_in_next_line = True
            elif replace_in_next_line:
                new_line_start = line[line.find('>'):]
                new_line_end = line[line.rfind('<'):]
                line = new_line_start + full_version + new_line_end
                replace_in_next_line = False
            sys.stdout.write(line)

    # for glob_pattern, stext, version_start in search_data:
    #     full_version = version_start + "." + version_rub
    #
    #     for f in work_dir.glob(glob_pattern):
    #         print f
    #
    #     pass
    #     files_platform = [str(f) for f in work_dir.glob(glob_pattern)]
    #     replace_in_next_line = False
    #     if not files_platform == []:
    #         for line in fileinput.input(files_platform, inplace=1):
    #             lineno = string.find(line, stext)
    #             if lineno > 0:
    #                 replace_in_next_line = True
    #             if replace_in_next_line:
    #                 new_line_start = line[line.find('>'):]
    #                 new_line_end = line[line.rfind('<'):]
    #                 ine = new_line_start + full_version + new_line_end
    #                 replace_in_next_line = False
    #
    #             sys.stdout.write(line)

    files_platform = [filename for path, filename in files_found]
    files_master = list(work_dir.glob('**/mcg_master*.xml'))
    files_stand = list(work_dir.glob('**/0000-mcg_stand*.xml'))
    files = [files_platform, files_master, files_stand]
    print files

    return result, err_msg


def update_mcg_master_files(top_dir, new_version):
    result = True
    err_msg = "No error"
    # result, errMsg = update_master_xml()
    result, err_msg = update_platform_xml(top_dir, new_version)
    return result, err_msg


if __name__ == "__main__":
    update_platform_xml('3.22.1.0')





