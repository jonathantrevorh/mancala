mancala
=======

Play [Mancala](http://en.wikipedia.org/wiki/Mancala#General_gameplay) via SMS by running `python server.py` on a public server and pointing [Twilio](http://twilio.com) to `http://your-domain.example.com/sms`

Warning: It runs in debugging mode, which is a bad idea for production services.

## Getting running
### Setting up your environment and running the server
```Python
git clone git@github.com:jonathantrevorh/mancala.git
cd mancala
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python server.py
```

### Configuring Twilio
1. [Sign up](https://www.twilio.com/try-twilio) or [log in](https://www.twilio.com/login)
1. Navigate to the [Numbers page](https://www.twilio.com/user/account/phone-numbers/incoming)
1. Select the number you want to use for Mancala, and change its Messaging URL to `http://your-domain.example.com/sms`


### Configuring Apache
Yeah, I'm sorry to add this as a dependency, but I haven't searched once for how to bind Flask to the public interface. Included is an Apache 2.2 virualhost configuration for proxying port 5000 to a domain. I copied from the Internet.


## Playing
All commands are case-insensitive. Text `start` to your number to get going.

### Cheat Codes
- `win` automatically win
- `computer_play` make the computer play a move
- `start` and `help` to get help text
- `reset` start a new game
