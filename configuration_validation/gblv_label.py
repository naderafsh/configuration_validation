from time import strftime
from configuration_validation import extract_data
from configuration_validation import configuration_validation_tool
from configuration_validation import data_format
import os


# This tool exports application style labels to be distributed to GBLV's to denote their software configuration. The
# output file is a .csv file that can be used as a database in the P.Touch labeling software. There is also a
# template file that can be used in conjunction with this output data to ease mass printing of labels.
def main():
    user_response = input('Do you want to search for all master.pmc files? [Y/N]\n')
    master_file_list = list()
    if user_response.lower() == 'y':
        master_file_list = configuration_validation_tool.find_all_master()
    elif user_response.lower() == 'n':
        master_file_list.append(configuration_validation_tool.find_one_master())
    else:
        print('That is not a valid answer, please try again.')
        main()
    file_data = list()
    for file in master_file_list:
        controller_data = import_label_data(file)
        gblv_label = raw_gblv_label(controller_data)
        file_data.append(gblv_label)
    mcs = extract_data.main(master_file_list[0], 'e_BrickN_P').irow(0)['e_BrickN_P'].strip("'")
    export_gblv_label(file_data, mcs)
    answer = input('Would you like to produce more GBLV labels? [Y/N]\n or type "Other" to select a different tool.\n')
    configuration_validation_tool.retry(answer, '4')


def import_label_data(master_path):
    # Imports the raw data required for the labels from a '.e.pmc' file.
    data_filter = ['e_BrickN_P',
                   'e_DevName_P',
                   'e_AxisID_P',
                   'b_AxisN_P',
                   'e_BrickIP_P',
                   'e_MotionRackIP_P',
                   ]
    controller_frame = extract_data.main(master_path, data_filter)
    return controller_frame


def raw_gblv_label(controller_data):
    # Creates dict with all the values of the label
    if 'e_BrickN_P' in controller_data and isinstance(controller_data.irow(0)['e_BrickN_P'], str):
        brick = controller_data.irow(0)['e_BrickN_P'].strip("'")
    else:
        brick = '**Error**'
    if 'e_BrickIP_P' in controller_data and isinstance(controller_data.irow(0)['e_BrickIP_P'], str):
        ip_address = controller_data.irow(0)['e_BrickIP_P'].strip("'")
    else:
        ip_address = '**Error**'
    if 'e_MotionRackIP_P' in controller_data and isinstance(controller_data.irow(0)['e_MotionRackIP_P'], str):
        moxa_ip_address = controller_data.irow(0)['e_MotionRackIP_P'].strip("'")
    else:
        moxa_ip_address = '**Error**'
    axis_dict = dict()
    for i in range(8):
        if str(i) in controller_data.index:
            if isinstance(controller_data.irow(i)['e_DevName_P'], str):
                dev_name = controller_data.irow(i)['e_DevName_P'].strip("'")
            else:
                dev_name = '**Error**'
            if isinstance(controller_data.irow(i)['e_AxisID_P'], str):
                axis_name = controller_data.irow(i)['e_AxisID_P'].strip("'")
            else:
                axis_name = '**Error**'
            axis_dict['Axis ' + str(i + 1)] = dev_name + ':' + axis_name
        else:
            axis_dict['Axis ' + str(i + 1)] = 'NOT USED'
    gblv_label_data = '"{0}","{1}","{2}",' \
                      '{Axis 1},' \
                      '{Axis 2},' \
                      '{Axis 3},' \
                      '{Axis 4},' \
                      '{Axis 5},' \
                      '{Axis 6},' \
                      '{Axis 7},' \
                      '{Axis 8}\n'.format(brick, ip_address, moxa_ip_address, **axis_dict)
    return gblv_label_data


def export_gblv_label(formatted_data, mcs):
    # Formats the data for use with the P-touch labeler
    output_path = os.getcwd().rsplit('\\', 1)[0]
    filename = output_path + '\\output\\GBLV_Label_MCS-{0}_Date-{1}'.format(mcs, strftime("%Y%m%d%H%M%S"))
    with open(filename + '.csv', 'w') as f:
        f.write(data_format.gblv_header)
        for gblv_label in formatted_data:
            f.write(gblv_label)
        f.close()
