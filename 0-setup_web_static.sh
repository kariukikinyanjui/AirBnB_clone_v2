#!/usr/bin/env bash
# Install Nginx
sudo apt-get update
sudo apt-get -y install nginx

# Create directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create HTML file to test your Nginx configuration
echo "Hello Mike!" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration
config_file='/etc/nginx/sites-available/default'
sudo sed -i '/location \/hbnb_static {/!b;n;c\\talias /data/web_static/current/;' "$config_file"

sudo service nginx restart
