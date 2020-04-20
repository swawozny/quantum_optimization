import numpy as np

import qubo_matrices_helpers


def get_cdiag_text(C_diag):
    res_c = ""
    cdiaglen = len(C_diag)
    for i in range(len(C_diag) - 1):
        res_c += "{} x{} + ".format(C_diag[i], i)
    res_c += "{} x{}".format(C_diag[cdiaglen - 1], cdiaglen - 1)
    return res_c

def get_ab_rows_texts_list(A,b):
    lines = []
    for i in range(len(b)):
        res_row = "c{}: ".format(i)
        for j in range(len(A[i])):
            res_row += "{} x{} + ".format(A[i][j], j)
        res_row = res_row[:-3] + " = " + str(-b[i])
        lines.append(res_row)
    return lines

def get_binaries_text_list(number):
    lines = []
    for i in range(number):
        lines.append("0 <= x{} <= 1".format(i))
    return lines

S=10
A, b, C, paths, tasks_number, machines_number, D= qubo_matrices_helpers.get_smaller_18_qubits_data(S)
C_diag = np.diagonal(C)
# print(get_cdiag_text(C_diag))
# print_Ab_rows(A,b)
# print_binaries(len(C_diag))



to_file = "Minimize\nobj: "
to_file += "{}\n".format(get_cdiag_text(C_diag))
to_file += "Subject To\n"
for line in get_ab_rows_texts_list(A,b):
    to_file += "{}\n".format(line)
to_file += "Bound\n"
for line in get_binaries_text_list(len(C_diag)):
    to_file += "{}\n".format(line)
to_file += "Integer\nx0"
for i in range(1,len(C_diag)):
    to_file += " x{}".format(i)
to_file += "\nEnd"

print(to_file)





# Subject To
# c1: - x1 + x2 + x3 + 10 x4 <= 20
# c2: x1 - 3 x2 + x3 <= 30