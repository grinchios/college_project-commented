# Middle Square Weyl Sequence PRNG

'''

The defects associated with the original middle-square generator can 
be rectified by running the middle square with a Weyl sequence. 
The Weyl sequence prevents convergence to zero.

'''

'''
S1
A secure and encrypted login system will be used before viewing the system. This includes hashing passwords on input and checking against the correct ones.
P9
On sign in the passwords will be hashed and checked against the correct ones.
'''

class msws():
	'''
	S1
	A secure and encrypted login system will be used before viewing the system. This includes hashing passwords on input and checking against the correct ones.
	'''
	'''
	P9
	On sign in the passwords will be hashed and checked against the correct ones.
	'''
    def __init__(self, seed):
        #  seed is constant
        self.seed = seed
        
        #  x holds previous value
        self.x = self.genSeed()
        
        #  w,s are Weyl 'masks'
        self.w = 0xa6f7db83ec2be49d
        self.s = 0xb5ad4eceda1ce2a9b5ad4eceda1ce2a9b5ad4eceda1ce2a9
        
        #  z holds 'throwaway' value
        self.z = 0
        
        #  m holds length of the values
        self.m = 64
        self.m2 = 1
        
        #  ra holds the amount of times ran
        self.ra = 1
        
        #  lim is a length limiter for speed
        self.lim = (self.m % 512)
        
    def genSeed(self):
        #  check input is int
        try:
            self.z = int(self.seed)
            
        #  if not then it's converted to int
        #  based on ascii value
        
        except:
            if len(self.seed) > 1:
                    self.z = 0
                    for i in self.seed:
                        self.z += ord(i) * ord(i)
                        
            else:
                self.z = ord(self.seed) * ord(self.seed)
                
        return (self.z * self.z * self.z)
        
    def mid(self):
        """
        Return middle n chars of string.
        """

        if self.m <= 0:
          return 0

        if self.m > len(self.z):
          return int(self.z)

        ofs = (len(self.z) - self.m) // 2

        return int(self.z[ofs : ofs + self.m])
      
    def msws(self):
        self.z = self.x
        
        #  Von Neumans middle Square      
        self.z *= self.z
        self.w += self.s
        self.z += self.w
        
        #  bitwise operation to return the
        #  middle of the value (Weyl method)
        #self.z = str((self.z >> self.lim)|(self.z << self.lim))
        
        self.z = str(self.z)
        self.x = self.mid()
        
        #print(self.x)
        #  user length into temp
        self.m2 = self.m
        
        #  get as many values as can be quickly
        #  calculated to improve randomness
        self.m = 128
        #self.s = self.mid()
        
        #  swap user val back into actual value
        self.m = self.m2
        
        if self.ra <= 1:
            self.ra += 1
            
            #  recurse here to extend the length
            #  and to improve the randomness
            #  by changing s for Weyl's method
            
            self.s = self.msws()
                   
        self.ra += 1
        
        return self.x