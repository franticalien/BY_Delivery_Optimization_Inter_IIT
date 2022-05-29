"""Capacited Vehicles Routing Problem (CVRP)."""

from pickle import PickleBuffer
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from utils import *
import math

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    
    data['distance_matrix'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]

    data['xy_matrix'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]

    data['zup_matrix'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]

    data['zdown_matrix'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]



    data['pickups_deliveries'] = [
        [0, 1],
        
        [16, 14],
    ]


    data['payloadWeights'] = [1, -1, 1, 3, 6, 3, 6, 8, 8, 1, 2, 1, 2, 6, 6, 8, 8] #weight constraints location wise, neg for drop
    data['payloadVolumes']= [100, -100, 1, 3, 6, 3, 6, 8, 8, 1, 2, 1, 2, 6, 6, 8, 8] #volume constraints location wise

    data['vehicleWeightCapacities'] = [150, 150, 150, 150] #weight capacity of each vehicle
    data['vehicleSlotCapacities'] = [150, 150, 150, 150] #weight capacity of each vehicle
    data['vehicleFuelCapacities'] = [150, 150, 150, 150] #weight capacity of each vehicle
    data['vehicleVolumeCapacities'] = [150, 150, 150, 150] #volume capacity of each vehicle

    data['time_windows'] = [
        (0, 5),  # depot
        (7, 12),  # 1
        (10, 15),  # 2
        (16, 18),  # 3
        (10, 13),  # 4
        (0, 5),  # 5
        (5, 10),  # 6
        (0, 4),  # 7
        (5, 10),  # 8
        (0, 3),  # 9
        (10, 16),  # 10
        (10, 15),  # 11
        (0, 5),  # 12
        (5, 10),  # 13
        (7, 8),  # 14
        (10, 15),  # 15
        (11, 15),  # 16
    ]
    data['num_vehicles'] = 4
    
    data['starts'] = [1, 2, 15, 16] #start location dronewise
    data['ends'] = [0, 0, 0, 0] #end location dronewise
    return data


