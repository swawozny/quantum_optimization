import numpy as npa

from omnisolver.pt.sampler import PTSampler

import qubo_matrices_helpers

from utils.jobshop_helpers import ones_from_sample

stars = "\n**************************************************************************\n"

for S in [10]:
    A, b, C, paths, tasks_number, machines_number, deadline = qubo_matrices_helpers.get_8_qubits_data(S)
    real_qubits_number = tasks_number * machines_number
    for P in [8]:  # itertools.chain(range(3,13,3), range(17,35,5), range(45,76,15)):
        # SOLUTION

        D = npa.diag(2 * A.transpose().dot(b))
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
        # embedding = qubo_matrices_helpers.convert_to_x_dict(chimera.find_clique_embedding(k=qubits_number, m=16))
        maxval = max(list(Q.values()))
        minval = min(list(Q.values()))

        print(maxval)
        print(minval)

        # results_file.close()
        cs_large = abs(maxval) if abs(maxval) > abs(minval) else abs(minval)
        cs = cs_large/4.0
        results_file = open("PTSolverAllResults.txt", "a+")
        for chain_strength in [18000.0]:  # in range(100, 60000000, 8000000000):
            params_string = "P={} S={} chain_strength={}\n".format(P, S, chain_strength)
            print(params_string)
            # tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=chain_strength)
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
            sampling_result = PTSampler().sample_qubo(Q)
            # TODO try QBSolv()
            # CHECK FOR NOT EMBEDDED PROBLEM
            for s in list(sampling_result.data()):
                ss = "SAMPLE: {}, ENERGY: {}, OCCURENCES: {}".format(str([one for one in ones_from_sample(s.sample) if int(one[1:]) < machines_number * tasks_number]),
                                                                     s.energy, s.num_occurrences)
                print(ss)
                results_file.write(ss)
            # CHECK FOR EMBEDDED PROBLEM
        #     check_gaps = True
        #     list_sampling_result = list(sampling_result.data())
        #     sum = 0
        #     energies = []
        #     if check_gaps:
        #         gaps = 50.0
        #         min_num = list_sampling_result[0].energy
        #         max_num = list_sampling_result[len(list_sampling_result) - 1].energy
        #         diff = max_num - min_num
        #         gap = diff/int(gaps)
        #     for s in list_sampling_result:
        #         sum += s.num_occurrences
        #         info, cost, time = qubo_matrices_helpers.check_sample(ones_from_sample(s.sample), embedding,
        #                                                               reverse_embedding, qubits_number, C, paths,
        #                                                               tasks_number, machines_number, A, deadline)
        #         deadline_mark = ""
        #         if max(time) > deadline:
        #             deadline_mark = "DEADLINE "
        #         res_str = "{}{}, COST: {}, TIME: {}, DEADLINE: {}, ENERGY: {}, OCCURENCES: {}/{}".format(deadline_mark, info, cost, time,
        #                                                                                                  deadline,
        #                                                                                                  s.energy,
        #                                                                                                  s.num_occurrences,
        #                                                                                                  sum)
        #         energies.append(s.energy)
        #         print(res_str)
        #         results_file.write("{}\n".format(res_str))
        #     if check_gaps:
        #         gaps_sizes = []
        #         samples_index = 0
        #         tmp_reference_energy = min_num
        #         for i in range(int(gaps)):
        #             counter = 0
        #             while samples_index != len(list_sampling_result) and list_sampling_result[samples_index].energy < tmp_reference_energy + gap:
        #                 counter += 1
        #                 samples_index += 1
        #             gaps_sizes.append(counter)
        #             tmp_reference_energy += gap
        #         print(gaps_sizes)
        #         results_file.write("{}\n".format(gaps_sizes))
        # results_file.close()

# for key in sorted(reverse_embedding.keys()):
#     print("{} -> {}".format(key, reverse_embedding[key]))

# print(embedding)