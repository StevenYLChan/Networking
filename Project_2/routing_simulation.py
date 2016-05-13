import sys
import random
import math


# python hsim.py adjacency_list_file.txt

# Link State Routing
def link_state_routing(adj_list, no_nodes):
    average_transmissions = int(calculate_ls_average_transmissions(adj_list, no_nodes))
    average_path_length = 0
    start = 0
    garbholder = 0
    while start < no_nodes:
        costs_list = search(adj_list, no_nodes, int(start))
        temp, garbholder = add_costs(costs_list, no_nodes, garbholder)
        average_path_length += temp
        start += 1
    average_path_length /= no_nodes
    return average_transmissions, average_path_length


# Distance Vector Routing
def distance_vector_routing(adj_list, no_nodes):
    average_transmissions = 0
    average_path_length = 0
    lsp = 0
    start = 0
    while start < no_nodes:
        costs_list = search(adj_list, no_nodes, int(start))
        temp, lsp = add_costs(costs_list, no_nodes, lsp)
        average_path_length += temp
        start += 1
    average_path_length /= no_nodes

    for node in range(no_nodes):
        average_transmissions += len(adj_list[node]) * lsp
    average_transmissions /= no_nodes

    return average_transmissions, average_path_length


# Hot Potato I Routing
def hot_potato_1_routing(adj_list, no_nodes):
    src = 0
    dst = 1
    path_track = 0
    path_store = 0
    track = 0
    paths_taken = []
    transmissions_list = [0 for _ in range(10)]
    paths_list = [0 for _ in range(10)]

    for i in range(0, no_nodes):
        j = i + 1
        track += no_nodes - j

    while not track == path_track:
        if path_store < (no_nodes - 1 - src):
            paths_taken += [list()]
            # 10 tests
            test = 0
            while test < 10:
                route_discovery, src, initial = forward(adj_list, src, dst)
                length_rd = len(route_discovery)
                paths_taken[path_track].append(length_rd)
                transmissions_list[test] += length_rd

                btrace = backward(route_discovery, src)
                length_bt = len(btrace)
                paths_taken[path_track][test] += length_bt
                transmissions_list[test] += length_bt
                paths_list[test] += length_bt
                test += 1
            # update
            dst += 1
            path_store += 1
            path_track += 1
        else:
            src += 1
            path_store = 0
            dst = (src + 1)

    trial = 0
    while trial < 10:
        transmissions_list[trial] = calculator(trial, transmissions_list, no_nodes)
        paths_list[trial] = calculator(trial, paths_list, track)
        trial += 1

    average_no_transmissions = calculate_average_no_transmissions(transmissions_list)
    average_path_length = calculate_average_path_length(paths_list)

    std_no_transmissions = calculate_std(transmissions_list, average_no_transmissions)
    std_path_length = calculate_std(paths_list, average_path_length)

    ci_no_transmissions_LB, ci_no_transmissions_UB = calculate_ci(std_no_transmissions, average_no_transmissions)
    ci_no_transmissions = (ci_no_transmissions_LB, ci_no_transmissions_UB)

    ci_path_length_LB, ci_path_length_UB = calculate_ci(std_path_length, average_path_length)
    ci_path_length = (ci_path_length_LB, ci_path_length_UB)

    return average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length


