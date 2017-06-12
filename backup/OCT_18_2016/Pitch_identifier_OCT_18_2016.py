# program dft
# programmer Oliver Zhang
# date Oct 14 2016

"""Must use unsigned 8 bit WAV input data"""

import wave
from signalprocessing import *

filename = "data/short_piano_A_unsigned_8bit.wav"
wave_file = wave.open(filename, "rb")

(nchannels, sampwidth, framerate, nframes, comptype, compname) = wave_file.getparams()

print "framerate:", framerate, "Hz"
print "number of frames:", nframes
print "sample width:", sampwidth, "bytes"

samples = list(wave_file.readframes(nframes))
# converts each sample from an unsigned 8 bit bytestring into a float between -1.0 and 1.0
samples = [(ord(sample) - 128) / 256.0 for sample in samples]

freq_bins = dft(samples)
prominent_freq_bin = max_bin(freq_bins)
prominent_freq = freq_bin_to_hertz(prominent_freq_bin, framerate, nframes)
print "detected frequency:", prominent_freq, "Hz"
detected_note = hertz_to_note(prominent_freq)
print detected_note[0] + str(detected_note[1]), detected_note[2], "cents"

'''N = len(samples)
base_freq = note_to_freq("A", octave=4, accidental=None)
harmonic_bins = freq_to_harmonic_freq_bins(base_freq, framerate, N, 5)
for sample in samples: print sample
K = harmonic_bins[0]
for K in harmonic_bins[1]:
for k in range(N):
    # k = K + i * 1
    Re = sum(samples[n] * cos(2 * pi * k * n / N) for n in range(N))
    Im = sum(samples[n] * sin(2 * pi * k * n / N) for n in range(N))
    mag_squared = Re ** 2 + Im ** 2
    # print "k:", k, "    power:", mag_squared, "     freq:", freq_bin_to_hertz(k, framerate, nframes), "Hz"
    print mag_squared'''