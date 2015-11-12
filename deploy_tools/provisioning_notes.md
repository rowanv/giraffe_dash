Provisioning the dashboard
==========================

## Required packages:

* nginx
* Python 3
* Git
* Pip
* virtualenv

e.g., on Ubuntu:

	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with domain name, e.g. staging.my-domain.com


# Automated deploy
## on my machine

fab deploy --host=rowan@dash.rowanv.com

## Then on the actual server, within source for the website

sed "s/SITENAME/dash.rowanv.com/g" \
    deploy_tools/nginx.template.conf | sudo tee \
    /etc/nginx/sites-available/dash.rowanv.com

sudo ln -s ../sites-available/dash.rowanv.com \
    /etc/nginx/sites-enabled/dash.rowanv.com

sed "s/SITENAME/dash.rowanv.com/g" \
    deploy_tools/gunicorn-upstart.template.conf | sudo tee \
    /etc/init/gunicorn-dash.rowanv.com.conf

sudo service nginx reload
sudo start gunicorn-dash.rowanv.com
# or sudo restart gunicorn-dash.rowanv.com
# Actually, currently starting gunicorn with:
# ../virtualenv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app -D
# To view running gunicorn processes:
# ps ax|grep gunicorn
