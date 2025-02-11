# seti_test_file_gen
Generate raw test files with a large number of drifting tones for De-Doppler testing, using setigen.

The jupyter notebook "00_multichirp_raw_file_gen.ipynb" generates a RAW file with multiple drifting tones in noise (e.g. 80 tones across one coarse channel).  These can be used for end-to-end testing of DeDoppler detection performance.  

Note: For 00_multichirp_raw_file_gen.ipynb, only a single array element (or beam) is generated for use in seticore dedoppler mode or in turbo seti. Currently, raw files with GBT, MeerKat or COSMIC parameters may be generated. After generating the raw file, rawspec is run and spectra are created for verification.

A limited number of coarse channels are generated, typically 4 or 8.  As configured, the tones will appear one coarse channel, and are set up to span this channel from edge to edge.  For the multiple tones, drift rates are assigned from min to max corresponding to frequencies min to max.  The assigned center frequency of the coarse channels is unimportant as the signal generation assumes a baseband model.  Setigen creates multiple signals in noise, and passes these through a polyphase filter bank with an 8-bit quantizer for each I/Q stream applied to each coarse channel.

Setup instructions appear in the jupyter files themselves.

The raw files tend to be large (e.g. 16 GB for 8 coarse channels/2 polarizations/single dish for GBT parameters and 366 seconds), and are time consuming to generate. In general these should be generated once, placed in bulk storage, and copied locally as needed.