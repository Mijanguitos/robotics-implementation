"""Filtrar datos con un filtro pasabajas."""

import numpy as np
from matplotlib import pyplot as plt
from numpy import pi, sin

from filters import fourier_filter, iir_filter


def filter():
    """Filtrar datos."""
    np.random.seed(42)

    # Crear timesteps
    fs = 80  # Frecuencia de muestreo, Hz
    ts = np.arange(0, 5, 1.0 / fs)  # Vector de tiempo, 5 segundos

    x_t = np.sin(2 * pi * 1.0 * ts)

    noise = (
        0.2 * sin(2 * pi * 15.3 * ts)
        + 0.1 * sin(2 * pi * 16.7 * ts * 0.1)
        + 0.1 * sin(2 * pi * 23.45 * ts * 0.8)
    )

    x_noise = x_t + noise

    # Plotear señal original
    plt.figure(figsize=(12, 5))
    plt.plot(ts, x_t, alpha=0.8, lw=3, color="C1", label="Señal original")
    plt.plot(ts, x_noise, color="C0", label="Señal con ruido")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.legend(
        loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize="smaller"
    )
    plt.tight_layout()
    plt.show()

    # Señal con transformada de Fourier
    xf, yf = fourier_filter(x_noise, sample_rate=fs, duration=5)
    plt.figure(figsize=(12, 5))
    plt.plot(xf, np.abs(yf))
    plt.show()

    # Definir filtro pasabajas a frecuencia de corte de 10 Hz
    fc = 10
    x_filtered = iir_filter(x_noise, fc, fs)

    # Señal filtrada con la transformada de Fourier
    xf, yf = fourier_filter(x_filtered, sample_rate=fs, duration=5)
    plt.figure(figsize=(12, 5))
    plt.plot(xf, np.abs(yf))
    plt.show()

    plt.figure(figsize=(12, 5))
    plt.plot(ts, x_noise, label="Señal original")
    plt.plot(ts, x_filtered, alpha=0.8, lw=3, label="Señal filtrada")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.legend(
        loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize="smaller"
    )
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    filter()
