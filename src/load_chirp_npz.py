# -*- coding: utf-8 -*-
"""
Script to take npz keys form npz file and place members in local variables
Requires npz_file = '--/---' prior to calling
Call: %run -i "~/load_chirp_npz.py"
@author: K Houston
"""

z  = np.load(npz_file,allow_pickle=True)
p = z['p']
p = p.tolist()

test_case = np.array2string(z['test_case'])
test_case = test_case[1:-1]

fine_fft_size_list = z['fine_fft_size_list']
n_sti_list = z['n_sti_list']
n_lti_list = z['n_lti_list']
T_avg_list = z['T_avg_list']

telescope = np.array2string(z['telescope'])
telescope = telescope[1:-1]

samples_per_block = z['samples_per_block']
search_max_drift = z['search_max_drift']
search_min_drift = z['search_min_drift']
search_z_threshold = z['search_z_threshold']
select_params = z['select_params']
select_params2 = z['select_params2']
f_sigma_drift = z['f_sigma_drift']
sigma_drift = z['sigma_drift']
run_turbo = z['run_turbo']
run_seticore = z['run_seticore']

search_app_name = np.array2string(z['search_app_name'])
search_app_name = search_app_name[1:-1]
search_app_string = search_app_name

time_rawspec = z['time_rawspec']
time_search = z['time_search']
time_search_total = z['time_search_total']
time_run = z['time_run']
f_start_truth_all = z['f_start_truth_all']
drift_rate_truth_all = z['drift_rate_truth_all']
ref_snr_db_all = z['ref_snr_db_all']
n_det_all = z['n_det_all']
n_det1 = z['n_det1']
det_f_start_MHz_all = z['det_f_start_MHz_all']
det_drift_rate_all = z['det_drift_rate_all']
det_snr_db_all = z['det_snr_db_all']
N_spread_all = z['N_spread_all']
det_snr_db_wavg_all = z['det_snr_db_wavg_all']
raw_size_MB = z['raw_size_MB']
h5_size_MB_all = z['h5_size_MB_all']
n_coarse_channels = z['n_coarse_channels']

if (0):
    dechirp_eff_db_all = z['dechirp_eff_db_all']
    dechirp_eff_pct_all = z['dechirp_eff_pct_all']
    pred_dechirp_eff_pct_all = z['pred_dechirp_eff_pct_all']
    pred_dechirp_eff_db_all = z['pred_dechirp_eff_db_all']
    pred_sqrt_dechirp_eff_pct_all = z['pred_sqrt_dechirp_eff_pct_all']
    pred_sqrt_dechirp_eff_db_all = z['pred_sqrt_dechirp_eff_db_all']
    dechirp_eff_pct_wavg_all = z['dechirp_eff_pct_wavg_all']
else:
    dechirp_eff_db_all = z['det_eff_db_all']
    dechirp_eff_pct_all = z['det_eff_pct_all']
    pred_dechirp_eff_pct_all = z['pred_det_eff_pct_all']
    pred_dechirp_eff_db_all = z['pred_det_eff_db_all']
    pred_sqrt_dechirp_eff_pct_all = z['pred_sqrt_det_eff_pct_all']
    pred_sqrt_dechirp_eff_db_all = z['pred_sqrt_det_eff_db_all']
    dechirp_eff_pct_wavg_all = z['det_eff_pct_wavg_all']

t_obs = p['t_obs']
search_app_string = search_app_name
n_det_max = det_snr_db_all.shape[0]
raw_file_base_name = p['raw_file_stem']
raw_file_stem = p['raw_file_stem']

sig_max_drift = search_max_drift
sig_min_drift = search_min_drift