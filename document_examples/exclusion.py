import sys

import dwave
import dwavebinarycsp
from dwave.system import EmbeddingComposite, DWaveSampler
from dwave_networkx import chimera_graph

from utils.jobshop_helpers import ones_from_sample

qubits_number = 6


def main():
    embedded = int(sys.argv[1])
    connections = [[-1.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                   [0.0, -1.0, 2.0, 2.0, 2.0, 2.0],
                   [0.0, 0.0, -1.0, 2.0, 2.0, 2.0],
                   [0.0, 0.0, 0.0, -1.0, 2.0, 2.0],
                   [0.0, 0.0, 0.0, 0.0, -1.0, 2.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, -1.0]]
    linear = {}
    quadratic = {}
    for i in range(qubits_number):
        linear['x{}'.format(i), 'x{}'.format(i)] = float(connections[i][i])
    for i in range(qubits_number):
        for j in range(i + 1, qubits_number):
            val = connections[i][j]
            if val != 0:
                quadratic['x{}'.format(i), 'x{}'.format(j)] = float(val)

    Q = dict(linear)
    Q.update(quadratic)
    if embedded == 0:
        response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=100)
        for s in list(response.data()):
            print(s.sample, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)
    else:
        embedding = {}
        emb_numbers = [[0, 4, 128]
            , [1, 5, 129]
            , [2, 6, 130]
            , [3, 7, 131]
            , [132, 136, 140]
            , [133, 137, 141]
                     ]
        for num, arr in enumerate(emb_numbers):
            tmp_embedding = set()
            for elem in sorted(arr):
                tmp_embedding.add(elem)

            embedding['x{}'.format(num)] = tmp_embedding

        tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=1.0)
        response = DWaveSampler().sample_qubo(tQ, num_reads=200)

        print("UNEMBEDED RESULTS")
        source_bqm = dwavebinarycsp.dimod.BinaryQuadraticModel.from_qubo(Q)  # (linear, quadratic, 0, Vartype.BINARY)
        suma = 0
        for i, val in enumerate(dwave.embedding.unembed_sampleset(response, source_bqm=source_bqm, embedding=embedding)):
            suma += list(response.data())[i].num_occurrences
            print(ones_from_sample(val), list(response.data())[i].num_occurrences, list(response.data())[i].energy, suma)


if __name__ == '__main__':
    main()
