# ClassCapture_Synth
This project collects multiple synchronized audio files or streams of the same "event" [in particular, a lecture] and filters out idiosyncrasies in each recording like silences, pops and bumps, and background noise (like talking).

## Current Status
Currently, I have four artificial recordings for a proof-of-concept. When the program `median_fft_poc.py` is run, it takes the three modified recordings and reconstructs the original. Note that the records are already synchronized perfectly and, in many places, are the same waveform.
 * `darkness.wav` is the base; it is the beginning of Darkness by LEVV.
 * `darkness_click.wav` includes a pen-click sound at the beginning.
 * `darkness_silence.wav` fades out and back in near the end.
 * `darkness_speak.wav` includes some spoken text in the middle, in particular, "One" by La Dispute.
 * `darkness_filtered.wav` is the reconstructed sound, after the script is run.

## Usage
In the ClassCapture_Synth directory, run:
`python synth/median_fft_poc.py`
and the filtered WAV file will appear.
