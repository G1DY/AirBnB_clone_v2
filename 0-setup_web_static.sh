#!/usr/bin/env bash
# setting up nginx servers for deployment of web_static
set -x
sudo apt-get -y update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'ssh'
sudo ufw allow 443

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

sudo touch /data/web_static/releases/test/index.html
echo "Best School" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {
    listen 80 default_server,
    listen [::]:80 default_server,
    add_header X_served-By $HOSTNAME;
    root /var/www/html/;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-available/default

sudo service nginx restart
