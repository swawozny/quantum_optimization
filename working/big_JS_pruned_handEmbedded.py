import dwave
import dwavebinarycsp
from dwave.embedding import embed_qubo
from dwave.system import DWaveSampler

from dwave_networkx import chimera_graph

from utils.jobshop_helpers import ones_from_sample
from utils.jobshopproblem import JobShopProblem, pruned_big_number

job_shop_problem = JobShopProblem.from_data([[2, 1], [2, 1, 2]], 2, 7)
# alfa = 0.95
# beta = 1.
# ni = 0.7
# job_shop_problem.init_coefficients(beta, alfa, ni)
job_shop_problem.add_starts_once_constraint()
job_shop_problem.add_one_job_one_machine_constraint()
job_shop_problem.add_operations_order_constraint()
job_shop_problem.add_late_penalty()

# Q, offset = dwavebinarycsp.stitch(job_shop_problem.csp, max_graph_size=16, min_classical_gap=0.6).to_qubo()
#
# response = QBSolv().sample_qubo(job_shop_problem.qubo_pruned, solver=sampler, solver_limit=30)

linear = {}
quadratic = {}
qubits_number = pruned_big_number
for i in range(qubits_number):
    linear['x{}'.format(i), 'x{}'.format(i)] = int(job_shop_problem.qubo_pruned_big[i, i])
for i in range(qubits_number):
    for j in range(i + 1, qubits_number):
        val = job_shop_problem.qubo_pruned_big[i, j]
        if (val != 0):
            quadratic['x{}'.format(i), 'x{}'.format(j)] = int(val)

Q = dict(linear)
Q.update(quadratic)

print(Q)

embedding = {}

emb_numbers = []
# print(job_shop_problem.row_length)
cells_number = int(qubits_number / 4) + 1
for i in range(cells_number):
    tmp = []
    # row
    for j in range(1, i + 1 + 1, 1):
        tmp.append(i * 128 + 4 * (2 * j - 1))
    for j in range(i, cells_number):
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

# print(embedding)
# response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=200)
#



tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=15.26)


# response = "fff"
# response = dwavebinarycsp.dimod.ExactSolver().sample_qubo(Q)
response = DWaveSampler().sample_qubo(tQ, num_reads=300)
# sampler = EmbeddingComposite(DWaveSampler())
# response = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=30)
for s in list(response.data()):
    print(ones_from_sample(s.sample), "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)
#
#

print("UNEMBEDED RESULTS")
source_bqm = dwavebinarycsp.dimod.BinaryQuadraticModel.from_qubo(Q)  # (linear, quadratic, 0, Vartype.BINARY)
suma = 0
for i, val in enumerate(dwave.embedding.unembed_sampleset(response, source_bqm=source_bqm, embedding=embedding)):
    suma += list(response.data())[i].num_occurrences
    print(ones_from_sample(val), list(response.data())[i].num_occurrences, list(response.data())[i].energy, suma,
          job_shop_problem.check_soc_constraint_big_pruned(ones_from_sample(val)),
          job_shop_problem.check_ojomc_constraint_big_pruned(ones_from_sample(val)),
          job_shop_problem.check_order_constraint_big_pruned(ones_from_sample(val)),
          job_shop_problem.get_makespan(ones_from_sample(val)))

# missing nodes: 215, 336, 577, 691, 1012, 1105, 1276, 1730, 1776, 1858
