"""Main interface."""

import sys
import wave

import numpy as np
import sounddevice as sd
from pyqtgraph import PlotWidget
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDial,
    QFileDialog,
    QLabel,
    QMainWindow,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from scipy.io import wavfile

import filters


class Interface(QMainWindow):
    """Main interface for the application."""

    def __init__(self, parent=None):
        """Initialize the parameters and UI components."""
        super().__init__(parent)
        self.setWindowTitle("Signal Processing")

        # Initialize variables for audio file and processing parameters
        self.file = None
        self.original_signal = None
        self.signal = None
        self.f_rate = None
        self.lowcut = 0
        self.highcut = 0

        # Create UI components
        self.central_widget = QWidget()
        self.graphWidget = PlotWidget()
        self.lowDialWidget = QDial()
        self.lowLabel = QLabel("Low cutoff frequency: " + str(self.lowcut))
        self.highLabel = QLabel("High cutoff frequency: " + str(self.highcut))
        self.highDialWidget = QDial()
        self.filterSelectWidget = QComboBox()
        self.toolbar = QToolBar("Toolbar")

        self.layout = QVBoxLayout()

        # Initialize the interface
        self.create_actions()
        self.connect_actions()
        self.create_toolbar()
        self.create_dials()
        self.create_filterSelect()
        self.create_graph()

        self.show()

    def create_toolbar(self):
        """Create the toolbar with action buttons and widgets."""
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(35, 35))

        # Add actions and widgets to the toolbar
        self.toolbar.addAction(self.loadAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.filterAction)
        self.toolbar.addAction(self.playAction)
        self.toolbar.addAction(self.pauseAction)

        self.toolbar.addWidget(QWidget().setFixedWidth(2))
        self.toolbar.addWidget(self.lowDialWidget)
        self.toolbar.addWidget(self.lowLabel)
        self.toolbar.addWidget(self.highDialWidget)
        self.toolbar.addWidget(self.highLabel)
        self.toolbar.addWidget(QWidget().setFixedWidth(2))
        self.toolbar.addWidget(QLabel("Filter type: "))
        self.toolbar.addWidget(self.filterSelectWidget)

    def create_actions(self):
        """Create actions for the toolbar."""
        self.loadAction = QAction(
            QIcon("./resources/abrir-documento.png"), "&Load file", self
        )
        self.filterAction = QAction(
            QIcon("./resources/filtro-de-cafe.png"), "&Apply filter", self
        )
        self.playAction = QAction(
            QIcon("./resources/boton-de-play.png"), "&Play audio", self
        )
        self.pauseAction = QAction(QIcon("./resources/pausa.png"), "&Pause audio", self)
        self.saveAction = QAction(
            QIcon("./resources/disquete.png"), "&Save audio file", self
        )

    def connect_actions(self):
        """Connect actions to their corresponding functions."""
        self.loadAction.triggered.connect(self.load_file)
        self.filterAction.triggered.connect(self.add_filter)
        self.playAction.triggered.connect(self.play_audio)
        self.pauseAction.triggered.connect(self.pause_audio)
        self.saveAction.triggered.connect(self.save_file)

    def load_file(self):
        """Load an audio file and update the signal and graph."""
        initial_directory = "./signals/"
        file_types = "Audio Files (*.wav *.mp3)"
        self.file, _ = QFileDialog.getOpenFileName(
            self, "Open File", initial_directory, file_types
        )

        if self.file:
            self.signal = wave.open(self.file)
            self.f_rate = self.signal.getframerate()
            self.signal = self.signal.readframes(-1)
            self.signal = np.frombuffer(self.signal, dtype="int16")
            self.original_signal = self.signal
            self.update_graph()

    def add_filter(self):
        """Apply the selected filter to the signal."""
        if self.filterSelectWidget.currentIndex() == 0:
            self.signal = filters.butter_lowpass(self.signal, self.lowcut, self.f_rate)
        elif self.filterSelectWidget.currentIndex() == 1:
            self.signal = filters.butter_bandpass(
                self.signal, self.lowcut, self.highcut, self.f_rate
            )
        elif self.filterSelectWidget.currentIndex() == 2:
            self.signal = filters.butter_highpass(
                self.signal, self.highcut, self.f_rate
            )

        self.update_graph()

    def play_audio(self):
        """Play the current audio signal."""
        sd.play(self.signal, self.f_rate)

    def pause_audio(self):
        """Pause the audio playback."""
        sd.stop()

    def save_file(self):
        """Save the altered audio signal to a file."""
        wavfile.write("./signals/Altered.wav", self.f_rate, self.signal)

    def create_filterSelect(self):
        """Create a combo box for selecting filter types."""
        self.filterSelectWidget.addItems(
            ["Lowpass filter", "Bandpass filter", "Highpass filter"]
        )

    def create_dials(self):
        """Create dials for adjusting low and high cutoff frequencies."""
        self.lowDialWidget.setMinimum(0)
        self.lowDialWidget.setMaximum(500)
        self.lowDialWidget.setValue(0)
        self.lowDialWidget.valueChanged.connect(self.update_labels)

        self.highDialWidget.setMinimum(0)
        self.highDialWidget.setMaximum(500)
        self.highDialWidget.setValue(0)
        self.highDialWidget.valueChanged.connect(self.update_labels)

    def update_labels(self):
        """Update the labels for low and high cutoff frequencies based on dial values."""
        self.lowcut = self.lowDialWidget.value()
        self.lowLabel.setText("Low cutoff frequency: " + str(self.lowcut))

        self.highcut = self.highDialWidget.value()
        self.highLabel.setText("High cutoff frequency: " + str(self.highcut))

    def create_graph(self):
        """Create the graph widget to display the signal."""
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        layout.addWidget(self.graphWidget)

    def update_graph(self):
        """Update the graph to display the current signal."""
        self.graphWidget.clear()

        time = np.linspace(0, len(self.signal) / self.f_rate, num=len(self.signal))
        self.graphWidget.plot(time, self.signal)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    interface = Interface()
    interface.show()
    interface.resize(1200, 800)

    sys.exit(app.exec())
