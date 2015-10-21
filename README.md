# ClassCapture_Synth
This project collects multiple synchronized audio files or streams of the same "event" [in particular, a lecture] and filters out idiosyncrasies in each recording like silences, pops and bumps, and background noise (like talking) to produce one, robust recording.

## Current Status

### Sanity Check
Currently, I have four artificial recordings for a sanity check - verifying the program reconstructs the proper signal if it has very little noise in the input. When the program `filtering_demo.py` is run, it takes the three modified recordings and reconstructs the original. Note that the records are already synchronized perfectly and, in many places, are the same exact waveform.
 * `darkness.wav` is the base; it is the beginning of Darkness by LEVV.
 * `darkness_click.wav` includes a pen-click sound at the beginning.
 * `darkness_silence.wav` fades out and back in near the end.
 * `darkness_speak.wav` includes some spoken text in the middle, in particular, "One" by La Dispute.
 * `darkness_filtered.wav` is the reconstructed sound, after the script is run.

### Proof-of-Concept, Median Filter
I manually synchronized three recordings from our phones my friends and I made one night, then ran the filtering algorithm. There was significant distortion in the output, but the best method I've found so far is the combination of a "complex median" and feathering [linear blending / cross-fading] the sections.

## Usage
In the ClassCapture_Synth/synth directory, run:
`python filtering_demo.py`
and the filtered WAV files will appear.
