def solve_qubo(Q):
    result_list = []
    length = 12
    for i in range(0, 2 ** length - 1):
        test_case = [int(x) for x in '{:012b}'.format(i)]
        diagonal = sum(Q[i][i] * test_case[i] for i in range(0, length))
        rest = 0.0
        for j in range(0, length):
            for k in range(j + 1, length):
                rest += 2 * Q[j][k] * test_case[j] * test_case[k]
        result = diagonal + rest
        result_list.append((test_case, result))
        # print("Number: {}, result: {}".format(test_case, result))
    return result_list

# P=30
# qubo_for_minimum_vertex_cover = [[1-4*P,P,P,0,0],
#         [P,1-4*P,0,P,0],
#         [P,0,1-6*P,P,P],
#         [0,P,P,1-6*P,P],
#         [0,0,P,P,1-4*P]]
#
# qubo_for_simple_ilp = \
#     [[4-40*P,8*P,4*P,0,0,0,16*P,8*P,4*P,0,0,0],
#     [8*P,2-24*P,2*P,0,0,0,8*P,4*P,2*P,0,0,0],
#     [4*P,2*P,1-13*P,0,0,0,4*P,2*P,1*P,0,0,0],
#     [0,0,0,-4-40*P,8*P,4*P,0,0,0,16*P,8*P,4*P],
#     [0,0,0,8,-2-24*P,2*P,0,0,0,8*P,4*P,2*P],
#     [0,0,0,4*P,2*P,-1-14*P,0,0,0,4*P,2*P,1*P],
#     [16*P,8*P,4*P,0,0,0,-40*P,8*P,4*P,0,0,0],
#     [8*P,4*P,2*P,0,0,0,8*P,-24*P,2*P,0,0,0],
#     [4*P,2*P,1*P,0,0,0,4*P,2*P,-13*P,0,0,0],
#     [0,0,0,16*P,8*P,4*P,0,0,0,-40*P,8*P,4*P],
#     [0,0,0,8*P,4*P,2*P,0,0,0,8*P,-24*P,2*P],
#     [0,0,0,4*P,2*P,1*P,0,0,0,4*P,2*P,-13*P]]
#
# print(qubo_for_simple_ilp)
#
#
