# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:04:12 2017

@author: AhrensLab
"""

# List of directories with images to compress
from glob import glob
from os import remove, walk
from os.path import split, sep, join

Dirs = [   'F:\\Maarten\\20170606\\'
]

for y in range(0, len(Dirs)):
        rawDir= Dirs[y]
        print (Dirs[y])
        base_dirs = list()
        for root, dirs, files in walk(rawDir, topdown=False):
            for name in dirs:
                base_dirs.append(join(root, name))
                
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
    if len(Dirs) == 1:
        print('Begin compressing images.')
        for base_dir in Dirs:
            print(Dirs)
            process_images(base_dir)
        print('Finished compressing images.') 
    
    else:
        print('Finished compressing images.')
        print('Begin compressing images.')
        for base_dir in base_dirs:
            print(base_dir)
            process_images(base_dir)
        print('Finished compressing images.')                    
    