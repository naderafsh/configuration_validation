from time import strftime
from configuration_validation import extract_data
from configuration_validation import configuration_validation_tool
import os


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
    file_data, mcs = build_file(master_file_list)
    export_label_data(mcs, file_data)
    print('Cables labels produced.')
    answer = input('Would you like to produce more cable labels? [Y/N]\n or type "Other" to select a different tool.\n')
    configuration_validation_tool.retry(answer, '3')


def build_file(master_files):
    file_data = list()
    mcs = 'MCS Not found'
    for file in master_files:
        controller_frame = import_label_data(file)
        cable_label_data = cable_label(controller_frame)
        for i in cable_label_data:
            axis_formatted_data = format_cable_label(i)
            file_data.append(axis_formatted_data)
        mcs = str(cable_label_data[0]['mcs'])
    return file_data, mcs


def import_label_data(master_path):
    # Imports the raw data required for the labels from a '.e.pmc' file.
    data_fields = ['e_BrickN_P',
                   'e_DevName_P',
                   'e_AxisID_P',
                   'b_AxisN_P',
                   'a_Commutation_D',
                   'a_IsBrakeUsed_X',
                   'e_StageEncPortN_X',
                   'b_StageEncPortN_P',
                   'e_MotEncPortN_X',
                   'b_MotEncPortN_P',
                   'a_IsEncoderUsed_X',
                   'e_BrickIP_P',
                   ]
    controller_frame = extract_data.main(master_path, data_fields)
    return controller_frame


def cable_label(controller_data):
    # Applies consistent wording for variables, and imports encoder details if required.
    data = list()
    aux = dict()
    for i, v in controller_data.iterrows():
        label = dict()
        i = int(i)
        if controller_data.iloc[i]['a_Commutation_D'].lower() == "'directmicrostepping'":
            label['motor_type'] = 'Stepper'
        elif controller_data.iloc[i]['a_Commutation_D'].lower() == "'notdirectmicrostepping'":
            label['motor_type'] = 'Stepper'
        elif controller_data.iloc[i]['a_Commutation_D'].lower() == "'brushlessdc'":
            label['motor_type'] = 'BrushlessDC'
        elif controller_data.iloc[i]['a_Commutation_D'].lower() == "'dcbrush'":
            label['motor_type'] = 'DCBrushed'
        else:
            print(controller_data.iloc[i]['a_Commutation_D'])
            label['motor_type'] = 'Error'
        if controller_data.iloc[i]['a_IsEncoderUsed_X'] == '1':
            label['enc_type'] = 'ENC'
            label['stage_enc_axis'] = controller_data.iloc[i]['b_StageEncPortN_P']
            label['motor_enc_axis'] = controller_data.iloc[i]['b_MotEncPortN_P']
        else:
            label['enc_type'] = False
            label['stage_enc_axis'] = 'none'
            label['motor_enc_axis'] = 'none'
        if controller_data.iloc[i]['a_IsBrakeUsed_X'] == '1':
            aux['maux'] = 'aux'
            aux['mcs'] = strip_grab(controller_data, 'e_BrickN_P', i)
        label['mcs'] = strip_grab(controller_data, 'e_BrickN_P', i)
        label['axis'] = strip_grab(controller_data, 'b_AxisN_P', i)
        label['axisname'] = strip_grab(controller_data, 'e_AxisID_P', i)
        label['devname'] = strip_grab(controller_data, 'e_DevName_P', i)
        data.append(label.copy())
    data.append(aux.copy())
    return data


def format_cable_label(label_data):
    # Formats the data for use with BMP-71 labeler.
    formatted_data = list()
    valid_mot_axis = ['Stepper', 'BrushlessDC', 'DCBrushed', ]
    valid_enc_axis = ['1', '2', '3', '4', '5', '6', '7', '8', ]
    if 'maux' in label_data and label_data['maux'] == 'aux':
        formatted_data.append('MCS{0},MAUX,\n'.format(label_data['mcs']))
        return formatted_data
    if 'motor_type' in label_data and label_data['motor_type'] in valid_mot_axis:
        formatted_data.append('MCS{0},{1},#{2} - {3},:{4},\n'.format(label_data['mcs'],
                                                                       label_data['motor_type'],
                                                                       label_data['axis'],
                                                                       label_data['devname'],
                                                                       label_data['axisname'], ))
    elif 'motor_type' in label_data and label_data['motor_type'] not in valid_mot_axis:
        formatted_data.append('Motor Type not found!,ERROR,ERROR,ERROR,\n')
    if 'enc_type' in label_data and label_data['enc_type'] is not False and label_data['stage_enc_axis'] in \
            valid_enc_axis:
        formatted_data.append('MCS{0},{1},#{2} - {3},:{4},\n'.format(label_data['mcs'],
                                                                       label_data['enc_type'],
                                                                       label_data['stage_enc_axis'],
                                                                       label_data['devname'],
                                                                       label_data['axisname']))
    if 'enc_type' in label_data and label_data['enc_type'] is not False and label_data['motor_enc_axis'] in \
            valid_enc_axis:
        formatted_data.append('MCS{0},{1},#{2} - {3},:{4},\n'.format(label_data['mcs'],
                                                                       label_data['enc_type'],
                                                                       label_data['motor_enc_axis'],
                                                                       label_data['devname'],
                                                                       label_data['axisname']))

    return formatted_data


def export_label_data(mcs, data):
    # Writs the data to a csv file.
    mcs = str(mcs)
    output_path = os.getcwd().rsplit('\\', 1)[0]
    filename = output_path + '\\Tool data\\Labels_MCS{0}_{1}'.format(mcs, strftime("%Y%m%d%H%M%S"))
    with open(filename + '.csv', 'w') as f:
        for label in data:
            for line in label:
                f.write(line)
        f.close()


def strip_grab(dataframe, var, i):
    # Strips values of unnecessary quotation marks.
    try:
        value = dataframe.iloc[i][var]
    except KeyError:
        value = ' No valid data.'
    if isinstance(value, str):
        value = value.strip("'")
        return value
    else:
        return value
