import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
from dwave_qbsolv import QBSolv

from jobshopproblem import JobShopProblem


job_shop_problem = JobShopProblem.from_data([[2, 1], [1, 2]], 2, 4)

job_shop_problem.add_starts_once_constraint()
job_shop_problem.add_one_job_one_machine_constraint()
job_shop_problem.add_operations_order_constraint()


bqm = dwavebinarycsp.stitch(job_shop_problem.csp, max_graph_size=16, min_classical_gap=0.6)

Q, offset = bqm.to_qubo()

# response = DWaveSampler().sample_qubo(Q)
sampler = EmbeddingComposite(DWaveSampler())
response = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=30)
# response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=200)

for s in list(response.data()):
    print(job_shop_problem.csp.check(s.sample), s.sample, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)
