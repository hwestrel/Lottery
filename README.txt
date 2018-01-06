#######################################
System folders on the PI:
Image folder  /usr/share/apache2/icons
cgi-bin folder  /usr/lib/cgi-bin
doc root  /var/www/html 


ToDo to set Lottery on PI:

#0 PI Setup
------------------------
sudo raspi-config
 change pi password
 set hostname
 set boot option
 set local (sv UTF8)
 enable camera, ssh
 advance options, expand filesystem
 update
sudo reboot 
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git

# Install python/libs
ls /usr/bin/python*
#Install python 3.x if not already
sudo apt-get install python3
sudo apt-get install python3-pip
# Install python libs
sudo apt-get install python3-gpiozero
sudo apt-get install python3-picamera
pip install requests


# Optional
#sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
#sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2
#python --version
#update-alternatives --list python
#update-alternatives --config python


# Install Apache2
# if needed, sudo apt-get update  --fix-missing
sudo apt-get install apache2 -y
sudo apt-get install libapache2-mod-python
sudo a2enmod cgi
sudo mv /etc/apache2/apache2.conf /etc/apache2/apache2.conf_org
sudo cp ~/Lottery/config_files/apache2.conf_with_cgi_AND_mod_python_AND_basic-auth /etc/apache2/apache2.conf
sudo service apache2 restart

Setup WiFi
------------------
# start wlan0
sudo ifup wlan0

https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
sudo iwlist wlan0 scan
#Gen key (optional)
wpa_passphrase "HIF"

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

network={
        ssid="your ssid"
        psk="your generated psk key"
}
or 
network={
        ssid="yuor ssid"
        psk="your passphrase"
        key_mgmt=WPA-PSK
}

Note that, although wpa_passphrase returns the psk value unquoted, the  wpa_supplicant.conf file requires this value to be quoted, otherwise your Pi will not connect to your network.
sudo wpa_cli reconfigure
#check if connected
ifconfig wlan0


#1 Git clone Lottery or unzip to /home/pi/Lottery
--------------------------------------------------
git clone "https://github.com/hwestrel/Lottery.git"

cd ~/Lottery
sudo chown www-data:www-data log.txt
sudo chown root:root cgi/index.py


#2 Create folder sym links
cd /usr/share/apache2/icons
sudo ln -s /home/pi/Lottery/face.jpg face.jpg
sudo ln -s /home/pi/Lottery/winner.jpg winner.jpg
sudo ln -s /home/pi/Lottery/Quadcopter.jpg Quadcopter.jpg
sudo mv openlogo-75.png openlogo-75.png_old
sudo ln -s  /home/pi/Lottery/Automic-Logotype-Black.png openlogo-75.png


cd /usr/lib/cgi-bin
sudo ln -s /home/pi/Lottery/cgi/index.py index.py

cd /var/www/html
sudo mv index.html index.html_org
sudo ln -s /home/pi/Lottery/index.html index.html
sudo ln -s /home/pi/Lottery/index.html1 index.html1
sudo ln -s /home/pi/Lottery/index.html2 index.html2
sudo ln -s /home/pi/Lottery/style.css style.css
sudo ln -s /home/pi/Lottery/winner.html winner.html


# Install AE Agent
copy agent-archive from binaries/  and unzip/untar
to  /opt


 # Setup Crontab
sudo crontab -e
@reboot /opt/automic/bin/start.sh

# pi Crontab (not needed anymore)
@reboot python3 /home/pi/Lottery/PiCamera_snapshot.py


# Make apache user www-data possible to take picture
# ----------------------------------------------------
sudo chmod o+rwx /dev/vchiq

It's not sticky across a reboot so it probably needs a UDEV rule to fix that.
sudo -i
echo 'SUBSYSTEM=="vchiq",GROUP="video",MODE="0660"' > /etc/udev/rules.d/10-vchiq-permissions.rules
usermod -a -G video www-data
exit

sudo usermod -a -G www-data pi
sudo chgrp www-data /home/pi
sudo chgrp www-data /home/pi/Lottery
chmod g+w /home/pi
chmod g+w /home/pi/Lottery
