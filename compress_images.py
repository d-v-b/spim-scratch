# -*- coding: utf-8 -*-
"""
Compress binary images

Created on Thu May  4 16:25:34 2017
   
@author: d-v-b
""" 

from glob import glob
from os.path import sep
from functools import partial
# List of directories with images to compress

base_dirs = glob('F:\\EN\\*\\*\\')

# Specify the source format of the data. Must be 'tif' or 'stack' 
srce_format = 'stack'
# specify the destination format of the data. Must be 'h5' or 'tif'
dest_format = 'h5'

for ind, val in enumerate(base_dirs):
    base_dirs[ind] += sep

def convert(v, dest_format, verbose=False, ):
    from fish.util.fileio import image_conversion
    image_conversion(v, dest_fmt = dest_format, wipe=True)
    
    if verbose:    
        print('Processed image number {0}'.format(v))

converter = partial(convert, dest_format=dest_format)

def process_images(base_dir):
    from multiprocessing import cpu_count
    from multiprocessing.pool import Pool    
    from glob import glob
    
    fnames = glob(base_dir + 'TM*.{0}'.format(srce_format))
    if len(fnames) > 0:
        num_workers = cpu_count()-1
        p = Pool(num_workers)
        p.map(converter, fnames[0:-3])
        p.close()
    else:
        print('No {0} files found in {1}'.format(srce_format, base_dir))

if __name__ == '__main__':
    # this stupid line is needed to prevent spyder from throwing a fit
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
   
    print('Begin compressing images.')
    for base_dir in base_dirs:
        print(base_dir)
        process_images(base_dir)
        try:
            process_images(base_dir)
        except:
            print('Problem compressing data in {0}'.format(base_dir))
            pass
    print('Finished compressing images.')                    
    
