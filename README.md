BirdFeederMessenger
==========
A small Raspberry Pi application which sends short videos of detected birds at your bird feeder to your mobile phone.

It involves the following:
- **Raspberry Pi** with a camera module.
- Object detection using the **tiny yolo v4** model.
- **Telegram API** for sending videos.

All credits to the following authors from which most of the information was gathered:
- Asadullah Dal (https://github.com/Asadullah-Dal17/yolov4-opencv-python)
- Florian Dedov (https://github.com/NeuralNine)
- Ahmed Fadlelmawla (https://medium.com/@eddawy)
- Vikas Jha (https://www.youtube.com/watch?v=NYT1KFE1X2o&t=245s)
- Maddie Moate (https://www.youtube.com/watch?v=IiOH5LUVkWo)

<br/><br/>

<p align="center">
  <img src="doc/SNA_banner.png" width="100%"/>
  <br>
</p>


[**Installation**](#installation)
&nbsp; &nbsp; &vert; &nbsp; &nbsp;
[Telegram Bot](#Telegram Bot)
&nbsp; &nbsp; &vert; &nbsp; &nbsp;
[Clone this repo to your Raspberry Pi](#Clone this repo to your Raspberry Pi)
&nbsp; &nbsp; &vert; &nbsp; &nbsp;
[Apply solution to Mastodon](#Apply solution to Mastodon)


---

## Connect to your Raspberry Pi via SSH or VNC and then...

##  Installation

0. Install `python` >= 3.7.9 (I used 3.7.9), Install `pip` >= 20.1.1 
1. Clone the repository
`git clone https://github.com/krussmann/BirdFeederMessenger.git`
2. Change directory into repository `cd BirdFeederMessenger`

### Using Python Virtual Environment
1. Install Virtualenv
`sudo -H python3 -m pip install virtualenv`

2. Setup a Virtual Environment
`python3 -m virtualvenv env`

3. Activate Virtual Environment
`source env/bin/activate`

4. Install required Packages to Virtual Environment
`pip install -r requirements.txt`

## Setting up a Telegram Bot

1. Install Telegram on your mobile phone.
2. Create a Telegram bot by writing `/newbot` to the verified telegram user "BotFather".
3. Save the API token as an environment variable `TelegramTok` in your system.
4. Create a group with the bot and save the group id as an environment variable `GroupID` in your system. The Bot will send the Videos to this group.

## Place Raspberry Pi next to bird feeder and run detection
1. `python3 detection.py`