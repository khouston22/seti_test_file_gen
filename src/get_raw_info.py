# -*- coding: utf-8 -*-
"""
Functions to read header information into convenient variables
@author: K Houston, B. Bryski
"""
import sys
import os

import numpy as np
from astropy import units as u
import blimpy as bl

from pathlib import Path

sys.path.append(os.getenv('SETIGEN_PATH'))

import setigen as stg

def get_blocks_in_raw_group(raw_file_stem,
        raw_dir,
        verbose=True):
    """
    finds all files in raw file group and computes number of blocks
    """
    # os.system('ls -A ' + raw_dir + raw_file_stem + '*.raw')
    # os.system('ls -A ' + raw_dir + raw_file_stem + '*.raw | wc -l ')
    # import subprocess
    # n_raw_files_str = subprocess.check_output('ls -A ' + raw_dir + raw_file_stem + '*.raw | wc -l ', shell=True) 
    # n_raw_files = int(n_raw_files_str[0:-1])
    # print(n_raw_files)

    raw_file_base_name = raw_dir + raw_file_stem + '.0000.raw'

    n_raw_files = 0
    n_blocks = 0
    i_file = -1
    while True:
        i_file += 1
        raw_file_name = raw_dir + raw_file_stem + f'.{i_file:04d}.raw'
        if os.path.isfile(raw_file_name): 
            n_raw_files = i_file + 1
            # get # blocks
            header = stg.voltage.read_header(raw_file_base_name)
            header_size = int(512 * np.ceil((80 * (len(header) + 1)) / 512))
            block_size = int(header['BLOCSIZE'])
            raw_file_stats = os.stat(raw_file_name)
            raw_file_size = raw_file_stats.st_size
            n_blocks_incr = round((raw_file_size-header_size)/block_size)
            n_blocks += n_blocks_incr
            if verbose: print(f'{raw_file_name=} found, {n_blocks_incr=}, {n_blocks=}')
            if (n_blocks_incr==0): 
                print(f'{n_blocks_incr=}, {raw_file_size=}, {header_size=}, {block_size=} {(raw_file_size-header_size)/block_size}')
        else:
            if verbose: print(f'{raw_file_name=} not found, {n_raw_files=}, Total blocks={n_blocks}')
            break

    return n_blocks, n_raw_files

def get_run_params(raw_file_stem,
        raw_dir,
        fine_fft_size,
        n_sti,
        verbose=True):
    """
    returns dictionary of key raw file run parameters
    """
    n_blocks, n_raw_files = get_blocks_in_raw_group(raw_file_stem,raw_dir,verbose)

    raw_file_base_name = raw_dir + raw_file_stem + '.0000.raw'
        
    header = stg.voltage.read_header(raw_file_base_name)
    header_size = int(512 * np.ceil((80 * (len(header) + 1)) / 512))

    telescop = header['TELESCOP'] # 'GBT     '
    time_string = header['DAQPULSE'] #: 'Thu Sep 10 20:33:03 2020' local time
    mjd_day = int(header['STT_IMJD']) #: '59103'
    src_name = header['SRC_NAME'] #: 'KEPLER-160'
    ra_deg = float(header['RA']) #: '287.7736'
    dec_deg = float(header['DEC']) #: '42.8694'
    ctr_freq_MHz = float(header['OBSFREQ']) #: '845.21484375' center freq
    obs_bw_MHz = float(header['OBSBW']) #: '-187.5'
    obs_bw_sign = 1 if (obs_bw_MHz > 0.) else -1
    f_min_MHz = ctr_freq_MHz - abs(obs_bw_MHz)/2.
    f_max_MHz = ctr_freq_MHz + abs(obs_bw_MHz)/2.

    n_bits = int(header['NBITS'])
    chan_bw = float(header['CHAN_BW']) * 1e6
    n_pols = int(header['NPOL'])
    if n_pols == 4: n_pols = 2
    block_size = int(header['BLOCSIZE'])
    t_coarse = float(header['TBIN'])
    try:
        n_antennas = int(header['NANTS'])
    except KeyError:
        n_antennas = 1
    n_coarse_channels = int(header['OBSNCHAN']) // n_antennas

    t_fine = t_coarse * fine_fft_size
    t_res = t_fine * n_sti
    samples_per_block = block_size/n_pols/n_coarse_channels/n_antennas/(2*n_bits/8)
    n_coarse_samples = n_blocks*samples_per_block
    n_fine_samples = n_coarse_samples/fine_fft_size
    n_lti = n_fine_samples//n_sti
    n_avg = n_lti*n_sti
    t_obs = t_fine*n_avg
    obs_time_per_block = t_obs/n_blocks
    
    fs_coarse = 1/t_coarse
    fs_fine = 1/t_fine

    fch1 = ctr_freq_MHz - abs(obs_bw_MHz)/2. + chan_bw/2.*1e-6
    foff = fs_fine

    raw_file_stats = os.stat(raw_file_base_name)
    raw_size_MB = raw_file_stats.st_size/1024./1024.
    n_blocks_base = (raw_file_stats.st_size-header_size)//block_size
    expected_file_size = n_antennas*n_pols*n_coarse_channels*n_coarse_samples*2/1024./1024.

    p = {'raw_file_stem':raw_file_stem}
    p['raw_size_MB'] = raw_size_MB
    p['n_raw_files'] = n_raw_files

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
    p['n_antennas'] = n_antennas
    p['n_coarse_channels'] = n_coarse_channels
    p['n_pols'] = n_pols
    p['n_bits'] = n_bits
    p['fs_coarse'] = fs_coarse
    p['fine_fft_size'] = fine_fft_size
    p['n_sti'] = n_sti
    p['n_lti'] = n_lti
    p['n_avg'] = n_avg
    p['t_coarse'] = t_coarse
    p['t_fine'] = t_fine
    p['t_res'] = t_res
    p['n_coarse_samples'] = n_coarse_samples
    p['n_fine_samples'] = n_fine_samples
    p['fs_fine'] = fs_fine
    p['samples_per_block'] = samples_per_block
    p['n_blocks'] = n_blocks
    p['n_blocks_base'] = n_blocks_base
    p['block_size'] = block_size
    p['obs_time_per_block'] = obs_time_per_block
    p['raw_dir'] = raw_dir
    
    if verbose:
        print(f'{raw_file_base_name = }')
        if os.path.isfile(raw_file_base_name): print('Raw file found')
        print(f'Raw File size = {raw_size_MB:6.0f} MB, {n_raw_files = }')
        print(f'{expected_file_size = } MB excl header')

        print(f'\n{telescop}, {time_string}, {mjd_day=}, {src_name}, {ra_deg = :.3f}, {dec_deg = :.3f}')
        print(f'{ctr_freq_MHz = :.3f}, {obs_bw_MHz = }, {chan_bw = :.3f}, {f_min_MHz = :.3f}, {f_max_MHz = :.3f}')

        print(f'\n{t_obs = :.3f}, {n_antennas = }, {n_coarse_channels = }, {n_pols = }, {n_bits = }, {chan_bw = :.3f}')
        print(f'{fs_coarse = :.3f}, {fine_fft_size = }, {n_sti = }, {n_lti = }, {n_avg = }')
        print(f'{t_coarse = :.3e}, {t_fine = :.3f}, {t_res = :.3f}')
        print(f'{fs_coarse = :.3f}, {fs_fine = :.3f}')
        print(f'{n_coarse_samples = }, {n_fine_samples = }')
        print(f'{samples_per_block = }, {n_blocks = }, {n_blocks_base = }, {block_size = }, {obs_time_per_block = :.3f}\n')

    return p, header