# program spectrogram
# programmer Oliver Zhang
# date Nov 22 2016

from signalprocessing import *
import peakdetect
import fileio
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
dft_slices_queue = Queue.Queue()
diff_thres = 2000000.0
height_thres = 2000000.0

def events():
    global done, width, height, max_spectrum_size, is_spectrum, diff_thres, height_thres
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
            if event.key == K_SPACE:
                if stream.is_active():
                    stream.stop_stream()
                else:
                    stream.start_stream()
            keys = key.get_pressed()
            if event.key == K_UP:
                if keys[K_d]:
                    diff_thres *= 1.05
                if keys[K_h]:
                    height_thres *= 1.05
            if event.key == K_DOWN:
                if keys[K_d]:
                    diff_thres /= 1.05
                if keys[K_h]:
                    height_thres /= 1.05
            print diff_thres, height_thres
            if event.key == K_s:
                is_spectrum = not is_spectrum
            render()


def logic():
    while len(dft_slices_queue.queue) > max_spectrum_size:
        dft_slices_queue.get()  # removes the oldest slice


def render():
    print "rendered"
    if is_spectrum:
        render_spectrum()
    else:
        render_detected_notes()


def render_detected_notes():
    if len(dft_slices_queue.queue) < 5:
        return
    screen.fill(back_color)
    dft_slices_array = np.asarray(dft_slices_queue.queue)
    peaks = np.apply_along_axis(peakdetect.find_peaks, 0,
                                dft_slices_array, diff_thres, height_thres, dist_thres=3)

    nfreqs = dft_slices_array.shape[1]
    for (row, col), freq_bin in np.ndenumerate(peaks):
        if freq_bin:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        draw.rect(screen, color,
                  Rect(col * width / nfreqs, row * spectrum_height, width / nfreqs + 1, spectrum_height))
    display.update()


def render_spectrum():
    if len(dft_slices_queue.queue) < 5:
        return
    screen.fill(back_color)
    dft_slices_array = np.asarray(dft_slices_queue.queue)
    max = np.max(dft_slices_array)
    dft_slices_array = np.interp(dft_slices_array, [0, max], [0, 765])

    nfreqs = dft_slices_array.shape[1]
    for (row, col), freq_bin in np.ndenumerate(dft_slices_array):
        if freq_bin > 510:
            color = (255, 255, freq_bin % 255)
        elif freq_bin > 255:
            color = (255, freq_bin % 255, 0)
        else:
            color = (freq_bin % 255, 0, 0)
        draw.rect(screen, color,
                  Rect(col * width / nfreqs, row * spectrum_height, width / nfreqs + 1, spectrum_height))
    display.update()


def callback(in_data, frame_count, time_info, status):
    samples = np.asarray(struct.unpack(str(frame_count) + "h", in_data))
    dft_slice = dft_at_musical_notes(samples, samprate=RATE)
    dft_slices_queue.put(dft_slice)
    return (None, pyaudio.paContinue)

audio = pyaudio.PyAudio()
stream = audio.open(format=AUDIO_FORMAT,
                channels=CHANNELS,
                frames_per_buffer=CHUNK,
                rate=RATE,
                input=True,
                stream_callback=callback)


frame = 0
done = False
is_spectrum = True
while not done:
    clock.tick(10)
    events()
    logic()
    if frame % 10 == 0 and stream.is_active():
        render()
    frame += 1
    # print clock.get_fps()
stream.close()

notes = np.asarray(dft_slices_queue.queue).T
'''for note, values in enumerate(notes):
    # fileio.write_WAV_file("output/" + str(note), values / 1000, sample_width=2)
    fileio.write_txt_file("output/" + str(note), values)'''

pygame.quit()
sys.exit()