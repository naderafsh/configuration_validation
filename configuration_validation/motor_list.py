from time import strftime
import extract_data
import configuration_validation_tool
import data_format
import os


def main():
    # Runs the asbuilt commands.
    final_data = list()
    beamlines = configuration_validation_tool.find_all_master()
    for beamline in beamlines:
        raw_data = import_data(beamline)
        formatted_data = format_asbuilt(raw_data)
        final_data.append(formatted_data)
    export_asbuilt(final_data)
    answer = input('Would you like to make another asbuilt document? [Y/N]\n or type "Other" to select a different tool'
                   '.\n')
    configuration_validation_tool.retry(answer, '5')


def import_data(master_file):
    # Imports filtered data from master.pmc.
    filter_variables = data_format.motor_list_filter_variables
    data = extract_data.main(master_file, filter_variables)
    return data


def format_asbuilt(data):
    # Applies formatting to data. Refer to data_format.motor_list_formatting for the order of values.
    formatted_data = list()
    for axis in data.index:
        formatting = data_format.motor_list_formatting  # Grabs formatting from data_format.py
        value = list()
        for i in formatting:
            try:
                if data.irow(axis)[i] == 'nan':
                    value.append('')
                elif data.irow(axis)[i] and isinstance(data.irow(axis)[i], str):
                    element_data = data.irow(axis)[i].strip("'")
                    value.append(element_data)
                elif data.irow(axis)[i] and isinstance(data.irow(axis)[i], int):
                    element_data = data.irow(axis)[i]
                    value.append(element_data)
                else:
                    value.append('')
            except KeyError:
                value.append('')
        line_formatting = ("{0},,{1},,,{2},{3},{4},{5},{6},{7}{8}:{9},{10},{11},{12},{13},{14},,,,,,,,,,,,,,,,,,,,,\n"
                           .format(axis, *value))
        formatted_data.append(line_formatting)
    return formatted_data


def export_asbuilt(data):
    # Exports file as csv. Includes header for table.
    output_path = os.getcwd().rsplit('\\', 1)[0]  # Gets the working directory.
    filename = output_path + '\\output\\Asbuilt-FINAL-{0}'.format(strftime("%Y%m%d%H%M%S"))
    header = data_format.motor_list_header  # Starts the file with the header from data_format.py
    with open(filename + '.csv', 'w') as f:
        f.write(header)
        for controller in data:  # Iterates over the controllers.
            for axis in controller:  # Iterates over the axis on the controller.
                f.write(axis)
        f.close()
