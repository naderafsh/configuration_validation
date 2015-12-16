import pandas as pd
import re
import os


def main(master_path, filter_vars=None):
    controller_file_list = controller_axis_list(master_path)
    valid_controller_axis_list = check_axis_list(controller_file_list)
    controller_raw_variables = controller_raw_data(valid_controller_axis_list)
    if filter_vars is None:
        final_controller_variables = controller_raw_variables
    else:
        final_controller_variables = filter_controller_data(controller_raw_variables, filter_vars)
    table_format = format_controller_data(final_controller_variables)
    motion_controller_data = build_controller(table_format)
    return motion_controller_data


def controller_axis_list(master_path):
    # Builds list of axis file paths on the controller from the master.pmc.
    regex = re.compile(r'^#include "(.*.e.pmc)"')
    axis_list = list()
    with open(master_path) as f:
        master_path = master_path.rstrip('Master.pmc')
        for line in f:
            if '.e.pmc' in line.lower() and '#include' in line.lower() and 'sr00id' not in line.lower() and \
                            'prereleasechanges' not in line.lower():
                match = regex.search(line)
                if match:
                    path = match.group(1)
                    path = path.replace('/', '\\')
                    axis_list.append(os.path.join(master_path, path))
    return axis_list


def check_axis_list(axis_list):
    # Checks if file is in the designated location. The file is omitted if not.
    valid_list = list()
    for index, path in enumerate(axis_list):
        check_file = path.split('\\', -1)
        filename = ''.join(check_file[-1])
        root_check_file = '\\'.join(check_file[:-1])
        for root, subdir, files in os.walk(root_check_file):
            if filename not in files:
                continue
            else:
                valid_list.append(path)
    if isinstance(valid_list, list):
        return valid_list
    else:
        return valid_list


def controller_raw_data(valid_list):
    # Formats all data for each axis, splitting data into variables, values, unit, etc.
    regex_xmodel_var = re.compile(r';>(?P<Variable>[\S]*)'
                                  r'\s*=\s*'
                                  r'(?P<Value>.*)\;'
                                  r'(?P<Unit>[^{]*)'
                                  r'{(?P<Comment>.*)}'
                                  r'(?P<Reference>.*)')
    regex_gblv_var = re.compile(r'^(?P<Variable>[IPip][\S]*)'
                                r'\s*=\s*'
                                r'(?P<Value>.*)\;'
                                r'(?P<Unit>[^{]*)'
                                r'{(?P<Comment>.*)}'
                                r'(?P<Reference>.*)')
    raw_data = dict()
    for index, axis_path in enumerate(valid_list):
        index = str(index)
        raw_data[index] = list()
        with open(axis_path) as f:
            for line in f:  # Read line data from *.e.pmc
                match_xmodel = regex_xmodel_var.search(line)
                match_gblv = regex_gblv_var.search(line)
                if match_xmodel:
                    raw_data[index].append(match_xmodel.groupdict())
                elif match_gblv:
                    raw_data[index].append(match_gblv.groupdict())
    return raw_data


def filter_controller_data(raw_data, filter_list):
    # Filters the variables in the pandas data frame from controller_raw_data().
    filtered_data = dict()
    for axis in raw_data:
        filtered_data[axis] = list()
        for entry in raw_data[axis]:
            if entry['Variable'] in filter_list:
                filtered_data[axis].append(entry)
    return filtered_data


def format_controller_data(filtered_data):
    # Formats data for Pandas.
    table_of_elements = dict()
    for axis in filtered_data:
        element = dict()
        for variable in filtered_data[axis]:
            element[variable['Variable']] = variable['Value']
        table_of_elements[axis] = element
    return table_of_elements


def build_controller(table_of_elements):
    # Builds the Pandas DataFrame
    data = pd.DataFrame(table_of_elements)
    data = data.transpose()
    return data
