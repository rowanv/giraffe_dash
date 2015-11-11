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


