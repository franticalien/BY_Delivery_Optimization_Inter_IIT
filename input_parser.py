from optparse import NO_DEFAULT

from black import color_diff


def read_demand(filename):
    demand = {"Day 1": [], "Day 2": [], "Day 3": []}

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines[1:]:
        words = line.split(",")
        entry = {
            "id": words[1],  # unqiue and monotonic?
            "wh": words[0],
            "item": words[2],
            "d_loc": [int(words[4]), int(words[5]), int(words[6])],
            "d_time": [words[7], words[8]],
            "d_fail": int(words[9]),
        }
        demand[words[3]].append(entry)

    return demand


def read_params(filename):
    drone_params = {}
    station_params = {}
    M = 0
    c = 0.0
    no_fly_zones = {}

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines[1:]:
        words = line.split(",")

        if words[0] == "MaxSpeed (M)":
            M = int(words[1])
        elif words[0] == "Cost(C)":
            c = float(words[1])
        elif words[3].strip("\n") == "Noflyzone":
            # is unit guaranteed to always be meter?
            id = "NFZ" + words[0][1]
            vid = int(words[0][2]) - 1
            coord = int(words[1])
            if id not in no_fly_zones:
                no_fly_zones[id] = [[0, 0, 0] for i in range(8)]
            if words[0][0] == "X":
                no_fly_zones[id][vid][0] = coord
            if words[0][0] == "Y":
                no_fly_zones[id][vid][1] = coord
            if words[0][0] == "Z":
                no_fly_zones[id][vid][2] = coord
        elif words[3][:2] == "WH":
            id = "WH" + words[3][-2]
            coord = int(words[1])
            if id not in station_params:
                station_params[id] = [0, 0]
            if words[0][3] == "X":
                station_params[id][0] = coord
            if words[0][3] == "Y":
                station_params[id][1] = coord
        elif words[3][:8] == "Recharge":
            id = words[3].strip("\n")
            coord = int(words[1])
            if id not in station_params:
                station_params[id] = [0, 0]
            if words[0][1] == "X":
                station_params[id][0] = coord
            if words[0][1] == "Y":
                station_params[id][1] = coord
        elif words[3][:5] == "Drone":
            id = words[3].strip("\n")
            val = float(words[1])
            if id not in drone_params:
                drone_params[id] = {"speed": {"P": 0, "Q": 0}, "energy": {"A": 0, "B": 0, "C": 0}, "count": 0}
            if words[0][0] == "P":
                drone_params[id]["speed"]["P"] = val
            if words[0][0] == "Q":
                drone_params[id]["speed"]["Q"] = val
            if words[0][0] == "A":
                drone_params[id]["energy"]["A"] = val
            if words[0][0] == "B":
                drone_params[id]["energy"]["B"] = val
            if words[0][0] == "C":
                drone_params[id]["energy"]["C"] = val
            if words[0][:2] == "DT":
                drone_params[id]["count"] = val

    return drone_params, station_params, no_fly_zones, M, c
