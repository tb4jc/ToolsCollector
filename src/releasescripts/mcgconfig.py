#
# Script for updating MCG Master configurations to new gien version.
#

from pathlib import *
import os
import fnmatch


root_dir = Path('/workspace/TWCS/03_mcg-dev/5_mcg-config/branches/RTC_CR_197559_TCNService_disabling')
rel_master_dir = Path('06_mcg_firmware_cfg/mcg_master_cfg')

workdir = root_dir.joinpath(rel_master_dir)

files_platform = workdir.glob('**/mcg_platform*.xml')
files_master = sorted(workdir.glob('**/mcg_master*.xml'))
files_ = workdir.glob('**/mcg_stand*.xml'))
print files

pass






