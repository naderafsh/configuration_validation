import re
import os
from configuration_validation import configuration_validation_tool
from configuration_validation import extract_data


def st_match(st_path, master_path):
    # This checks that the data in the st.cmd file is consistent within the st.cmd file and also checks that the file
    # against the master.pmc.
    st_data = {'SPORT': 'No SPORT found', 'PORT': 'No PORT found'}
    ioc_path = check_st_cmd(st_path)
    master_ip_addr = extract_data.main(master_path, ['e_BrickIP_P'])['e_BrickIP_P']
    # Check if all IP's are the same. (They should be, this verification should be done before this stage.
    # In the asbuilt tool.)
    if all(x == master_ip_addr[0] for x in master_ip_addr):
        st_controller = st_master_compare(ioc_path, str(master_ip_addr[0]))
        st_data['SPORT'] = st_controller['IPPort']
        st_data['PORT'] = st_controller['PortName']
        print('ST values found.')
        return st_data
    elif not all(x == master_ip_addr[0] for x in master_ip_addr):
        print('IP addresses do not match for all the axis on this controller.\n')
        return st_data
    else:
        st_data = st_ask_input()
        return st_data


def check_st_cmd(st_path):
    # There are two methods to init the ioc configuration with the gblv settings, in the st.cmd file or in a separate
    # file. User is asked to submit st.cmd file and then gblv.cmd file is searched for and the relevant file passed
    #  back to main().
    ioc_path = [st_path[:-6], 'gblv.cmd']
    gblv_cmd_path = ''.join(ioc_path)
    if os.path.isfile(gblv_cmd_path):
        return gblv_cmd_path
    else:
        return st_path


def st_master_compare(ioc_path, master_ip_addr):
    # Checks the data in the st.cmd file, if it matches with master_value(MCS IP address) it will then check that the
    # data for that MCS in the st.cmd file. It will check the brick number and that the IPPort and Port are consistent.
    # Group 0 is MCSport, Group 1 is IP address.
    ip_regex = re.compile('pmacAsynIPConfigure\(\W*(\w*)\W*,\W*(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):\d{1,5}"\W*\)\n')
    # Group 0 is MCS, Group 1 is Addr, Group 2 is BrickNum, Group 3 is Naxes.
    create_mcs_regex = re.compile('pmacAsynMotorCreate\(\W*"(\w*)"\W*,\W*(\d*)\W*,\W*(\d*)\W*,\W*(\d*)\W*\)')
    # Group 0 is MCS, Group 1 Driver name, Group 2 is brickNum, Group 3 Naxes+1.
    configure_mcs_regex = re.compile('drvAsynMotorConfigure\(\W*(\w{1,5})\W*,\W*"(\w*)"\W*,\W*(\d*)\W*,\W*(\d*)\W*\)')
    match_data = dict()
    with open(os.path.join(ioc_path)) as f:  # Opens the st.cmd file.
        for line in f:
            match = ip_regex.search(line)
            # If a valid IP configure line is found it is searched for the IP of the MCS in question.
            if match and match.group(2) in master_ip_addr:
                # Checks if IP address matches the IP provided.
                match_data['IPPort'] = match.group(1)  # Grabs the IPPort to match to pmacAsynMotorCreate.
                match_data['IPAddr'] = match.group(2)  # Grabs the IPAddr to match to confirm record.
                continue
            match = create_mcs_regex.search(line)
            if match and 'IPPort' in match_data and match.group(1) == match_data['IPPort']:
                # Checks if the IPPort name from pmacAsynIPConfigure matches the pmacAsynMotorCreate.
                match_data['BrickNum'] = match.group(3)  # Grabs the Brick number, to compare in drvAsynMotorConfigure.
                continue
            match = configure_mcs_regex.search(line)
            if match and 'BrickNum' in match_data and match.group(1) in match_data['IPPort'] and match.group(3) == \
                    match_data['BrickNum']:
                # Checks if Port name is in IPPort from pmacAsynMotorCreate matches in drvAsynMotorConfigure,
                # also checks Brick number is relevant.
                match_data['PortName'] = match.group(1)  # If so, grabs the MCS port name.
                continue
    return match_data


def st_ask_input():
    # If values are not able to be found, asks to manually enter the values or inputs 'UNKNOWN'
    ask_input = input('The tool was not able to find valid MCS sport or MCS port values. If no, tool will input '
                      '"UNKNOWN" into the affected fields.Would you like to manually enter data? [Y/N] or type "exit"'
                      ' to quit.\n')
    st_data_dict = dict()
    if ask_input.lower() == 'y':
        st_data_dict['SPORT'] = input('Input SPORT value. E.g. "MCSxxport"')
        st_data_dict['PORT'] = input('Input PORT value. E.g. "MCSxx"')
        return st_data_dict
    elif ask_input.lower() == 'n':
        st_data_dict['SPORT'] = 'UNKNOWN'
        st_data_dict['PORT'] = 'UNKNOWN'
        return st_data_dict
    elif ask_input.lower() == 'exit':
        configuration_validation_tool.close()
    else:
        print('That was not a valid answer, try again.\n')
        st_ask_input()
