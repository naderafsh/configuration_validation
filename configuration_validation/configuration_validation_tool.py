# Disclaimer: I have no idea how to program.

from time import strftime
import sys
import os
from configuration_validation import cable_labels
from configuration_validation import epics_motor_record
from configuration_validation import configuration_validation
from configuration_validation import motor_list
from configuration_validation import gblv_label


def main():
    # This runs the entire app.
    try:
        print('\n########################################################'
              '\n#                                                      #'
              '\n#                                                      #'
              '\n#         Xmodel Configuration validation tool         #'
              '\n#                                                      #'
              '\n#                                                      #'
              '\n########################################################\n\n\n')
        retry()
    except(KeyboardInterrupt, SystemExit):
        print('Exiting...')
        sys.exit()
    except Exception as error:
        print(error)
        #with open('logfile.txt', 'a') as f:
        #    f.write("{} : KeyError:{}\n".format(strftime("%Y%m%d%H%M"), error))
        return error_message()


def retry(answer='', tool=''):
    if tool == '':
        tool = input('\nType the number of the operation that you would like to complete and hit Enter.\n'
                     '\n\t\t1 - Configuration Validation tool'
                     "\n\t\t2 - Motor Record output for EPIC's"
                     '\n\t\t3 - Cable Labels'
                     '\n\t\t4 - GBLV Front Panel Labels'
                     '\n\t\t5 - Export a Motor List'
                     '\n\nType "Exit" to Quit.\n')
        answer = 'y'
        return retry(answer, tool)
    if answer.lower() == 'y':
        if tool.lower() == '1':
            print('Configuration Validation tool')
            return configuration_validation.main()
        elif tool.lower() == '2':
            print("Motor Record output for EPIC's")
            return epics_motor_record.main()
        elif tool.lower() == '3':
            print('Cable Labels')
            return cable_labels.main()
        elif tool.lower() == '4':
            print('GBLV Front Panel Labels')
            return gblv_label.main()
        elif tool.lower() == '5':
            print('Export a Motor List')
            return motor_list.main()
        elif tool.lower() == 'exit':
            return close()
        else:
            print('The tool chosen was invalid, please try again.\n')
            tool = ''
            return retry(tool)
    elif answer.lower() == 'n':
        return close()
    elif answer.lower() == 'other':
        tool = ''
        return retry(answer, tool)
    elif answer.lower() == '':
        answer = input('Would you like to try again? [Y/N]\n')
        return retry(answer, tool)
    elif answer.lower() == 'exit':
        return close()
    else:
        print('That answer was invalid. Please try again.\n')
        return retry()


def find_one_master():
    # Checks if the master path provided is valid for a Master.pmc
    master_path = input('Provide the FILEPATH of the "Master.pmc" for the Motion Control System(MCS) that you would'
                        ' like to assess.\n').lower()
    if 'master.pmc' in master_path.lower():
        return master_path
    elif master_path.lower() == 'exit':
        return close()
    else:
        print('That was not a valid path. Please try again.\n')
        return find_one_master()


def find_all_master():
    # Finds all master.pmc files in the location provided.
    location = input('Provide the LOCATION of the files that you would like to assess.\n').lower()
    if location.lower() == "exit":
        return close()
    master_files_list = list()
    for root, dirs, files in os.walk(location):
        for file in files:
            if '~' in file.lower():
                pass
            elif "master.pmc" in file.lower():
                master_files_list.append(os.path.join(root, file))
    if master_files_list:
        return master_files_list
    else:
        print('No master files found. Please try again.\n')
        return find_all_master()


def st_file():
    # Checks to see if the st.cmd file is a valid file.
    st_path = input('Provide the location of the "st.cmd" file of the IOC that the MCS is located on.\n')
    if st_path.lower() == 'exit':
        return close()
    elif 'st.cmd' in st_path:
        return st_path
    else:
        print('That was not a valid file. Try again.\n')
        return st_file()


def close():
    # Tries to gracefully close the program.
    confirm = input('Press enter to exit or "retry" to start again.\n')
    if confirm == '':
        return sys.exit()
    elif confirm != '':
        return retry()
    else:
        pass


def error_message():
    # Used to gracefully return to main.
    print("\n\nThis tool was not able to complete that request, please try again. Please check the files are valid"
          " Xmodel configurations.\n\n")
    return retry()


if __name__ == '__main__':
    main()
