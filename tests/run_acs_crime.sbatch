#!/bin/bash
#SBATCH --job-name=acs_crime
#SBATCH --output=acs_crime.out
#SBATCH --error=acs_crime.err
#SBATCH --time=36:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=24
#SBATCH --ntasks-per-node=14
#SBATCH --mem-per-cpu=2000

module load Anaconda3/5.3.0
source activate myenv
python -m unittest test_main_acs_crime.py