def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    print(f'Objective: {assignment.ObjectiveValue()}')
    # Display dropped nodes.
    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    print(dropped_nodes)
    # Display routes
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['payloadWeights'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total Distance of all routes: {}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'], data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # print(dir(routing))


    # Create and register a transit callback.
    


    # Define cost of each arc.
    # routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    #TODO: custom time callbacks


    # Add Capacity constraint.
    ########### TODO: Weight scale used: 2x to avoid floats###############
    def payloadWeight_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to payloadWeights  NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['payloadWeights'][from_node]

    def payloadVolume_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to payloadVolumes  NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['payloadVolumes'][from_node]

    def isWH(index):
        #TODO: implement 
        return True
    
    def isRefuelStation(index):
        #TODO: implement 
        return True

    def getFuel(fromI, toI, index, V, W):
        ##### TODO: Test it #####
        drone = drone_indices[index]
        drone_p, drone_q, drone_a, drone_b, drone_c = drone_params[drone]['speed']['P'], drone_params[drone]['speed']['Q'], drone_params[drone]['enery']['A'], drone_params[drone]['enery']['B'], drone_params[drone]['enery']['C']
        drone_t = get_time(fromI, toI, drone_p, drone_q, 1)
        energy = drone_t * W * (drone_a + data['zup_matrix'][get_loc(fromI)][get_loc[toI]] * drone_c) + W * drone_b * get_distance[fromI][toI]
        return math.ceil(energy/2)
    
    payloadWeight_callback_index = routing.RegisterUnaryTransitCallback(
        payloadWeight_callback)
    payloadVolume_callback_index = routing.RegisterUnaryTransitCallback(
        payloadVolume_callback)

    fu=[]
    fu2=[]


    for i in range(len(data['vehicleFuelCapacities'])):
        def fuel_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]


            #TODO: custom fuel_callback time
            # return -getFuel(from_node, to_node, data['P'], data['Q'], i, -1)
    

        fuel_callback_index = routing.RegisterTransitCallback(fuel_callback)
        routing.SetArcCostEvaluatorOfVehicle(fuel_callback_index, i)
        fu.append(fuel_callback_index)

        def distance_callback(from_index, to_index):
            """Returns the time between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

            #TODO: service time, time
            # return getFuel(from_node, to_node, data['P'], data['Q'], i, -1)

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        fu2.append(transit_callback_index)




    

    weight = 'Weight'
    routing.AddDimension(
        payloadWeight_callback_index,
        360000000,  # allow waiting time
        360000000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        weight)
    weight_dimension = routing.GetDimensionOrDie(weight)

    volume = 'Volume'
    routing.AddDimension(
        payloadVolume_callback_index,
        360000000,  # allow waiting time
        360000000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        volume)
    volume_dimension = routing.GetDimensionOrDie(volume)

   
    routing.AddDimensionWithVehicleCapacity(
        payloadWeight_callback_index,
        0,  # null capacity slack
        data['vehicleWeightCapacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'WeightCapacity')
    
    routing.AddDimensionWithVehicleCapacity(
        payloadVolume_callback_index,
        0,  # null capacity slack
        data['vehicleVolumeCapacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'VolumeCapacity')
    # Allow to drop nodes.

    routing.AddDimensionWithVehicleTransitAndCapacity(
        fu,
        3600000,  
        data['vehicleFuelCapacities'],  # vehicle maximum capacities
        False,  # start cumul to zero
        'Fuel')
    # Allow to drop nodes.

    
    time = 'Time'
    routing.AddDimensionWithVehicleTransits(
        fu2,
        360000000,  # allow waiting time
        360000000,  # maximum time per vehicle
        True,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    fuel_dimension = routing.GetDimensionOrDie('Fuel')

    
    for i in range(routing.Size()):
        if( not (isWH(i) or isRefuelStation(i))):
            fuel_dimension.SlackVar(i).SetValue(0)


    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if (location_idx in data['starts']) or location_idx in data['ends']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])


    # Add time window constraints for each vehicle start node.
    # for vehicle_id in range(data['num_vehicles']):
    #     index = routing.Start(vehicle_id)
    #     time_dimension.CumulVar(index).SetRange(
    #         data['time_windows'][data['starts'][vehicle_id]][0],
    #         data['time_windows'][data['starts'][vehicle_id]][1])
    
    # for vehicle_id in range(data['num_vehicles']):
    #     index = routing.End(vehicle_id)
    #     time_dimension.CumulVar(index).SetRange(
    #         data['time_windows'][data['ends'][vehicle_id]][0],
    #         data['time_windows'][data['ends'][vehicle_id]][1])

    # for i in range(data['num_vehicles']):
    #     routing.AddVariableMinimizedByFinalizer(
    #         time_dimension.CumulVar(routing.Start(i)))
    #     routing.AddVariableMinimizedByFinalizer(
    #         time_dimension.CumulVar(routing.End(i)))
    # 
    #     

    penalty = 1000 #TODO: change penalty




    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)


        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(
                delivery_index))

        routing.solver().Add(
            time_dimension.CumulVar(pickup_index) <=
            time_dimension.CumulVar(delivery_index))



        # routing.solver().Add(
        #     time_dimension.CumulVar(pickup_index) <= data['vehicleWeightCapacities'][routing.VehicleVar(pickup_index)])

        # routing.solver().Add(
        #     weight_dimension.CumulVar(pickup_index) <= data['vehicleWeightCapacities'][routing.VehicleVar(pickup_index)])

        # routing.solver().Add(
        #     weight_dimension.CumulVar(delivery_index) <= data['vehicleWeightCapacities'][routing.VehicleVar(delivery_index)])
        
        # routing.solver().Add(
        #     volume_dimension.CumulVar(pickup_index) <= data['vehicleVolumeCapacities'][routing.VehicleVar(pickup_index)])

        # routing.solver().Add(
        #     volume_dimension.CumulVar(delivery_index) <= data['vehicleVolumeCapacities'][routing.VehicleVar(delivery_index)])

        
        # routing.solver().Add(
        #     weight_dimension.CumulVar(pickup_index) >=0)

        # routing.solver().Add(
        #     weight_dimension.CumulVar(delivery_index) >=0)
        
        # routing.solver().Add(
        #     volume_dimension.CumulVar(pickup_index) >=0)

        # routing.solver().Add(
        #     volume_dimension.CumulVar(delivery_index) >=0)

    def getRate(i):
        return 1

    

    for request in range(len(data['vehicleFuelCapacities'])):
        if(not (isWH(request) or isRefuelStation(request))):
            continue
        index = manager.NodeToIndex(request)
        if(isWH(request)):

            routing.solver().Add(
            (time_dimension.SlackVar(index)*getRate(request)) >= 
            (fuel_dimension.CumulVar(index)))

    # TODO:refuel copies, fuel optimisation using slack 

    for node in range(1, len(data['distance_matrix'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)



    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    # print(dir(time_dimension.SlackVar(0)))

    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment)


if __name__ == '__main__':
    main()
