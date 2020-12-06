## Introduction
partar is a Python app using mpi4py to create multiple tarballs of large number of files in parallel.

## Requirements:
- Python3
- mpi4py

partar does not have a argument parser included as yet but will be done so in future to make it more configurable. 
Until then, please customize the python script at your discretion.



To create synthetic benchmark (i.e a good number of files with decent data), a script is included "data_mpi.py".

### Jobscript
A sample slurm job script to launch the taring would look something like this:

```
#!/bin/bash 
#SBATCH --partition=workq
#SBATCH --ntasks=8
#SBATCH --time=04:00:00


srun --hint=nomultithread -n 8 python partar.py -i /path/to/input_dir -o /path/to/output_dir
```

## Scaling:
The scaling on the sythetic data looks promising.
```
	Num MPI procs		Time(min)
	     4			226.9283333
	     8			119.6616667
	     16			58.8805
	     32			32.3585
	     64			8.833333333
```

