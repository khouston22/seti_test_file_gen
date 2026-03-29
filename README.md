# seti_test_file_gen
Generate a) raw test files with a large number of drifting tones for De-Doppler testing, using setigen, or b) create/modify h5 capture files with a large number of drifting tones.  

#### Option a): 

This uses setigen voltage mode to create actual chirps which are added to Gaussian noise and saved into raw files.  These can be converted into spectra and h5 files using rawspec.

The jupyter notebook "00_multichirp_raw_file_gen.ipynb" generates a RAW file with multiple drifting tones in noise (e.g. 80 tones across one coarse channel).  These can be used for end-to-end testing of DeDoppler detection performance.  

Note: For 00_multichirp_raw_file_gen.ipynb, only a single array element (or beam) is generated for use in seticore dedoppler mode or in turbo seti. Currently, raw files with GBT, MeerKat or COSMIC parameters may be generated. After generating the raw file, rawspec is run and spectra are created for verification.

A limited number of coarse channels are generated, typically 4 or 8.  As configured, the tones will appear one coarse channel, and are set up to span this channel from edge to edge.  For the multiple tones, drift rates are assigned from min to max corresponding to frequencies min to max.  The assigned center frequency of the coarse channels is unimportant as the signal generation assumes a baseband model.  Setigen creates multiple signals in noise, and passes these through a polyphase filter bank with an 8-bit quantizer for each I/Q stream applied to each coarse channel.

Setup instructions appear in the jupyter files themselves.

The raw files tend to be large (e.g. 16 GB for 8 coarse channels/2 polarizations/single dish for GBT parameters and 366 seconds), and are time consuming to generate. In general these should be generated once, placed in bulk storage, and copied locally as needed.

#### Option b): 

This uses setigen to add simulated drifting tones to spectra from an existing h5 capture file, and outputs to a new h5 or fil file.  With a simulated chi-squared noise-only file, this can be used to evaluate noise-only detection performance.  With h5 files from actual captures, tones are added to the capture.  This can be used to evaluate detection performance with various levels of RFI.

Jupiter notebook 01_gen_synthetic_h5.ipynb creates simulated chi-square noise h5 capture files with various PFB filter bank frequency responses, and spectral slopes (non-flat over many coarse channels).

Jupiter notebook 02_sig_inject.ipynb inputs h5 capture files (real or simulated) and adds simulated drifting tones using setigen, and outputs h5 or fil files.