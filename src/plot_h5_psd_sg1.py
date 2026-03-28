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
from src import get_h5_info as h5info

def db(x):
    """ Convert linear value to dB value """
    return 10*np.log10(np.abs(x.astype(np.float64))+1e-20)

def get_dc_freqs(f12,fch1,foff,fine_fft_size):
    """ 
    Return dc freq values given plot limits f12=[f1,f2] - may be empty
    Bin offset is from lower frequency min(f1,f2)
    """
    f_dc_MHz = []
    bin_offset = []
    
    coarse_bw_MHz = foff*fine_fft_size
    coarse_limits = np.round((f12-fch1)/coarse_bw_MHz)
    if (coarse_limits[0]>coarse_limits[1]):
        coarse_limits = [coarse_limits[1],coarse_limits[0]]
    coarse_dc = np.arange(coarse_limits[0]+0.5,coarse_limits[1],1.0)
    if (len(coarse_dc)>0):
        # quantize for added precision
        coarse_dc_x2 = np.round(coarse_dc*2.).astype(int)
        f_dc_MHz = fch1 + (coarse_dc_x2*fine_fft_size/2)*foff
        bin_offset = np.round((f_dc_MHz-min(f12))/abs(foff)).astype(int)
        # print(f'{f12=}, {coarse_limits=}, {coarse_dc=}, {f_dc_MHz=}, {bin_offset=}')
    return f_dc_MHz, bin_offset

def DC_replace(psd_ctr, DC_replace_ofs=15, DC_mean_pts=40):
    """ 
    Remove DC bins and replace by adjacent mean
    psd_ctr is part of a vector of PSD values centered on the DC (mid) point
    call sequence:
        ii_ctr = range(i_dc-n_ctr2,i_dc+n_ctr2+1) 
        psd[ii_ctr] = DC_replace(psd[ii_ctr],DC_replace_ofs,DC_mean_pts)
    Note: 2*n_ctr2 + 1 >= 2*DC_mean_pts + 2*DC_replace_ofs + 1
    """
    if (len(psd_ctr) < 2*DC_mean_pts + 2*DC_replace_ofs + 1):
        print('DC_replace: {DC_replace_ofs=} {DC_mean_pts=} {len(psd_ctr)=} vs. {2*DC_mean_pts + 2*DC_replace_ofs + 1} required')
        raise ValueError("Error in DC_replace: length of psd center segment is too small")
    
    i_ctr = len(psd_ctr)//2
    adj_mean = (np.sum(psd_ctr[i_ctr - DC_replace_ofs - np.arange(DC_mean_pts)]) + \
                np.sum(psd_ctr[i_ctr + DC_replace_ofs + np.arange(DC_mean_pts)]))/(2*DC_mean_pts)
    
    psd_ctr[i_ctr - DC_replace_ofs + np.arange(2*DC_replace_ofs+1)] = adj_mean

    return psd_ctr

def DC_replace_test(i_dc=60,n_ctr2=70,DC_replace_ofs=15, DC_mean_pts=40):
    """ 
    Test of DC_replace function
    """
    rng = np.random.default_rng()
    wgn = rng.normal(size=(2*n_ctr2+1,100))
                        
    psd = np.mean(np.square(wgn),axis=1)
    psd[i_dc] += 100
    ii_ctr = np.arange(i_dc-n_ctr2,i_dc+n_ctr2+1) 
    print(ii_ctr)
    print(np.round(psd[ii_ctr]*1000.).astype(int))
    psd[ii_ctr] = DC_replace(psd[ii_ctr],DC_replace_ofs, DC_mean_pts)
    print(np.round(psd[ii_ctr]*1000.).astype(int))
    return 0
    