# Hot Potato II Routing
def hot_potato_2_routing(adj_list, no_nodes):
    src = 0
    dst = 1
    path_track = 0
    path_store = 0
    track = 0
    paths_taken = []
    transmissions_list = [0 for _ in range(10)]
    paths_list = [0 for _ in range(10)]

    for i in range(0, no_nodes):
        j = i + 1
        track += no_nodes - j

    while not track == path_track:
        if path_store < (no_nodes - 1 - src):
            paths_taken += [list()]
            # 10 tests
            test = 0
            while test < 10:
                route_discovery, src, initial = forward2(adj_list, src, dst)
                length_rd = len(route_discovery)
                paths_taken[path_track].append(length_rd)
                transmissions_list[test] += length_rd

                btrace = backward(route_discovery, src)
                length_bt = len(btrace)
                paths_taken[path_track][test] += length_bt
                transmissions_list[test] += length_bt
                paths_list[test] += length_bt
                test += 1
            # update
            dst += 1
            path_store += 1
            path_track += 1
        else:
            src += 1
            path_store = 0
            dst = (src + 1)

    trial = 0
    while trial < 10:
        transmissions_list[trial] = calculator(trial, transmissions_list, no_nodes)
        paths_list[trial] = calculator(trial, paths_list, track)
        trial += 1

    average_no_transmissions = calculate_average_no_transmissions(transmissions_list)
    average_path_length = calculate_average_path_length(paths_list)

    std_no_transmissions = calculate_std(transmissions_list, average_no_transmissions)
    std_path_length = calculate_std(paths_list, average_path_length)

    ci_no_transmissions_LB, ci_no_transmissions_UB = calculate_ci(std_no_transmissions, average_no_transmissions)
    ci_no_transmissions = (ci_no_transmissions_LB, ci_no_transmissions_UB)

    ci_path_length_LB, ci_path_length_UB = calculate_ci(std_path_length, average_path_length)
    ci_path_length = (ci_path_length_LB, ci_path_length_UB)

    return average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length


def search(adj_list, no_nodes, start):
    # assign initial infinity
    costs_list = [9999999 for _ in range(no_nodes)]

    parse_list = list()
    parse_list2 = list()
    costs_list[start] = 0

    # all initial neighbours have a distance of only 1
    for neighbour in adj_list[start]:
        neighbour = int(neighbour)
        costs_list[neighbour] = 1
        parse_list.append(neighbour)

    dist = 2
    # as go further, distance increases by 1 each outter. min 2

    while True:
        # done going through so can stop
        if len(parse_list) == 0:
            break
        for neighbour in parse_list:
            for pos in adj_list[int(neighbour)]:
                pos = int(pos)
                if ((pos == start) or (costs_list[pos] <= dist)):
                    continue
                elif costs_list[pos] > dist:
                    costs_list[pos] = dist
                    if pos in parse_list2:
                        continue
                    else:
                        parse_list2.append(pos)
        parse_list = parse_list2
        parse_list2 = list()
        dist += 1
    return costs_list


def forward(adj_list, src, dst):
    route_discovery = list()
    previous = src
    chosen = random_Chooser(adj_list, src)
    initial = int(adj_list[src][chosen])
    route_discovery.append(initial)
    # keep going until reach dst
    while not initial == dst:
        chosen2 = random_Chooser(adj_list, initial)
        nnext = int(adj_list[initial][chosen2])
        if nnext == previous:
            if len(adj_list[initial]) != 1:
                continue
        previous = initial
        initial = nnext
        route_discovery.append(initial)
    return route_discovery, src, initial


def forward2(adj_list, src, dst):
    route_discovery = list()
    previous = src
    # the nodes know their neighbor ids and, if the destination is a neighbor,
    # the discovery packet is routed directly there; otherwise, a neighbor is chosen at random as in Hot Potato Routing I.
    if str(dst) in adj_list[src]:
        initial = dst
    else:
        chosen = random_Chooser(adj_list, src)
        initial = int(adj_list[src][chosen])
    route_discovery.append(initial)
    # keep going until reach dst
    while not initial == dst:
        if str(dst) in adj_list[initial]:
            nnext = dst
        else:
            chosen2 = random_Chooser(adj_list, initial)
            nnext = int(adj_list[initial][chosen2])
            if nnext == previous:
                if len(adj_list[initial]) != 1:
                    continue
        previous = initial
        initial = nnext
        route_discovery.append(initial)
    return route_discovery, src, initial


def backward(route_discovery, src):
    btrack = 0
    btrace = route_discovery
    for node in route_discovery:
        if node == src:
            tlist = list()
            for node in route_discovery[btrack + 1:]:
                tlist.append(node)
            btrace = tlist
        btrack += 1
    return btrace


def random_Chooser(adj_list, node):
    no_neighbours = len(adj_list[node])
    random_num = random.randint(0, no_neighbours - 1)
    return random_num


def add_costs(costs_list, no_nodes, lsp):
    ttl_cost = 0
    for cost in costs_list:
        cost = int(cost)
        if cost > lsp:
            lsp = cost
        ttl_cost += cost
    ttl_cost /= (no_nodes - 1)
    return ttl_cost, lsp


