# program spectrogram
# programmer Oliver Zhang
# date Nov 22 2016

import numpy as np
import struct
import sys
import Queue
import pyaudio
import pygame
from pygame import *

import signalprocessing as sp
import peakdetect
import sheetmusicrender


pygame.init()
width, height, = 800, 600
BACK_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
clock = pygame.time.Clock()
screen = display.set_mode((width, height), RESIZABLE)

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

spectrum_height = 5
is_spectrum = True
max_spectrum_size = height / spectrum_height * 2/3
dft_slices_queue = Queue.Queue()
diff_thres = 4000000.0
height_thres = 4000000.0


def events():
    global done, width, height, max_spectrum_size, is_spectrum, diff_thres, height_thres
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == VIDEORESIZE:
            width, height = event.size
            max_spectrum_size = height / spectrum_height * 2/3
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
            print "Differential Thres:", diff_thres
            print "Intensity Thres:", height_thres
            print
            if event.key == K_s:
                is_spectrum = not is_spectrum
            render()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                render_detected_notes(True)


def logic():
    while len(dft_slices_queue.queue) > max_spectrum_size:
        dft_slices_queue.get()  # removes the oldest slice


def render():
    # print "rendered"
    if is_spectrum:
        render_spectrum()
    else:
        render_detected_notes()
    # render instruction text
    f = pygame.font.SysFont("segoe ui", 24)
    note_text = f.render("Click to view sheet music", True, TEXT_COLOR)
    note_x = width / 2 - note_text.get_rect().centerx
    note_y = height * 5/6 - note_text.get_rect().height
    screen.blit(note_text, Rect(note_x, note_y, 0, 0))
    display.update()


def render_detected_notes(generate_sheet=False):
    if len(dft_slices_queue.queue) < 5:
        return
    screen.fill(BACK_COLOR)
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
    if generate_sheet:
        # for peak in peaks:
            # print peak
        sheetmusicrender.sheets_from_peaks(peaks)

def render_spectrum():
    if len(dft_slices_queue.queue) < 5:
        return
    screen.fill(BACK_COLOR)
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


def callback(in_data, frame_count, time_info, status):
    samples = np.asarray(struct.unpack(str(frame_count) + "h", in_data))
    dft_slice = sp.dft_at_musical_notes(samples, samprate=RATE)
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
while not done:
    clock.tick(10)
    events()
    logic()
    if frame % 2 == 0 and stream.is_active():
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