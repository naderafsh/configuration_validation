import extract_data


# Test checks that files returned by check_axis_list are e.pmc files
def test_controller_axis_list():
    dummy_master_file = r'H:\Personal_Folder\Documents\Programming\Current App\tests\dummy folder\Devices\MCS01\
    Settings\Master.pmc'
    path_list = extract_data.controller_axis_list(dummy_master_file)
    assert all('.e.pmc' in path.lower() for path in path_list)


def test_check_axis_list():
    dummy_master_file = r'H:\Personal_Folder\Documents\Programming\Current App\tests\dummy folder\Devices\MCS01\
    Settings\Master.pmc'
    axis_list = extract_data.check_axis_list()