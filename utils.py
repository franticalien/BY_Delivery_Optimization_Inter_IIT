from cmath import inf
import math
from datetime import datetime

from run import *

by_locations = {
}
all_locations = []
item_locs = []
item_indices = {}
drone_indices = []
data = {}
data['path_matrix'] = {}
data['xy_matrix'] = {}
data['zup_matrix'] = {}
data['zdown_matrix'] = {}
data['distance_matrix'] = {}

def inp_ALL(filename):
    # Read output from Bipplav and Piyush's code
    # * Expects all WH, RS, Deliveries in this order, in both locations as well as paths
    global by_locations, all_locations, item_locs, item_indices, drone_indices, data
    n_sum = 0
    with open(filename) as f:
        n_sum += inp_COORDS(f, "WH")
        n_sum += inp_COORDS(f, "RS")
        n_sum += inp_COORDS(f, "Deliveries")
        data['n'] = n_sum
        for i in range(n_sum):
            inp_PATHS(f, i, n_sum)
    
def inp_COORDS(f, s):
    global by_locations, all_locations, item_locs, item_indices, drone_indices, data
    n = int(f.readline())
    points = f.readline().split()
    locs = []
    for p in range(n):
        loc = [int(points[3*p]), int(points[3*p+1]), int(points[3*p+2])]
        locs.append(loc)
    by_locations[s] = locs
    all_locations += locs
    return n

def inp_PATHS(f, i, n):
    global by_locations, all_locations, item_locs, item_indices, drone_indices, data
    data['path_matrix'][i] = {}
    for j in range(n):
        m = f.readline().split()
        k = int(m[0])
        path = []
        points = f.readline().split()
        for p in range(k):
            point = [int(points[3*p]), int(points[3*p+1]), int(points[3*p+2])]
            path.append(point)
        data['path_matrix'][i][j] = path

def is_WH(point):
    global by_locations, all_locations, item_locs, item_indices, drone_indices, data
    if point in by_locations["WH"]:
        return True
    else:
        for i in range(len(by_locations['WH'])):
            if point in item_indices[i]:
                return True
    return False
def is_RS(point):
    global by_locations, all_locations, item_locs, item_indices, drone_indices, data
    if point in by_locations["RS"]:
        return True
    else:
        for i in range(len(by_locations['RS'])):
            if point in item_indices[i+len(by_locations['WH'])]:
                return True
    return False
def is_Delivery(point):
    global by_locations, all_locations, item_locs, item_indices, drone_indices, data
    return not (is_WH(point) or is_RS(point))

