from numpy import fft, real
from scipy.io import wavfile
from ccsaux import simple_noise_filter, complex_median, feather

files = ["../samples/darkness_click.wav",
             "../samples/darkness_silent.wav",
             "../samples/darkness_speak.wav"] 
target = "darkness_filtered.wav"
simple_noise_filter(target, files)

files = ["../samples/cassie_clip.wav",
             "../samples/eric_clip.wav",
             "../samples/warren_clip.wav"] 
target = "friends_clip.wav"
simple_noise_filter(target, files, method=complex_median, combination=feather)
