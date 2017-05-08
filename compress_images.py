# -*- coding: utf-8 -*-
"""
Compress binary images

Created on Thu May  4 16:25:34 2017

@author: d-v-b
"""
# List of directories with images to compress
from glob import glob
from os.path import sep
base_dirs = glob('F:/davis/20170430/*')

for ind, val in enumerate(base_dirs):
    base_dirs[ind] += sep

def convert(v, verbose=False):
    from fish.util.fileio import image_conversion
    image_conversion(v, dest_fmt = 'h5', wipe=True)
    
    if verbose:    
        print('Processed image number {0}'.format(v))

def process_images(base_dir):
    from multiprocessing import cpu_count
    from multiprocessing.pool import Pool    
    from glob import glob
    
    fnames = glob(base_dir + 'TM*.stack')
    if len(fnames) > 0:
        num_workers = cpu_count()
        p = Pool(num_workers)
        p.map(convert, fnames)
        p.close()
    else:
        print('No .stack files found in {0}'.format(base_dir))


if __name__ == '__main__':    
    print('Begin compressing images.')
    for base_dir in base_dirs:
        process_images(base_dir)
    
    print('Finished compressing images.')                    
    
