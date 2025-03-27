import numpy as np
import math    
import copy as cp         

class BitString:
  """
  Simple class to implement a config of bits
  """
  def __init__(self, N):
      self.N = N
      self.config = np.zeros(N, dtype=int) 

  def __repr__(self):
      out = ""
      for i in self.config:
          out += str(i)
      return out

  def __eq__(self, other):        
      return all(self.config == other.config)
  
  def __len__(self):
      return len(self.config)

  def on(self):
      """
      Return number of bits that are on
      """
      numOn = 0
      for digit in self.config:
          if digit == 1:
              numOn += 1
      
      return numOn

  def off(self):
    """
    Return number of bits that are off
    """
    numOff = 0
    for digit in self.config:
        if digit == 0:
            numOff += 1
    
    return numOff

  def flip_site(self,i):
    """
    Flip the bit at site i
    """
    if self.config[i] == 1:
        self.config[i] = 0
    else:
        self.config[i] = 1


  def integer(self):
    """
    Return the decimal integer corresponding to BitString
    """
    integer = 0
    for i in range(0, self.N - 1):
        integer += self.config[self.N - 1 - i] * pow(2, (i))

    return integer

  def set_config(self, s:list[int]):
    """
    Set the config from a list of integers
    """
    self.config = s

  def set_integer_config(self, dec:int):
    """
    convert a decimal integer to binary

    Parameters
    ----------
    dec    : int
        input integer
        
    Returns
    -------
    Bitconfig
    """
    for i in range(0, self.N):
        self.config[self.N - 1 - i] = dec % 2
        dec = dec // 2
