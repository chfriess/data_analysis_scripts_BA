import json
from particle_filter.utils.map3D import Map3D

def prepare_cross_validation_maps():
    SAMPLES = ["2", "3", "5", "6", "7", "8", "9", "10"]

    DESTINATION = "C:\\Users\\Chris\\OneDrive\\Desktop\\pruning\\"

    for sample_nr in SAMPLES:
        m = Map3D()
        MAIN_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\main branch old setup\\sample_" + sample_nr +\
                    "\\reference_for_cross_validation\\impedance per groundtruth" + sample_nr + ".json"
        SIDE_PATH = "C:\\Users\\Chris\\OneDrive\\Desktop\\tilt_phantom\\side branch old setup\\sample_" + sample_nr + \
                    "\\reference_for_cross_validation\\impedance per groundtruth" + sample_nr + ".json"

        with open(MAIN_PATH, "r") as infile:
            vessel_to_read = json.load(infile)
            main_vessel = vessel_to_read["signal_per_centerline_position"]

        with open(SIDE_PATH, "r") as infile:
            vessel_to_read = json.load(infile)
            side_vessel = vessel_to_read["signal_per_centerline_position"]

        start_index_aorta = 0
        start_index_side_branch = 0

        for i, el in enumerate(main_vessel):
            if el["centerline_position"] >= 80:
                start_index_aorta = i
                break

        for i, el in enumerate(main_vessel):
            if el["centerline_position"] >= 180:
                start_index_side_branch = i
                break

        aorta_before = main_vessel[start_index_aorta:start_index_side_branch]
        offset = aorta_before[0]["centerline_position"]
        for i, el in enumerate(aorta_before):
            aorta_before[i]["centerline_position"] -= offset

        aorta_after = main_vessel[start_index_side_branch:]
        offset = aorta_after[0]["centerline_position"]
        for i, el in enumerate(aorta_after):
            aorta_after[i]["centerline_position"] -= offset

        m.add_vessel_as_list_of_dicts(main_vessel[:start_index_aorta], 0)

        m.add_vessel_as_list_of_dicts(aorta_before, 1)
        m.add_vessel_as_list_of_dicts(aorta_after, 2)

        start_index_side_branch = 0
        for i, el in enumerate(side_vessel):
            if el["centerline_position"] >= 180:
                start_index_side_branch = i
                break

        renal = side_vessel[start_index_side_branch:]
        offset = renal[0]["centerline_position"]
        for i, el in enumerate(renal):
            renal[i]["centerline_position"] -= offset
        m.add_vessel_as_list_of_dicts(renal, 3)

        m.add_mapping([0, 1])
        m.add_mapping([1, 2])
        m.add_mapping([2, 3])

        for key in m.vessels.keys():
            print(str(key) + "_" + str(m.vessels[key]))
        m.save_map(DESTINATION, "cross_reference_map_" + sample_nr)

