import dwave
import dwavebinarycsp
from dwave.embedding import embed_qubo

from dwave.system import DWaveSampler
from dwave_networkx import chimera_graph

from utils.jobshop_helpers import ones_from_sample
from utils.jobshopproblem import JobShopProblem, pruned_number

job_shop_problem = JobShopProblem.from_data([[2, 1], [1,2]], 2, 4)

job_shop_problem.add_starts_once_constraint()
job_shop_problem.add_one_job_one_machine_constraint()
job_shop_problem.add_operations_order_constraint()


print(job_shop_problem.qubo)
print(job_shop_problem.qubo_pruned)
# Q, offset = dwavebinarycsp.stitch(job_shop_problem.csp, max_graph_size=16, min_classical_gap=0.6).to_qubo()
#
# response = QBSolv().sample_qubo(job_shop_problem.qubo_pruned, solver=sampler, solver_limit=30)

linear = {}
quadratic = {}
qubits_number = pruned_number
for i in range(qubits_number):
    linear['x{}'.format(i), 'x{}'.format(i)] = int(job_shop_problem.qubo_pruned[i, i])
for i in range(qubits_number):
    for j in range(i + 1, qubits_number):
        val = job_shop_problem.qubo_pruned[i, j]
        if (val != 0):
            quadratic['x{}'.format(i), 'x{}'.format(j)] = int(val)

Q = dict(linear)
Q.update(quadratic)

print(Q)

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

# for i,num in enumerate(emb_numbers):
#     print("i={}, numbers: {}".format(i,num))

for num, arr in enumerate(emb_numbers):
    for i in range(4):
        tmp_embedding = set()
        for elem in sorted(arr):
            tmp_embedding.add(elem + i + 16)

        # tmp_embedding.add(elem + i)
        # print("Num: {}, arr: {}, i: {}, embedding: {}".format(num, sorted(arr), i, sorted(tmp_embedding)))

        embedding['x{}'.format(4 * num + i)] = tmp_embedding
        # print("x{}: {}".format(4 * num + i, sorted(tmp_embedding)))

# embedding = {'x0': {0,4}, 'x1': {1,5}, 'x2': {2,6}, 'x3': {3,7}}


# response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=1000)
#

tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=7.8)

response = DWaveSampler().sample_qubo(tQ, num_reads=200)

for s in list(response.data()):
    print(ones_from_sample(s.sample), "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)
#
#

print("UNEMBEDED RESULTS")
source_bqm = dwavebinarycsp.dimod.BinaryQuadraticModel.from_qubo(Q)# (linear, quadratic, 0, Vartype.BINARY)
suma = 0
for i, val in enumerate(dwave.embedding.unembed_sampleset(response, source_bqm=source_bqm, embedding=embedding)):
    suma += list(response.data())[i].num_occurrences
    print(ones_from_sample(val), list(response.data())[i].num_occurrences, list(response.data())[i].energy, suma)
