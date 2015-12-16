# Variables to be used for cross checking data in 'check_xmodel_asbuilt.py' . 'alevel' is axis scope, 'blevel' is brick
# scope and 'clevel' is channel scope.
#
# Variables can be added at anytime to their respective category to be included in the cross checking process.
levels = {
    'axis_level': [],
    'brick_level_unique': ['b_AxisN_P',
                           'b_AxisCompanionN_P',
                           'b_StageEncPortN_P',
                           'b_MotEncPortN_P',
                           ],
    'brick_level_consistent': ['e_BrickIP_P',
                               'e_BrickN_P',
                               'b_MotBusVdc_D',
                               'b_FullRangeCurr_D',
                               'b_MaxContCurr_D',
                               'b_ActualADCRes_D',
                               'b_IsTCompTable_E',
                               'b_CurrConvScale_X',
                               'I10',
                               'I30',
                               'I51',
                               'I35',
                               'I65',
                               'P899',
                               'P898',
                               'P1099',
                               'P1098',
                               'P908',
                               ],
    'channel_level_consistent': {'xmodel': ['b_ICNumber_X',
                                            'b_PhaseClock_D',
                                            'b_ServoClock_D',
                                            'b_PWMFreq_D', ],
                                 'ivars': ['I7m00',
                                           'I7m01',
                                           'I7m02',
                                           'I7m03',
                                           'I7m04',
                                           'I7mn0',
                                           'I7mn1',
                                           'I7mn2',
                                           'I7mn3',
                                           'I7mn6',
                                           'I7mn9', ]
                                 },
    'channel_level_unique': [],
    'misc': [],
}
# ----------------------------------------------------------------------------------------------------------------------
# Variables here should not need to be changed unless changes are made to the Xmodel. Or bugs, there is always bugs.


# Epics motor record data structure. To change a default to a variable that is gathered from the Xmodel update the
# relevant 'variable' keys value. Cosmetically, also replace the 'value' keys value with an empty string.
epics_record_structure = {
    'ACCL': {'scope': 'GBLV', 'variable': 'e_ACCL_X', 'value': ''},
    'ADDR': {'scope': 'GBLV', 'variable': 'b_AxisN_P', 'value': ''},
    'DHLM': {'scope': 'GBLV', 'variable': 'e_DHLM_X', 'value': ''},
    'DLLM': {'scope': 'GBLV', 'variable': 'e_DLLM_X', 'value': ''},
    'EGU': {'scope': 'GBLV', 'variable': 's_EGU_S', 'value': ''},
    'ERES': {'scope': 'GBLV', 'variable': 'e_ERES_X', 'value': ''},
    'ID': {'scope': 'GBLV', 'variable': 'e_EpicsPVName_X', 'value': ''},
    'M': {'scope': 'GBLV', 'variable': 'e_AxisID_P', 'value': ''},
    'MAXCURR': {'scope': 'GBLV', 'variable': 'a_MagCurrMove_E', 'value': ''},
    'MRES': {'scope': 'GBLV', 'variable': 'e_MRES_X', 'value': ''},
    'P': {'scope': 'GBLV', 'variable': 'e_EpicsPVName_X', 'value': ''},
    'VMAX': {'scope': 'GBLV', 'variable': 'e_VMAX_X', 'value': ''},
    'ADEL': {'scope': 'GBLV', 'variable': '', 'value': 0.1},
    'BACC': {'scope': 'GBLV', 'variable': '', 'value': 0.2},
    'BDST': {'scope': 'GBLV', 'variable': '', 'value': 0.1},
    'BVEL': {'scope': 'GBLV', 'variable': '', 'value': 1},
    'DIR': {'scope': 'GBLV', 'variable': '', 'value': 0},
    'PREC': {'scope': 'GBLV', 'variable': 'e_PREC_X', 'value': ''},
    'RDBD': {'scope': 'GBLV', 'variable': '', 'value': 0},
    'TWV': {'scope': 'GBLV', 'variable': '', 'value': 0},
    'UEIP': {'scope': 'GBLV', 'variable': '', 'value': 0},
    'VELO': {'scope': 'GBLV', 'variable': '', 'value': 1},
    'OFF': {'scope': 'GBLV', 'variable': '', 'value': 0},
    'DESC': {'scope': 'GBLV', 'variable': '', 'value': '*Description*'},
    'SPORT': {'scope': 'IOC', 'variable': 'SPORT', 'value': ''},
    'PORT': {'scope': 'IOC', 'variable': 'PORT', 'value': ''},
    'BEAMLINE': {'scope': 'GBLV', 'variable': 'e_SectorN_P', 'value': ''},
    'CONTROLLER': {'scope': 'GBLV', 'variable': 'e_PORT_P', 'value': ''},
}

