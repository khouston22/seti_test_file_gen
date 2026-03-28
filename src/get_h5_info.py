# -*- coding: utf-8 -*-
"""nchans
Functions to read h5 header information into convenient variables
@author: K Houston
"""
import sys
import os

import numpy as np
from astropy import units as u
import blimpy as bl
from astropy.time import Time

from pathlib import Path


def get_h5_params(base_h5_name,
        verbose=True):
    """
    returns dictionary of key h5 file run parameters
    and h5hdr
    """

    wf = bl.Waterfall(base_h5_name)

    p = get_wf_params(wf,base_h5_name,verbose)
    
    return p

def get_wf_params(wf,base_h5_name,verbose=True):
    """
    returns dictionary of key h5 file run parameters
    """

    h5hdr = wf.header

    az_start = h5hdr['az_start'] # 0.0, 
    data_type = h5hdr['data_type'] #  1, 
    fch1 = h5hdr['fch1'] #  8438.96484375, 
    foff = h5hdr['foff'] #  -2.7939677238464355e-06, 
    
    try:
        ibeam = h5hdr['ibeam'] #  -1, 
    except:
        ibeam = -1
    machine_id = h5hdr['machine_id'] #  20, 

    try:
        nbeams = h5hdr['nbeams'] #  1, 
    except:
        nbeams = 1

    n_bits = h5hdr['nbits'] #  32, 
    nchans = h5hdr['nchans'] #  67108864, 
    try:
        nfpc = h5hdr['nfpc'] #  1033216 = 1009K, # earlier rawspec output format ???
    except:
        nfpc = 0 

    try:
        nifs = h5hdr['nifs'] #  1, 
    except:
        nifs = 1

    try:    
        rawdatafile = h5hdr['rawdatafile'] #  'blc23_guppi_59046_80036_DIAG_VOYAGER-1_0011.0000.raw', 
    except:
        rawdatafile = ''

    source_name = h5hdr['source_name'] #  'VOYAGER-1', 
    src_dej = h5hdr['src_dej'] #  <Angle 12.4041 deg>, 
    src_raj = h5hdr['src_raj'] #  <Angle 17.21123333 hourangle>, 
    telescope_id = h5hdr['telescope_id'] #  6, 
    tsamp = h5hdr['tsamp'] #  1.431655765333332, 
    tstart = h5hdr['tstart'] #  59046.92634259259, 
    time_string = Time(tstart, format='mjd').isot #: 'Thu Sep 10 20:33:03 2020' local time
    
    za_start = h5hdr['za_start'] #  0.0


    if (telescope_id==6):
        telescop = 'GBT'
        if (nfpc==0):
            nfpc = 1024*1024
    elif (telescope_id==4):
        telescop = 'Parkes'
    elif (telescope_id==9):
        telescop = 'ATA'
        nfpc = 256*1024
    elif (telescope_id==12):
        telescop = 'VLA'
    elif (telescope_id==64):
        telescop = 'MeerKat'
    else:
        telescop = ' '

    if (nfpc==0):
        print('File {base_h5_name}:')
        raise ValueError("Error in get_h5_params: No informaton about nfpc (fine FFT size) in file header")
    
    fine_fft_size = nfpc
    n_coarse_channels = nchans//nfpc

    mjd_day = int(tstart) #: '59103'
    src_name = source_name #: 'VOYAGER-1'
    ra_deg = src_raj.deg #: '287.7736'
    dec_deg = src_dej.deg #: '42.8694'

    chan_bw = foff*fine_fft_size*1e6

    ctr_freq_MHz = fch1 + nchans*foff/2.
    obs_bw_MHz = n_coarse_channels*foff*fine_fft_size
    obs_bw_sign = 1 if (obs_bw_MHz > 0.) else -1
    f_min_MHz = ctr_freq_MHz - abs(obs_bw_MHz)/2.
    f_max_MHz = ctr_freq_MHz + abs(obs_bw_MHz)/2.

    t_fine = 1./abs(foff*1e6)
    t_coarse = t_fine/fine_fft_size
    n_sti = int(tsamp/t_fine + 0.5)
    n_lti = wf.n_ints_in_file
    n_avg = n_lti*n_sti
    t_obs = t_fine*n_avg
    t_res = tsamp
        
    fs_coarse = 1/t_coarse
    fs_fine = 1/t_fine

    h5_size_MB = wf.file_size_bytes/1024./1024.
    n_h5_files = 1

    p = {'base_h5_name':base_h5_name}
    p['h5_size_MB'] = h5_size_MB
    p['n_h5_files'] = n_h5_files
    p['rawdatafile'] = rawdatafile

    p['telescop'] =  telescop
    p['time_string'] = time_string
    p['mjd_day'] = mjd_day
    p['src_name'] = src_name
    p['ra_deg'] = ra_deg
    p['dec_deg'] = dec_deg
    p['ctr_freq_MHz'] = ctr_freq_MHz
    p['obs_bw_MHz'] = obs_bw_MHz
    p['obs_bw_sign'] = obs_bw_sign
    p['chan_bw'] = chan_bw
    p['f_min_MHz'] = f_min_MHz
    p['f_max_MHz'] =f_max_MHz
    p['fch1'] = fch1
    p['foff'] = foff

    p['t_obs'] = t_obs
    p['n_coarse_channels'] = n_coarse_channels
    p['n_bits'] = n_bits
    p['fs_coarse'] = fs_coarse
    p['fine_fft_size'] = fine_fft_size
    p['n_sti'] = n_sti
    p['n_lti'] = n_lti
    p['n_avg'] = n_avg
    p['t_coarse'] = t_coarse
    p['t_fine'] = t_fine
    p['t_res'] = t_res
    p['fs_fine'] = fs_fine

    p['ibeam'] = ibeam
    p['nbeams'] = nbeams
    p['nifs'] = nifs
    p['za_start'] = za_start
        
    if verbose:
        print(f'{base_h5_name = }')
        if os.path.isfile(base_h5_name): print('h5 file found')
        print(f'h5 File size = {h5_size_MB:6.0f} MB, {n_h5_files = }')

        print(f'\n{telescop}, {time_string}, {mjd_day=}, {src_name}, {ra_deg = :.3f}, {dec_deg = :.3f}')
        print(f'{ctr_freq_MHz = :.3f}, {obs_bw_MHz = }, {chan_bw = :.3f}, {f_min_MHz = :.3f}, {f_max_MHz = :.3f}')

        print(f'\n{t_obs = :.3f}, {n_coarse_channels = }, {n_bits = }, {chan_bw = :.3f}')
        print(f'{fs_coarse = :.3f}, {fine_fft_size = }, {n_sti = }, {n_lti = }, {n_avg = }')
        print(f'{t_coarse = :.3e}, {t_fine = :.3f}, {t_res = :.3f}')
        print(f'{fs_coarse = :.3f}, {fs_fine = :.3f}')

    return p