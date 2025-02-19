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

def db(x):
    """ Convert linear value to dB value """
    return 10*np.log10(np.abs(x.astype(np.float64))+1e-20)

def plot_h5_sg(base_h5_name,
        fig =[],
        fig_f_limits_MHz=[],
        min_max_db=[],
        fig_title='',
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrogram of h5 filterbank file over desired frequency range
    """
    if len(fig_f_limits_MHz)==2:
        wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])
    else:
        wf = bl.Waterfall(base_h5_name)

    if not fig:
        fig = plt.figure(figsize=(10, 6))
        this_is_subplot = False
    else:
        this_is_subplot = True

    # wf.plot_waterfall(logged=True,cb=False)
    wf.plot_waterfall()
    
    # if len(min_max_db)==2     # TODO: add limits
    #     plt.colorbar(???)
    if len(fig_title)>0:
        plt.title(fig_title)

    if this_is_subplot:
        return

    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    else:
        plt.close(fig)

    return

def plot_h5_sg_psd(base_h5_name,
        fig_f_limits_MHz=[],
        min_max_db=[],
        fig_title='',
        fig_text_list=[],
        rel_freq = False,
        display_fig=True,
        savfig_name=''):
    """
    Plots psd(top) and spectrogram (bottom) of h5 filterbank file over desired frequency range
    """
    if len(fig_f_limits_MHz)==2:
        wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])
    else:
        wf = bl.Waterfall(base_h5_name)
                      
    fig = plt.figure(figsize=(10, 6))

    plt.subplot(2,1,1)

    plot_h5_psd_db(base_h5_name,
        fig = fig,
        wf = wf,
        fig_f_limits_MHz=[],
        min_max_db=min_max_db,
        fig_title=fig_title,
        fig_text_list=fig_text_list,
        rel_freq = rel_freq)

    plt.subplot(2,1,2)
    
    # wf.plot_waterfall(logged=True,cb=False)
    wf.plot_waterfall(cb=False)

    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    else:
        plt.close(fig)

    return

def plot_h5_psd_db(base_h5_name,
        fig = [],
        wf = [],
        fig_f_limits_MHz=[],
        min_max_db=[],
        fig_title='',
        fig_text_list=[],
        rel_freq = True,
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrum in dB of h5 filterbank file over desired frequency range,
    but optionally plots frequency axis in KHz offset from center frequency when rel_freq is True
    Uses blimpy waterfall and plot_spectrum functions
    """
    if not wf:  # if wf empty, not passed into fn
        if len(fig_f_limits_MHz)==2:
            wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])
        else:
            wf = bl.Waterfall(base_h5_name)
        
    if len(fig_f_limits_MHz)==2:
        freqs, plot_data = wf.grab_data(fig_f_limits_MHz[0],fig_f_limits_MHz[1])
    else:
        freqs, plot_data = wf.grab_data()

    # Using accending frequency for all plots.
    if wf.header['foff'] < 0:
        plot_data = plot_data[..., ::-1]  # Reverse data
        freqs = freqs[::-1]

    if len(fig_f_limits_MHz)!=2:
        fig_f_limits_MHz = [freqs[0],freqs[-1]]

    if len(plot_data.shape) > 1:
        spectrum = db(plot_data.mean(axis=0))
    else:
        spectrum = db(plot_data.mean())
    
    f_mid = (fig_f_limits_MHz[0]+fig_f_limits_MHz[1])/2.
    
    if rel_freq:
        freqs = (freqs - f_mid)*1e3
        f1 = (fig_f_limits_MHz[0]-f_mid)*1e3
        f2 = (fig_f_limits_MHz[1]-f_mid)*1e3
    else:
        f1 = fig_f_limits_MHz[0]
        f2 = fig_f_limits_MHz[1]
    
    if not fig:
        fig = plt.figure(figsize=(10, 6))
        this_is_subplot = False
    else:
        this_is_subplot = True
    
    plt.plot(freqs,spectrum)
    
    if len(fig_title)>0:
        plt.title(fig_title)
    if len(fig_f_limits_MHz)==2:
        plt.xlim(f1,f2)
    if len(min_max_db)==2:
        plt.ylim(min_max_db[0],min_max_db[1])
    
    plt.ylabel('Spectrum Level (dB)')
    for ifig,ft in enumerate(fig_text_list):
        plt.figtext(ft[0],ft[1],ft[2])
    plt.grid()
    
    if this_is_subplot:
        return
    
    if rel_freq:
        plt.xlabel(f'Frequency (KHz) offset from {f_mid:.6f} MHz')
    else:
        plt.xlabel(f'Frequency (MHz)')

    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    else:
        plt.close(fig)
    return

def plot_h5_psd_db_bl(base_h5_name,
        fig = [],
        wf = [],
        fig_f_limits_MHz=[],
        min_max_db=[],
        fig_title='',
        fig_text_list=[],
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrum in dB of h5 filterbank file over desired frequency range
    Uses blimpy waterfall and plot_spectrum functions
    """
    if not wf:  # if wf empty, not passed into fn
        if len(fig_f_limits_MHz)==2:
            wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])
        else:
            wf = bl.Waterfall(base_h5_name)

    if not fig:
        fig = plt.figure(figsize=(10, 6))
        this_is_subplot = False
    else:
        this_is_subplot = True

    wf.plot_spectrum(t='all',logged=True)

    if len(fig_title)>0:
        plt.title(fig_title)
    if len(fig_f_limits_MHz)==2:
        plt.xlim(fig_f_limits_MHz[0],fig_f_limits_MHz[1])
    if len(min_max_db)==2:
        plt.ylim(min_max_db[0],min_max_db[1])
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Spectrum Power Level (dB)')
    for ifig,ft in enumerate(fig_text_list):
        plt.figtext(ft[0],ft[1],ft[2])
    plt.grid()

    if this_is_subplot:
        return

    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    else:
        plt.close(fig)
    return

def plot_h5_psd_linear(base_h5_name,
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