# Epics motor record header.
epics_record_header = (
    'pattern {' +
    '{0:>13}P,'
    '{0:>9}M,'
    '{0:>14}DESC,'
    '{0:>8}DIR,'
    '{0:>7}VELO,'
    '{0:>14}ACCL,'
    '{0:>7}BDST,'
    '{0:>7}BVEL,'
    '{0:>7}BACC,'
    '{0:>10}SPORT,'
    '{0:>7}PORT,'
    '{0:>7}ADDR,'
    '{0:>16}MRES,'
    '{0:>2}PREC,'
    '{0:>3}EGU,'
    '{0:>7}DHLM,'
    '{0:>7}DLLM,'
    '{0:>8}TWV,'
    '{0:>16}ERES,'
    '{0:>7}UEIP,'
    '{0:>7}VMAX,'
    '{0:>8}OFF,'
    '{0:>7}MAXCURR,'
    '{0:>7}RDBD,'
    '{0:>7}ADEL,'
    '{0:>15}HOME'.format('') + '}\n'
)

# Asbuilt_file variables.
motor_list_filter_variables = ['e_AxisID_P',
                               's_MotType_S',
                               's_StageClass_X',
                               'a_Commutation_D',
                               'e_SBSID_P',
                               's_EffectivePitch_S',
                               'a_BrakePortN_P',
                               'a_InterlockPortN_P',
                               'b_MotEncPortN_P',
                               'b_StageEncPortN_P',
                               'e_ERES_X',
                               'e_DevName_P',
                               'e_AxisID_P',
                               'b_AxisN_P',
                               'e_BrickN_P',
                               ]
# Asbuilt_file variables.
motor_list_formatting = ('e_AxisID_P',
                         's_MotType_S',
                         's_StageClass_X',
                         'a_Commutation_D',
                         'e_BrickN_P',
                         'b_AxisN_P',
                         'e_SBSID_P',
                         'e_DevName_P',
                         'e_AxisID_P',
                         's_EffectivePitch_S',
                         'a_BrakePortN_P',
                         'a_InterlockPortN_P',
                         'b_MotEncPortN_P',
                         'b_StageEncPortN_P',
                         )
# Asbuilt_file variables.
motor_list_header = ('Item,'
                     'Apparatus,'
                     'Stage,'
                     'Product,'
                     'Stage Part number,'
                     'Motor Part number,'
                     'Stage class,'
                     'Motor Class,'
                     'GBLV ID,'
                     'GBLV Axis,'
                     'Motor PV Name,'
                     'Max acceleration distance,'
                     'Effective pitch(mm/rev or deg/rev),'
                     'Brake Port,'
                     'Interlock port,'
                     'Encoder port,'
                     'Stage encoder res(mm or deg),'
                     'Stage encoder part number,'
                     'Motor encoder Resolution,'
                     'Desired position precision,'
                     'Desired velocity variation,'
                     'Desired velocity,'
                     'Status: GBLV pre configuration,'
                     'Status: tuning,'
                     'Status: Assembly and wiring,'
                     'Status: Installation,'
                     'Status: Commissioning,'
                     'Date stage available,'
                     'Date motor available,'
                     'Date hardware available,'
                     'Date to be operational,'
                     'Development effort estimate,'
                     'Controls application engineering effort estimate,'
                     'Motion controls commissioning effort,\n')

# GBLV label header.
gblv_header = 'MCS,IP address,MOXA IP Address,Axis 1,Axis 2,Axis 3,Axis 4,Axis 5,Axis 6,Axis 7,Axis 8\n'
