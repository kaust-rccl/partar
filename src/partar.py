#!/bin/env python
import argparse
from mpi4py import MPI
import glob,subprocess as sb,os
import numpy as np


parser = argparse.ArgumentParser(description='Parallel Tarball.')
parser.add_argument('-i','--indir', type=str, nargs=1,default=['data'],
                    help='Path to input directory')
parser.add_argument('-o','--outdir', type=str, nargs=1,default=['.'],
                    help='Path to output directory')
args = parser.parse_args()

indir=args.indir[0]
outdir=args.outdir[0]
print("Reading CSV files from: ", indir)
print("Writing tarballs in: ",outdir)

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
nprocs=comm.Get_size()

os.chdir(indir)
if rank == 0: 
    os.makedirs(outdir+'/tarfiles',exist_ok=True)

req_r=comm.irecv(source=0,tag=100)

if rank == 0:
    fname_lst=glob.glob('*.csv')
    div,rem=divmod(len(fname_lst),nprocs)
    # count: the size of each sub-task
    count = [div + 1 if p < rem else div for p in range(nprocs)]
    count = np.array(count)

    # start and end index of each sub-task
    start = [sum(count[:p]) for p in range(nprocs)]
    end =   [(start[p]+count[p]) for p in range(nprocs)]
    
    # send data to all processes including rank 0
    for p in range(nprocs):
        req_s=comm.isend(fname_lst[start[p]:end[p]],dest=p,tag=100)
        req_s.wait()


# After recv posted above is finished, put data in my_lst
my_lst=req_r.wait()

tarball=outdir+'/tarfiles/task%d.tar'%rank
for i in range(len(my_lst)):
    out = sb.run(['tar','rvf',tarball,my_lst[i]],stdout=sb.PIPE,stderr=sb.PIPE)
    if str(out.stderr.decode("utf-8")) != "":
        print(str(out.stderr.decode("utf-8")))
    else:
        continue



    
