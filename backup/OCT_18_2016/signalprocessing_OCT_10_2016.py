# signalprocessing module
# programmer Oliver Zhang
# date Oct 14 2016

"""Must use unsigned 8 bit WAV input data"""

from math import pi, sin, cos, log

using_sharps = True
letter_to_semitone = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

semitone_to_letter = {0: "C", 1: ("C#", "Db"), 2: "D", 3: ("D#", "Eb"), 4: "E",
                      5: "F", 6: ("F#", "Gb"), 7: "G", 8: ("G#", "Ab"), 9: "A",
                      10: ("A#", "Bb"), 11: "B"}
def dft(samples):
    """returns the discrete fourier transform of samples"""
    freq_bins = []
    N = len(samples)
    # N/2 because we cannot go over the Nyquist limit
    for k in range(N/10):
        Re = sum(samples[n] * cos(2*pi * k * n / N) for n in range(N))
        Im = sum(samples[n] * -sin(2*pi * k * n / N) for n in range(N))
        mag_squared = Re ** 2 + Im ** 2
        freq_bins.append(round(mag_squared, 1))
    return freq_bins


def improve_dft_res(samples, freq_bins, error_threshold_ratio):
    """Tries to improve the resolution of the dft by calculating "fractional"
    freq bins between the peak freq bin and its highest neighbor.
    Returns the improved peak freq bin and its value"""
    peak_bin = max_bin(freq_bins)
    neighbor_bin_val = max(freq_bins(peak_bin + 1), freq_bins(peak_bin - 1))
    neighbor_bin = freq_bins.index(neighbor_bin_val)

    N = len(samples)
    peak_bin_val = freq_bins[peak_bin]
    while True:
        k = (peak_bin + neighbor_bin)/2.0    # k is the bin between peak and neighbor
        Re = sum(samples[n] * cos(2*pi * k * n / N) for n in range(N))
        Im = sum(samples[n] * -sin(2*pi * k * n / N) for n in range(N))
        mag_squared = Re ** 2 + Im ** 2
        print k, mag_squared


def max_bin(sequence):
    return sequence.index(max(sequence))


def find_peaks(samples, n):
    """returns the list of the (index, value) pairs of the highest n peaks in data"""
    samples_copy = list(samples)
    peaks = []
    for i in range(n):
        peak = max(samples_copy)
        peak_index = samples_copy.index(peak)
        peaks.append(peak_index, peak)
        del samples_copy[peak_index]


def freq_bin_to_hertz(bin, samprate, nsamples):
    return float(bin) * samprate / nsamples

def hertz_to_freq_bin(hertz, samprate, nsamples):
    return hertz * (nsamples/float(samprate))

def freq_to_harmonic_freq_bins(hertz, samprate, nsamples, nharmonics):
    fundamental_bin = hertz_to_freq_bin(hertz, samprate, nsamples)
    return [fundamental_bin * (harmonic + 1) for harmonic in range(nharmonics)]


def note_to_freq(letter_name, accidental, octave):
    """returns the frequency (Hz) corresponding to the note information"""

    note_num = letter_to_semitone[letter_name.upper()]
    if accidental == "#":
        note_num += 1
    elif accidental == "b":
        note_num -= 1
    note_num += 12 * (octave - 1) + 4    # add 4 semitones since notes begin at A
    return 440 * 2**((note_num - 49) / 12.0)

def freq_to_note(freq):
    """converts a frequency (Hz) to the name of the closest note, in addition to the
    percentage pitch difference between the frequency given and the frequency
    of the closest note."""

    note = 12 * log((freq/440.0), 2) + 49
    closest_note = int(round(note))
    closest_note_freq = 440 * 2**((closest_note - 49) / 12.0)
    cents = round(1200 * log(freq / closest_note_freq, 2))
    # print (freq/closest_note_freq)    # linear piecewice approximation
    octave = (closest_note - 4) / 12 + 1
    semitone = (closest_note - 4) % 12
    letter_name = semitone_to_letter[semitone]
    if type(letter_name) == tuple:
        if using_sharps:
            letter_name = letter_name[0]
        else:
            letter_name = letter_name[1]

    return (letter_name, octave, cents)