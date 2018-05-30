#
# Tools Collector which provides easy access to multiple tools developed
# during different actions.
#
import sys
import ConfigParser

class TCConfig(object):
    def __init__(self, configfilename):
        # read ini file
        self.configfilename = configfilename
        self.config = ConfigParser.ConfigParser()
        self.config.optionxform = str
        self.config.read(configfilename)
        self.tc_config_meta = {'McgFwVersionHistory' = {'max_options' = 10},
                               'McgFwDirHistory' = {'max_options' = 10},
                               'McgPackDirHistory' = {'max_options' = 10},
                               'McgPackVersionHistory' = {'max_options' = 10},
                               'CreateMcgPackBranchHistory' = {'max_options' = 10},
                               'CreateMcgPackTagHistory' = {'max_options' = 10},
                               'CopyToInstallSrcHistory' = {'max_options' = 10},
                               'CopyToInstallDstHistory' = {'max_options' = 10}}

    def saveConfig(self):
        with open('toolsCollector_s.ini', 'wb') as configfile:
            self.config.write(configfile)
        
    def printOutConfig(self):
        for section_name in self.config.sections():
            print 'Section:', section_name
            print '  Options:', self.config.options(section_name)
            for name, value in self.config.items(section_name):
                print '  %s = %s' % (name, value)
            print

    def getSectionValues(self, section_name):
        valueList = list()
        for name, value in self.config.items(section_name):
            valueList.append(value)
        return valueList

    def getSectionFull(self, section_name):
        sectionList = list()
        for name, value in self.config.items(section_name):
            sectionList.append((name, value))
        return sectionList

    def updateSection(self, section_name, new_section_data):
        option_counter = 0
        max_options = self.tc_config_meta[section_name]['max_options']
        for item in self.mcgFwVersions:
            self.config.set(section_name, str(optionCounter), item)
            optionCounter += 1

    
if __name__ == "__main__":
    testConfig = TCConfig('toolscollector.ini')
    # testConfig.printOutConfig()
    sectionName = 'McgFwVersionHistory'

    sectionTouples = testConfig.getSectionFull(sectionName)
    print 'Listing values of section %s' % sectionName
    for option, value in sectionTouples:
        print "%s=%s" % (option, value)

    sectionValues = testConfig.getSectionValues(sectionName)
    print 'Listing values of section %s' % sectionName
    for value in sectionValues:
        print "value %s" % value
    