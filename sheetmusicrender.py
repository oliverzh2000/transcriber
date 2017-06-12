import numpy as np
import webbrowser
import os
import mingus.extra.lilypond as LilyPond
import mingus.core.intervals as intervals
from mingus.containers import Note, NoteContainer, Bar, Instrument, Track


'''def add_rest(track, duration):
    if not track.bars:
        track.add_bar(Bar())
    if track.bars[-1].is_full():
        track.add_bar(Bar())
    track.bars[-1].place_rest(duration)'''


def merge_rests(treble_track, bass_track):
    for bar in (treble_track.bars + bass_track.bars):
        bar_is_rest = True
        for note in bar:
            if note[2] != None:
                bar_is_rest = False
        if bar_is_rest:
            bar.empty()
            bar.place_rest(1)


def sheets_from_peaks(peaks):
    """Generate and open the sheet music pdf that represents the notes contained in peaks."""

    bass_range = Instrument()
    bass_range.set_range(['A-0', 'C-4'])
    bass_track = Track(bass_range)

    treble_range = Instrument()
    treble_range.set_range(['C-4', 'C-8'])
    treble_track = Track(treble_range)

    treble_track.add_bar(Bar())
    bass_track.add_bar(Bar())

    for time_slice in peaks:
        bass_chord, treble_chord = [], []
        for note_index, note_value in enumerate(time_slice):
            if note_value:
                # add 9 to note_index to start at A-0
                note = Note().from_int(note_index + 9)
                if bass_range.note_in_range(note):
                    bass_chord.append(note)
                elif treble_range.note_in_range(note):
                    treble_chord.append(note)
        if bass_chord == treble_chord == []:
            continue
        for chord, track in ((bass_chord, bass_track), (treble_chord, treble_track)):
            if track.bars[-1].is_full():
                track.add_bar(Bar())
            if chord:
                print chord
                track.bars[-1] + chord
                print track
            else:
                track.bars[-1].place_rest(4)

    print bass_track
    print treble_track
    merge_rests(treble_track, bass_track)
    save_and_print(treble_track, bass_track)



def save_and_print(treble_track, bass_track):
    ly_input = """
    \header {
        composer = "Zhang Transcriber 2016"
        tagline = "Music engraving by LilyPond 2.18.2. Note identification algorithm by Oliver Zhang."
    }
    \\new PianoStaff <<
        \\new Staff { \clef treble %s }
        \\new Staff { \clef bass %s }
    >>
    """ % (LilyPond.from_Track(treble_track)[1:-1], LilyPond.from_Track(bass_track)[1:-1])

    LilyPond.to_pdf(ly_input, "my_first_bar")
    webbrowser.open_new(r'file://' + os.path.realpath("my_first_bar.pdf"))

peaks_list = [[False for i in range(88)] for i in range(20)]
peaks_list[3][45] = True
peaks_list[3][40] = True

# sheets_from_peaks(np.asarray(peaks_list))


'''elif len(current_chord) == 1:
            note = current_chord[0]
            if bass_range.note_in_range(note):
                bass_track + Note().from_int(note_index)
                add_rest(treble_track, 4)
            elif treble_range.note_in_range(note):
                treble_track + Note().from_int(note_index)
                add_rest(bass_track, 4)'''