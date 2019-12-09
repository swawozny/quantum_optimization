import numpy as np
from collections import defaultdict

import dimod


def solve_matrix_with_gurobi(Q):
    from gurobi_files.gurobisampler import GurobiSampler
    linear, quadratic = prepare_qubo_dicts_from_matrix(Q)
    bqm = dimod.BinaryQuadraticModel(linear,
                                     quadratic,
                                     offset=0.0,
                                     vartype=dimod.BINARY)
    # print(linear)
    # print(quadratic)
    sampler = GurobiSampler()
    sampling_res = sampler.sample(bqm, method="mip", num_reads=2000, gurobi_params_kw={"TimeLimit": 30})
    return sampling_res


def get_minimize_X_minus_Y_data():
    # MAXIMIZE X-Y
    A = np.array([[4, 2, 1, 0, 0, 0, 4, 2, 1, 0, 0, 0], [0, 0, 0, 4, 2, 1, 0, 0, 0, 4, 2, 1]])
    b = np.array([-7, -7])
    C_diag = np.array([4, 2, 1, -4, -2, -1, 0, 0, 0, 0, 0, 0])
    C = np.diag(C_diag)
    return A, b, C


def get_system_of_lin_ineqs_no_slack_data():
    # PROBABLY SYSTEM OF BINARY LINEAR INEQUALITIES
    A = np.array([
        [1, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 1, 1],
        [0, 0, 1, 1, 1, 0],
        [1, 1, 0, 1, 0, 1]
    ])
    b = np.array([-1, -1, -1, -1])
    C_diag = np.array([3, 2, 1, 1, 3, 2])
    C = np.diag(C_diag)
    return A, b, C


def get_lin_ineqs_slacks_book_data():
    # SYSTEM OF LINEAR INEQUALITIES FROM BOOK WITH TWO SLACKS
    # WARNING: THIS IS MAXIMIZATION (REVERSE PROBLEM)
    A = np.array([[2, 2, 4, 3, 2, 1, 2, 0, 0, 0],
                  [1, 2, 2, 1, 2, 0, 0, 0, 0, 0],
                  [3, 3, 2, 4, 4, 0, 0, -1, -2, -4]])
    b = np.array([-7, -4, -5])
    C_diag = [6, 4, 8, 5, 5, 0, 0, 0, 0, 0]
    C = np.diag(C_diag)
    return A, b, C


def get_smallest_workflow_data(S):
    # S = 60
    D = 100
    A = np.array([[16, 32, 8, 6, 12, 3, 32, 16, 8, 4, 2, 1],
                  [S, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, S, 0, 0, S, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, S, 0, 0, S, 0, 0, 0, 0, 0, 0]])
    b = np.array([D, -S, -S, -S])
    C_diag = [144, 288, 22, 96, 192, 48, 0, 0, 0, 0, 0, 0]
    C = np.diag(C_diag)
    paths = [[0, 1, 2]]
    return A, b, C, paths, 3, 2, 100