def calculator(trial, list, no):
    tvar = float(list[trial] / no)
    return tvar


def calculate_ls_average_transmissions(adj_list, no_nodes):
    transmissions = 0
    for i in range(no_nodes):
        for j in adj_list[i]:
            if j == int(i):
                continue
        transmissions += len(adj_list[i])
    average_transmissions = transmissions / 2
    return average_transmissions


def calculate_degree(adj_list):
    degree_list = list()
    for node in adj_list[1:]:
        count_degree = 0
        for neighbour in node:
            count_degree += 1
        degree_list.append(count_degree)
    return degree_list


def calculate_average_degree(degree_list):
    sum_degree = 0
    for degree in degree_list:
        sum_degree += degree
    average_degree = float(sum_degree / len(degree_list))
    return average_degree


def calculate_average_no_transmissions(transmissions_list):
    total_no_transmissions = 0.0
    for trial in transmissions_list:
        total_no_transmissions += trial
    average_no_transmissions = float(total_no_transmissions / 10)
    return average_no_transmissions


def calculate_average_path_length(paths_list):
    sum_path_lengths = 0.0
    for trial in paths_list:
        sum_path_lengths += trial
    average_path_length = float(sum_path_lengths / 10)
    return average_path_length


def calculate_std(list, average):
    # calculate standard deviation as s=sqrt(sum i=1 => T (xi-x)^2 / T-1)
    std = 0.0
    for trial in range(10):
        std += float(((list[trial] - average) ** 2))
    std = float(std / 9)
    std = math.sqrt(std)
    return std


def calculate_ci(std, average):
    # sqrt(10) because sqrt(T) and T = trials = 10
    # c1 = x - t[] * s / sqrt(t)
    # c2 = x + t[]* s / sqrt(t)
    # t[0.975;9] => 2.2622
    lower_bound = average - (2.2622 * std / (math.sqrt(10)))
    upper_bound = average + (2.2622 * std / (math.sqrt(10)))
    return lower_bound, upper_bound


def output_degree(adj_list, average_degree):
    print(adj_list[0][0] + " " + str(average_degree))


def output_ls(average_no_transmissions, average_path_length):
    print("Link State Routing: " + str(average_no_transmissions) + " " + str(average_path_length))


def output_dv(average_no_transmissions, average_path_length):
    print("Distance Vector Routing: " + str(average_no_transmissions) + " " + str(average_path_length))


def output_hp1(average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length):
    print("Hot Potato I: " + str(average_no_transmissions) + " " + str(ci_no_transmissions) + " , " + str(
        average_path_length) + " " + str(ci_path_length))


def output_hp2(average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length):
    print("Hot Potato II: " + str(average_no_transmissions) + " " + str(ci_no_transmissions) + " , " + str(
        average_path_length) + " " + str(ci_path_length))


def main():
    if (len(sys.argv) != 2):
        raise ValueError('[ERROR] Invalid number of arguments.')

    infile = open(sys.argv[1])
    adj_list = list()
    for node in infile:
        string = node.strip().split(" ")
        if '' in string:
            string.remove('')
        adj_list.append(string)

    # AVERAGE DEGREE
    degree_list = calculate_degree(adj_list)
    average_degree = calculate_average_degree(degree_list)
    output_degree(adj_list, average_degree)

    no_nodes = int(adj_list[0][0])
    del adj_list[0]

    # LINK-STATE ROUTING
    average_no_transmissions, average_path_length = link_state_routing(adj_list, no_nodes)
    output_ls(average_no_transmissions, average_path_length)

    # DISTANCE VECTOR ROUTING
    average_no_transmissions, average_path_length = distance_vector_routing(adj_list, no_nodes)
    output_dv(average_no_transmissions, average_path_length)

    # HOT POTATO ROUTING I
    average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length = hot_potato_1_routing(adj_list,
                                                                                                              no_nodes)
    output_hp1(average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length)

    # HOT POTATO ROUTING II
    average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length = hot_potato_2_routing(adj_list,
                                                                                                              no_nodes)
    output_hp2(average_no_transmissions, ci_no_transmissions, average_path_length, ci_path_length)


if __name__ == "__main__":
    main()
