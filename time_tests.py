from collections import defaultdict

qubits_for_tasks = defaultdict()
tasks_number = 6
machines_number = 3
paths = [[0, 1, 3, 5], [0, 1, 4, 5], [0, 2, 4, 5]]
A_vec = [i for i in range(tasks_number * machines_number)]

for t in range(tasks_number):
    qubits_for_tasks[t] = [tasks_number * m + t for m in range(machines_number)]
print(qubits_for_tasks)
paths_qubits = []
for path in paths:
    new_path = []
    for task_index in path:
        new_path.extend(qubits_for_tasks[task_index])
    paths_qubits.append(new_path)
print(paths_qubits)

times = [sum([A_vec[qubit_number] for qubit_number in single_path]) for single_path in paths_qubits]
print(times)