import numpy as np

import qubo_matrices_helpers
from omnisolver.pt.sampler import PTSampler
from utils.jobshop_helpers import ones_from_sample

# WORKFLOW DATA
S = 10
P = 8
A, b, C, paths, tasks_number, machines_number, deadline = qubo_matrices_helpers.get_8_qubits_data(S)
real_qubits_number = tasks_number * machines_number

# PREPARE QUBO
D = np.diag(2 * A.transpose().dot(b))
QUBO = P * (A.transpose().dot(A) + D) + C
linear, quadratic = qubo_matrices_helpers.prepare_qubo_dicts_dwave(QUBO)
Q = dict(linear)
Q.update(quadratic)

stars = "\n********************************************************************\n"

results_file = open("ptsampler_results.txt", "a+")
results_file.write("*************PTSAMPLER****************\n")
params_string = "S={}, P={}\n".format(S, P)
results_file.write(params_string)
for sampling_iter in range(100):
    results_file.write("\nSAMPLE={}\t".format(sampling_iter + 1))
    sampler = PTSampler()
    # GET SAMPLING RESULT
    sampling_result = sampler.sample_qubo(Q, num_replicas=20, num_pt_steps=1000, num_sweeps=100, beta_min=0.5, beta_max=1.0)
    for s in list(sampling_result.data()):
        chosen_qubits = [q for q in ones_from_sample(s.sample) if q < real_qubits_number]
        slack_qubits = [q for q in ones_from_sample(s.sample) if q >= real_qubits_number]
        chosen_qubits_vector = [0 for i in range(real_qubits_number)]
        for cq in chosen_qubits:
            chosen_qubits_vector[cq] = 1
        total_qubits_len = len(A[0])
        slack_mark, times = qubo_matrices_helpers.check_chosen_and_slack_qubits(chosen_qubits_vector, slack_qubits,
                                                                                total_qubits_len,
                                                                                real_qubits_number, paths, deadline,
                                                                                qubo_matrices_helpers.create_avec(A,
                                                                                                                  paths,
                                                                                                                  real_qubits_number)
                                                                                , tasks_number, machines_number)
        deadline_mark = ""
        if max(times) > deadline:
            deadline_mark = "DEADLINE "
        tasks_number_mark = ""
        if len(list(filter(lambda x: x < real_qubits_number,
                           chosen_qubits))) != tasks_number:
            tasks_number_mark = "TASKS_NUM "
        cost = qubo_matrices_helpers.get_cost(C, real_qubits_number, chosen_qubits_vector)
        res_str = "{}{}{}{}/{},COST: {}, RESULT: {}, ENERGY: {}, OCCURRENCES: {}".format(tasks_number_mark,
                                                                                         deadline_mark, slack_mark,
                                                                                         times, deadline, cost,
                                                                                         ones_from_sample(s.sample),
                                                                                         s.energy, s.num_occurrences)
        print(res_str)
        results_file.write(res_str)

results_file = open("gurobi_results.txt", "a+")
results_file.write("*************GUROBISAMPLER***************\n")
params_string = "S={}, P={}\n".format(S, P)
results_file.write(params_string)
for sampling_iter in range(100):
    results_file.write("\nSAMPLE={}\t".format(sampling_iter + 1))
    # GET SAMPLING RESULT
    sampling_result = qubo_matrices_helpers.solve_matrix_with_gurobi(QUBO)
    for s in list(sampling_result.data()):
        chosen_qubits = [q for q in ones_from_sample(s.sample) if q < real_qubits_number]
        slack_qubits = [q for q in ones_from_sample(s.sample) if q >= real_qubits_number]
        chosen_qubits_vector = [0 for i in range(real_qubits_number)]
        for cq in chosen_qubits:
            chosen_qubits_vector[cq] = 1
        total_qubits_len = len(A[0])
        slack_mark, times = qubo_matrices_helpers.check_chosen_and_slack_qubits(chosen_qubits_vector, slack_qubits,
                                                                                total_qubits_len,
                                                                                real_qubits_number, paths, deadline,
                                                                                qubo_matrices_helpers.create_avec(A,
                                                                                                                  paths,
                                                                                                                  real_qubits_number)
                                                                                , tasks_number, machines_number)
        deadline_mark = ""
        if max(times) > deadline:
            deadline_mark = "DEADLINE "
        tasks_number_mark = ""
        if len(list(filter(lambda x: x < real_qubits_number, chosen_qubits))) != tasks_number:
            tasks_number_mark = "TASKS_NUM "
        cost = qubo_matrices_helpers.get_cost(C, real_qubits_number, chosen_qubits_vector)
        res_str = "{}{}{}{}/{},COST: {}, RESULT: {}, ENERGY: {}, OCCURRENCES: {}".format(tasks_number_mark,
                                                                                         deadline_mark, slack_mark,
                                                                                         times, deadline, cost,
                                                                                         ones_from_sample(s.sample),
                                                                                         s.energy, s.num_occurrences)
        print(res_str)
        results_file.write(res_str)
