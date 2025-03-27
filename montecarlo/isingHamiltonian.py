import networkx as nx
from . import bitString as bs
import math
import numpy as np

class IsingHamiltonian:
    def __init__(self, G):
        self.G = G
        self.mus = np.array([0 for i in range(len(self.G))])

    def set_mu(self, mus: np.array):
        self.mus = mus

        return self


    def energy(self, bs: bs.BitString):
        """Compute energy of configuration, `bs`

            .. math::
                E = \\left<\\hat{H}\\right>

        Parameters
        ----------
        bs   : Bitstring
            input configuration
        G    : Graph
            input graph defining the Hamiltonian
        Returns
        -------
        energy  : float
            Energy of the input configuration
        """
        # 2-D array that represents the weights of the edges
        A = nx.adjacency_matrix(self.G).todense()

        total_energy = 0
        for i in range(0, bs.N):
            for j in range(i, bs.N):
                if (bs.config[i] == 0 and bs.config[j] == 0) or (bs.config[i] == 1 and bs.config[j] == 1):
                    total_energy +=  A[i][j]
                else:
                    total_energy += -1 * A[i][j]
            
            if bs.config[i] == 1:
                total_energy += self.mus[i]
            else:
                total_energy += -1 * self.mus[i]
        return total_energy
    
    def compute_average_values(self, T: float):
        E  = 0.0
        M  = 0.0
        Z  = 0.0
        EE = 0.0
        MM = 0.0

        bitString = bs.BitString(len(self.G))
        for i in range(0, pow(2, bitString.N)):
            bitString.set_integer_config(i)
            bs_energy = self.energy(bitString)

            P = (math.exp(-bs_energy/T))
            
            bs_magnetism = 0
            for j in range(0, bitString.N):
                if bitString.config[j] == 1:
                    bs_magnetism += 1 
                else:
                    bs_magnetism += -1

            E += P * bs_energy
            M += P * bs_magnetism

            EE += P * pow(bs_energy, 2)
            MM += P * pow(bs_magnetism, 2)
            Z += P
        
        E /= Z
        M /= Z
        EE /= Z
        MM /= Z

        HC = (EE - E*E) * pow(T, -2)
        MS = (MM - M*M) * pow(T, -1)

        return E, M, HC, MS