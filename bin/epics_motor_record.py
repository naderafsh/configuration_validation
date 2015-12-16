from time import strftime
import extract_data
import data_format
from motor_list import format_asbuilt
import motor_record_st_grab
import configuration_validation_tool
import os
import copy


def main():
    master_path = configuration_validation_tool.find_one_master()  # Asks for the location of the 'master.pmc'.
    st_path = configuration_validation_tool.st_file()  # Asks for the location of the 'st.cmd'.
    raw_mcs_data = mcs_data_grab(master_path)
    st_data = motor_record_st_grab.st_match(st_path, master_path)
    mcs_data = epics_dict(raw_mcs_data)
    data = format_data(mcs_data, st_data)
    beamline = mcs_data[0]['BEAMLINE']['value']
    mcs = mcs_data[0]['CONTROLLER']['value']
    export_motor_record(data, mcs,
                        beamline)  # Exports the Motor Record to a file in the directory that the program is running.
    answer = input('Would you like to make another motor record? [Y/N]\n or type "Other" to select a different tool.\n')
    configuration_validation_tool.retry(answer, '2')


def export_motor_record(data, mcs, beamline):

    output_path = os.getcwd().rsplit('\\', 1)[0]
    filename = output_path + '\\Tool data\\MotorRecord-SR{0}-MCS{1}-{2}'.format(beamline, mcs, strftime("%Y%m%d%H%M%S"))
    with open(filename + '.csv', 'w') as f:
        for line in data:
            f.write(line)
        print('Your file has been created.\n')
        f.close()


def mcs_data_grab(master_path):
    data_structure = data_format.epics_record_structure
    xmodel_fil_vars = list()
    for i, k in enumerate(data_structure):
        if data_structure[k]['scope'] == 'GBLV':
            xmodel_fil_vars.append(data_structure[k]['variable'])
    mcs_data = extract_data.main(master_path, xmodel_fil_vars)
    return mcs_data


def epics_dict(data):
    data_structure = data_format.epics_record_structure
    mcs_data = list()
    for data_index in data.index:
        mcs_data.append(copy.deepcopy(data_structure))
        for mcs_index, mcs_key in enumerate(mcs_data[int(data_index)]):
            if mcs_data[int(data_index)][mcs_key]['scope'] == 'GBLV':
                mcs_var = mcs_data[int(data_index)][mcs_key]['variable']
                if mcs_var in data.iloc[int(data_index)] and isinstance(data.iloc[int(data_index)][mcs_var], str):
                    value = data.iloc[int(data_index)][mcs_var].strip("'")
                    mcs_data[int(data_index)][mcs_key]['value'] = value
                elif mcs_var in data.iloc[int(data_index)]:
                    mcs_data[int(data_index)][mcs_key]['value'] = data.iloc[int(data_index)][mcs_var]
    return mcs_data


def format_data(mcs_data, st_data):
    epics_record = list()
    epics_record.append(data_format.epics_record_header)
    for i, k in enumerate(mcs_data):
        strindex = mcs_data[i]['ID']['value'].index(":")
        mcs_data[i]['ID']['value'] = mcs_data[i]['ID']['value'][0:strindex]
        epics_record_line = (
            '{' +
            '{0[ID][value]: >22},'
            ':{0[M][value]: >9},'
            '"{0[DESC][value]: >18}",'
            '{0[DIR][value]: >11},'
            '{0[VELO][value]: >11},'
            '{0[ACCL][value]: >18},'
            '{0[BDST][value]: >11},'
            '{0[BVEL][value]: >11},'
            '{0[BACC][value]: >11},'
            '{1[SPORT]: >15},'
            '{1[PORT]: >11},'
            '{0[ADDR][value]: >11},'
            '{0[MRES][value]: >20},'
            '{0[PREC][value]: >6},'
            '{0[EGU][value]: >6},'
            '{0[DHLM][value]: >11},'
            '{0[DLLM][value]: >11},'
            '{0[TWV][value]: >11},'
            '{0[ERES][value]: >20},'
            '{0[UEIP][value]: >11},'
            '{0[VMAX][value]: >11},'
            '{0[OFF][value]: >11},'
            '{0[MAXCURR][value]: >14},'
            '{0[RDBD][value]: >11},'
            '{0[ADEL][value]: >11},'
            '{0[ID][value]: >20}'
            .format(mcs_data[i], st_data) + '}\n'
        )
        epics_record.append(epics_record_line)
    return epics_record
