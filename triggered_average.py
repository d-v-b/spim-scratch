# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 13:44:56 2017

@author: AhrensLab
"""

def trigger_data(triggers, window, fnames, average=False, single_plane = False, z=None):
    from numpy import array, memmap
    from fish.image.vol import get_stack_dims
    from fish.util.fileio import load_image
    from os.path import split, sep

    dims = get_stack_dims(split(fnames[0])[0] + sep)[::-1]
    ims_trial = []
    
    for ind, trig in enumerate(triggers):
        
        tr = []        
        for t_w in window:
            if single_plane:
                tr.append(load_single_plane(fnames, trig + t_w, tuple(dims)))
            elif z is None:
                tr.append(load_image(fnames[trig + t_w]))
            else:
                tr.append(array(memmap(fnames[trig + t_w], shape=tuple(dims), dtype='uint16')[z]))
        tr = array(tr)
        
        
        if (len(ims_trial) == 0) or not average:
            ims_trial.append(tr)
        #todo: simplify this, do division at end 
        if average:
            if ind == 0:
                ims_trial[0] = ims_trial[0].astype('float32') / len(triggers) 
            
            ims_trial[0] += tr.astype('float32') / len(triggers)
        
    if average:         
        return ims_trial[0]
    else:
        return array(ims_trial)
    
def match_cam_time(events, cam, timing):
    from numpy import array
    output = []
    for a in events:
        lags = array([a-b for b in cam])
        before = len(lags[lags > 0]) - 1
        after = before + 1
        
        if (before >= 0) and (after < len(cam)):
            if timing == 'pre':                
                output.append(before)
            if timing == 'post':
                output.append(after)    
    return array(output)

def load_single_plane(fnames, t, dims):
    from numpy import memmap, array    
    fn = fnames[t // dims[0]]
    mem = memmap(fn, shape=dims, dtype='uint16')
    return array(mem[t % dims[0]])