import dwavebinarycsp

from jobshop_helpers import *

# used for ensuring, that one operation starts only once
def constraint_eight_vars_xor(a, b, c, d, e, f, g, h):
    return (a + b + c + d + e + f + g + h) == 1


def nand(first, second):
    if first == 1:
        return second == 0
    else:
        return True

class JobShopProblem(object):
    # ************************************************************************************
    # just python things to make it work
    def __init__(self, jobs, number_of_machines, time_limit):
        self.jobs = jobs
        self.number_of_machines = number_of_machines
        self.time_limit = time_limit
        self.number_of_operations = sum([len(job) for job in self.jobs])
        self.row_length = self.number_of_machines * self.number_of_operations
        self.number_of_qubits = self.row_length * self.time_limit
        self.csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

    @classmethod
    def default(self):
        return self([[2, 1], [1, 2]], 2, 4)

    @classmethod
    def from_data(self, jobs, number_of_machines, time_limit):
        return self(jobs, number_of_machines, time_limit)
    # *************************************************************************************

    # adding the proper constraints using dwavebinarycsp library

    # adding starts once constraint
    def add_starts_once_constraint(self):
        starts_once_constraints = []
        for operation_number in range(self.number_of_operations):
            tmp_operation = []
            for machine_number in range(self.number_of_machines):
                tmp_operation.extend(
                    ['x{}'.format(operation_number + self.number_of_operations * machine_number + self.row_length * time) for time
                     in
                     range(self.time_limit)])
            starts_once_constraints.append(tmp_operation)
        for constraint_variable in starts_once_constraints:
            self.csp.add_constraint(constraint_eight_vars_xor, constraint_variable)

    # adding one job on one machine constraint
    def add_one_job_one_machine_constraint(self):
        one_job_one_machine_cubits = get_one_job_one_machine_csp(self.jobs, self.row_length, self.number_of_operations,
                                                                 self.number_of_qubits, self.time_limit)
        for i, qubit_list in enumerate(one_job_one_machine_cubits):
            for qubit in qubit_list:
                self.csp.add_constraint(nand, ['x{}'.format(i), 'x{}'.format(qubit)])

    # adding order constraint
    def add_operations_order_constraint(self):
        order_constraints = csp_get_order_constraint(self.jobs, self.number_of_machines, self.time_limit, self.number_of_operations)
        for constraint in order_constraints:
            for cons_elem in constraint[1]:
                self.csp.add_constraint(nand, ['x{}'.format(constraint[0]), 'x{}'.format(cons_elem)])