#
# Script for updating MCG Firmware to new given version.
#

from pathlib import *


def update_mcg_fw_versions(top_dir, new_version):
    err_msg = "No error"
    mcg_fw_version_files = ['mcgbase/McgBase/version_file', 'mcgframework/McgFramework/version_file', 'mcgservices/McgServices/version_file']
    new_version_vrue = new_version.split('.')
    new_version_file_content = 'version="%s"\nrelease="%s"\nupdate="%s"\nevolution="%s"\n' % (new_version_vrue[0], new_version_vrue[1], new_version_vrue[2], new_version_vrue[3])
    new_build_ver = 'version=\"' + new_version + '\"'
    bld_ver_path = top_dir / 'bld/build.ver'
    if bld_ver_path.parent.exists():
        out_file = open(str(bld_ver_path), 'w')
        out_file.write(new_build_ver)
        out_file.close()
    else:
        err_msg = 'File path %s is invalid/doesn\'t exist - please check' % str(bld_ver_path.parent)
        return False, err_msg
    for f in mcg_fw_version_files:
        file_path = top_dir / f
        parent_dir = file_path.parent
        if parent_dir.exists():
            outfile = open(str(file_path), 'w')
            outfile.write(new_version_file_content)
            outfile.close()
        else:
            err_msg = 'File path %s is invalid/doesn\'t exist - please check' % str(parent_dir)
            return False, err_msg
    return True, err_msg


if __name__ == "__main__":
    test_dir = Path('c:\\Users\Thomas\Development\python\ToolsCollector\src\__mcg_firmware')
    if update_mcg_fw_versions(test_dir, '3.22.1.0'):
        print("Files created")
    else:
        print("Error occurred")