def plot_h5_sg(base_h5_name,
        fig =[],
        fig_f_limits_MHz=[],
        min_max_db=[],
        fig_title='',
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrogram of h5 filterbank file over desired frequency range
    TODO: Apply DC blanking to waterfall plots (spectrograms)
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
    # wf.plot_waterfall(origin='upper')   # reverses image top <-> bottom, but time axis doesn't change
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
        f_ref_list_MHz=[],
        min_max_db=[],
        fig_title='',
        fig_text_list=[],
        rel_freq = False,
        dc_blank_enable = False,
        display_fig=True,
        savfig_name=''):
    """
    Plots psd(top) and spectrogram (bottom) of h5 filterbank file over desired frequency range
    Also plots vertical reference lines in spectrum at frequencies in f_ref_list_MHz
    TODO: Apply DC blanking to waterfall plots (spectrograms)
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
        f_ref_list_MHz=f_ref_list_MHz,
        min_max_db=min_max_db,
        fig_title=fig_title,
        fig_text_list=fig_text_list,
        dc_blank_enable = dc_blank_enable,
        rel_freq = rel_freq)

    plt.subplot(2,1,2)
    
    # wf.plot_waterfall(logged=True,cb=False)
    wf.plot_waterfall(cb=False)

    if len(savfig_name)>0:
        plt.savefig(savfig_name,bbox_inches='tight')
    if display_fig:
        plt.show()
    plt.close(fig)

    return

def get_h5_psd_db(base_h5_name,
        fig_f_limits_MHz=[],
        fig_t_limits_sec=[],
        dc_blank_enable = True):
    """
    Obtains spectrum in dB of h5 filterbank file over desired range of frequency and time
    Uses blimpy waterfall and plot_spectrum functions
    TODO: Break up time and/or frequency if wf data exceeds memory limits
    """
    if len(fig_f_limits_MHz)==2:
        if len(fig_t_limits_sec)==2:
            wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1],
                              t_start=fig_t_limits_sec[0],t_stop=fig_t_limits_sec[1])
        else:
            wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])
    else:
        if len(fig_t_limits_sec)==2:
            wf = bl.Waterfall(base_h5_name,t_start=fig_t_limits_sec[0],t_stop=fig_t_limits_sec[1])
        else:
            wf = bl.Waterfall(base_h5_name)
    
    freqs_MHz, plot_data = wf.grab_data()

    # Using ascending frequency for all plots.
    if wf.header['foff'] < 0:
        plot_data = plot_data[..., ::-1]  # Reverse data
        freqs_MHz = freqs_MHz[::-1]

    if len(plot_data.shape) > 1:
        spectrum_db = db(plot_data.mean(axis=0))
    else:
        spectrum_db = db(plot_data.mean())
    
    if (dc_blank_enable):
        p = h5info.get_wf_params(wf,base_h5_name,verbose=False)

        f_dc_MHz, bin_offset = get_dc_freqs(fig_f_limits_MHz,p['fch1'],p['foff'],p['fine_fft_size'])
        
        for i_blank in range(len(bin_offset)):
            f_dc = f_dc_MHz[i_blank]
            i_dc = bin_offset[i_blank]
            n_ctr2 = 15
            ii_ctr = np.arange(i_dc-n_ctr2,i_dc+n_ctr2+1) 
            # print(f'Blanking DC at {f_dc:.3f} MHz, offset={i_dc}')
            # print(np.round(spectrum_db[ii_ctr]).astype(int))
            spectrum_db[ii_ctr] = np.nan
            # print(np.round(spectrum_db[ii_ctr]).astype(int))    return freqs_MHz, spectrum_db


def plot_h5_psd_db(base_h5_name,
        fig = [],
        wf = [],
        fig_f_limits_MHz=[],
        f_ref_list_MHz=[],
        min_max_db=[],
        fig_title='',
        fig_text_list=[],
        dc_blank_enable = True,
        rel_freq = True,
        do_plot = True,   
        display_fig=True,
        savfig_name=''):
    """
    Plots spectrum in dB of h5 filterbank file over desired frequency range,
    but optionally plots frequency axis in KHz offset from center frequency when rel_freq is True
    Returns freqs_MHz, spectrum_db without doing plot if do_plot is False
    Uses blimpy waterfall and plot_spectrum functions
    Also plots vertical reference lines at frequencies in f_ref_list_MHz
    DC blanking computes DC frequencies and outputs np.nan in vicinity rather than 
    local noise mean (latter was found to cause out-of-memory issues)
    """
    if not wf:  # if wf empty, not passed into fn
        if len(fig_f_limits_MHz)==2:
            wf = bl.Waterfall(base_h5_name,f_start=fig_f_limits_MHz[0],f_stop=fig_f_limits_MHz[1])
        else:
            wf = bl.Waterfall(base_h5_name)

    if len(fig_f_limits_MHz)==2:
        freqs_MHz, plot_data = wf.grab_data(fig_f_limits_MHz[0],fig_f_limits_MHz[1])
    else:
        freqs_MHz, plot_data = wf.grab_data()

    # Using ascending frequency for all plots.
    if wf.header['foff'] < 0:
        plot_data = plot_data[..., ::-1]  # Reverse data
        freqs_MHz = freqs_MHz[::-1]

    if len(fig_f_limits_MHz)!=2:
        fig_f_limits_MHz = [freqs_MHz[0],freqs_MHz[-1]]

    if (fig_f_limits_MHz[0]>fig_f_limits_MHz[1]):
        fig_f_limits_MHz = [fig_f_limits_MHz[1],fig_f_limits_MHz[0]]

    if len(plot_data.shape) > 1:
        spectrum_db = db(plot_data.mean(axis=0))
    else:
        spectrum_db = db(plot_data.mean())
    
    if (dc_blank_enable):
        p = h5info.get_wf_params(wf,base_h5_name,verbose=False)

        f_dc_MHz, bin_offset = get_dc_freqs(fig_f_limits_MHz,p['fch1'],p['foff'],p['fine_fft_size'])
        
        for i_blank in range(len(bin_offset)):
            f_dc = f_dc_MHz[i_blank]
            i_dc = bin_offset[i_blank]
            n_ctr2 = 15
            ii_ctr = np.arange(i_dc-n_ctr2,i_dc+n_ctr2+1) 
            # print(f'Blanking DC at {f_dc:.3f} MHz, offset={i_dc}')
            # print(np.round(spectrum_db[ii_ctr]).astype(int))
            spectrum_db[ii_ctr] = np.nan
            # print(np.round(spectrum_db[ii_ctr]).astype(int))

    db_min = np.nanmin(spectrum_db)
    db_max = np.nanmax(spectrum_db)
    
    f_mid = (fig_f_limits_MHz[0]+fig_f_limits_MHz[1])/2.
    
    if rel_freq:
        freqs_MHz = (freqs_MHz - f_mid)*1e3
        f1 = (fig_f_limits_MHz[0]-f_mid)*1e3
        f2 = (fig_f_limits_MHz[1]-f_mid)*1e3
    else:
        f1 = fig_f_limits_MHz[0]
        f2 = fig_f_limits_MHz[1]

    if not do_plot:
        return freqs_MHz, spectrum_db
    
    if not fig:
        fig = plt.figure(figsize=(10, 6))
        this_is_subplot = False
    else:
        this_is_subplot = True
    
    for i_f_ref, f_ref in enumerate(f_ref_list_MHz):
        plt.plot([f_ref, f_ref],[db_min-1,db_max-1],'--r')
    
    plt.plot(freqs_MHz,spectrum_db)

    if len(fig_title)>0:
        plt.title(fig_title)
    if len(fig_f_limits_MHz)==2:
        plt.xlim(f1,f2)
    if len(min_max_db)==2:
        plt.ylim(min_max_db[0],min_max_db[1])
    else:
        plt.ylim(db_min-1,db_max+1)
    
    plt.ylabel('dB')
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
    plt.close(fig)
    return


