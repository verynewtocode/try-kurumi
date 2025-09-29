"""Kurumi Tokisaki themed reminder overlay for Anki."""

from __future__ import annotations

import os
from typing import Optional

from aqt import mw
from aqt.qt import QLabel, QPixmap, Qt, QTimer
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

ADDON_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(ADDON_PATH, "my honey screenshot.png")
SOUND_PATH = os.path.join(ADDON_PATH, "my-honey-by Kurumi.mp3")

DISPLAY_DELAY_MS = 10_000
DISPLAY_DURATION_MS = 5_000
REPEAT_INTERVAL_MS = 30 * 60 * 1000


class KurumiHoneyReminder:
    """Controls the Kurumi overlay and audio playback schedule."""

    def __init__(self) -> None:
        self._label: Optional[QLabel] = None
        self._player: Optional[QMediaPlayer] = None
        self._audio_output: Optional[QAudioOutput] = None

        self._hide_timer = QTimer(mw)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._hide_overlay)

        self._repeat_timer = QTimer(mw)
        self._repeat_timer.setInterval(REPEAT_INTERVAL_MS)
        self._repeat_timer.timeout.connect(self._show_overlay)

        QTimer.singleShot(DISPLAY_DELAY_MS, self._start_sequence)

    def _start_sequence(self) -> None:
        self._show_overlay()
        self._repeat_timer.start()

    def _show_overlay(self) -> None:
        pixmap = QPixmap(IMAGE_PATH)
        if pixmap.isNull():
            print(f"Kurumi overlay could not load image at: {IMAGE_PATH}")
            return

        self._label = QLabel(mw)
        self._label.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self._label.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self._label.setStyleSheet("background-color: transparent;")
        self._label.setGeometry(mw.rect())
        self._label.setScaledContents(True)
        scaled = pixmap.scaled(
            mw.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._label.setPixmap(scaled)
        self._label.show()

        self._play_audio()
        self._hide_timer.start(DISPLAY_DURATION_MS)

    def _hide_overlay(self) -> None:
        if self._label is not None:
            self._label.close()
            self._label = None

        if self._player is not None:
            self._player.stop()
            self._player.deleteLater()
            self._player = None

        if self._audio_output is not None:
            self._audio_output.deleteLater()
            self._audio_output = None

    def _play_audio(self) -> None:
        if not os.path.exists(SOUND_PATH):
            print(f"Kurumi overlay could not find audio at: {SOUND_PATH}")
            return

        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        self._player.setSource(QUrl.fromLocalFile(SOUND_PATH))
        self._audio_output.setVolume(1.0)
        self._player.play()


KurumiHoneyReminder()

