# program Pitch_identifier_OCT_28_2016
# programmer Oliver Zhang
# date Oct 29 2016

import pygame
from pygame import *
import pyaudio
from struct import unpack
import sys
import wave
from signalprocessing import *
import time

pygame.init()
width, height, = 800, 600
back_color = (240, 240, 240)
clock = pygame.time.Clock()
screen = display.set_mode((width, height), RESIZABLE)
display.set_caption("Oliver Zhang Pitch Identifier")

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

using_sharps = False
SHARP_CHR = u'\u266F'
FLAT_CHR = u'\u266D'
TEXT_COLOR = (70, 70, 70)


start_freq = note_to_hertz("A", accidental="#", octave=1)
end_freq = note_to_hertz("A", accidental=None, octave=8)
step_semitones = 2.0
thres_semitones = 0.001

current_samples = ()
current_samples_processed = True
identified_freq = 463


def record_chunk():
    stream.start_stream()
    audio_data = stream.read(CHUNK)
    stream.stop_stream()
    samples = unpack(str(CHUNK) + "h", audio_data)
    max_value = float(max(samples))
    normalized_data = [frame / max_value for frame in samples]
    return normalized_data


def write_to_file(filename, samples):
    file = open(filename, 'w')
    file.writelines([str(sample) + "\n" for sample in samples])
    file.close()


def events():
    global done, width, height, identified_freq, current_samples, current_samples_processed
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == VIDEORESIZE:
            width, height = event.size
            screen = display.set_mode((width, height), RESIZABLE)
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                current_samples = record_chunk()
                current_samples_processed = False
                # write_to_file("output.txt", samples)

            if event.key == K_ESCAPE:
                done = True


def render():
    screen.fill(back_color)
    # draw.line(screen, (0, 0, 0), (0, height / 2), (width, height / 2))
    # draw.line(screen, (0, 0, 0), (width/2, 0), (width / 2, height))
    letter_name, octave, cents = hertz_to_note(identified_freq)
    if type(letter_name) == tuple:  # tuple of enharmonically equivalent note names.
        if using_sharps:
            letter_name = letter_name[0]
        else:
            letter_name = letter_name[1]
        letter_name = letter_name.replace("#", SHARP_CHR)
        letter_name = letter_name.replace("b", FLAT_CHR)
    if cents > 0:
        cents = ", +" + str(cents) + " cents"
    elif cents < 0:
        cents = ", " + str(cents) + " cents"
    else:
        cents = ""

    # render note name text
    f = pygame.font.SysFont("segoe ui symbol", 96)
    note_text = f.render(letter_name + unichr(8320 + octave), True, TEXT_COLOR)
    note_x = width/2 - note_text.get_rect().centerx
    note_y = height/2 - note_text.get_rect().height
    screen.blit(note_text, Rect(note_x, note_y, 0, 0))

    # render pitch information text
    f = pygame.font.SysFont("segoe ui", 32)
    freq_text = f.render(str(round(identified_freq, 2)) + "Hz" + cents, True, TEXT_COLOR)
    freq_x = width/2 - freq_text.get_rect().centerx
    freq_y = height/2
    screen.blit(freq_text, Rect(freq_x, freq_y, 0, 0))
    display.update()



# begin recording
audio = pyaudio.PyAudio()
stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Wait out the latency period.
done_latency = False
while not done_latency:
    samples = unpack(CHUNK * "h", stream.read(CHUNK))
    for sample in samples:
        if sample < -1 or sample > 1:
            done_latency = True
            break
stream.stop_stream()


done = False
while not done:
    # clock.tick(1)
    events()
    global current_samples_processed, identified_freq
    if not current_samples_processed:
        print current_samples
        print "\n\n\n"
        identified_freq = identify_freq(samples=current_samples, samprate=RATE,
                                        start_freq=note_to_hertz("A", accidental=None, octave=2),
                                        end_freq=note_to_hertz("A", accidental=None, octave=7),
                                        step_semitones=2, thres_cents=5)
        print identified_freq
        current_samples_processed = True
    render()
pygame.quit()
sys.exit()