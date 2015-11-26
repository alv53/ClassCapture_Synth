# this function probably has a better replacement
from numpy import argsort, array, append, real, sort, copy, linspace, repeat, fft, real
from scipy.io import wavfile
from time import time
from os import devnull
import subprocess

def mp4_to_wav(target_wav, input_mp4):
    # Takes an input mp4 file and generates a resulting wavfile. Will be useful for taking incoming mp4 files and processing the audio components.
    # Requires ffmpeg to be setup on the machine. https://www.ffmpeg.org
    command = "ffmpeg -i " + input_mp4 + " -y " + target_wav + " 2> /dev/null"
    subprocess.call(command, shell=True)

def flatten(list_of_lists):
    ret = array(list_of_lists[0], dtype = list_of_lists[0].dtype)
    print ret.shape
    for l in list_of_lists[1:]:
        ret = append(ret, l, axis=0)
    return ret

def section_by_length(feed, target_length):
    return [feed[i:i+target_length] for i in range(0,len(feed),target_length)]

def complex_median(freqs, j):
    # build a representative entry by finding the median of the complex
    # and imaginary parts in parallel
    sources = len(freqs)
    
    left_real = sort([freq[j][0].real for freq in freqs])[sources/2]
    left_imag = sort([freq[j][0].imag for freq in freqs])[sources/2]
    right_real = sort([freq[j][1].real for freq in freqs])[sources/2]
    right_imag = sort([freq[j][1].imag for freq in freqs])[sources/2]
    
    return array([left_real + left_imag*1j, right_real + right_imag*1j])

def median_by_intensity(freqs, j):
    # Choose the representative entry by finding the median intensity
    # of all of the *left-channel* frequencies.
    lvals = [abs(freq[j][0]) for freq in freqs]
    #rvals = [abs(freq[j][1]) for freq in freqs]
    # pick the one with the median magnitude
    return freqs[argsort(lvals)[len(freqs) / 2]][j]

def feather(list_of_lists):
    lfb = 256
    backup = [copy(i) for i in list_of_lists]
    sections = len(list_of_lists)
    section_len = len(list_of_lists[0])
    feather_A_main = linspace(0.5, 1, lfb).reshape(lfb, 1)
    feather_A_duet = linspace(0.5, 0, lfb).reshape(lfb, 1)
    feather_B_main = linspace(1, 0.5, lfb).reshape(lfb, 1)
    feather_B_duet = linspace(0, 0.5, lfb).reshape(lfb, 1)
    for i in range(1, sections - 1):
        # [---B]
        #     ^
        # [A--B]
        list_of_lists[i-1][-lfb:] = backup[i][-lfb:] * feather_B_duet + backup[i-1][-lfb:] * feather_B_main

        # [A--B]
        #  v
        # [A---]
        list_of_lists[i+1][:lfb] = backup[i][:lfb] * feather_A_duet + backup[i+1][:lfb] * feather_A_main

    return flatten(list_of_lists)

def simple_noise_filter(target, files, method=median_by_intensity, combination=flatten, section_length=4096):
    # load all .mp3 files into an arrays 
    # bin each to a certain length
    #print time()
    feeds = [section_by_length(wavfile.read(file)[1], section_length) for file in files]
    samplerate = wavfile.read(files[0])[0]
    #print time()
    # perform fft on each bin, select median of each 
    max_len = len(max(feeds, key=len))
    sections = []
    for i in range(max_len):
        begin = time()
        freqs = [fft.fft(feed[i], axis=0) for feed in feeds]
        #print "Fourier per ~.1s feed: ",
        #print (time()-begin)/3.
        begin = time()
        #filtered_freqs = [median_by_intensity(freqs, j) for j in range(len(freqs[0]))] # traverse the arrays in parallel
        filtered_freqs = [method(freqs, j) for j in range(len(freqs[0]))]
        #print "Filtering: ",
        #print (time()-begin)
        begin = time()
        sections += [real(fft.ifft(filtered_freqs, axis=0)).astype(feeds[0][0].dtype)]
        #print "Inversing per ~.1s feed: ",
        #print (time() - begin)
    # output
    #print time()
    samples = combination(sections)
    wavfile.write(target, samplerate, samples)
    #print time()
