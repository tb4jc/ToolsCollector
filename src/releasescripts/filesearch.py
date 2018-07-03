import fileinput
import glob
import string
import sys
import os
from os.path import join
from pathlib import *
import re


def find_files(top_dir, pattern, recursive=True):
    # type (string, string, boolean) -> list((string, string))
    matching_files = []
    file_matcher = re.compile(pattern)
    for root_dir, dirs, files in os.walk(top_dir, topdown=True):
        for name in files:
            if file_matcher.match(name):
                # print name
                matching_files.append((join(root_dir, name), name))
            pass
    return matching_files


def replace_in_files(top_dir, search_string, replace_string, file_filter='.?'):
    # type: (Path, str, str, str) -> list(string)
    """
    Search recursively through top directory and replace search_string through replace_string in files matching given file_filter.
    In order to be able to replace multiple line search strings, the whole file is read in and a string replace is executed.
    The file_filter has to be a regular expression pattern.
    Returns the list of files changed.
    """
    changed_files = []
    matching_files = find_files(str(top_dir), file_filter)
    for full_path, file_name in matching_files:
        input_file = open(full_path, 'r')
        try:
            file_content = input_file.read()
        except:
            print('read error')
            return
        input_file.close()
        if file_content.find(search_string) >= 0:
            changed_files.append(full_path)
            new_file_content = file_content.replace(search_string, replace_string)
            output_file = open(full_path, 'w')
            output_file.write(new_file_content)
            output_file.close()
    return changed_files


if __name__ == "__main__":
    work_dir = Path('c:/Users/Thomas/Development/python/ToolsCollector/src/__mcg_config/06_mcg_firmware/mcg_master_cfg')
    glob_pattern = '**/mcg_platform*.xml'
    for file in work_dir.glob(glob_pattern):
        print('file = ' + str(file))

    files_found = find_files(str(work_dir), '.*mcg.?_platform.*\.xml')
    for full_path, file_name in files_found:
        if file_name == "mcg_plaform_BT.xml":
            pass

    files_changed = replace_in_files(Path('c:/Users/Thomas/Development/python/ToolsCollector/src/__testdir'), '''<Release>22</Release>
                <Update>1</Update>
                <Evolution>0</Evolution>''', '''<Release>22</Release>
                <Update>0</Update>
                <Evolution>2</Evolution>''', 'mcg_master.*/.xml')
    for item in files_changed:
        print('file = ' + item)
