import math
from collections import defaultdict


def get_time_slot(qubit_number, row_length):
   return math.ceil(float(qubit_number + 1)/float(row_length))

def get_machine_number(qubit_number, row_length, operations_number):
   return int((float(qubit_number % row_length) / float(operations_number)) + 1)

def get_machine_and_time_slot(qubit_number, row_length, operations_number):
   return get_machine_number(qubit_number, row_length, operations_number), get_time_slot(qubit_number, row_length)

def get_qubits_from_slot_and_machine(machine_number, time_slot, number_of_operations, row_length):
    return range(row_length * (time_slot - 1) + (machine_number - 1)* number_of_operations , row_length * (time_slot - 1) + machine_number * number_of_operations)


def get_operation_length(jobs, operation_number):
   return [item for sublist in jobs for item in sublist][operation_number]


def is_last_row(time_slot, time_limit):
   return time_slot == time_limit

def csp_get_one_job_on_machine_constraint_dict(jobs, row_length, number_of_operations, number_of_qubits, time_limit):
    result = defaultdict(int)
    for qubit_number in range(number_of_qubits):
        qubits_for_this_qubit = []
        machine_number, time_slot = get_machine_and_time_slot(qubit_number, row_length, number_of_operations)
        operation_number = qubit_number % number_of_operations
        operation_length = get_operation_length(jobs, operation_number)
        if (is_last_row(time_slot, time_limit)):
            shift = 0
            qubits = get_qubits_from_slot_and_machine(machine_number, time_slot + shift, number_of_operations,
                                                      row_length)
            qubits_for_this_qubit.extend(filter(lambda q: (q - qubit_number) % row_length != 0,qubits))
        else:
            for shift in range(operation_length):
                qubits = get_qubits_from_slot_and_machine(machine_number, time_slot + shift, number_of_operations,
                                                          row_length)
                qubits_for_this_qubit.extend(filter(lambda q: (q - qubit_number) % row_length != 0,qubits))
        result['{}'.format(qubit_number)] = qubits_for_this_qubit

    return result


def get_one_job_one_machine_csp(jobs, row_length, number_of_operations, number_of_qubits, time_limit):
    constraint_dict = csp_get_one_job_on_machine_constraint_dict(jobs, row_length, number_of_operations, number_of_qubits, time_limit)
    csp_list = []
    for i in range(number_of_qubits):
        # print("i: {}, len: {}".format(i, len(constraint_dict['{}'.format(i)])), constraint_dict['{}'.format(i)])
        csp_list.append(constraint_dict['{}'.format(i)])
    # print(csp_list)
    return csp_list

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


def csp_get_order_constraint(jobs, number_of_machines, time_limit, number_of_operations):
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
                print(qubit_checked_op, qubits_for_tmp_op)
                # for qubit_tmp_op in qubits_for_tmp_op:
                #   checked_op_time_slot = get_time_slot(qubit_checked_op, row_len)
                #   tmp_op_time_slot = get_time_slot(qubit_tmp_op, row_len)
                  # if checked_op_time_slot - tmp_op_time_slot < tmp_op_len:
                  #    connections[qubit_tmp_op, qubit_checked_op] += multiplier


# csp_get_order_constraint([[2,1],[1,2]], 2, 4, 4)
# print(get_one_job_one_machine_csp([[2,1],[1,2]], 8, 4, 40, 5))






# starts_once_constraints = \
#     [['x{}'.format(global_operation_number + 8 * time ) for time in range(5)] \
#      for global_operation_number in range(8)]
# print(starts_once_constraints)

# csp.add_constraint(one_one, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
# csp.add_constraint(n_one_one, ['a', 'b', 'c', 'd'])
# csp.add_constraint(all_equal, ['a', 'b', 'c'])

# print(csp.check({'a': 0, 'b': 1, 'c': 1, 'd': 0}))

# print(csp.check({'a': 1, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}))

# resp = DWaveSampler().sample(bqm)
#
# for sample, energy in resp.data(['sample', 'energy']):
#     print(sample, csp.check(sample), energy)
