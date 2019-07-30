SENSITIVITY = 30  # 1 - 100
MIN_CONTOUR = 5000
TG_BOT_API_KEY = ''
TG_CHANNEL_ID = ''
GIF_FOLDER = 'gifs'
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
GIF_FPS = 3
MAX_FRAMES = 100

try:
    from .settings_local import *
except ImportError:
    pass
