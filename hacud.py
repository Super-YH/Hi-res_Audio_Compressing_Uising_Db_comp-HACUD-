import numpy as np
import librosa
import sys
import math
import soundfile as sf
import tqdm

def encode(dat, fs):
    dat /= 2
    ffted = librosa.stft(dat)
    ffted_base = np.zeros((int(ffted.shape[0]/2), ffted.shape[1]), dtype = 'complex_')
    ffted_hf = np.zeros(((int(ffted.shape[0]/2), ffted.shape[1])), dtype = 'complex_')
    for i in tqdm.tqdm(range(ffted.shape[1])):
        ffted_base[:,i] = (ffted[:,i][:int(ffted.shape[0]/2)])
        ffted_hf[:,i] = (ffted[:,i][int(ffted.shape[0]/2+1):])
    iffted_base = librosa.istft(ffted_base)
    iffted_hf = librosa.istft(ffted_hf)
    iffted_base = librosa.db_to_amplitude(librosa.amplitude_to_db(iffted_base)/2) * np.sign(iffted_base)
    iffted_hf = librosa.db_to_amplitude(librosa.amplitude_to_db(iffted_hf)/16) * np.sign(iffted_hf)
    for i in tqdm.tqdm(range(1)):
        N = 1
        delta, sigma = np.zeros(N+1), np.zeros(N+1)
        a = np.arange(N+1)
        out = 0
        out2 = 0
        for j in tqdm.tqdm(range(len(iffted_base))):
            for k in range(1,N+1):
                if k == 1:
                    sigma[k] += iffted_base[j] - out2
                else:
                    sigma[k] += sigma[k-1] - out2
            out2 = (np.round(sigma[-1]*(2**(10-1))))/(2**(10-1))
            for k in range(1,N+1):
                if not k == N:
                    delta[k] = delta[k+1]
                else:
                    delta[k] = out2
            iffted_base[j] = out2
        delta, sigma = np.zeros(N+1), np.zeros(N+1)
    for i in tqdm.tqdm(range(1)):
        N = 1
        delta, sigma = np.zeros(N+1), np.zeros(N+1)
        a = np.arange(N+1)
        out = 0
        out2 = 0
        for j in tqdm.tqdm(range(len(iffted_hf))):
            for k in range(1,N+1):
                if k == 1:
                    sigma[k] += iffted_hf[j] - out2
                else:
                    sigma[k] += sigma[k-1] - out2
            out2 = (np.round(sigma[-1]*(2**(6-1))))/(2**(6-1))
            for k in range(1,N+1):
                if not k == N:
                    delta[k] = delta[k+1]
                else:
                    delta[k] = out2
            iffted_hf[j] = out2
        delta, sigma = np.zeros(N+1), np.zeros(N+1)
    return ((np.round(iffted_hf*(2**5))+(2**5)) + np.round(iffted_base*(2**9)) * (2**6))/(2**15)

def decode(dat, fs):
    dat *= 2**15
    hf = ((dat % (2**6))-(2**5))/(2**5)
    base = np.round(dat / (2**6)) / (2**9)
    base = librosa.db_to_amplitude(librosa.amplitude_to_db(base)*2) * np.sign(base)
    hf = librosa.db_to_amplitude(librosa.amplitude_to_db(hf)*16) * np.sign(hf)
    ffted_base = librosa.stft(base, n_fft=512)
    ffted_hf = librosa.stft(hf, n_fft=512)
    ffted_all = np.zeros((ffted_hf.shape[0]*2, ffted_hf.shape[1]), dtype = 'complex_')
    for i in tqdm.tqdm(range(ffted_base.shape[1])):
        ffted_all[:,i][:ffted_hf.shape[0]] = ffted_base[:,i]
        ffted_all[:,i][ffted_hf.shape[0]:] = ffted_hf[:,i]
    return librosa.istft(ffted_all)*2

def main():
    mode = sys.argv[1]
    input = sys.argv[2]
    output = sys.argv[3]
    dat, fs = sf.read(input)
    if mode == "enc":
        l = encode(dat[:,0], fs)
        r = encode(dat[:,1], fs)
    if mode == "dec":
        l = decode(dat[:,0], fs)
        r = decode(dat[:,1], fs)
    dat = np.array([l,r]).T
    if mode == "enc":
        sf.write(output, dat, int(fs/2), format="WAV", subtype="PCM_16")
    if mode == "dec":
        sf.write(output, dat, fs*2, format="WAV", subtype="PCM_24")
    return 0

if __name__ == '__main__':
    main()
