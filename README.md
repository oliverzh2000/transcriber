# transcriber

Transcriber is able to take in microphone input and output a (crude) sheet music approximation to the detected frequencies. 

This program is still very much in it's infancy and is not sophisticated enough to consistently deduce if a "note" is truly an independent note or merely part of the harmonic series of a concurrent note that is lower in frequency. This can lead to false positvies of the overtones (most commonly the 1st or 2nd overtone) of certain instruments with a very rich harmonic spectrum being recognized as individual notes. For example, a violin has much more richer overtones than a piano does, so while a piano sound only occasionally suffers from false positives, a violin transcription may be teeming with false positives. 

I suspect that should the user restrict themselves to just the piano, ML will be able to do a decent job at this, after being trained on dense chords where its constituent notes overlap considerably with each other in terms of their overtones. Plentiful amounts of high quality test cases can be generated purely in software via any commercially available virtual piano, such as the American Concert D by Synthogy (sampled from a Steinway D), post-processed with variable amounts of software reverb and equalization for training robustness. Some other cases are far less difficult. For example a major 9th interval played harmonically can simply be unabiguously detected as a 2 separate notes, separated by a major 9th, since the major 9th is too sharp to be the first overtone (which is 1 octave above the fundamental). I may implement this in the future as a proof of concept, and you are welcome to contact me for any suggestions/ideas.

At the heart of this program is the discrete fourier transform (DFT). Its job is to transform microphone audio in the time domain (not useful for our purposes) into the frequency domain. Array processing from Numpy is used to make this happen efficiently, but performance was never the concern here as any modern computer can easily handle this anyways. 

The spectrogram is rendered onto the screen with a black-red-yellow-white colormap.

For most accurate note detection, there are thresholds for the both minimum value and the time-derivative of frequency intensities that need to be calibrated (slightly) depending on the nature of the sound source. Having a threshold for time-derivative of frequency intensities ensures that one continuous tone is not detected as multiple notes being played in rapid succession. 

This program was designed and calibrated to work best for piano, as the piano is the instrument dearest to me. 

#### Dependencies:
* Python 2.7.9
* PyAudio 0.2.9
* numpy 1.11.2
* pygame 1.9.2a0
* lilypond 2.16.0
* mingus 0.5.1