def get_32_qubits_data():
    D = 40
    A = np.array([
        [12, 6, 0, 0, 30, 0, 0, 24, 4, 2, 0, 0, 10, 0, 0, 8, 8, 4, 0, 0, 20, 0, 0, 16, 6, 3, 0, 0, 15, 0, 0, 12, 128,
         64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [12, 6, 0, 0, 0, 6, 0, 24, 4, 2, 0, 0, 0, 2, 0, 8, 8, 4, 0, 0, 0, 4, 0, 16, 6, 3, 0, 0, 0, 3, 0, 12, 0, 0, 0, 0,
         0, 0, 0, 0, 128, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [12, 0, 42, 0, 0, 6, 0, 24, 4, 0, 14, 0, 0, 2, 0, 8, 8, 0, 28, 0, 0, 4, 0, 16, 6, 0, 21, 0, 0, 3, 0, 12, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [12, 0, 0, 18, 0, 0, 12, 24, 4, 0, 0, 6, 0, 0, 4, 8, 8, 0, 0, 12, 0, 0, 8, 16, 6, 0, 0, 9, 0, 0, 6, 12, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 64, 32, 16, 8, 4, 2, 1],
        [500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    b = np.array([-D, -D, -D, -D, -500, -500, -500, -500, -500, -500, -500, -500])
    C_diag = [120, 60, 420, 180, 300, 60, 120, 240, 72, 36, 252, 108, 180, 36, 72, 144, 48, 24, 168, 72, 120, 24, 48,
              96, 96, 48, 336, 144, 240, 48, 96, 192
        , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C = np.diag(C_diag)
    return A, b, C


def get_18_qubits_data(S):
    D = 60
    A = np.array([
        [12, 6, 0, 18, 0, 24, 4, 2, 0, 6, 0, 8, 8, 4, 0, 12, 0, 16, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [12, 6, 0, 0, 30, 24, 4, 2, 0, 0, 10, 8, 8, 4, 0, 0, 20, 16, 0, 0, 0, 0, 0, 0, 0, 64, 32, 16, 8, 4, 2, 1, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [12, 0, 42, 18, 0, 24, 4, 0, 14, 6, 0, 8, 8, 0, 28, 12, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, 32,
         16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0],
        [12, 0, 42, 0, 30, 24, 4, 0, 14, 0, 10, 8, 8, 0, 28, 0, 20, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 64, 32, 16, 8, 4, 2, 1],
        [S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    b = np.array([-D, -D, -D, -D, -S, -S, -S, -S, -S, -S])
    C_diag = [96, 48, 336, 144, 240, 192, 72, 36, 252, 108, 180, 144, 48, 24, 168, 72, 120, 96, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C = np.diag(C_diag)
    paths = [[0, 1, 3, 5], [0, 1, 4, 5], [0, 2, 3, 5], [0, 2, 4, 5]]
    return A, b, C, paths, 6, 3, D


def get_smaller_18_qubits_data(S):
    D = 50
    A = np.array([
        [12, 6, 0, 18, 0, 24, 4, 2, 0, 6, 0, 8, 8, 4, 0, 12, 0, 16, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0],
        [12, 6, 0, 0, 30, 24, 4, 2, 0, 0, 10, 8, 8, 4, 0, 0, 20, 16, 0, 0, 0, 0, 0, 0, 0, 64, 32, 16, 8, 4, 2, 1, 0, 0,
         0, 0, 0, 0, 0],
        [12, 0, 42, 18, 0, 24, 4, 0, 14, 6, 0, 8, 8, 0, 28, 12, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, 32,
         16, 8, 4, 2, 1],
        [S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0],
        [0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0],
        [0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0],
        [0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0],
        [0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0],
        [0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0]
    ])
    b = np.array([-D, -D, -D, -S, -S, -S, -S, -S, -S])
    C_diag = [96, 48, 336, 144, 240, 192, 72, 36, 252, 108, 180, 144, 48, 24, 168, 72, 120, 96, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C = np.diag(C_diag)
    paths = [[0, 1, 3, 5], [0, 1, 4, 5], [0, 2, 3, 5]]
    return A, b, C, paths, 6, 3, D


def get_8_qubits_data(S):
    D = 19
    A = np.array([
        [6, 3, 0, 9, 2, 1, 0, 3, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0],
        [6, 0, 12, 9, 2, 0, 4, 3, 0, 0, 0, 0, 0, 16, 8, 4, 2, 1],
        [S, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, S, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, S, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, S, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    b = np.array([-D, -D, -S, -S, -S, -S])
    C_diag = [6, 3, 12, 9, 8, 4, 16, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C = np.diag(C_diag)
    paths = [[0, 1, 3], [0, 2, 3]]
    return A, b, C, paths, 4, 2, D


def get_10_qubits_data(S):
    D = 19
    A = np.array([[6, 3, 0, 0, 6, 2, 1, 0, 0, 2, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [6, 0, 12, 0, 6, 2, 0, 4, 0, 2, 0, 0, 0, 0, 0, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0],
                  [6, 0, 0, 9, 6, 2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 8, 4, 2, 1],
                  [S, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, S, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, S, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, S, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, S, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                  ])
    b = np.array([-D, -D, -D, -S, -S, -S, -S, -S])
    C_diag = [6, 3, 12, 9, 6, 8, 4, 16, 12, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C = np.diag(C_diag)
    paths = [[0,1,4],[0,2,4],[0,3,4]]
    return A, b, C, paths, 5, 2, D


def prepare_qubo_dicts_from_matrix(Q):
    linear = {i: Q[i, i] for i in range(len(Q[0]))}
    quadratic = defaultdict()
    for i in range(len(Q[0])):
        for j in range(len(Q[0])):
            if i < j:
                quadratic[(i, j)] = 2 * Q[i][j]
    return linear, quadratic


def prepare_qubo_dicts_dwave(QUBO):
    qubits_number = len(QUBO[0])
    linear = {}
    quadratic = {}
    for i in range(qubits_number):
        linear['x{}'.format(i), 'x{}'.format(i)] = float(QUBO[i, i])
    for i in range(qubits_number):
        for j in range(qubits_number):
            if i < j:
                val = QUBO[i, j]
                if val != 0:
                    quadratic['x{}'.format(i), 'x{}'.format(j)] = 2 * float(val)
    return linear, quadratic


def find_complete_graph_embedding(qubits_number):
    embedding = {}

    emb_numbers = []
    cells_number = int(qubits_number / 4) + 1
    for i in range(cells_number):
        tmp = []
        # row
        for j in range(1, i + 1 + 1, 1):
            tmp.append(i * 128 + 4 * (2 * j - 1))
        for j in range(i, cells_number):
            tmp.append(j * 128 + i * 8)
        emb_numbers.append(tmp)
    #
    # for i, num in enumerate(emb_numbers):
    #     print("i={}, numbers: {}".format(i, num))
    #
    for num, arr in enumerate(emb_numbers):
        for i in range(4):
            tmp_embedding = set()
            for elem in sorted(arr):
                tmp_embedding.add(elem + i + 0)
            # print("Num: {}, arr: {}, i: {}, embedding: {}".format(num, sorted(arr), i, sorted(tmp_embedding)))
            embedding['x{}'.format(4 * num + i)] = tmp_embedding
            # print("x{}: {}".format(4 * num + i, sorted(tmp_embedding)))
    return embedding


def get_reverse_embedding(embeddding):
    result = defaultdict()
    for key in embeddding.keys():
        for value in embeddding[key]:
            result[value] = key
    return result


def solve_dict_with_gurobi(tQ):
    from gurobi_files.gurobisampler import GurobiSampler
    linear = {}
    quadratic = {}
    for key in tQ.keys():
        if (key[0] == key[1]):
            linear[key[0]] = tQ[key]
        else:
            quadratic[key] = tQ[key]
    bqm = dimod.BinaryQuadraticModel(linear,
                                     quadratic,
                                     offset=0.0,
                                     vartype=dimod.BINARY)

    sampler = GurobiSampler()
    sampling_res = sampler.sample(bqm, method="mip", num_reads=2000, gurobi_params_kw={"TimeLimit": 30})
    return sampling_res


def check_sample(ones_list, embedding, reverse_embedding, qubits_number, C, paths, tasks_number, machines_number, A):
    qubits_for_tasks = defaultdict()
    real_qubits_number = tasks_number * machines_number

    # GET PART OF MATRIX C ONLY REFERRING TO THE ACTUAL PROBLEM
    C_small = np.zeros((real_qubits_number, real_qubits_number))
    for i in range(real_qubits_number):
        for j in range(real_qubits_number):
            C_small[i][j] = C[i][j]
    # print(C_small)

    # GET PART OF MATRIX A ONLY REFERRING TO DEADLINE CONSTRAINT
    A_small = np.zeros((len(paths), real_qubits_number))
    for p in range(len(paths)):
        for qn in range(real_qubits_number):
            A_small[p][qn] = A[p][qn]
    # print("A small: {}".format(A_small))
    A_vec = [0 for i in range(real_qubits_number)]
    for row in A_small:
        for i, element in enumerate(row):
            if element != 0:
                A_vec[i] = element
    # print("A_VEC: {}".format(A_vec))

    for t in range(tasks_number):
        qubits_for_tasks[t] = [tasks_number * m + t for m in range(machines_number)]
    paths_qubits = []
    for path in paths:
        new_path = []
        for task_index in path:
            new_path.extend(qubits_for_tasks[task_index])
        paths_qubits.append(new_path)
    reproduced_embedding = defaultdict(list)
    for qubit in ones_list:
        reproduced_embedding[reverse_embedding[qubit]].append(qubit)
    # print("REPRODUCED EMBEDDING: {}".format(reproduced_embedding))

    # COMPUTE REAL PROBLEM ENERGY (NOT QUBO ENERGY)
    chosen_qubits = [int(q[1:]) for q in reproduced_embedding.keys() if int(q[1:]) < real_qubits_number]
    chosen_qubits_vector = [0 for i in range(real_qubits_number)]
    for cq in chosen_qubits:
        chosen_qubits_vector[cq] = 1
    cost = sum(C_small.dot(chosen_qubits_vector))
    # print("PATHS QUBITS {}\n".format(paths_qubits))
    # print("ENERGY: {}".format(cost))

    # COMPUTE TIME AND RETURN
    times = [sum([A_vec[qubit_number] * chosen_qubits_vector[qubit_number] for qubit_number in single_path]) for
             single_path in paths_qubits]


    # print("TIMES: {}".format(time))

    # CHECK CHAINS AND RETURN RESULTS
    chains_broken = []
    for key in reproduced_embedding.keys():
        if int(key[1:]) < qubits_number and set(reproduced_embedding[key]) != set(embedding[key]):
            # print("key: {} < {}, {} != {}".format(key, qubits_number, set(reproduced_embedding[key]), set(embedding[key])))
            chains_broken.append(key)
    tasks_number_mark = ""
    if len(list(filter(lambda x: int(x[1:]) < real_qubits_number, list(reproduced_embedding.keys())))) != tasks_number:
        tasks_number_mark = "WRONG TASKS NUMBER"
    if len(chains_broken) == 0:
        return tasks_number_mark + str(list(filter(lambda x: int(x[1:]) < 200, list(reproduced_embedding.keys())))), cost, times
    else:
        return "CHAINS BROKEN: {} for solution {}".format(chains_broken, list(reproduced_embedding.keys())), cost, times


def convert_to_x_dict(input):
    result = defaultdict(list)
    for key in list(input.keys()):
        result['x{}'.format(key)] = input[key]
    return result


def create_problem_matrices(L, V, K, paths):
    pass


def div_d(my_dict, value):
    for i in my_dict:
        my_dict[i] = float(my_dict[i] / value)

    return my_dict
