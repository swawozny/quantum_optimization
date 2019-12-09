import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
from dwave_qbsolv import QBSolv

from jobshopproblem import JobShopProblem


# create job shop problem instance with given jobs, machine number and time limit (respectively)
job_shop_problem = JobShopProblem.from_data([[2, 1], [1, 2]], 2, 4)

# add constraints
job_shop_problem.add_starts_once_constraint()
job_shop_problem.add_one_job_one_machine_constraint()
job_shop_problem.add_operations_order_constraint()

# transform Constraint Satisfaction Problem to Binary Quadratic and further to QUBO
bqm = dwavebinarycsp.stitch(job_shop_problem.csp, max_graph_size=16, min_classical_gap=0.6)
Q, offset = bqm.to_qubo()


# run on D'Wave computer:

# run QUBO just as it is
# response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=200)

# run with QBSolv (making big QUBO's smaller and submitting it to D'Wave)
sampler = EmbeddingComposite(DWaveSampler())
response = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=30)

# print responses received from D'Wave
for s in list(response.data()):
    print(job_shop_problem.csp.check(s.sample), s.sample, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)
