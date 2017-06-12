# transcriber

Nov 22 2016.

Transcriber is able to take in microphone input and output a very crude sheet music approximation to the detected frequencies. This program is still very much in it's infancy and is unable to detect rhythms, let alone remove overtones. 

At the heart of this program is the famous discrete fourier transform. It only job is to break down the microphone input into its constituent frequencies. Array processing from numpy is used to make this happen efficiently. 

Pygame is used to render the results of the "spectrogram" on the screen with a black-red-yellow-white colormap.

For note detection the user must manually adjust thresholds for the minimum value and also the time-derivative of frequency intensities.

Once the notes have been detected, the mingus library formats the detected notes into a file compatible with lilypond, which is an external application that does the sheet music engraving to pdf format.

#### Dependencies:
* Python 2.7.9
* PyAudio 0.2.9
* numpy 1.11.2
* pygame 1.9.2a0
* lilypond 2.16.0
* mingus 0.5.1
