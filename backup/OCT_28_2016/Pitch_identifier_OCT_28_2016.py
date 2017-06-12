# program dft
# programmer Oliver Zhang
# date Oct 28 2016

import wave
from signalprocessing import *


filename = "data/short_piano_A_unsigned_8bit.wav"
wave_file = wave.open(filename, "rb")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wave_file.getparams()

samples = list(wave_file.readframes(nframes))
# converts each sample from an unsigned 8 bit bytestring into a float between -1.0 and 1.0
samples = [(ord(sample) - 128) / 256.0 for sample in samples]
nsamples = len(samples)

print "framerate:", framerate, "Hz"
print "number of frames:", nframes
print "sample width:", sampwidth, "bytes"


start_freq = note_to_hertz("A", accidental="#", octave=1)
end_freq = note_to_hertz("A", accidental=None, octave=8)
step_semitones = 2.0
thres_semitones = 0.001

start_bin = hertz_to_freq_bin(start_freq, framerate, nsamples)
end_bin = hertz_to_freq_bin(2000, framerate, nsamples)
step_ratio = 2**(step_semitones/12)
thres = 2**(thres_semitones/12)

print "initial conditions:", start_bin, end_bin, step_ratio
dft_x, dft_bins = dft(samples, start_bin, end_bin, step_ratio)

max_bin, max_value = get_max(dft_x, dft_bins)
max_bin_index = dft_x.index(max_bin)

initial_p1 = dft_x[max_bin_index - 1], dft_bins[max_bin_index - 1]
initial_p2 = max_bin, max_value
initial_p3 = dft_x[max_bin_index + 1], dft_bins[max_bin_index + 1]

print "error threshold:", thres
peak_x, peak_bin =  dft_peak_x_thres(initial_p1, initial_p2, initial_p3, samples, thres)
print "k:", peak_x, "    power:", peak_bin, "     freq:", freq_bin_to_hertz(peak_x, framerate, nframes), "Hz"
print "note:", hertz_to_note(freq_bin_to_hertz(peak_x, framerate, nframes))
'''




N = len(samples)
initial_k = 39 - 5
for shift in range(1000):
    k = initial_k + shift * 0.01
    freq_bin_mag = freq_bin_at(k, samples)
    # print "k:", k, "    power:", freq_bin_mag, "     freq:", freq_bin_to_hertz(k, framerate, nframes), "Hz"
    # print "note:", hertz_to_note(freq_bin_to_hertz(k, framerate, nframes))
    print freq_bin_mag
    # print'''