#
# Script for updating MCG Master configurations to new gien version.
#

import fileinput
import string
import sys
from pathlib import *
from filesearch import replace_in_files

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


def update_platform_xml(new_firmware_version):
    # root_dir = Path('/workspace/TWCS/03_mcg-dev/5_mcg-config/branches/RTC_CR_197559_TCNService_disabling')
    root_dir = Path("c:\Users\Thomas\Development\python\ToolsCollector\src")
    # rel_master_dir = Path('06_mcg_firmware_cfg/mcg_master_cfg')
    rel_master_dir = Path("__testdir\mcg_master_cfg")

    workdir = root_dir.joinpath(rel_master_dir)

    version_nrtos1 = '3.22.2.0'
    version_vrue = version_nrtos1.split('.')
    version_nrtos2 = '4.%s.%s.%s' % (version_vrue[1], version_vrue[1], version_vrue[3])
    version_nrtos4 = '4.%s.%s.%s' % (version_vrue[1], version_vrue[1], version_vrue[3])
    version_rub = version_nrtos1[version_nrtos1.find('.'):]

    # replace mcg platform version
    search_data = [('**/mcg_platform', '<SciMdluName>0000-mcg_stand_nrt1', '3'),
                   ('**/mcg2_platform', '<SciMdluName>0000-mcg_stand_nrt2', '4'),
                   ('**/mcg4_platform', '<SciMdluName>0000-mcg_stand_nrt4', '5')]

    for glob_pattern, stext, version_start in search_data:
        full_version = version_start + "." + version_rub

        files_platform = [str(f) for f in workdir.glob(glob_pattern)]
        replace_in_next_line = False
        for line in fileinput.input(files_platform, inplace=1):
            lineno = string.find(line, stext)
            if lineno > 0:
                replace_in_next_line = True
            if replace_in_next_line:
                new_line_start = line[line.find('>'):]
                new_line_end = line[line.rfind('<'):]
                ine = new_line_start + full_version + new_line_end
                replace_in_next_line = False

            sys.stdout.write(line)

    files_master = list(workdir.glob('**/mcg_master*.xml'))
    files_stand = list(workdir.glob('**/0000-mcg_stand*.xml'))
    files = [files_platform, files_master, files_stand]
    print files

    pass


if __name__ == "__main__":
    update_platform_xml('3.22.1.0')





