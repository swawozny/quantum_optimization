from collections import defaultdict, OrderedDict

import numpy as np


def solve_15q():
    time_matrix = np.array([[6, 3, 12, 9, 6], [2, 1, 4, 3, 2], [4, 2, 8, 6, 4]])
    cost_matrix = np.array([[6, 3, 12, 9, 6], [8, 4, 16, 12, 8], [8, 4, 16, 12, 8]])
    paths = [[0, 1, 4], [0, 2, 4], [0, 3, 4]]
    machines = [0, 1, 2]
    deadline = 17
    time_dict = defaultdict()
    for zeroth in machines:
        for first in machines:
            for second in machines:
                for third in machines:
                    for fourth in machines:
                        all = [zeroth, first, second, third, fourth]
                        path_times = []
                        for path in paths:
                            path_time = 0
                            for qubit in path:
                                path_time += time_matrix[all[qubit]][qubit]
                            path_times.append(path_time)

                        time_dict[(zeroth, first, second, third, fourth)] = path_times

    # print(time_dict)
    # print(len(list(time_dict.keys())))
    print("15Q: {}/{}".format(len(list(filter(lambda key: max(time_dict[key]) <= deadline, list(time_dict.keys())))),
                              len(list(time_dict.keys()))))
    solutions_list = list(filter(lambda key: max(time_dict[key]) <= deadline, list(time_dict.keys())))
    cost_map = defaultdict()
    for sol in solutions_list:
        cost = 0
        for i in range(5):
            cost += cost_matrix[sol[i]][i]
        cost_map[sol] = cost
    print({k: v for k, v in sorted(cost_map.items(), key=lambda item: item[1])}
          )


def solve_18q():
    time_matrix = np.array([[12, 6, 42, 18, 30, 24], [4, 2, 14, 6, 10, 8], [8, 4, 28, 12, 20, 16]])
    cost_matrix = np.array([[96,48,336,144,240,192],[72,36,252,108,180,144],[48,24,168,72,120,96]])
    machines = [0, 1, 2]
    time_dict = defaultdict()
    paths = [[0, 1, 3, 5], [0, 1, 4, 5], [0, 2, 4, 5]]
    deadline = 70
    for zeroth in machines:
        for first in machines:
            for second in machines:
                for third in machines:
                    for fourth in machines:
                        for fifth in machines:
                            all = [zeroth, first, second, third, fourth, fifth]
                            path_times = []
                            for path in paths:
                                path_time = 0
                                for qubit in path:
                                    path_time += time_matrix[all[qubit]][qubit]
                                path_times.append(path_time)

                            time_dict[(zeroth, first, second, third, fourth, fifth)] = path_times

    # print(time_dict)
    # print(len(list(time_dict.keys())))
    print("18Q : {}/{}".format(len(list(filter(lambda key: max(time_dict[key]) <= deadline, list(time_dict.keys())))),
                               len(list(time_dict.keys()))))
    solutions_list = list(filter(lambda key: max(time_dict[key]) <= deadline, list(time_dict.keys())))
    cost_map = defaultdict()
    for sol in solutions_list:
        cost = 0
        for i in range(6):
            cost += cost_matrix[sol[i]][i]
        cost_map[sol] = cost
    print({k: v for k, v in sorted(cost_map.items(), key=lambda item: item[1])})

solve_18q()
