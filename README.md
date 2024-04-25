BirdWatchCam
==========
A small Raspberry Pi application which sends short videos of detected birds to your mobile phone.

It involves the following:
- **Raspberry Pi** with a camera module.
- Object detection using the **tiny yolo v4** model.
- **Telegram API** for sending videos.

<br/><br/>


https://github.com/krussmann/BirdWatchCam/assets/91115542/ac856ada-f0c4-49a9-aaf9-1b27f94d3fea


[**Virtual Environment**](#seting-up-a-virtual-environment)
&nbsp; &nbsp; &vert; &nbsp; &nbsp;
[Installation](#installation)
&nbsp; &nbsp; &vert; &nbsp; &nbsp;
[Telegram Bot](#seting-up-a-telegram-bot)


---

## Connect to your Raspberry Pi via SSH or VNC and then...
0. Install `python` >= 3.7.9 (I used 3.7.9), Install `pip` >= 20.1.1

## Setting up a Virtual Environment
1. Install Virtualenv
`sudo -H python3 -m pip install virtualenv`

2. Setup a Virtual Environment
`python3 -m virtualvenv env`

3. Activate Virtual Environment
`source env/bin/activate`

##  Installation
1. Clone the repository
`git clone https://github.com/krussmann/BirdWatchCam.git`

2. Change directory into repository `cd BirdWatchCam`

3. Install required Packages to Virtual Environment
`pip install -r requirements.txt`

## Setting up a Telegram Bot

1. Install Telegram on your mobile phone.
2. Create a Telegram bot by writing `/newbot` to the verified telegram user "BotFather".
3. Save the API token as an environment variable `TelegramTok` in your system.
4. Create a group with the bot and save the group id as an environment variable `GroupID` in your system. The Bot will send the Videos to this group.

## Place Raspberry Pi next to bird feeder and run detection
1. `python3 detection.py`
