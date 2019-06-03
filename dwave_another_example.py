import math

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import numpy as np
# Set Q for the problem QUBO
from jobshop_helpers import get_machine_and_time_slot, get_operation_length, is_last_row, get_qubits_from_slot_and_machine, \
   get_time_slot


def main():
   # qubo_matrix = np.zeros((40,40))
   jobs = [[2, 1], [1,2]]
   j_flat = []
   for job in jobs:
      j_flat.extend(job)

   time_limit = 5
   number_of_machines = 2
   qubits_number = number_of_machines * len(j_flat) * time_limit
   connections = prepare_connections(jobs, number_of_machines, time_limit)

   linear = {}
   quadratic = {}
   for i in range(qubits_number):
      linear['x{}'.format(i), 'x{}'.format(i)] = int(connections[i,i])
   for i in range(qubits_number):
      for j in range(i + 1, qubits_number):
         val = connections[i,j]
         if (val != 0):
            quadratic['x{}'.format(i), 'x{}'.format(j)] = int(val)

   # linear = {('x0', 'x0'): -1, ('x1', 'x1'): -1, ('x2', 'x2'): -1, ('x3', 'x3'): -1,
   #           ('x4', 'x4'): -1, ('x5', 'x5'): -1, ('x6', 'x6'): -1, ('x7', 'x7'): -1}
   # quadratic = {('x0', 'x2'): 2, ('x0', 'x4'): 2, ('x0', 'x6'): 2, ('x2', 'x4'): 2, ('x2', 'x6'): 2, ('x4', 'x6'): 2,
   #              ('x1', 'x3'): 2, ('x1', 'x5'): 2, ('x1', 'x7'): 2, ('x3', 'x5'): 2, ('x3', 'x7'): 2, ('x5', 'x7'): 2}
   # quadratic = {('x0', 'x2'): 2, ('x0', 'x4'): 2, ('x0', 'x6'): 2, ('x1', 'x3'): 2, ('x1', 'x5'): 2, ('x1', 'x7'): 2,
   #              ('x2', 'x4'): 2, ('x2', 'x6'): 2, ('x3', 'x5'): 2, ('x3', 'x7'): 2
   #               , ('x4', 'x6'): 2,('x5', 'x7'): 2}
   print(linear)
   print(quadratic)
   Q = dict(linear)
   Q.update(quadratic)
   # Minor-embed and sample 1000 times on a default D-Wave system
   # response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=100)
   # for s in list(response.data()):
   #    print(s.sample, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)


def add_starts_only_once_constraint(connections, row_length, number_of_qubits, number_of_operations, multiplier):
   starting_points = range(row_length)
   only_one_one_qubits_lists = [list(range(starting_point, number_of_qubits, number_of_operations)) for starting_point in starting_points]
   for oper_list in only_one_one_qubits_lists:
      for qubit in oper_list:
         connections[qubit, qubit] = -1 * multiplier
         print("-1 for [{}, {}]".format(qubit, qubit))
      for (i, first_elem) in enumerate(oper_list):
         for (j, second_elem) in enumerate(oper_list[i + 1:]):
            connections[first_elem, second_elem] = 2 * multiplier
            print("2 for [{}, {}]".format(first_elem, second_elem))

   return connections


def add_one_job_on_machine_constraint(connections, jobs, row_length, number_of_operations, number_of_qubits, time_limit, multiplier):

   for qubit_number in range(number_of_qubits):
       machine_number, time_slot = get_machine_and_time_slot(qubit_number, row_length, number_of_operations)
       operation_number = qubit_number % number_of_operations
       operation_length = get_operation_length(jobs, operation_number)
       if (is_last_row(time_slot, time_limit)):
          shift = 0
          qubits = get_qubits_from_slot_and_machine(machine_number, time_slot + shift, number_of_operations, row_length)
          for qubit in qubits:
             connections[qubit_number, qubit] += multiplier
       else:
          for shift in range(operation_length):
             qubits = get_qubits_from_slot_and_machine(machine_number, time_slot + shift, number_of_operations,
                                                       row_length)
             print("For qubit {} qubits are {}".format(qubit_number, list(qubits)))
             for qubit in qubits:
                if (qubit - qubit_number) % row_length != 0:
                   connections[qubit_number, qubit] += multiplier

   
   for (i,c) in enumerate(connections):
      print(i, c)

   return connections


def get_global_op_num(job_lens, job_number, checked_op_num):
   previous_operations_number = 0
   for job_len in job_lens[:job_number]:
      previous_operations_number += job_len
   return previous_operations_number + checked_op_num


def get_qubits_for_operation(job_number, checked_op_num, job_lens, number_of_machines, time_limit, number_of_operations):
   global_op_num = get_global_op_num(job_lens, job_number, checked_op_num)
   row_len = number_of_machines * number_of_operations
   qubits = []
   for machine_number in range(1,number_of_machines + 1):
      qubits.extend([global_op_num + (number_of_operations * (machine_number - 1)) + row_len * cur_time for cur_time in range(time_limit)])
   return qubits

