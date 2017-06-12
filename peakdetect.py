from signalprocessing import *
import fileio


def find_peaks(samples, diff_thres, height_thres, dist_thres):
    """
    Return a numpy bool array that represents whether or not
    a peak occurred at each time frame in samples.

    Diff_thres defines the value that the first difference of samples
    needs to be at a certain location in order to be classified as a peak.
    """

    peaks = np.zeros(len(samples), dtype=bool)
    diff = np.diff(samples)
    i = 1
    while i < len(samples):
        if diff[i - 1] > diff_thres and samples[i] > height_thres:
            peaks[i] = True
            i += dist_thres
        else:
            i += 1
    # for peak in peaks: print peak
    return peaks


filename = "data/peakdetect/set1/54.txt"
file = open(filename)
samples = [sample for sample in file.read().split('\n')]
samples = [float(sample) for sample in samples if sample]
find_peaks(samples, diff_thres=2000000, height_thres=2000000, dist_thres=10)
