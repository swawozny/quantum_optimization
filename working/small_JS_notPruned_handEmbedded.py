import dwave
import dwavebinarycsp
from dwave.embedding import embed_qubo

from dwave.system import DWaveSampler
from dwave_networkx import chimera_graph

from utils.jobshop_helpers import ones_from_sample
from utils.jobshopproblem import JobShopProblem


job_shop_problem = JobShopProblem.from_data([[2, 1], [1,2]], 2, 4)

job_shop_problem.add_starts_once_constraint()
job_shop_problem.add_one_job_one_machine_constraint()
job_shop_problem.add_operations_order_constraint()

print(job_shop_problem.qubo)
#
# print(job_shop_problem.csp)
# bqm = dwavebinarycsp.stitch(job_shop_problem.csp, max_graph_size=16, min_classical_gap=0.6)
#
# Q, offset = bqm.to_qubo()
# print(Q)

# response = DWaveSampler().sample_qubo(Q)
# sampler = EmbeddingComposite(DWaveSampler())
# response = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=30)
# response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=200)


# function to find embedding of one graph in another
# minorminer.find_embedding()

# for s in list(response.data()):
#     print(job_shop_problem.csp.check(s.sample), s.sample, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)
# expected_results = [-1,0,2,10,20]
# count = 0
# for row in job_shop_problem.qubo:
#     for val in row:
#         if int(val) not in expected_results:
#             count += 1
#             print(val)
# print(count)

# for row in job_shop_problem.qubo:
#     print(row)
linear = {}
quadratic = {}
qubits_number = len(job_shop_problem.qubo[0])
for i in range(qubits_number):
    linear['x{}'.format(i), 'x{}'.format(i)] = int(job_shop_problem.qubo[i, i])
for i in range(qubits_number):
    for j in range(i + 1, qubits_number):
        val = job_shop_problem.qubo[i, j]
        if (val != 0):
            quadratic['x{}'.format(i), 'x{}'.format(j)] = int(val)

Q = dict(linear)
Q.update(quadratic)
# for row in job_shop_problem.qubo:
#     print(row)
print("Prepared qubo")
embedding = {}

emb_numbers = []
# print(job_shop_problem.row_length)
cells_number = int(qubits_number/4)
for i in range(cells_number):
    tmp = []
    # row
    for j in range(1,i + 1 + 1,1):
        tmp.append(i * 128 + 4 * (2 * j - 1))
    for j in range(i,cells_number):
        tmp.append(j * 128 + i * 8)
    emb_numbers.append(tmp)

for i,num in enumerate(emb_numbers):
    print("i={}, numbers: {}".format(i,num))

for num, arr in enumerate(emb_numbers):
    for i in range(4):
        tmp_embedding = set()
        for elem in sorted(arr):
            tmp_embedding.add(elem + i + 32)

        # tmp_embedding.add(elem + i)
        # print("Num: {}, arr: {}, i: {}, embedding: {}".format(num, sorted(arr), i, sorted(tmp_embedding)))

        embedding['x{}'.format(4 * num + i)] = tmp_embedding
        print("x{}: {}".format(4 * num + i, sorted(tmp_embedding)))

    # embedding['x{}'.format(i)] = {0 + i, 4 + i, 128 + i, 256 + i, 384 + i, 512 + i, 640 + i, 768 + i, 896 + i, 1024 + i, 1152}
    # embedding['x{}'.format(i + 4)] = {132 + i, 136 + i, 140 + i, 256 + i, 384 + i, 512 + i, 640 + i, 768 + i, 896 + i, 1024 + i, 1152}
    # embedding['x{}'.format(i)] = {0 + i + 16, 4 + i + 16,128 + i + 16,256 + i + 16}
    # embedding['x{}'.format(i + 4)] = {132 + i + 16, 136 + i + 16,140 + i + 16,264 + i + 16}
    # embedding['x{}'.format(i + 8)] = {260 + i + 16, 268 + i + 16,272 + i + 16,276 + i + 16}

# for emb in list(embedding.keys()):
#     print(embedding[emb])

# sampler = VirtualGraphComposite(Sam, embedding, chain_strength=2.0)
# print("Prepared embedding, running on D'Wave computer")
# response = sampler.sample_qubo(Q, num_reads=100)
# for sample in response.samples():
#     print(sample)

# target = nx.complete_graph(12)
# embedded_qubo = embed_qubo(Q, embedding, target)
# print(embedded_qubo)
# Q2 = {('a', 'b'): 1, ('b', 'c'): 1, ('a', 'c'): 1}

# print("Embeddings")

# embedding2 = {'a': {0}, 'b': {1}, 'c': {2, 3}}
print(embedding)
#
tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=5.83)
# print(tQ)

# print(Q2)

# response = ScaleComposite(DWaveSampler()).sample(, num_reads=200)
#
# response = DWaveSampler().sample_qubo(tQ, num_reads=1000)


# print("ORIGINAL FROM D'WAVE")
sampler = DWaveSampler()
# response = QBSolv().sample_qubo(tQ, solver=sampler, solver_limit=30)
response = sampler.sample_qubo(tQ, num_reads=200)
for s in list(response.data()):
    print(ones_from_sample(s.sample), "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)

print("UNEMBEDED RESULTS")
source_bqm = dwavebinarycsp.dimod.BinaryQuadraticModel.from_qubo(Q)# (linear, quadratic, 0, Vartype.BINARY)
suma = 0
for i, val in enumerate(dwave.embedding.unembed_sampleset(response, source_bqm=source_bqm, embedding=embedding)):
    suma += list(response.data())[i].num_occurrences
    print(ones_from_sample(val), list(response.data())[i].num_occurrences, list(response.data())[i].energy, suma)
