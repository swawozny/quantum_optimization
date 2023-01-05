"""Simple implementation of dummy random sampler."""
import random
from functools import partial

import dimod


class RandomSampler(dimod.Sampler):
    """Implementation of simple random-sampler.

    This sampler assigns randomly chosen value to each variable, either from
    the set {0, 1} or the set {-1, 1}, depending on the vartype of BQM
    being solved.
    """

    variable_samplers = {
        dimod.vartypes.SPIN: lambda prob: int(random.random() > prob) * 2 - 1,
        dimod.vartypes.BINARY: lambda prob: int(random.random() > prob),
    }

    def __init__(self, prob):
        self.prob = prob

    def get_random_sample(self, bqm):
        """Get random assignment of variables in given BQM."""
        get_random_value = partial(self.variable_samplers[bqm.vartype], prob=self.prob)
        return {variable: get_random_value() for variable in bqm.variables}

    def sample(self, bqm, num_reads=1, **parameters):
        samples = [self.get_random_sample(bqm) for _ in range(num_reads)]
        energies = [bqm.energy(sample) for sample in samples]

        return dimod.SampleSet.from_samples(samples, energy=energies, vartype=bqm.vartype)

    def sample_qubo(self,
                    Q,
                    **parameters):
        bqm = dimod.BQM.from_qubo(Q, offset=0.0)

        return self.sample(bqm)

    def sample_ising(self,
                     h,
                     J,
                     **parameters):
        bqm = dimod.BQM.from_ising(h, J, 0)

        return self.sample(bqm)

    @property
    def properties(self):
        return dict()

    @property
    def parameters(self):
        return {"num_reads": []}
