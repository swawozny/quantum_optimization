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
from dwave_qbsolv import QBSolv

from qubo_solver import solve_qubo

import qubo_solver
import qubo_matrices_helpers

# DATA
from utils.jobshop_helpers import ones_from_sample
# DR RYCERZ https://uk.linkedin.com/in/andy-mason-0753a64
# DONE NIE SKALOWAĆ RYSUNKU W LATEXU!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DONE kolory: dobre/złe
# DONE wszystko ma być dobrze wytłumaczone
# DONE statystycznie jest tyle rozw popr, a dwave znalazł tyle i tyle niepoprwanych
# REJECTED tabelka: poprawne - niepoprawne - złamany łańcuch - niezłamany łańcuch (jeśli dopuszczamy łamanie łańcuchów)
# DONE educated guess
# DONE jak się isinga przeskaluje, to wszystko działa inaczej
# DONE https://www.fujitsu.com/global/digitalannealer/

stars = "\n**************************************************************************\n"
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
# 10 S=25,P=14,fact=0.000075,CS=0.5
# 10 S=25,P=14,fact=1.0,CS=6650.0
# 15 S=10, P=11, fact=1.0, CS=2800.0
# 18 S=25 P=6 fact=1 CS=14000


for S in [40]:
    A, b, C, paths, tasks_number, machines_number, deadline = qubo_matrices_helpers.get_smaller_18_qubits_data(S)
    real_qubits_number = tasks_number * machines_number
    for P in [6]:  # itertools.chain(range(3,13,3), range(17,35,5), range(45,76,15)):
        # SOLUTION
        D = np.diag(2 * A.transpose().dot(b))
        QUBO = P * (A.transpose().dot(A) + D) + C
        # X = np.array([0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,0,1,0])
        # print(qubo_matrices_helpers.calculate_energy_of_QUBO_for_result(QUBO, X))
        # raise Exception()
        # QUBO = QUBO * 0.0001
        qubits_number = len(QUBO[0])
        # linear, quadratic = qubo_matrices_helpers.prepare_qubo_dicts(QUBO)
        linear, quadratic = qubo_matrices_helpers.prepare_qubo_dicts_dwave(QUBO)
        Q = dict(linear)
        Q.update(quadratic)
        # result_list = qubo_solver.solve_qubo(QUBO)
        # qubo_matrices_helpers.gurobi_solve_no_embedding(QUBO, S,P,real_qubits_number, paths, deadline, tasks_number, machines_number, C, A)
        # continue
        embedding = qubo_matrices_helpers.find_complete_graph_embedding(qubits_number)
        # embedding = qubo_matrices_helpers.convert_to_x_dict(chimera.find_clique_embedding(k=qubits_number, m=16))
        reverse_embedding = qubo_matrices_helpers.get_reverse_embedding(embedding)
        maxval = max(list(Q.values()))
        minval = min(list(Q.values()))

        print(maxval)
        print(minval)

        # results_file.close()
        cs_large = abs(maxval) if abs(maxval) > abs(minval) else abs(minval)
        cs = cs_large/4.0
        results_file = open("gurobiAllResults.txt", "a+")
        for chain_strength in [18000.0]:  # in range(100, 60000000, 8000000000):
            params_string = "P={} S={} chain_strength={}\n".format(P, S, chain_strength)
            print(params_string)
            tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=chain_strength)
            # tQ = qubo_matrices_helpers.div_d(tQ, 40000.0)
            results_file.write(stars)
            # print(stars)
            results_file.write(params_string)
            #     SOLVE WITH GUROBI
            # sampling_result = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=100, auto_scale=True, annealing_time=20, postprocess="optimization")
            # for s in sampling_result.data():
            #     print("{}, {}, {}".format(ones_from_sample(s.sample), s.energy, s.num_occurrences))
            # raise Exception()
            # sampling_result = response = DWaveSampler().sample_qubo(tQ, num_reads=100, auto_scale=True, annealing_time=8, postprocess="optimization")
            sampling_result = qubo_matrices_helpers.solve_dict_with_gurobi(tQ)
            # TODO try QBSolv()
            # CHECK FOR NOT EMBEDDED PROBLEM
            # for s in list(sampling_result.data()):
            #     ss = "SAMPLE: {}, ENERGY: {}, OCCURENCES: {}".format(str([one for one in ones_from_sample(s.sample) if int(one[1:]) < machines_number * tasks_number]),
            #                                                          s.energy, s.num_occurrences)
            #     print(ss)
            #     results_file.write(ss)
            # CHECK FOR EMBEDDED PROBLEM
            check_gaps = True
            list_sampling_result = list(sampling_result.data())
            sum = 0
            energies = []
            if check_gaps:
                gaps = 50.0
                min_num = list_sampling_result[0].energy
                max_num = list_sampling_result[len(list_sampling_result) - 1].energy
                diff = max_num - min_num
                gap = diff/int(gaps)
            for s in list_sampling_result:
                sum += s.num_occurrences
                info, cost, time = qubo_matrices_helpers.check_sample(ones_from_sample(s.sample), embedding,
                                                                      reverse_embedding, qubits_number, C, paths,
                                                                      tasks_number, machines_number, A, deadline)
                deadline_mark = ""
                if max(time) > deadline:
                    deadline_mark = "DEADLINE "
                res_str = "{}{}, COST: {}, TIME: {}, DEADLINE: {}, ENERGY: {}, OCCURENCES: {}/{}".format(deadline_mark, info, cost, time,
                                                                                                         deadline,
                                                                                                         s.energy,
                                                                                                         s.num_occurrences,
                                                                                                         sum)
                energies.append(s.energy)
                print(res_str)
                results_file.write("{}\n".format(res_str))
            if check_gaps:
                gaps_sizes = []
                samples_index = 0
                tmp_reference_energy = min_num
                for i in range(int(gaps)):
                    counter = 0
                    while samples_index != len(list_sampling_result) and list_sampling_result[samples_index].energy < tmp_reference_energy + gap:
                        counter += 1
                        samples_index += 1
                    gaps_sizes.append(counter)
                    tmp_reference_energy += gap
                print(gaps_sizes)
                results_file.write("{}\n".format(gaps_sizes))
        results_file.close()

# for key in sorted(reverse_embedding.keys()):
#     print("{} -> {}".format(key, reverse_embedding[key]))

# print(embedding)