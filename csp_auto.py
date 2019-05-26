import dwavebinarycsp
import dimod
from dwave.system import DWaveSampler, EmbeddingComposite
import helpers


def eight_one_one(a, b, c, d, e, f, g, h):  # works for both dwavebinarycsp.BINARY and dwavebinarycsp.SPIN
    return (a + b + c + d + e + f + g + h) == 1

def sixteen_one_one(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p):
    return (a + b + c + d + e + f + g + h + i + j + k + l +  + n + o + p) == 1


def ten_one_one(a, b, c, d, e, f, g, h, i, j):
    return a + b + c + d + e + f + g + h + i + j == 1


def all_equal(a, b, c):
    return a == b and b == c




def first_one_rest_zero_three(first, arg1, arg2, arg3):
    if first == 1:
        return arg1 == 0 and arg2 == 0 and arg3 == 0
    else:
        return True


def first_one_rest_zero_six(first, arg1, arg2, arg3, arg4, arg5, arg6):
    if first == 1:
        return arg1 == 0 and arg2 == 0 and arg3 == 0 and arg4 == 0 and arg5 == 0 and arg6 == 0
    else:
        return True


# csp = dwavebinarycsp.factories.random_2in4sat(8, 4)  # 8 variables, 4 clauses
#


csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
jobs = [[2, 1], [1, 2]]
number_of_machines = 2
time_limit = 4
number_of_operations = sum([len(job) for job in jobs])
row_length = number_of_machines * number_of_operations
number_of_qubits = row_length * time_limit

# adding starts once constraint
starts_once_constraints = []
for operation_number in range(number_of_operations):
    tmp_operation = []
    for machine_number in range(number_of_machines):
        tmp_operation.extend(['x{}'.format(operation_number + number_of_operations * machine_number + row_length * time) for time in range(time_limit)])
    starts_once_constraints.append(tmp_operation)

for constraint_variable in starts_once_constraints:
    print("Adding {}".format(constraint_variable))
    csp.add_constraint(eight_one_one, constraint_variable)

# adding one job on one machine constraint
one_job_one_machine_cubits = helpers.get_one_job_one_machine_csp(jobs, row_length, number_of_operations, number_of_qubits, time_limit)
for i, qubit_list in enumerate(one_job_one_machine_cubits):
    small = 3
    big = 6
    if len(qubit_list) == big:
        print("Adding {}, {}".format(i, qubit_list))
        csp.add_constraint(first_one_rest_zero_six,
                           ['x{}'.format(i), 'x{}'.format(qubit_list[0]), 'x{}'.format(qubit_list[1]),
                            'x{}'.format(qubit_list[2]), 'x{}'.format(qubit_list[3]),
                            'x{}'.format(qubit_list[4]), 'x{}'.format(qubit_list[5])])
    if len(qubit_list) == small:
        print("Adding {}, {}".format(i, qubit_list))
        csp.add_constraint(first_one_rest_zero_three,
                           ['x{}'.format(i), 'x{}'.format(qubit_list[0]), 'x{}'.format(qubit_list[1])
                               , 'x{}'.format(qubit_list[2])])
    if (len(qubit_list) != small and len(qubit_list) != big):
        raise Exception


# adding order constraint


bqm = dwavebinarycsp.stitch(csp, max_graph_size=16, min_classical_gap=0.6)

Q, offset = bqm.to_qubo()
# print(bqm.to_qubo())

response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=100)
for s in list(response.data()):
    print(s.sample, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)



