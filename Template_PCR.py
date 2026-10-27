from opentrons import protocol_api
import math
import re

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'PCR-Prep',
    'description': '''''',
    'author': 'JW'
    }


def run(protocol: protocol_api.ProtocolContext):
    tips1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 10)  # tips
    tips2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 11)  # tips
    tips3 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 7)  # tips

    s_plate1 = protocol.load_labware('suedlaborpink_96_wellplate_200ul', 1)  #
    s_plate2 = protocol.load_labware('suedlaborgreen_96_wellplate_200ul', 2)  #
    s_plate3 = protocol.load_labware('nest0.2mlpcr8striptubes_96_aluminumblock_200ul', 4)  #
    s_plate4 = protocol.load_labware('suedlabororange_96_wellplate_200ul', 5)  #
    mastermix = protocol.load_labware('sarstedtsafeseal_24_aluminumblock_2000ul', 8)  #

    # Load Temperature Module 1 in deck slot 3 on USB port 1
    temperature_module1 = protocol.load_module('temperature module gen2', 3)
    # Load Temperature Module 2 in deck slot 6 on USB port 2
    temperature_module2 = protocol.load_module('temperature module gen2', 6)

    tm1_pcr_stripes = temperature_module1.load_labware('nest0.2mlpcr8striptubes_96_aluminumblock_200ul',
                                                     label='Temperature-Controlled Tubes')
    tm2_pcr_stripes = temperature_module2.load_labware('nest0.2mlpcr8striptubes_96_aluminumblock_200ul',
                                                     label='Temperature-Controlled Tubes')

    s_p300 = protocol.load_instrument('p300_single_gen2', 'left',
                                   tip_racks=[]) # tip_racks=[tips1, tips2] if more than in one rack is needed
    s_p20 = protocol.load_instrument('p20_single_gen2', 'right',
                                   tip_racks=[tips1, tips2, tips3])  # tip_racks=[tips1, tips2] if more than in one rack is needed
    soll_temp = temp_mod
### start protocol:
    # s_p20.pick_up_tip()
    s_p20.flow_rate.aspirate = f_r_asp  # in µL/s
    s_p20.flow_rate.dispense = f_r_dis  # in µL/s
    master_vol = m_v  # in µl
    max_spped = m_s
    tr_vol = t_v
    tot_checked_labels = ["t_c_l"]

    temperature_module1.set_temperature(soll_temp)  # in °C, will pause your protocol until your target temperature is reached
    if len(tot_checked_labels) > 96:
        temperature_module2.set_temperature(soll_temp)

    s_p20.pick_up_tip()

    if math.ceil(len(tot_checked_labels)/96) < 2:
        tm1_run = len(tot_checked_labels)
        tm2_run = 0
    else:
        tm1_run = 96
        tm2_run = len(tot_checked_labels)-96

    factor_master, _ = divmod(20, master_vol)
    k_tm1, res_tm1 = divmod(tm1_run, factor_master)

    for i in range(0, k_tm1*factor_master, factor_master):
        # Intake of mastermix
        s_p20.aspirate(factor_master * master_vol, mastermix['A1'])
        protocol.max_speeds['a'] = max_spped  # in mm/s default: delete or None
        s_p20.move_to(mastermix['A1'].top())
        protocol.max_speeds['a'] = None
        for j in range(i, i + factor_master):
            s_p20.dispense(master_vol, tm1_pcr_stripes.wells()[j])
            protocol.max_speeds['a'] = max_spped
            s_p20.move_to(tm1_pcr_stripes.wells()[j].top(-15))
            protocol.max_speeds['a'] = None
    if res_tm1 !=0:
        # Intake of residual mastermix
        s_p20.aspirate(res_tm1 * master_vol, mastermix['A1'])
        protocol.max_speeds['a'] = max_spped  # in mm/s default: delete or None
        s_p20.move_to(mastermix['A1'].top())
        protocol.max_speeds['a'] = None
        for j_res in range(k_tm1*factor_master, (k_tm1*factor_master)+res_tm1):
            s_p20.dispense(master_vol, tm1_pcr_stripes.wells()[j_res])
            protocol.max_speeds['a'] = max_spped
            s_p20.move_to(tm1_pcr_stripes.wells()[j_res].top(-15))
            protocol.max_speeds['a'] = None

    if tm2_run != 0:
        k_tm2, res_tm2 = divmod(tm2_run, factor_master)

        for i in range(0, k_tm2 * factor_master, factor_master):
            # Intake of mastermix
            s_p20.aspirate(factor_master * master_vol, mastermix['A1'])
            protocol.max_speeds['a'] = max_spped  # in mm/s default: delete or None
            s_p20.move_to(mastermix['A1'].top())
            protocol.max_speeds['a'] = None
            for j in range(i, i + factor_master):
                s_p20.dispense(master_vol, tm2_pcr_stripes.wells()[j])
                protocol.max_speeds['a'] = max_spped
                s_p20.move_to(tm2_pcr_stripes.wells()[j].top(-15))
                protocol.max_speeds['a'] = None
        if res_tm2 != 0:
            # Intake of residual mastermix
            s_p20.aspirate(res_tm2 * master_vol, mastermix['A1'])
            protocol.max_speeds['a'] = max_spped  # in mm/s default: delete or None
            s_p20.move_to(mastermix['A1'].top())
            protocol.max_speeds['a'] = None
            for j_res in range(k_tm2 * factor_master, (k_tm2 * factor_master) + res_tm2):
                s_p20.dispense(master_vol, tm2_pcr_stripes.wells()[j_res])
                protocol.max_speeds['a'] = max_spped
                s_p20.move_to(tm2_pcr_stripes.wells()[j_res].top(-15))
                protocol.max_speeds['a'] = None

    s_p20.drop_tip()

    s_p20.well_bottom_clearance.aspirate = w_b_c  # in mm; default = 1

    dict = {1: s_plate1,
            2: s_plate2,
            3: s_plate3,
            4: s_plate4}

    for index, well_name in enumerate(tot_checked_labels):
        if index < 96:
            s_p20.transfer(tr_vol, dict[int(re.split(r'_', well_name)[0])].wells(re.split(r'_', well_name)[1]),
                           tm1_pcr_stripes.wells()[index], new_tip='always')
        else:
            s_p20.transfer(tr_vol, dict[int(re.split(r'_', well_name)[0])].wells(re.split(r'_', well_name)[1]),
                           tm2_pcr_stripes.wells()[index-95], new_tip='always')


