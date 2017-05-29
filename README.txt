System folders on the PI:
Image folder  /usr/share/apache2/icons
cgi-bin folder  /usr/lib/cgi-bin
doc root  /var/www/html 


ToDo to set Lottery on PI:

#0   
sudo raspi-config
 change pi password
 set hostname
 set boot option
 set local (se UTF8)
 enable camera, ssh
 advance options, expand filesystem
 update
sudo reboot 
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git

Setup WiFi
https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
sudo iwlist wlan0 scan
wpa_passphrase "HIF"
network={
        ssid="your ssis"
        #psk="your passphrase"
        psk="your generated psk key"
}

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
Note that, although wpa_passphrase returns the psk value unquoted, the  wpa_supplicant.conf file requires this value to be quoted, otherwise your Pi will not connect to your network.



#1 Git clone Lottery or unzip to /home/pi/Lottery
git clone "https://github.com/hwestrel/Lottery.git"

#2 Create folder sym links
cd /usr/share/apache2/icons
sudo ln -s /home/pi/Lottery/face.jpg face.jpg
sudo ln -s /home/pi/Lottery/winner.jpg winner.jpg 

cd /usr/lib/cgi-bin
sudo ln -s /home/pi/Lottery/cgi/index.py index.py

cd /var/www/html
sudo ln -s /home/pi/Lottery/index.html index.html
sudo ln -s /home/pi/Lottery/index.html1 index.html1
sudo ln -s /home/pi/Lottery/index.html2 index.html2
sudo ln -s /home/pi/Lottery/style.css style.css
sudo ln -s /home/pi/Lottery/winner.html winner.html


 
# Install Apache2
# if needed, sudo apt-get update  --fix-missing
sudo apt-get install apache2 -y
sudo a2enmod cgi
Copy apache2.conf template from config_files/ to replace 
/etc/apache2/apache2.conf



# Check python
ls /usr/bin/python*
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2
python --version
update-alternatives --list python
update-alternatives --config python

# Install python libs
sudo apt-get install python-gpiozero python3-gpiozero
sudo apt-get install python3-picamera

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
sudo chmod o+rwx /dev/vchiq.

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
