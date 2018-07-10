#
# Tools Collector which provides easy access to multiple tools developed
# during different actions.
#
from __future__ import print_function
import sys

if sys.version[0] == '2':
    from ConfigParser import ConfigParser, NoSectionError
else:
    from configparser import ConfigParser, NoSectionError


class TCConfig(object):
    TCC_CONFIGURATION = 0
    TCC_LAYOUT = 1
    TCC_MCG_FW_DIR_HIST = 2
    TCC_MCG_FW_VERS_HIST = 3
    TCC_MCG_CFG_DIR_HIST = 4
    TCC_MCG_CFG_VERS_HIST = 5
    TCC_MCG_PACK_DIR_HIST = 6
    TCC_PRODBASE_VERS_HIST = 7
    TCC_INST_DST_HIST = 8
    TCC_PACK_BRNCH_HIST = 9
    TCC_PACK_TAG_HIST = 10
    TCC_INST_SRC_HIST = 11
    TCC_INST_DST_HIST = 12
    TCC_INST_DIR_HIST = 13
    TCC_SECTION_NAMES = {
        TCC_CONFIGURATION:      'Configuration',
        TCC_LAYOUT:             'Layout',
        TCC_MCG_FW_DIR_HIST:    'McgFwDirHistory',
        TCC_MCG_FW_VERS_HIST:   'McgFwVersionHistory',
        TCC_MCG_CFG_DIR_HIST:   'McgCfgDirHistory',
        TCC_MCG_CFG_VERS_HIST:  'McgCfgVersionHistory',
        TCC_MCG_PACK_DIR_HIST:  'McgPackDirHistory',
        TCC_PRODBASE_VERS_HIST: 'ProdBaseVersionHistory',
        TCC_PACK_BRNCH_HIST:    'CreateMcgPackBranchHistory',
        TCC_PACK_TAG_HIST:      'CreateMcgPackTagHistory',
        TCC_INST_SRC_HIST:      'CopyToInstallSrcHistory',
        TCC_INST_DST_HIST:      'CopyToInstallDstHistory',
        TCC_INST_DIR_HIST:      'InstallDirHistory'
    }

    def __init__(self, config_file_name):
        # read ini file
        self.config_file_name = config_file_name
        self.config = ConfigParser()
        self.config.optionxform = str
        self.config.read(config_file_name)
        self.tc_config_meta = {
            self.TCC_MCG_FW_DIR_HIST:  {'max_options': 10},
            self.TCC_MCG_FW_VERS_HIST: {'max_options': 10},
            self.TCC_MCG_CFG_DIR_HIST:  {'max_options': 10},
            self.TCC_MCG_CFG_VERS_HIST: {'max_options': 10},
            self.TCC_MCG_PACK_DIR_HIST: {'max_options': 10},
            self.TCC_PRODBASE_VERS_HIST: {'max_options': 10},
            self.TCC_PACK_BRNCH_HIST: {'max_options': 10},
            self.TCC_PACK_TAG_HIST: {'max_options': 10},
            self.TCC_INST_SRC_HIST: {'max_options': 10},
            self.TCC_INST_DST_HIST: {'max_options': 10},
            self.TCC_INST_DIR_HIST: {'max_options': 10}
        }

    def saveConfig(self, config_file_name):
        # watch out, write expects file open as text file - not binary!!
        with open(config_file_name, 'w') as configfile:
            try:
                self.config.write(configfile)
            except:
                print('Unexpected error:', str(sys.exc_info()))

    def printOutConfig(self):
        for section_name in self.config.sections():
            print('Section:', section_name)
            print('  Options:', self.config.options(section_name))
            for name, value in self.config.items(section_name):
                print('  %s = %s' % (name, value))
            print()

    def getSectionValues(self, section_id):
        valueList = list()
        try:
            for name, value in self.config.items(self.TCC_SECTION_NAMES[section_id]):
                valueList.append(value)
        except NoSectionError:
            print('Section %s does not exists', self.TCC_SECTION_NAMES[section_id])
        except:
            print('Unexpected error:', sys.exc_info()[0])
        return valueList

    def getSectionFull(self, section_id):
        if section_id == TCConfig.TCC_LAYOUT:
            section_list = dict()
            try:
                for option_name, option_value in self.config.items(self.TCC_SECTION_NAMES[section_id]):
                    if option_name in ['geometry', 'state']:
                        section_list[option_name] = option_value
                    else:
                        section_list[option_name] = int(option_value)
            except NoSectionError:
                print('Section %s does not exists', self.TCC_SECTION_NAMES[section_id])
            except:
                print('Unexpected error:', sys.exc_info()[0])
        else:
            section_list = list()
            for option_name, option_value in self.config.items(self.TCC_SECTION_NAMES[section_id]):
                section_list.append((option_name, option_value))
        return section_list

    def updateSection(self, section_id, new_section_data):
        if section_id == TCConfig.TCC_LAYOUT:
            for option_name in new_section_data:
                try:
                    self.config.set(self.TCC_SECTION_NAMES[section_id], option_name, new_section_data[option_name])
                except NoSectionError:
                    print('Section %s does not exists', self.TCC_SECTION_NAMES[section_id])
                except:
                    print('Unexpected error:', sys.exc_info()[0])
        else:
            option_counter = 0
            max_options = self.tc_config_meta[section_id]['max_options']
            for data_value in new_section_data:
                self.config.set(self.TCC_SECTION_NAMES[section_id], str(option_counter), data_value)
                option_counter += 1
                if option_counter >= max_options:
                    break
                pass


if __name__ == "__main__":
    testConfig = TCConfig('toolscollector.ini')
    testConfig.printOutConfig()
    sectionID = TCConfig.TCC_MCG_FW_VERS_HIST

    sectionTouples = testConfig.getSectionFull(sectionID)
    print('Listing values of section %s' % TCConfig.TCC_SECTION_NAMES[sectionID])
    for option, value in sectionTouples:
        print("%s=%s" % (option, value))

    sectionValues = testConfig.getSectionValues(sectionID)
    print('Listing values of section %s' % TCConfig.TCC_SECTION_NAMES[sectionID])
    for value in sectionValues:
        print("value %s" % value)

    # create test elements
    sectionValues.insert(0, '3.22.0.x')
    sectionValues.insert(0, '5.22.0.x')
    sectionValues.insert(0, '4.22.0.x')
    sectionValues.insert(0, '2.22.0.x')
    sectionValues.insert(0, '2.21.0.x')
    sectionValues.insert(0, '2.20.0.x')

    testConfig.updateSection(sectionID, sectionValues)

    testConfig.saveConfig('toolscollector_s.ini')
