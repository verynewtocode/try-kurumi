## Warning: Use it at your own risk
import os

from aqt import mw
from aqt.qt import QLabel, QPixmap, Qt, QTimer
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

config = mw.addonManager.getConfig(__name__)

ADDON_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(ADDON_PATH, "kurumi.png")
SOUND_PATH = os.path.join(ADDON_PATH, "jumpscare.mp3")

DISPLAY_DELAY_MS = 10_000
DISPLAY_DURATION_MS = 5_000
VOLUME_SET = float(config.get("volume", 100))

_label = None
_player = None
_audio_output = None


def _close_overlay():
    global _label, _player, _audio_output

    if _player is not None:
        _player.stop()

    if _label is not None:
        _label.close()

    _label = None
    _player = None
    _audio_output = None


def _show_overlay():
    global _label, _player, _audio_output

    if _label is not None:
        return

    pixmap = QPixmap(IMAGE_PATH)

    if pixmap.isNull():
        print("Kurumi overlay: failed to load image", IMAGE_PATH)
        return

    _label = QLabel(mw)
    _label.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    _label.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    _label.setStyleSheet("background-color: transparent;")
    _label.setGeometry(mw.rect())
    _label.setScaledContents(True)
    _label.setPixmap(
        pixmap.scaled(
            mw.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
    )
    _label.show()

    try:
        _player = QMediaPlayer()
        _audio_output = QAudioOutput()
        _player.setAudioOutput(_audio_output)
        _player.setSource(QUrl.fromLocalFile(SOUND_PATH))
        _audio_output.setVolume(VOLUME_SET)
        _player.play()
    except Exception as err:
        print("Kurumi overlay: sound error", err)

    QTimer.singleShot(DISPLAY_DURATION_MS, _close_overlay)


def _schedule_overlay():
    if not mw.isActiveWindow():
        # Try again shortly if the main window is not ready yet
        QTimer.singleShot(500, _schedule_overlay)
        return

    _show_overlay()


QTimer.singleShot(DISPLAY_DELAY_MS, _schedule_overlay)
