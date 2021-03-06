# RaspGuard
A tiny DIY home video security tool for Raspberry Pi. Written in Python using OpenCV and Telegram API (for notifications). 

## About RaspGuard
It is quite dark near my apartment entrance door, so in addition to a motion light sensor I have written this small script which tracks 
any motion when light turns on and sends me a GIF animation in a private telegram group. See `raspguard/settings.py` to configure telegram.


## Installation and setup

**1. Clone the raspguard repo**
```
git clone git@github.com:aogz/raspguard.git
```

**2. Install requirements**
```
cd raspguard
mkvirtualenv -p python3 raspguard  # Or virtualenv -p python3 venv && source venv/bin/activate
pip install -r requirements.txt
```

[Install OpenCV on Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/)

**3. Create bot and channel and make bot admin**

[How to create a bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and [How to create a channel](https://telegram.org/faq_channels#q-what-39s-a-channel)

**4. Then make your bot channel administrator**
1. Open Channel info (in app title)
2. Choose Administrators
3. Add Administrator
4. There will be no bots in contact list, so you need to search for it. Enter your bot's username
5. Clicking on it you make it as administrator.

**5. Set bot api key and channel in settings**

_Lifehack_: If you want to use a private channel, use one of these solutions:

[How to obtain the chat id of a private telegram channel](https://stackoverflow.com/questions/33858927/how-to-obtain-the-chat-id-of-a-private-telegram-channel)

**6. Play with settings.SENSITIVITY and settings.MIN_CONTOUR to get better results**

**7. Connect a camera to your awesome Raspberry Pi**

## Run it
```
python start.py
```

## Run it in background on reboot
```
crontab -e 
```

Add this at the end of the file:
```
@reboot python3 /home/pi/raspguard/start.py  # replace with your own path
```

