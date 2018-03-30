# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:57:27 2018

@author: AhrensLab
"""

# get mean and variance across a large timeseries

import numpy as np
from multiprocessing import Pool
from glob import glob
from os.path import exists
from os import makedirs
from pathlib import Path

num_workers = 10
fnames = sorted(glob('F:/davis/20180128/gain_test_5mW_20180128_133326/TM*.h5'))
exp_name = Path(fnames[0]).parts[-2]
output_dir = 'F:/davis/20180128/output_for_ziqiang/{0}/'.format(exp_name)

if not exists(output_dir):
    makedirs(output_dir)

def get_stats(fn):
    print('Started working on {0}'.format(fn))
    from fish.util.fileio import load_image
    from numpy import array    
    data = load_image(fn)
    
    mean_ = data.mean(0)
    var_ = data.var(0)
    print('Finished working on {0}'.format(fn))
    return(array([mean_, var_]))

    
if __name__ == '__main__':
    # this stupid line is needed to prevent spyder from throwing a fit
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    
    with Pool(num_workers) as p:
        result = p.map(get_stats, fnames)
    print('saving results')
    for ind, val in enumerate(result):
        np.save(output_dir + 't_{0}.npy'.format(ind), val)
    
    