def add_order_constraint(connections, jobs, number_of_machines, time_limit, number_of_operations, multiplier):
   job_lens = [len(job) for job in jobs]
   row_len = number_of_machines * number_of_operations
   # for every job
   for (job_number, job) in enumerate(jobs):
      # for every operation except first in job
      for checked_op_num in range(1,len(job)):
         qubits_for_checked_op = get_qubits_for_operation(job_number, checked_op_num, job_lens,
                                                          number_of_machines, time_limit, number_of_operations)
         # for every operation, that is before operation with number op_num
         for (tmp_op_num, tmp_op_len) in enumerate(job[:checked_op_num]):
            qubits_for_tmp_op = get_qubits_for_operation(job_number, tmp_op_num, job_lens,
                                                          number_of_machines, time_limit, number_of_operations)
         #    print("Job: {}, Checked op_num: {}, tmp op num: {}, tmp op len: {}".format(job, checked_op_num, tmp_op_num, tmp_op_len))
            for qubit_checked_op in qubits_for_checked_op:
               for qubit_tmp_op in qubits_for_tmp_op:
                  checked_op_time_slot = get_time_slot(qubit_checked_op, row_len)
                  tmp_op_time_slot = get_time_slot(qubit_tmp_op, row_len)
                  if checked_op_time_slot - tmp_op_time_slot < tmp_op_len:
                     connections[qubit_tmp_op, qubit_checked_op] += multiplier
   return connections

def prepare_connections(jobs, number_of_machines, time_limit):

   # jobs = [[2,1],[1,2]]


   number_of_operations = sum([len(job) for job in jobs])
   number_of_qubits = number_of_machines * number_of_operations * time_limit
   row_length = number_of_machines * number_of_operations

   beta = 1
   eta = -1
   alpha = 1

   connections = np.zeros((number_of_qubits, number_of_qubits))
   # connections = add_starts_only_once_constraint(connections, row_length, number_of_qubits, number_of_operations, beta)
   connections = add_one_job_on_machine_constraint(connections, jobs, row_length, number_of_operations,
                                                   number_of_qubits, time_limit, alpha)
   # connections = add_order_constraint(connections, jobs, number_of_machines, time_limit, number_of_operations, eta)
   # for (num, conn) in enumerate(connections):
   #    print(num, conn)




   # connections = [[] for i in range(40)]
   # connections[0] = [1, 2, 3, 8, 9, 10, 11, 16, 24, 32]
   # connections[1] = [2, 3, 8, 9, 16, 17, 24, 25, 32, 33]
   # connections[2] = [3, 10, 18, 26, 34]
   # connections[3] = [8, 9, 10, 11, 18, 19, 26, 27, 34, 35]
   # connections[4] = [5, 6, 7, 12, 13, 14, 15, 20, 28, 36]
   # connections[5] = [6, 7, 12, 13, 20, 21, 28, 29, 36, 37]
   # connections[6] = [7, 14, 22, 30, 38]
   # connections[7] = [12, 13, 14, 15, 22, 23, 30, 31, 38, 39]
   # connections[8] = [9, 10, 11, 16, 17, 18, 19, 24, 32]
   # connections[9] = [10, 11, 16, 17, 24, 25, 32, 33]
   # connections[10] = [11, 18, 26, 34]
   # connections[11] = [16, 17, 18, 19, 26, 27, 34, 35]
   # connections[12] = [13, 14, 15, 20, 21, 22, 23, 28, 36]
   # connections[13] = [14, 15, 20, 21, 28, 29, 36, 37]
   # connections[14] = [15, 22, 30, 38]
   # connections[15] = [20, 21, 22, 23, 30, 31, 38, 39]
   # connections[16] = [17, 18, 19, 24, 25, 26, 27, 32]
   # connections[17] = [18, 19, 24, 25, 32, 33]
   # connections[18] = [19, 26, 34]
   # connections[19] = [24, 25, 26, 27, 34, 35]
   # connections[20] = [21, 22, 23, 28, 29, 30, 31, 36]
   # connections[21] = [22, 23, 28, 29, 36, 37]
   # connections[22] = [23, 30, 38]
   # connections[23] = [28, 29, 30, 31, 38, 39]
   # connections[24] = [25, 26, 27, 32, 33, 34, 35]
   # connections[25] = [26, 27, 32, 33]
   # connections[26] = [27, 34]
   # connections[27] = [32, 33, 34, 35]
   # connections[28] = [29, 30, 31, 36, 37, 38, 39]
   # connections[29] = [30, 31, 36, 37]
   # connections[30] = [31, 38]
   # connections[31] = [36, 37, 38, 39]
   # connections[32] = [32, 33, 34, 35]
   # connections[33] = [34, 35]
   # connections[34] = [35]
   # connections[35] = [35]
   # connections[36] = [36, 37, 38, 39]
   # connections[37] = [36, 38, 39]
   # connections[38] = [39]
   # connections[39] = [39]
   return connections

if __name__=='__main__':
   main()
