from input_parser import read_demand, read_params

demand_file = "input/Demand.csv"
param_file = "input/Parameters.csv"


items = {}  # Item Master Table

items["Item-1"] = {"wt": 1, "l": 5, "b": 8, "h": 5}
items["Item-2"] = {"wt": 6, "l": 5, "b": 10, "h": 8}
items["Item-3"] = {"wt": 4, "l": 5, "b": 10, "h": 15}
items["Item-4"] = {"wt": 2, "l": 15, "b": 10, "h": 8}
items["Item-5"] = {"wt": 5, "l": 20, "b": 15, "h": 10}

demand = read_demand(demand_file)

drone_master = {}
drone_master["Drone1"] = {
    "speed": {},
    "energy": {},
    "batt": 2000,
    "base_wt": 2,
    "payload_cap": {"kg": 5, "vol": 200},
    "slots": 1,
    "count": 0,
    "cost": {"fixed": 10, "var": 5},
}
drone_master["Drone2"] = {
    "speed": {},
    "energy": {},
    "batt": 2500,
    "base_wt": 2.5,
    "payload_cap": {"kg": 6, "vol": 500},
    "slots": 1,
    "count": 0,
    "cost": {"fixed": 15, "var": 8},
}
drone_master["Drone3"] = {
    "speed": {},
    "energy": {},
    "batt": 3000,
    "base_wt": 3,
    "payload_cap": {"kg": 7, "vol": 1000},
    "slots": 2,
    "count": 0,
    "cost": {"fixed": 20, "var": 13},
}
drone_master["Drone4"] = {
    "speed": {},
    "energy": {},
    "batt": 4000,
    "base_wt": 3.5,
    "payload_cap": {"kg": 8, "vol": 2000},
    "slots": 2,
    "count": 0,
    "cost": {"fixed": 20, "var": 15},
}
drone_master["Drone5"] = {
    "speed": {},
    "energy": {},
    "batt": 5000,
    "base_wt": 4,
    "payload_cap": {"kg": 9, "vol": 3000},
    "slots": 2,
    "count": 0,
    "cost": {"fixed": 30, "var": 20},
}
drone_master["Drone6"] = {
    "speed": {},
    "energy": {},
    "batt": 10000,
    "base_wt": 5,
    "payload_cap": {"kg": 10, "vol": 5000},
    "slots": 4,
    "count": 0,
    "cost": {"fixed": 50, "var": 25},
}

station_master = {}
station_master["WH1"] = {"slots": -1, "current": 5, "loc": []}
station_master["WH2"] = {"slots": -1, "current": 5, "loc": []}
station_master["WH3"] = {"slots": -1, "current": 5, "loc": []}
station_master["Recharge1"] = {"slots": 1, "current": 3, "loc": []}
station_master["Recharge2"] = {"slots": 1, "current": 3, "loc": []}
station_master["Recharge3"] = {"slots": 1, "current": 3, "loc": []}
station_master["Recharge4"] = {"slots": 4, "current": 3, "loc": []}
station_master["Recharge5"] = {"slots": 5, "current": 3, "loc": []}


drone_params, station_params, no_fly_zones, M, c = read_params(param_file)

for drone in drone_params:
    drone_master[drone]["speed"] = drone_params[drone]["speed"]
    drone_master[drone]["energy"] = drone_params[drone]["energy"]
    drone_master[drone]["count"] = drone_params[drone]["count"]

for station in station_params:
    station_master[station]["loc"] = station_params[station]
