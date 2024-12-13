import simnibs
import numpy as np
import os

# Basic setup verification
print("SimNIBS version:", simnibs.__version__)

# Create our project structure
project_dir = os.path.expanduser('tms_grid_project')
subdirs = ['models', 'simulations', 'results', 'coil_designs']

for subdir in subdirs:
    path = os.path.join(project_dir, subdir)
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")