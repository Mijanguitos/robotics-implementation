"""Filters file."""

from array import array

from scipy.signal import butter, lfilter


def butter_highpass(data: array, cutoff: float, fs: float, order: int = 5) -> tuple:
    """Apply a highpass Butterworth filter to the data."""
    # Calculate Nyquist frequency
    nyquist = 0.5 * fs
    # Normalize the cutoff frequency
    normal_cutoff = cutoff / nyquist
    # Get the filter coefficients for a highpass filter
    b, a = butter(order, normal_cutoff, btype="high", analog=False)
    # Apply the filter to the data
    y = lfilter(b, a, data)
    return y


def butter_lowpass(data: array, cutoff: float, fs: float, order: int = 5) -> tuple:
    """Apply a lowpass Butterworth filter to the data."""
    # Calculate Nyquist frequency
    nyquist = 0.5 * fs
    # Normalize the cutoff frequency
    normal_cutoff = cutoff / nyquist
    # Get the filter coefficients for a lowpass filter
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    # Apply the filter to the data
    y = lfilter(b, a, data)
    return y


def butter_bandpass(
    data: array, lowcut: float, highcut: float, fs: float, order: int = 5
) -> array:
    """Apply a bandpass Butterworth filter to the data."""
    # Get the filter coefficients for a bandpass filter
    b, a = butter(order, [lowcut, highcut], fs=fs, btype="band", analog=False)
    # Apply the filter to the data
    y = lfilter(b, a, data)
    return y
