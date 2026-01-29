# web_dev
A place to test out django, flask and a homemade webserver

## Setting up a website hosting service
I chose OVH cloud with the least powerful VPS, it's easily enough for a small website.

Then register with DNS and choose a website address, then set up a record to point to static ipv4 address of the VPS (see instructions elsewhere).

## Installation
Update debian
```
sudo apt update && sudo apt upgrade -y
```

Change ssh port from 22 to a random number for security. Edit the following:
```
sudo nano /etc/ssh/sshd_config
sudo nano /lib/systemd/system/ssh.socket
```

Restart the system
```
sudo systemctl daemon-reload
sudo systemctl restart sshd
```

### Install vncserver, get it running
```
sudo apt install xfce4 xfce4-goodies
sudo apt install tigervnc-standalone-server
vncserver :<random number>
vncserver --list to get port number
```

Connect with vnc viewer e.g. TigerVNC with server name:port number e.g. vps-xxxxxxxx.vps.ovh.net:xxxxx

### Install python
```
sudo apt-get install python3
sudo apt install spyder3
```

Make python virtual env and make available to all users in www dir
```
sudo apt install python3-venv
cd /var/www/
python3 -m venv .venv
chmod 766 -R .venv
source /var/www/.venv/bin/activate
pip install Django
pip install flask
pip install paramiko requests numpy altair pandas
```

Install sqlite brower. This will allow you to open any sqlite database files in a GUI:
```
sudo apt-get install sqlitebrowser
```

### Install apache

I use apache and mod_wsgi rather than nginx. Install and test as follows:
```
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
```

```
sudo apt install firefox-esr
```
To check if apache is working, go to:
```
http://<ipaddress>
```

### Set up git repository

Link to github. Run the command:
```
ssh-keygen
```
And copy the resulting public key (.pub) to github


Set up repository locally:
```
cd /var/www/
git clone git@github.com:irthomas/web_dev.git
```

To use the websites from the repository, you need to set up the secret keys and apache config files correctly:

Make the secret key python script. The secret keys are generated when you make a new web application.

Move them to a file not tracked by github, to avoid publishing the keys online:
```
nano /var/www/web_dev/settings/secret_keys.py
SECRET_KEYS = {"djhome":"<secret key>"}
ALLOWED_HOSTS = ['<ipaddress>', '<web domain>', '127.0.0.1']
```

Make apache2 config file like this:
```
nano /etc/apache2/sites-available/000-default.conf
<VirtualHost *:80>
	ServerName <ipaddress>
	ServerAlias <ipaddress>
	ServerAdmin <email address>
```

Followed by one process for each website.

Each process must have different number X=1,2,3. The main website should be last:

```
    WSGIDaemonProcess myprocX processes=1 python-home=<path to python venv root>
    WSGIScriptAlias <web url> <path to wsgi.py>
    <Directory <path to project directory>>
        WSGIProcessGroup myprocX
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
```
E.g.
```
    WSGIDaemonProcess myproc99 processes=1 python-home=/var/www/.venv
    WSGIScriptAlias / /var/www/web_dev/fl/website/wsgi.py
    <Directory /var/www/web_dev/fl/website>
        WSGIProcessGroup myproc99
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

Remember to restart the server after each change
```
sudo systemctl restart apache2
```
To check each site, go to:
```
http://<ipaddress>/<web url>
```

Set up the swapfile to avoid memory failures e.g. see https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-debian-11).


### Set up a cron job

This is to update databases and get new files.

```
sudo apt install cron
crontab -e
```
Add this line to the file to run at midnight each night:
```
0 0 * * * <path to shell script> <path to log file> 2>&1
```
E.g.
```
0 0 * * * /var/www/web_dev/cron_midnight.sh /var/www/cron.log 2>&1
```

Run the cron_midnight.sh script to build the required databases and static json files.


## To create a new Django website

### New django project
```
django-admin startproject djhello
```

Django helloworld
```
python
cd djhello
python3 manage.py startapp hello_world
```

Edit settings.py:
```
python
ALLOWED_HOSTS = ['<web domain>']
```

Edit views.py:
```
python
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello world from django!")
```

Edit /djhello/djhello/urls.py:
```
python
urlpatterns = [
path('', include('hello_world.urls')),
path('admin/', admin.site.urls),
]
```

Edit wsgi.py: 
```
python
sys.path.append('/var/www/web_dev/djhello')
os.environ["DJANGO_SETTINGS_MODULE"] = "djhello.settings"
```

Remember to add an entry for /var/www/web_dev/djhello/djhello/wsgi.py to the file /etc/apache2/sites-available/000-default.conf

Remember to set DEBUG = False before making a website available to the world.

Remember to move allowed hosts and secret keys to a separate file before pushing to a public github.

### Creating a new Flask website

Make dir:
```
mkdir /fl/hello_world
```

Make hello_world.py in fl/hello_world:
```
python
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello_world():
	return "Hello world from flask!"
if __name__ == "__main__":
    app.run()
```

Make wsgi.py in fl/hello_world:
```
python
sys.path.append('/var/www/web_dev/fl/hello_world')
from hello_world import app as application
```

Remember to add an entry for /var/www/web_dev/fl/hello_world/wsgi.py to the file /etc/apache2/sites-available/000-default.conf

Remember to set DEBUG = False before making a website available to the world.

Remember to move allowed hosts and secret keys to a separate file before pushing to a public github.
