from time import strftime
from configuration_validation import data_format
from configuration_validation import extract_data
from configuration_validation import configuration_validation_tool
import os
import pandas as pd


def main():
    filter_variables = list()
    values = iter_dict(data_format.levels)
    for value in values:
        filter_variables.append(expand_variables(value))
    master_paths = configuration_validation_tool.find_all_master()
    filename = export_config_validation()
    with open(filename, 'w') as f:
        f.write('\n')
        for gblv_path in master_paths:
            f.write(gblv_path + '\n')
            gblv_data = extract_data.main(gblv_path, filter_variables)
            for check in run_checks(gblv_data):
                for line in check:
                    f.write(line)
            f.write('\n\n')
    print('\nYour file has been created.')
    configuration_validation_tool.retry()


def export_config_validation():
    output_path = os.getcwd().rsplit('\\', 1)[0]  # Gets the working directory.
    filename = output_path + '\\Tool data\\Config_Validation-{0}.csv'.format(strftime("%Y%m%d%H%M%S"))
    return filename


def iter_dict(variables_dict):  # Grabs all the variables from all levels of a supplied dictionary. Used to grab
                                # variables from data_format.levels()
    for key, value in variables_dict.items():
        if isinstance(value, dict):
            for i in iter_dict(value):
                yield i
        elif isinstance(value, list):
            for variable in value:
                if isinstance(variable, str):
                    yield variable
        else:
            yield value


def expand_variables(value):  # Expands variables, easier to do this than hard code due to identification issues.
    if 'I7m' in value:
        for i in range(2):
            if 'n' in value:
                for j in range(4):
                    ic_assigned_value = value.replace('m', str(i))
                    channel_assigned_value = ic_assigned_value.replace('n', str(j + 1))
                    yield channel_assigned_value
            else:
                ic_assigned_value = value.replace('m', str(i))
                yield ic_assigned_value
    else:
        yield value


def run_checks(gblv_data):
    yield mcs_data_unique(gblv_data)
    yield mcs_data_consistent(gblv_data)
    yield channel_data_consistent_xmodel(gblv_data)
    yield channel_data_consistent_ivars(gblv_data)


def mcs_data_consistent(data):
    for var in data_format.levels['brick_level_consistent']:
        try:
            value_test = list()
            for index, value in enumerate(data[var]):
                if data[var].first_valid_index() == 'none':
                    continue
                else:
                    check_index = int(data[var].first_valid_index())
                if value != data[var].iloc[check_index] and pd.notnull(value):
                    value_test.append(data['b_AxisN_P'].iloc[index])
            if len(value_test) == 0:
                yield '{0}, OK, No action required, Axis, N/A\n'.format(var)
            else:
                axis = '. '.join(value_test)
                yield '{0}, NOT consistent, Check *.e.pmc, Axis, {1}\n'.format(var, axis)
        except KeyError:
            continue


def mcs_data_unique(data):
    for var in data_format.levels['brick_level_unique']:
        try:
            value_test = dict()
            for index, value in enumerate(data[var]):
                if pd.isnull(value):
                    continue
                elif value not in value_test.values():
                    value_test[data['b_AxisN_P'].iloc[index]] = value
            if len(value_test) > len(set(value_test.values())):
                axis_result = '. '.join(value_test.keys())
                yield '{0}, NOT unique, Check *.e.pmc, Axis, {1}\n'.format(var, axis_result)
            else:
                yield '{0}, OK, No action required, Axis, N/A \n'.format(var)
        except KeyError:
            continue


def channel_data_consistent_xmodel(data):
    for var in data_format.levels['channel_level_consistent']['xmodel']:
        ic0_value_test = dict()
        ic1_value_test = dict()
        try:
            for index, value in enumerate(data[var]):
                if 0 >= int(data['b_AxisN_P'].iloc[index]) >= 4 and pd.notnull(value):
                    ic0_value_test[data['b_AxisN_P'].iloc[index]] = value
                elif 5 >= int(data['b_AxisN_P'].iloc[index]) >= 8 and pd.notnull(value):
                    ic1_value_test[data['b_AxisN_P'].iloc[index]] = value
            if all(i == ic0_value_test.values()[0] for i in ic0_value_test.values()):
                yield '{0}, OK, No action required, Axis, N/A, Channel, 0 \n'.format(var)
            else:
                axis = '. '.join(ic0_value_test.keys())
                yield '{0}, NOT consistent, Check *.e.pmc, Axis, {1}, Channel, 0\n'.format(var, axis)
            if all(i == ic1_value_test.values()[0] for i in ic1_value_test.values()):
                yield '{0}, OK, No action required, Axis, N/A, Channel, 1 \n'.format(var)
            else:
                axis = '. '.join(ic0_value_test.keys())
                yield '{0}, NOT consistent, Check *.e.pmc, Axis, {1}, Channel, 1\n'.format(var, axis)
        except KeyError:
            continue


def channel_data_consistent_ivars(data):
    for var in data_format.levels['channel_level_consistent']['ivars']:
        try:
            if len(set(data['b_ICNumber_X'])) == 2:
                ic_count = 2
            elif len(set(data['b_ICNumber_X'])) == 1:
                ic_count = 1
            else:
                ic_count = 2
        except KeyError:
            ic_count = 2
        for i in range(ic_count):
            if 'I7m0' in var:
                ic_changed_var = var.replace('m', str(i))
                value_test = list()
                try:
                    for index, value in enumerate(data[ic_changed_var]):
                        if 0 + 4 * i < index < 4 + 4 * i and value != data[ic_changed_var].iloc[0 + 4 * i] \
                                and pd.notnull(value):
                            value_test.append(data['b_AxisN_P'].iloc[index])
                    if len(value_test) == 0:
                        yield '{0}, OK, No action required, Axis, N/A, Channel, {1}\n'.format(ic_changed_var, i)
                    else:
                        value_test = '. '.join(value_test)
                        yield '{0}, NOT consistent, Check *.e.pmc, Axis, {1}, Channel, {2}\n'\
                            .format(ic_changed_var, value_test, i)
                except KeyError:
                    continue
            elif 'I7mn' in var:
                try:
                    if int(data['b_AxisN_P'].apply(float).max()) > 4 and i == 0:
                        channel_count = 4
                    elif int(data['b_AxisN_P'].apply(float).max()) > 4 and i == 1:
                        channel_count = len(data['b_AxisN_P']) - 4
                    elif int(data['b_AxisN_P'].apply(float).max()) < 4 and i == 0:
                        channel_count = 5 - int(data['b_AxisN_P'].apply(float).max())
                    else:
                        channel_count = 4
                except KeyError:
                    channel_count = 4
                for j in range(channel_count):
                    value_test = dict()
                    ic_changed_var = var.replace('m', str(i))
                    channel_changed_var = ic_changed_var.replace('n', str(j + 1))
                    try:
                        for index, value in enumerate(data[channel_changed_var]):
                            if pd.notnull(value) and value not in value_test.values():
                                value_test[data['b_AxisN_P'].iloc[index]] = value
                        if len(value_test) == 1:
                            yield '{0}, OK, No action required, Axis, N/A, Channel, {1} \n'\
                                .format(channel_changed_var, i)
                        else:
                            value_test = '. '.join(value_test.keys())
                            yield '{0}, NOT consistent, Check *.e.pmc, Axis, {1}, Channel, {2}\n'\
                                .format(channel_changed_var, value_test, i)
                    except KeyError as e:
                        continue


# The Oompa Loompas did it.
