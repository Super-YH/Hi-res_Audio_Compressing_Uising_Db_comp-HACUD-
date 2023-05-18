# Hi-res_Audio_Compressing_Uising_Db_comp-HACUD-
This can encord 96KHz/24Bit to 48KHz/16Bit. and Encoding is possible while preserving as much of the original spectrogram as possible. (also above 24KHz signal)

This Time, I made Hi-res compress format like mqa, I upload it.
It called HACUD anyway. (I decide it.)

features:
  1. Hyper-Super-Light Decoding.
  2. Encoding is possible while preserving as much of the original spectrogram as possible. 

structure:
  1. Split to 2 Bands (Base/HF)
  2. Base Band will db-compress 2x.
  3. High-Freq Band will db-compress 32x.
  4. Both band will noise-shape 1 dimension.
  5. Base will be 10-Bit and HF will be 6-Bit.
  6. Mix Base and HF.

WARNING: Output signal is so-loud. Don't listen to Encoded WAVE Anyway.

