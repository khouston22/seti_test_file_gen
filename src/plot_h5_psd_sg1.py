# -*- coding: utf-8 -*-
"""
Functions to plot h5 spectra and spectrograms
@author: K Houston
"""
import sys
import os

import matplotlib.pyplot as plt

import numpy as np
from astropy import units as u
import blimpy as bl

from pathlib import Path

sys.path.append(os.getenv('SETIGEN_PATH'))

import setigen as stg

def db(x):
    """ Convert linear value to dB value """
    return 10*np.log10(np.abs(x.astype(np.float64))+1e-20)


def plot_h5_sg1(base_h5_name,
        fig_f_limits_MHz=[],
        min_max_db=[],
        fig_title='',
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrogram of h5 filterbank file over desired frequency range
    """
    wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])
    
    fig = plt.figure(figsize=(10, 6))
    wf.plot_waterfall()
    # if len(min_max_db)==2     # TODO: add limits
    #     plt.colorbar(???)
    if len(fig_title)>0:
        plt.title(fig_title)
    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    else:
        plt.close(fig)

    return

def plot_h5_psd1(base_h5_name,
        fig_f_limits_MHz=[],
        min_max_db=[],
        fig_title='',
        fig_text_list=[],
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrum in dB of h5 filterbank file over desired frequency range
    Uses blimpy waterfall and setigen integrate functions
    """
    wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])

    freqs = wf.get_freqs()[wf.container.chan_start_idx:wf.container.chan_stop_idx]
    
    frame = stg.Frame(wf)

    spectrum = db(stg.integrate(frame, normalize=True))

    fig = plt.figure(figsize=(10, 6))

    if (wf.get_freqs()[-1]>wf.get_freqs()[0]):
        plt.plot(freqs,spectrum)
    else:
        plt.plot(freqs[::-1],spectrum)
    
    if len(fig_title)>0:
        plt.title(fig_title)
    if len(fig_f_limits_MHz)==2:
        plt.xlim(fig_f_limits_MHz[0],fig_f_limits_MHz[1])
    if len(min_max_db)==2:
        plt.ylim(min_max_db[0],min_max_db[1])
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Spectrum Level (dB)')
    for ifig,ft in enumerate(fig_text_list):
        plt.figtext(ft[0],ft[1],ft[2])
    plt.grid()
    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    else:
        plt.close(fig)
    return

def plot_h5_psd2(base_h5_name,
        fig_f_limits_MHz=[],
        min_max=[],
        fig_title='',
        fig_text_list=[],
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrum in linear power units of h5 filterbank file over desired frequency range
    Uses blimpy waterfall and plot_spectrum functions
    """
    wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])

    fig = plt.figure(figsize=(10, 6))
    wf.plot_spectrum(t='all')

    if len(fig_title)>0:
        plt.title(fig_title)
    if len(fig_f_limits_MHz)==2:
        plt.xlim(fig_f_limits_MHz[0],fig_f_limits_MHz[1])
    if len(min_max)==2:
        plt.ylim(min_max[0],min_max[1])
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Spectrum Power Level (linear)')
    for ifig,ft in enumerate(fig_text_list):
        plt.figtext(ft[0],ft[1],ft[2])
    plt.grid()
    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    else:
        plt.close(fig)
    return


