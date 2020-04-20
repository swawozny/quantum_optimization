# import pandas as pd
import random

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from pandas import DataFrame
from matplotlib.backends.backend_pdf import PdfPages

res_8 = [45, 27, 15, 28, 20, 8, 19, 21, 9, 24, 3, 16, 7, 12, 6, 9, 1, 3, 17, 27, 19, 26, 24, 17, 10, 15, 8, 6, 9, 5, 6,
         2, 4, 3, 8, 0, 2, 4, 3, 1, 2, 4, 2, 3, 0, 4, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
# res_8_normalized = [float(x)/float(sum(res_8)) for x in res_8]
correct_8_number = 98
res_10 = [143, 99, 55, 13, 33, 24, 12, 0, 0, 16, 15, 2, 0, 0, 2, 9, 15, 25, 23, 34, 57, 76, 36, 26, 18, 14, 11, 7, 7, 9,
          6, 4, 4, 3, 10, 10, 20, 11, 8, 9, 18, 17, 14, 5, 5, 3, 4, 4, 0, 1, 2, 4, 1, 2, 1, 5, 1, 5, 0, 2, 1, 1, 1, 3,
          2, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
# res_10_normalized = [float(x)/float(sum(res_10)) for x in res_10]
correct_10_numbers = 27
res_15 = [217, 94, 64, 144, 258, 144, 100, 138, 155, 112, 71, 70, 71, 55, 44, 35, 28, 17, 24, 16, 16, 12, 14, 10, 6, 8,
          6, 2, 2, 1, 1, 6, 1, 3, 0, 2, 0, 2, 2, 0, 1, 0, 1, 0, 0, 2, 1, 0, 0, 1]
# res_15_normalized = [float(x)/float(sum(res_15)) for x in res_15]
correct_15_numbers = 4
res_18 = [124, 92, 42, 93, 126, 102, 83, 141, 96, 98, 109, 84, 76, 72, 90, 76, 63, 66, 40, 52, 45, 27, 29, 35, 24, 25,
          13, 15, 10, 7, 10, 4, 5, 2, 5, 2, 3, 2, 3, 0, 2, 1, 0, 0, 0, 0, 1, 0, 1, 1]
# res_18_normalized = [float(x)/float(sum(res_18)) for x in res_18]
correct_18_numbers = 0


def get_correct_and_wrong_list(source, correct_number):
    tmp = correct_number
    elements_number = 0
    while tmp > 0:
        tmp -= source[elements_number]
        elements_number += 1
    correct_solutions = source[:elements_number]
    if len(correct_solutions) > 0:
        correct_solutions[-1] += tmp
    wrong_solutions = source[(elements_number - 1):]
    return correct_solutions, wrong_solutions


res_8_correct, res_8_wrong = get_correct_and_wrong_list(res_8, correct_8_number)
res_8_correct, res_8_wrong = [float(x)/float(sum(res_8)) for x in res_8_correct], [float(x)/float(sum(res_8)) for x in res_8_wrong]
res_10_correct, res_10_wrong = get_correct_and_wrong_list(res_10, correct_10_numbers)
res_10_correct, res_10_wrong = [float(x)/float(sum(res_8)) for x in res_10_correct], [float(x)/float(sum(res_10)) for x in res_10_wrong]
res_15_correct, res_15_wrong = get_correct_and_wrong_list(res_15, correct_15_numbers)
res_15_correct, res_15_wrong = [float(x)/float(sum(res_8)) for x in res_15_correct], [float(x)/float(sum(res_15)) for x in res_15_wrong]


# res_18_correct, res_18_wrong = get_correct_and_wrong_list(res_18, correct_18_numbers)


def prepare_histogram(correct, wrong, ax, id):
    total_len = len(correct) + int(len(wrong)) - 1
    k = 2 if id <= 2 else 1
    xes = [''] + ['low energy'] + ['' for i in range(k)] + \
          ['high energy'] + ['' for j in range(int(total_len - 45))]
    ax.bar(np.arange(len(correct) - 1, total_len), wrong, color='red', label='wrong solutions')
    ax.bar(np.arange(len(correct)), correct, color='green', label='correct solutions')
    # ax.xticks(range(total_len), xes)
    ax.legend(loc='best')
    ax.set_xticklabels(xes)
    ax.set_title("Problem {}".format(id))
    # ax.set_axis_off()
    # ax.patch.set_visible(False)
    # ax.set_xlabel('ddd' + str(random.randint(5,156)))


fig, axs = plt.subplots(2, 2)
prepare_histogram(res_8_correct, res_8_wrong, axs[0,0], 1)
prepare_histogram(res_10_correct, res_10_wrong, axs[0, 1], 2)
prepare_histogram(res_15_correct, res_15_wrong, axs[1, 0], 3)
prepare_histogram([0], [float(x)/float(sum(res_18)) for x in res_18], axs[1, 1], 4)
for ax in axs.flat:
    ax.set(ylabel='Probability density')
# plt.show()
# plt.subplots_adjust(top=2)
fig.tight_layout(pad=0.75)

pdf = PdfPages("histogram_dwave.pdf")
pdf.savefig()
pdf.close()
# y_pos = np.arange(len(res_8))
# frame1 = plt.gca()
# frame1.axes.get_xaxis().set_visible(False)
# plt.xticks(y_pos, ['.' for i in range(len(res_8))])

# res8dict = [{"value": val, "color": 'wrong'} for val in res_8]
# for i in range(4):
#     res8dict[i]["color"] = "correct"
# df = DataFrame(res8dict)
# fig = px.bar(df, y="value", color='color')
# fig.show()

# x0 = np.random.randn(500)
# Add 1 to shift the mean of the Gaussian distribution
# x1 = np.random.randn(500) + 1


# range50 = list(range(10))
# range50.extend(['.' for i in range(40)])
# range80 = list(range(10))
# range80.extend(['.' for i in range(70)])
#
# all = [res_8, res_10, res_15, res_18]
#
## print(list(map(lambda x: len(x), all)))
#
# df8 = pd.DataFrame({'number of boxes':range80, 'number of occurences':res_8})
# ax8 = df8.plot.bar(x='number of boxes', y='number of occurences', rot=0)
# plt.show()
#
# df10 = pd.DataFrame({'number of boxes':range80, 'number of occurences':res_10})
# ax10 = df10.plot.bar(x='number of boxes', y='number of occurences', rot=0)
# plt.show()
#
# df15 = pd.DataFrame({'number of boxes':range50, 'number of occurences':res_15})
# ax15 = df15.plot.bar(x='number of boxes', y='number of occurences', rot=0)
# plt.show()
#
# df18 = pd.DataFrame({'number of boxes':range50, 'number of occurences':res_18})
# ax18 = df18.plot.bar(x='number of boxes', y='number of occurences', rot=0)
# plt.show()
