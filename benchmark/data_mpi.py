#!/usr/bin/env python
import numpy as np,os
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

os.chdir('data')
chunk=10
for i in range(rank*chunk,(rank+1)*chunk):
    fname="file%i.dat"%(i)
    np.random.random(50000000).tofile(fname,sep=",",format="%f")
