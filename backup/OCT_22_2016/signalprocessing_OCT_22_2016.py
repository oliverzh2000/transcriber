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


def dft(samples, start, end, step_ratio):
    """Compute the one dimensional discrete Fourier transform."""
    k_axis = []
    fourier_coefficients = []
    N = len(samples)

    k = start
    while k < end:
        k_axis.append(k)
        fourier_coefficients.append(freq_bin_at(k, samples))
        k *= step_ratio
    return (k_axis, fourier_coefficients)


def freq_bin_at(k, samples):
    """Compute the value of the kth frequency bin of samples."""
    N = len(samples)
    re = sum(samples[n] * cos(2 * pi * k * n / N) for n in range(N))
    im = sum(samples[n] * -sin(2 * pi * k * n / N) for n in range(N))
    mag_squared = re ** 2 + im ** 2
    return mag_squared


def quad_vertex((x1, y1), (x2, y2), (x3, y3)):
    """
    Compute the vertex of the quadratic function that goes through points
    (x1, y1), (x2, y2), (x3, y3), and whether or not the vertex is a maximum.

    This function simplifies the calculations by shifting all points
    by an equal amount such that x3 == 0. This trick effectively reduces the
    problem from solving a system of 3 linear equations in 3 variables into
    a system of 2 linear equations in 2 variables.
    """
    shift = x3
    x1 -= shift
    x2 -= shift
    # Because x3 - x3 == zero, we will exclude it from our problem.

    # The values a and b define a quadratic function of the form:
    # y = ax^2 + bx + c, where c == 0.
    denominator = x1**2 * x2 - x1 * x2**2
    a = (x1*(y3-y2) - x2*y3 + x2*y1)/denominator
    b = -(x1**2 * (y3-y2) - x2**2 * y3 + x2**2 * y1)/denominator
    # Because y = a * x3^2 + b * x3 + c, and x3 == 0, c == y3.
    return -b / (2*a) + shift,  y3 - b**2 / (4*a), bool(a < 0.0)


def dft_peak_x(pt1, pt2, pt3, iterations, samples):
    """
    Compute the x value of the peak of f(x) = freq_bin_at(x, samples), in the
    interval x1 <= x <= x3 by running recursively for the iterations given.

    This method uses a quadratic interpolation to recursively improve
    the accuracy of the peak found. It will find the vertex of the
    quadratic function that satisfies the points given and evaluate f(x) at the
    x value of the vertex. If iterations still remain, it will call itself
    with the new points (including the vertex point) in hopes of narrowing
    down the interval it has to search in.
    """
    print "iter:", iterations, "    points:", pt1, pt2, pt3
    vert_x, vert_y, vert_ismax = quad_vertex(pt1, pt2, pt3)
    if iterations == 0:
        return vert_x, freq_bin_at(vert_x, samples)
    else:
        iterations -= 1

        # finding left, mid, and right point
        min_x = min(pt1[0], pt2[0], pt3[0])
        max_x = max(pt1[0], pt2[0], pt3[0])
        for pt in (pt1, pt2, pt3):
            if pt[0] == min_x:
                left_pt = pt
            elif pt[0] == max_x:
                right_pt = pt
            else:
                mid_pt = pt
        new_pt = vert_x, freq_bin_at(vert_x, samples)
        new_vert_x, new_vert_y, new_vert_ismax = quad_vertex(left_pt, new_pt, mid_pt)
        if new_vert_ismax and left_pt[0] < new_vert_x < mid_pt[0]:
            return dft_peak_x(left_pt, new_pt, mid_pt, iterations, samples)
        else:
            return dft_peak_x(right_pt, new_pt, mid_pt, iterations, samples)


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

    if type(letter_name) == tuple:  # meaning it has 2 possible values
        if using_sharps:
            letter_name = letter_name[0]
        else:
            letter_name = letter_name[1]
    return (letter_name, octave, str(cents) + " cents")