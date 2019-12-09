import dwavebinarycsp

from utils.jobshop_helpers import *
import networkx as nx
import numpy as np

factor = 10.0
penalty_coefficient = 1.32
def constraint_eight_vars_xor(*args):
    return sum(args) == 1
    # return (a + b + c + d) == 1


def nand(first, second):
    if first == 1:
        return second == 0
    else:
        return True

pruned_number = 16
pruned_big_number = 38
class JobShopProblem(object):
    def __init__(self, jobs, number_of_machines, time_limit):
        self.graph = nx.Graph()
        self.jobs = jobs
        self.number_of_machines = number_of_machines
        self.time_limit = time_limit
        self.number_of_operations = sum([len(job) for job in self.jobs])
        self.row_length = self.number_of_machines * self.number_of_operations
        self.number_of_qubits = self.row_length * self.time_limit
        self.csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        self.qubo = np.zeros((self.number_of_qubits, self.number_of_qubits))
        self.qubo_pruned = np.zeros((pruned_number, pruned_number))
        self.qubo_pruned_big = np.zeros((pruned_big_number, pruned_big_number))
        self.starts_once_coefficient = 1.0
        self.one_job_one_machine_coefficient = 1.0
        self.order_coefficient = 1.0
        for i in range(self.number_of_qubits):
            self.graph.add_node(i, value=1)
        self.big_pruned_times = self.prepareTimes()

    def init_coefficients(self, starts_once_coefficient, one_job_one_machine_coefficient, order_coefficient):
        self.starts_once_coefficient = starts_once_coefficient
        self.one_job_one_machine_coefficient = one_job_one_machine_coefficient
        self.order_coefficient = order_coefficient

    @classmethod
    def default(self):
        return self([[2, 1], [1, 2]], 2, 4)

    @classmethod
    def from_data(self, jobs, number_of_machines, time_limit):
        return self(jobs, number_of_machines, time_limit)

    pruned_soc_list = [[1, 2, 3], [2, 3], [3], [], [5, 6, 7], [6, 7], [7], [], [9, 10, 11], [10, 11], [11], [],
                       [13, 14, 15], [14, 15], [15], []]
    pruned_big_soc_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [2, 3, 4, 5, 6, 7, 8, 9], [3, 4, 5, 6, 7, 8, 9],
                           [4, 5, 6, 7, 8, 9], [5, 6, 7, 8, 9],
                           [6, 7, 8, 9], [7, 8, 9], [8, 9], [9], [],
                           [11, 12, 13, 14, 15, 16, 17, 18, 19], [12, 13, 14, 15, 16, 17, 18, 19],
                           [13, 14, 15, 16, 17, 18, 19], [14, 15, 16, 17, 18, 19], [15, 16, 17, 18, 19],
                           [16, 17, 18, 19], [17, 18, 19], [18, 19], [19], [],
                           [21, 22, 23, 24, 25], [22, 23, 24, 25], [23, 24, 25], [24, 25], [25],
                           [], [27, 28, 29, 30, 31], [28, 29, 30, 31], [29, 30, 31], [30, 31],
                           [31], [], [33, 34, 35, 36, 37], [34, 35, 36, 37], [35, 36, 37], [36, 37], [37], []]
    pruned_ojomc_list = [[8, 9, 12], [4, 9, 12, 13], [10, 11, 14], [6, 11, 14, 15], [12, 13], [13], [14, 15], [15], [],
                         [12], [], [14], [13], [], [15], []]
    pruned_ojomc_list_big = [[1, 20, 21], [2, 10, 20, 21, 22, 26], [3, 10, 11, 21, 22, 26, 27, 32],
                             [4, 11, 12, 22, 27, 28, 32, 33], [12, 13, 28, 32, 33, 34],
                             [6, 23, 24], [7, 15, 23, 24, 25, 29], [8, 15, 16, 24, 25, 29, 30, 35],
                             [9, 16, 17, 25, 30, 31, 35, 36], [17, 18, 31, 35, 36, 37],
                             [21, 22, 26], [22, 27, 32], [28, 32, 33], [33, 34], [34, 35],
                             [24, 25, 29], [25, 30, 35], [31, 35, 36], [36, 37], [37],
                             [21], [22, 26], [26, 27, 32], [24], [25, 29],
                             [29, 30, 35], [], [32], [32, 33], [],
                             [35], [35, 36], [], [34], [], [36], [37], []]
    pruned_order_list = [[], [4, 6], [], [4, 6], [], [], [], [], [], [12, 14], [], [12, 14], [], [], [], []]
    pruned_order_list_big = [[], [10, 15], [10, 11, 15, 16], [10, 11, 12, 15, 16, 17], [10, 11, 12, 13, 15, 16, 17, 18],
                             [], [10, 15], [10, 11, 15, 16], [10, 11, 12, 15, 16, 17], [10, 11, 12, 13, 15, 16, 17, 18],
                             [], [], [], [], [],
                             [], [], [], [], [],
                             [], [26, 29], [26, 27, 29, 30], [], [26, 29],
                             [26, 27, 29, 30], [], [32], [32, 33], [],
                             [35], [35, 36], [], [], [],
                             [], [], []]
    pruned_big_time_list = [[0, 5, 20, 23], [1, 6, 21, 24], [2, 7, 10, 15, 22, 25, 26, 29],
                            [3, 8, 11, 16, 27, 30, 32, 35],
                            [4, 9, 12, 17, 28, 31, 33, 36], [13, 18, 34, 37], [14, 19]]
    def add_starts_once_constraint(self):

        # adding starts once constraint
        starts_once_constraints = []
        for operation_number in range(self.number_of_operations):
            tmp_operation = []
            for machine_number in range(self.number_of_machines):
                tmp_operation.extend(
                    [operation_number + self.number_of_operations * machine_number + self.row_length * time
                     for time in
                     range(self.time_limit)])
            starts_once_constraints.append(tmp_operation)
        for constraint_variable in starts_once_constraints:
            for v in constraint_variable:
                for w in constraint_variable:
                    if v == w:
                        self.qubo[v,w] += -1.0 * self.starts_once_coefficient * factor
                    else:
                        self.qubo[v,w] += 2.0 *  self.starts_once_coefficient * factor

            self.csp.add_constraint(constraint_eight_vars_xor, ['x{}'.format(var) for var in constraint_variable])
        for qubit_number in range(pruned_number):
            for reference_qubit_number in self.pruned_soc_list[qubit_number]:
                self.qubo_pruned[qubit_number, reference_qubit_number] += 2.0 * self.starts_once_coefficient * factor
            self.qubo_pruned[qubit_number, qubit_number] += -1.0 * self.starts_once_coefficient * factor
        for qubit_number in range(pruned_big_number):
            for reference_qubit_number in self.pruned_big_soc_list[qubit_number]:
                self.qubo_pruned_big[qubit_number, reference_qubit_number] += 2.0 * self.starts_once_coefficient * factor
            self.qubo_pruned_big[qubit_number, qubit_number] += -1.0 * self.starts_once_coefficient * factor

    def check_soc_constraint_big_pruned(self, points_list):
        points = [int(x[1:]) for x in points_list]
        # for every point, that is checked
        for checked_point in points:
            for forbidden_point in self.pruned_big_soc_list[checked_point]:
                for compared_point in points:
                    if forbidden_point == compared_point and checked_point != compared_point:
                        return 0
        return 1

    def check_ojomc_constraint_big_pruned(self, points_list):
        points = [int(x[1:]) for x in points_list]
        # for every point, that is checked
        for checked_point in points:
            for forbidden_point in self.pruned_ojomc_list_big[checked_point]:
                for compared_point in points:
                    if forbidden_point == compared_point and checked_point != compared_point:
                        return 0
        return 1

    def check_order_constraint_big_pruned(self, points_list):
        points = [int(x[1:]) for x in points_list]
        # for every point, that is checked
        for checked_point in points:
            for forbidden_point in self.pruned_order_list_big[checked_point]:
                for compared_point in points:
                    if forbidden_point == compared_point and checked_point != compared_point:
                        return 0
        return 1

    def add_one_job_one_machine_constraint(self):
        # adding one job on one machine constraint
        one_job_one_machine_cubits = get_one_job_one_machine_csp(self.jobs, self.row_length, self.number_of_operations,
                                                                         self.number_of_qubits, self.time_limit)
        for i, qubit_list in enumerate(one_job_one_machine_cubits):
            for qubit in qubit_list:
                # self.graph.add_edge(i, qubit, value=10)
                self.qubo[i, qubit] += self.one_job_one_machine_coefficient * factor * 1.0
                self.csp.add_constraint(nand, ['x{}'.format(i), 'x{}'.format(qubit)])
        for qubit in range(pruned_number):
            for reference in self.pruned_ojomc_list[qubit]:
                self.qubo_pruned[qubit, reference] += self.one_job_one_machine_coefficient * factor * 1.0
        for qubit in range(pruned_big_number):
            for reference in self.pruned_ojomc_list_big[qubit]:
                self.qubo_pruned_big[qubit, reference] += self.one_job_one_machine_coefficient * factor * 1.0

    def add_operations_order_constraint(self):
        # adding order constraint
        order_constraints = csp_get_order_constraint(self.jobs, self.number_of_machines, self.time_limit, self.number_of_operations)
        for constraint in order_constraints:
            for cons_elem in constraint[1]:
                # self.graph.add_edge(constraint[0], cons_elem, value=20)
                self.qubo[constraint[0], cons_elem] += self.order_coefficient * factor * 1.0
                self.csp.add_constraint(nand, ['x{}'.format(constraint[0]), 'x{}'.format(cons_elem)])
        for qubit in range(pruned_number):
            for reference in self.pruned_order_list[qubit]:
                self.qubo_pruned[qubit, reference] += self.order_coefficient * factor * 1.0
        for qubit in range(pruned_big_number):
            for reference in self.pruned_order_list_big[qubit]:
                self.qubo_pruned_big[qubit, reference] += self.order_coefficient * factor * 1.0

    def add_late_penalty(self):
        pass
        for i, q_list in enumerate(self.pruned_big_time_list):
            for q in q_list:
                self.qubo_pruned_big[q,q] += -1 + penalty_coefficient ** (i+1)

    def get_makespan(self, result):
        points = [int(x[1:]) for x in result]
        makespan = max([self.big_pruned_times[qubit] for qubit in points])
        return makespan + 1

    def prepareTimes(self):
        result = {}
        for time, timelist in enumerate(self.pruned_big_time_list):
            for qubit in timelist:
                result[qubit] = time
        return result

