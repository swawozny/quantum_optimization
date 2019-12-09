import itertools
from collections import defaultdict

import dwavebinarycsp
from dimod import SimulatedAnnealingSampler
from dwave.cloud import Solver
from dwave.embedding import embed_qubo, chimera

import dimod
import dwave
import numpy as np
from dwave.system import DWaveSampler, EmbeddingComposite
from dwave_networkx import chimera_graph

from qubo_solver import solve_qubo

import qubo_solver
import qubo_matrices_helpers

# DATA
from utils.jobshop_helpers import ones_from_sample

# print("*************************************")
# print("PARAMETERS")
# params = DWaveSampler().parameters
# for key in params.keys():
#     print("  {}: {}".format(key, params[key]))
# print("*************************************")
# print("PROPERTIES")
# props = DWaveSampler().properties
# for key in props.keys():
#     print("  {}: {}".format(key, props[key]))

# raise Exception()
# 8 qubits: S=30, P=0.2
# 8 qubits: P=12,S=30,fact=0.0005,CS=4.0,AT=20
# 8q P8 S20 div 12000.0
# 8q P8 S10 no div CS1200
# 10? S=25,P=14,fact=0.000075,CS=0.5

for S in range(25, 710, 1000):
    A, b, C, paths, tasks_number, machines_number, deadline = qubo_matrices_helpers.get_smaller_18_qubits_data(S)
    for P in [12]:  # itertools.chain(range(3,13,3), range(17,35,5), range(45,76,15)):
        # SOLUTION
        D = np.diag(2 * A.transpose().dot(b))
        QUBO = P * (A.transpose().dot(A) + D) + C
        # QUBO = QUBO * 0.000500
        qubits_number = len(QUBO[0])
        # linear, quadratic = qubo_matrices_helpers.prepare_qubo_dicts(QUBO)
        linear, quadratic = qubo_matrices_helpers.prepare_qubo_dicts_dwave(QUBO)
        Q = dict(linear)
        Q.update(quadratic)
        # result_list = qubo_solver.solve_qubo(QUBO)
        embedding = qubo_matrices_helpers.find_complete_graph_embedding(qubits_number)
        # embedding = qubo_matrices_helpers.convert_to_x_dict(chimera.find_clique_embedding(k=qubits_number, m=16))
        reverse_embedding = qubo_matrices_helpers.get_reverse_embedding(embedding)

        results_file = open("results.txt", "a+")

        for chain_strength in [30000]:  # in range(100, 60000000, 8000000000):
            tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=chain_strength)
            # tQ = qubo_matrices_helpers.div_d(tQ, 4000.0)
            stars = "********************************************************************\n"
            results_file.write(stars)
            print(stars)
            params_string = "P={} S={} chain_strength={}\n".format(P, S, chain_strength)
            results_file.write(params_string)
            print(params_string)
            #     SOLVE WITH GUROBI
            # sampling_result = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=100, auto_scale=True, annealing_time=20, postprocess="optimization")
            # for s in sampling_result.data():
            #     print("{}, {}, {}".format(ones_from_sample(s.sample), s.energy, s.num_occurrences))
            # raise Exception()
            sampling_result = response = DWaveSampler().sample_qubo(tQ, num_reads=50, auto_scale=True, annealing_time=20, postprocess="optimization")
            # sampling_result = qubo_matrices_helpers.solve_dict_with_gurobi(Q)
            # CHECK FOR NOT EMBEDDED PROBLEM
            # for s in list(sampling_result.data()):
            #     ss = "SAMPLE: {}, ENERGY: {}, OCCURENCES: {}".format(str([one for one in ones_from_sample(s.sample) if int(one[1:]) < machines_number * tasks_number]),
            #                                                          s.energy, s.num_occurrences)
            #     print(ss)
            #     results_file.write(ss)
            # CHECK FOR EMBEDDED PROBLEM
            sum = 0
            for s in list(sampling_result.data()):
                sum += s.num_occurrences
                info, cost, time = qubo_matrices_helpers.check_sample(ones_from_sample(s.sample), embedding,
                                                                      reverse_embedding, qubits_number, C, paths,
                                                                      tasks_number, machines_number, A)
                deadline_mark = ""
                if max(time) > deadline:
                    deadline_mark = "DEADLINE"
                res_str = "{}{}, COST: {}, TIME: {}, DEADLINE: {}, ENERGY: {}, OCCURENCES: {}/{}".format(deadline_mark, info, cost, time,
                                                                                                      deadline,
                                                                                                      s.energy,
                                                                                                      s.num_occurrences,
                                                                                                         sum)
                print(res_str)
            #     results_file.write(res_str)
        results_file.close()

# for key in sorted(reverse_embedding.keys()):
#     print("{} -> {}".format(key, reverse_embedding[key]))

# print(embedding)