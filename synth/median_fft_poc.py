from numpy import fft, array, append, real, argsort
from scipy.io import wavfile

def section_by_length(feed, target_length):
    return [feed[i:i+target_length] for i in range(0,len(feed),target_length)]

# this function probably has a better replacement
def flatten(list_of_lists):
    ret = array(list_of_lists[0], dtype = list_of_lists[0].dtype)
    print ret.shape
    for l in list_of_lists[1:]:
        ret = append(ret, l, axis=0)
    return ret

def median_by_intensity(freqs, j):
    # Choose the representative entry by finding the median intensity
    # of all of the *left-channel* frequencies.
    lvals = [abs(freq[j][0]) for freq in freqs]
    #rvals = [abs(freq[j][1]) for freq in freqs]
    # pick the one with the median magnitude
    return freqs[argsort(lvals)[len(freqs) / 2]][j]

#-- BEGIN SCRIPT --#
def simple_noise_filter(target, files):
    # load all .mp3 files into an arrays 
    # bin each to a certain length
    feeds = [section_by_length(wavfile.read(file)[1], 16384) for file in files]
    samplerate = wavfile.read(files[0])[0]

    # perform fft on each bin, select median of each 
    max_len = len(max(feeds, key=len))
    sections = []
    for i in range(max_len):
        freqs = [fft.fft(feed[i], axis=0) for feed in feeds]
        filtered_freqs = [median_by_intensity(freqs, j) for j in range(len(freqs[0]))] # traverse the arrays in parallel
        sections += [real(fft.ifft(filtered_freqs, axis=0)).astype(feeds[0][0].dtype)]
    # output
    samples = flatten(sections)
    print samples.shape
    wavfile.write(target, samplerate, samples)

# begin script #

files = ["darkness_click.wav",
             "darkness_silent.wav",
             "darkness_speak.wav"] 
target = "darkness_filtered.wav"
simple_noise_filter(target, files)
