from . import bitString as bs
from . import isingHamiltonian as isingHam
import math
import numpy as np

class MonteCarlo:
  def __init__ (self, ham: isingHam):
    self.ham = ham

  def run(self, T, n_samples, n_burn):
    bitstring = bs.BitString(len(self.ham.J))
    samples = n_samples + 1
    E = [0] * samples
    M = [0] * samples
    Z = 0
    prev_energy = self.ham.energy(bitstring)
    while n_samples > 0:
      for pos in range(0, bitstring.N):
        bitstring.flip_site(pos)
        new_energy = self.ham.energy(bitstring)

        W = math.exp(-(new_energy - prev_energy) / T)
        if W > np.random.rand():
          prev_energy = new_energy
          continue
        else:
          bitstring.flip_site(pos)
      
      if n_burn > 0:
        n_burn -= 1
      else:        
        bs_magnetism = 0
        for j in range(0, bitstring.N):
          if bitstring.config[j] == 1:
            bs_magnetism += 1 
          else:
            bs_magnetism += -1
        E[samples - n_samples] =  self.ham.energy(bitstring)
        M[samples - n_samples] =  bs_magnetism
        n_samples -= 1

    return E, M
  