# -*- coding: utf-8 -*-
"""
Script to take run parameters dictionary and place members in local variables
Requires p=get_run_params() prior to calling
e.g. p = ~.get_run_params(raw_file_stem,raw_dir,fine_fft_size,n_sti)
Call: %run -i "~/raw_info_script.py"
@author: K Houston, B. Bryski
"""

raw_size_MB = p['raw_size_MB']
n_raw_files = p['n_raw_files']

telescop = p['telescop']
time_string = p['time_string']
mjd_day = p['mjd_day']
src_name = p['src_name']
ra_deg = p['ra_deg']
dec_deg = p['dec_deg']
ctr_freq_MHz = p['ctr_freq_MHz']
obs_bw_MHz = p['obs_bw_MHz']
obs_bw_sign = p['obs_bw_sign']
chan_bw = p['chan_bw']
f_min_MHz = p['f_min_MHz']
f_max_MHz = p['f_max_MHz']
fch1 = p['fch1']
foff = p['foff']

t_obs = p['t_obs']
n_antennas = p['n_antennas']
n_coarse_channels = p['n_coarse_channels']
n_pols = p['n_pols']
n_bits = p['n_bits']
fs_coarse = p['fs_coarse']
fine_fft_size = p['fine_fft_size']
n_lti = p['n_lti']
n_avg = p['n_avg']
t_coarse = p['t_coarse']
t_fine = p['t_fine']
t_res = p['t_res']
n_coarse_samples = p['n_coarse_samples']
n_fine_samples = p['n_fine_samples']
fs_fine = p['fs_fine']
samples_per_block = p['samples_per_block']
n_blocks = p['n_blocks']
n_blocks_base = p['n_blocks_base']
block_size = p['block_size']
obs_time_per_block = p['obs_time_per_block']
    