def init_data(filename, day):
    # * What Kunwar wants, a part of it anyway
    global by_locations, all_locations, item_locs, item_indices, drone_indices, data
    inp_ALL(filename)

    for i in range(data['n']):
        data['xy_matrix'][i] = {}
        data['zup_matrix'][i] = {}
        data['zdown_matrix'][i] = {}
        data['distance_matrix'][i] = {}

        for j in range(data['n']):
            xy, z_up, z_down, dist = 0, 0, 0, 0
            prev = data['path_matrix'][i][j][0]
            for p in data['path_matrix'][i][j]:
                xy += ((p[0]-prev[0])**2 + (p[1]-prev[1])**2)**0.5
                z_up += max(0, p[2]-prev[2])
                z_down += max(0, prev[2]-p[2])
                dist += ((p[0]-prev[0])**2 + (p[1]-prev[1])**2 + z_up**2 + z_down**2)**0.5
                xy, dist = math.ceil(xy), math.ceil(dist)
                prev = p
            data['xy_matrix'][i][j], data['zup_matrix'][i][j], data['zdown_matrix'][i][j], data['distance_matrix'][i][j] = xy, z_up, z_down, dist

    data['pickups_deliveries'], data['payloadWeights'], data['payloadVolumes'], data['time_windows'] = [], [], [], []
    item_indices = {}
    for d in range(len(all_locations)):
        item_indices[d] = []
    for d in demand[day]:
        data['payloadWeights'].append(2*int(items[d['item']]['wt']))
        data['payloadVolumes'].append(items[d['item']]['l'] * items[d['item']]['b'] * items[d['item']]['h'])
        data['pickups_deliveries'].append(len(data['payloadWeights'])-1)
        item_indices[(int(d['wh'][2]))-1].append(len(data['payloadWeights'])-1)
        data['time_windows'].append([-inf, inf])

        data['payloadWeights'].append(2*int(-items[d['item']]['wt']))
        data['payloadVolumes'].append(-items[d['item']]['l'] * items[d['item']]['b'] * items[d['item']]['h'])
        data['pickups_deliveries'].append(len(data['payloadWeights'])-1)
        item_indices[all_locations.index(d['d_loc'])].append(len(data['payloadWeights'])-1)
        data['time_windows'].append([int(sum(x * int(t) for x, t in zip([3600, 60, 1], d['d_time'][0].split(":")))), int(sum(x * int(t) for x, t in zip([3600, 60, 1], d['d_time'][1].split(":"))))])

    # data['xy_matrix'][data['n']], data['distance_matrix'][data['n']], data['zup_matrix'][data['n']], data['zdown_matrix'][data['n']] = {}, {}, {}, {}
    # for i in range(data['n']):
    #     if is_WH(i):
    #         data['xy_matrix'][data['n']][i], data['distance_matrix'][data['n']][i], data['zup_matrix'][data['n']][i], data['zdown_matrix'][data['n']][i] = 0, 0, 0, 0
    #     else:
    #         data['xy_matrix'][data['n']][i], data['distance_matrix'][data['n']][i], data['zup_matrix'][data['n']][i], data['zdown_matrix'][data['n']][i] = inf, inf, inf, inf
    #     data['xy_matrix'][i][data['n']], data['distance_matrix'][i][data['n']], data['zup_matrix'][i][data['n']], data['zdown_matrix'][i][data['n']] = 0, 0, 0, 0
    # data['xy_matrix'][data['n']][data['n']], data['distance_matrix'][data['n']][data['n']], data['zup_matrix'][data['n']][data['n']], data['zdown_matrix'][data['n']][data['n']] = 0, 0, 0, 0
    
    data['num_vehicles'] = int(sum(drone_master[x]['count'] for x in drone_master))
    data['vehicleWeightCapacities'], data['vehicleSlotCapacities'], data['vehicleFuelCapacities'], data['vehicleVolumeCapacities'] = [], [], [], []
    for i in drone_master:
        for x in range(int(drone_master[i]['count'])):  
            data['vehicleWeightCapacities'].append(2*drone_master[i]['payload_cap']['kg'])
            data['vehicleVolumeCapacities'].append(drone_master[i]['payload_cap']['vol'])
            data['vehicleSlotCapacities'].append(drone_master[i]['slots'])
            data['vehicleFuelCapacities'].append(drone_master[i]['batt'])
            drone_indices.append(i)

    data['start'] = [0 for _ in range(len(data['payloadWeights']))]
    data['end'] = [0 for _ in range(len(data['payloadWeights']))]



def get_time(i, j, P, Q, f):
    t = 0
    for z in item_indices:
        if i in item_indices[z]:
            x = z
            break
    else:
        x = data['n']
    for z in item_indices:
        if j in item_indices[z]:
            y = z
            break
    else:
        y = data['n']
    prev = data['path_matrix'][x][y][0]
    for p in data['path_matrix'][x][y]:
        t1 = ((p[0]-prev[0])**2 + (p[1]-prev[1])**2)**0.5 / (M-P)
        t2 = max(max(0, p[2]-prev[2]) / (M-Q), max(0, prev[2]-p[2]) / (M))
        t += max(t1.ceil(), t2.ceil())
        prev = p
    s_time = 0 if is_Delivery(j) else 180
    return t + s_time
def get_distance(i, j):
    if i == int(1e8):
        return 0 if is_WH(j) else inf
    elif j == int(1e8):
        return inf
    for z in item_indices:
        if i in item_indices[z]:
            x = z
            break
    for z in item_indices:
        if j in item_indices[z]:
            y = z
            break
    return data['distance_matrix'][x][y]
def get_loc(i):
    for z in item_indices:
        if i in item_indices[z]:
            return z