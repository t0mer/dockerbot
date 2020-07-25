# DockerBot

DockerBot is a [Telepot](https://telepot.readthedocs.io/en/latest/) powerd, easy to use Telegram bot written in python that runs as Docker Container.
With DockerBot you can:
- List Exsisting Containers (and get status).
- Start, Stop and Restart Containers.
- Run SpeedTest.
- Get Memory Status (Used, Free, etc.)
- Get Disk Status.
- Get Server Time.
- Get Server Real (External) IP.


#### Credits:
=======

- [Adam Russak](https://github.com/AdamRussak) for working with me on this project


## Usage
### Run from hub

#### docker-compose from hub
```yaml
version: "3.7"

services:
  dockerbot:
    image: techblog/dockerbot
    container_name: dockerbot
    network_mode: host
    cap_add:
       - NET_ADMIN
    privileged: true
    restart: always
    environment:
      - API_KEY=  #Required
      - ALLOWED_IDS= #Required
    volumes:
       - /var/run/docker.sock:/var/run/docker.sock
```
Replace API_KEY with your bot token. if you do not have existing bot you can create one
using the instruction in this article:
[Bots: An introduction for developers](https://core.telegram.org/bots) 

In order to secure the bot and block unwanted calls from Unauthorized users add your allowd Id's with comma separated values into ALLOWED_IDS
environmet. in order to get your id use @myidbot in telegram and send the /getid command. the result will be your ID:

[![Get your ID](https://github.com/t0mer/dockerbot/raw/master/screenshots/Idbot.PNG "Get your ID")](https://github.com/t0mer/dockerbot/raw/master/screenshots/Idbot.PNG "Get your ID")

# Screenshots

[![Get Containers List](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_containers_list.PNG "Device Listing")](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_containers_list.PNG "Device Listing")

[![Show Disk Info](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_disk_info.PNG "Show Disk Info")](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_disk_info.PNG "Show Disk Info")

[![Run Speed Test](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_speedtest.PNG "Run Speed Test")](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_speedtest.PNG "Run Speed Test")


# Donation
<br>
If you find this project helpful, you can give me a cup of coffee :) 

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8CGLEHN2NDXDE)
