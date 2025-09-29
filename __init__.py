##Warning: Use it as your own risk
import os
import random
import xml.etree.ElementTree as ET

from aqt import mw
from aqt.qt import QLabel, QPainter, QPixmap, Qt, QTimer
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

config = mw.addonManager.getConfig(__name__) or {}


def _clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp ``value`` to the inclusive range ``[minimum, maximum]``."""

    return max(minimum, min(value, maximum))


def _load_configured_chance() -> float:
    """Return the per-second probability from the add-on configuration."""

    denominator = config.get("chance_out_of", 10_000)
    try:
        denominator = float(denominator)
    except (TypeError, ValueError):
        denominator = 10_000

    # Treat non-positive values as "always trigger" to avoid ZeroDivisionError.
    if denominator <= 0:
        return 1.0

    return 1.0 / denominator


def _load_configured_volume() -> float:
    """Return a volume between 0.0 and 1.0."""

    volume = config.get("volume", 1.0)
    try:
        volume = float(volume)
    except (TypeError, ValueError):
        volume = 1.0

    return _clamp(volume, 0.0, 1.0)


CHANCE = _load_configured_chance()
FPS = 20
VOLUME_SET = _load_configured_volume()
ADDON_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(ADDON_PATH, "foxy.png")
XML_PATH = os.path.join(ADDON_PATH, "foxy.xml")
SOUND_PATH = os.path.join(ADDON_PATH, "jumpscare.mp3")

player = None
audio_output = None
frames = []


def load_frames():
    global frames
    frames.clear()

    sheet = QPixmap(IMAGE_PATH)
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    for sub in root.findall("SubTexture"):
        x, y = int(sub.get("x")), int(sub.get("y"))
        w, h = int(sub.get("width")), int(sub.get("height"))
        fx, fy = int(sub.get("frameX", 0)), int(sub.get("frameY", 0))
        fw, fh = int(sub.get("frameWidth", w)), int(sub.get("frameHeight", h))

        subimg = sheet.copy(x, y, w, h)

        frame = QPixmap(fw, fh)
        frame.fill(Qt.GlobalColor.transparent)

        painter = QPainter(frame)

        painter.drawPixmap(-fx, -fy, subimg)
        painter.end()

        frames.append(frame)


def play_jumpscare():
    global player, audio_output
    if not frames:
        load_frames()


    label = QLabel(mw)
    label.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    label.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    label.setStyleSheet("background-color: transparent;")
    label.setGeometry(mw.rect())
    label.setScaledContents(True)
    label.show()


    try:
        player = QMediaPlayer()
        audio_output = QAudioOutput()
        player.setAudioOutput(audio_output)
        player.setSource(QUrl.fromLocalFile(SOUND_PATH))
        audio_output.setVolume(VOLUME_SET)
        player.play()
    except Exception as e:
        print("Sound error:", e)


    frame_index = {"i": 0}

    def next_frame():
        if frame_index["i"] < len(frames):
            f = frames[frame_index["i"]]
            label.setPixmap(f.scaled(
                mw.size(),  
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
            frame_index["i"] += 1
        else:
            label.close()


    anim_timer = QTimer(mw)
    anim_timer.timeout.connect(next_frame)
    anim_timer.start(1000 // FPS)
    next_frame()


def check_random():
    if not mw.isActiveWindow():
        return
    
    if random.random() < CHANCE:
        play_jumpscare()

timer = QTimer(mw)
timer.timeout.connect(check_random)
timer.start(1000)
