# program spectrogram
# programmer Oliver Zhang
# date Nov 5 2016

from signalprocessing import *
import pygame
from pygame import *
import sys
import Queue
import time


pygame.init()
width, height, = 800, 600
back_color = (240, 240, 240)
clock = pygame.time.Clock()
screen = display.set_mode((width, height), RESIZABLE)

spectrum_height = 5
max_spectrum_size = height / spectrum_height
dft_slices = Queue.Queue()


def record_chunk():
    stream.start_stream()
    for i in range(2):
        audio_data = stream.read(CHUNK)
        if i == 1:
            samples = struct.unpack(str(CHUNK) + "h", audio_data)
    stream.stop_stream()
    return samples


def events():
    global done, width, height, max_spectrum_size
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == VIDEORESIZE:
            width, height = event.size
            max_spectrum_size = height / spectrum_height
            screen = display.set_mode((width, height), RESIZABLE)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == K_UP:
                pass
            if event.key == K_DOWN:
                pass


def logic():
    while len(dft_slices.queue) > max_spectrum_size:
        dft_slices.get()  # removes the oldest slice



def render():
    screen.fill(back_color)

    dft_slices_array = np.asarray(dft_slices.queue)
    max = np.max(dft_slices_array)
    dft_slices_array = np.interp(dft_slices_array, [0, max], [0, 765])

    freq_width = dft_slices_array.shape[1]
    for (row, col), freq_bin in np.ndenumerate(dft_slices_array):
        if freq_bin > 510:
            color = (255, 255, freq_bin % 255)
        elif freq_bin > 255:
            color = (255, freq_bin % 255, 0)
        else:
            color = (freq_bin % 255, 0, 0)
        draw.rect(screen, color,
                  Rect(col * width / freq_width, row * spectrum_height, width / freq_width + 1, spectrum_height))
    display.update()


# begin recording
audio = pyaudio.PyAudio()
stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Wait out the latency period
done_latency = False
while not done_latency:
    samples = struct.unpack(str(CHUNK) + "h", stream.read(CHUNK))
    for sample in samples:
        if sample < -1 or sample > 1:
            done_latency = True
            break

frame = 0
done = False

while not done:
    samples = np.asarray(struct.unpack(str(CHUNK) + "h", stream.read(CHUNK)))
    # start = time.clock()
    dft_slice = dft_at_musical_notes(samples, samprate=RATE)
    dft_slices.put(dft_slice)
    # print time.clock() - start

    clock.tick()
    events()
    logic()
    render()
    frame += 1
stream.close()

'''notes = np.asarray(dft_slices.queue).T
for note, values in enumerate(notes):
    write_txt_file("output/" + str(note) + ".WAV", values)'''
pygame.quit()
sys.exit()