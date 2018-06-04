import fileinput
import glob
import string
import sys
import os
from os.path import join
from pathlib import *
import re


# # replace a string in multiple files
# def replace_in_file():
#     if len(sys.argv) < 2:
#         print "usage: %s search_text replace_text directory" % os.path.basename(sys.argv[0])
#         sys.exit(0)
#
#     stext = sys.argv[1]
#     rtext = sys.argv[2]
#     if len(sys.argv) == 4:
#         path = join(sys.argv[3], "*")
#     else:
#         path = "*"
#
#     print "finding: " + stext + " replacing with: " + rtext + " in: " + path
#
#     files = glob.glob(path)
#     for line in fileinput.input(files, inplace=1):
#         lineno = 0
#         lineno = string.find(line, stext)
#         if lineno > 0:
#             line = line.replace(stext, rtext)
#
#         sys.stdout.write(line)


def find_in_files(top, pattern):
    # type (Path, string) -> list(string)
    matching_files = []
    file_matcher = re.compile(pattern)
    for root, dirs, files in os.walk(str(top), topdown=True):
        for name in files:
            if file_matcher.match(name):
                # print name
                matching_files.append(join(root, name))
            pass
    return matching_files


def replace_in_files(top, search_string, replace_string, file_filter='.?'):
    # type: (object, str, str, str) -> list(string)
    """
    Search recursively through top directory and replace search_string through replace_string in files matching given file_filter.
    In order to be able to replace multiple line search strings, the whole file is read in and a string replace is executed.
    The file_filter has to be a regular expression pattern.
    Returns the list of files changed.
    """
    changed_files = []
    matching_files = find_in_files(top, file_filter)
    for f in matching_files:
        input_file = open(f, 'r')
        try:
            file_content = input_file.read()
        except:
            print 'read error'
            return
        input_file.close()
        if file_content.find(search_string) >= 0:
            changed_files.append(f)
            new_file_content = file_content.replace(search_string, replace_string)
            output_file = open(f, 'w')
            output_file.write(new_file_content)
            output_file.close()
    # for line in fileinput.input(matching_files, inplace=1):
    #     line_nr = string.find(line, search_string)
    #     if line_nr > 0:
    #         line = line.replace(search_string, replace_string)
    #         if not fileinput.filename() in changed_files:
    #             changed_files.append(fileinput.filename())
    #     sys.stdout.write(line)
    return changed_files


if __name__ == "__main__":
    # found_files = find_in_files(Path('c:\Users\Thomas\Development\python\ToolsCollector\src\__testdir'), '.*mcg.?_platform.*')
    # for item in found_files:
    #     print 'f = ' + item

    # files_changed = replace_in_files(Path('c:\Users\Thomas\Development\python\ToolsCollector\src\__testdir'),
    #     '22.1.0', '22.0.2', '.*mcg.?_platform.*')
    # for item in files_changed:
    #     print 'file = ' + item

    files_changed = replace_in_files(Path('c:\Users\Thomas\Development\python\ToolsCollector\src\__testdir'), '''<Release>22</Release>
                <Update>1</Update>
                <Evolution>0</Evolution>''', '''<Release>22</Release>
                <Update>0</Update>
                <Evolution>2</Evolution>''', 'mcg_master.*\.xml')
    for item in files_changed:
        print 'file = ' + item

    # found_files = find_in_files(Path('c:\Users\Thomas\Development\python\ToolsCollector\src\__testdir'), '.*master.*\.xml')
