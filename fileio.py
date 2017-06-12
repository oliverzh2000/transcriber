from signalprocessing import *

def read_txt_file(filename):
    file = open(filename)
    samples = [sample for sample in file.read().split('\n')]
    samples = [float(sample) for sample in samples if sample]
    return samples


def read_WAV_file(filename):
    """
    Read all the data from file as a list of integers.
    Format for file should be a mono 16 bit signed WAV file.
    """

    wave_file = wave.open(filename, "rb")
    samples = wave_file.readframes(wave_file.getnframes())
    return np.array(struct.unpack(str(wave_file.getnframes()) + "h", samples))


def write_WAV_file(filename, samples, sample_width=2):
    filename += ".WAV"
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(struct.pack(str(len(samples)) + "h", *tuple(samples)))
    wave_file.close()
    print "wrote to", filename


def write_txt_file(filename, samples):
    filename += ".txt"
    file = open(filename, "w")
    for sample in samples:
        file.writelines(str(sample) + "\n")
    file.close()
    print "wrote to", filename