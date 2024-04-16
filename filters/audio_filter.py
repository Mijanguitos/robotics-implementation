"""Docstring.

This script filters audio by removing noise from it.
The audio is read from a wav file and then normalized.
The audio is plotted and noise is added to it.
The Fourier Transform of the audio is calculated and plotted.
The noise is removed from the audio and the audio is plotted.
The noisy and noiseless audio is saved to a wav file.
The noisy and noiseless audio is played.
"""

import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
from scipy.io import wavfile


def audio_filter():
    """Function to filter audio."""
    playsound("filters/song.wav")

    # Read the wav file (mono).
    sampFreq, sound = wavfile.read("filters/song.wav")
    print(sound.dtype, sampFreq)

    # Normalize the audio.
    sound = sound / (2.0**15)

    # Just one channel.
    sound = sound[:, 0]

    # Measure in seconds.
    length_in_s = sound.shape[0] / sampFreq
    print("Length in seconds: ", length_in_s)

    # Plot the audio.
    plt.plot(sound[:], "r")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title("Audio Signal")
    plt.tight_layout()
    plt.show()

    # Time vector.
    time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s
    plt.plot(time, sound[:], "r")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title("Audio Signal")
    plt.tight_layout()
    plt.show()

    # Add noise.
    yerr = (
        0.005 * np.sin(2 * np.pi * 6000.0 * time)
        + 0.008 * np.sin(2 * np.pi * 8000.0 * time)
        + 0.006 * np.sin(2 * np.pi * 2500.0 * time)
    )

    signal = sound + yerr

    plt.plot(time[6000:7000], signal[6000:7000])
    plt.xlabel("Time")
    plt.show()

    fft_spectrum = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(signal.size, d=1.0 / sampFreq)
    print("Fourier Transform: ", fft_spectrum)
    fft_spectrum_abs = np.abs(fft_spectrum)

    plt.plot(freq, fft_spectrum_abs)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()

    for i, f in enumerate(freq):
        if f > 5900 and f < 6100:
            fft_spectrum[i] = 0.0

    noiseless_signal = np.fft.irfft(fft_spectrum)

    plt.plot(time, noiseless_signal, "r")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()

    wavfile.write("Noisy_Audio.wav", sampFreq, signal)
    wavfile.write("Noisless_Audio.wav", sampFreq, noiseless_signal)
    playsound("Noisy_Audio.wav")
    playsound("Noisless_Auddio.wav")


if __name__ == "__main__":
    audio_filter()
