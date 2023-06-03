# formatting sd-card:
# 1. unplug sd-card
# 2. put it in sd-card reader
# 3. plug reader to laptop
# 4. download and install RPi imager from official RPi site
# 5. write the default Raspian OS image to the sd-card
# 6. plug the sd-card back into the RPi
# 7. boot up and configure the RPi

# enable ssh from within the RPi using:
sudo systemctl enable ssh
sudo systemctl start ssh

# go on laptop now and continue from there

# how to resolve ssh error after formatting sd card?
# remove previous ip address line: 
#nano ~/.ssh/known_hosts
# for e.g. 192.168.1.131 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBIU5Tixh6l2rr9otfXA$

# ssh into RPi from laptop using:
ssh pi@192.168.1.132

sudo apt-get update
sudo apt-get install flac
sudo apt-get install python-pyaudio python3-pyaudio
sudo apt-get install mpg321
sudo apt-get install python3-bluez

# python libraries to install
pip3 install SpeechRecognition
pip3 install mapbox
pip3 install geocoder
pip3 install pynmea2
pip3 install gTTS pyttsx3 playsound

# follow the followignyoutube video to setup GPS:
# https://www.youtube.com/watch?v=IM3vgdAExGU
# in case you need to install raspi-config: https://gist.github.com/jgamblin/2441964a1266764ed71f3243f87bbeec
#cgps -s
#sudo apt-get install gpsd

# to setup github ssh follow steps in https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

# setup git configuration
#git config --global user.email "{github email}"
#git config --global user.name "{github name}"

# clone VA project
cd ~
# if git ssh was configured, use:
#git clone git@github.com:jacqu3lin3/Intellihelm.git
# otherwise, use:
git clone https://github.com/jacqu3lin3/Intellihelm.git

# install pre-requisite packages for phony
cd ~

# install dongle
sudo apt-get install bluetooth
dtoverlay=pi3-disable-bt
#hcitool scan
#sudo l2ping -c 1 {MAC Address}

# install bluez5
#sudo apt install libdbus-1-dev libudev-dev libical-dev libreadline-dev
sudo apt-get install autoconf libtool intltool libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev

#sudo apt-get install python-bluez
git clone https://git.kernel.org/pub/scm/bluetooth/bluez.git
cd bluez
git checkout tags/5.23
./bootstrap
./configure
make -j4
sudo make install
cd ..

# install ofono
sudo apt-get install autoconf libtool intltool libdbus-1-dev glib2.0 mobile-broadband-provider-info

git clone https://git.kernel.org/pub/scm/network/ofono/ofono.git
cd ofono
git checkout tags/1.17
./bootstrap
./configure
make -j4
sudo make install
cd ..

# install pulseaudio
sudo apt-get install pulseaudio pulseaudio-module-zeroconf alsa-utils avahi-daemon
# install alsaaudio
# to understand alsa, read https://superuser.com/questions/144648/how-do-alsa-and-pulseaudio-relate
sudo apt-get install python-alsaaudio
# enable alsa
#sudo modprobe snd-bcm2835
#echo "snd-bcm2835" | sudo tee -a /etc/modules
# to set up networking:
#sudo nano /etc/pulse/default.pa
# and uncomment the lines:
# load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;192.168.0.0/16
# load-module module-zeroconf-publish
# for system-wide setup:
#sudo pulseaudio --system

# setup soundcard by following steps in link: https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi/

# test speakers
# sudo nano /usr/share/alsa/alsa.conf
speaker-test -c2 -twav
aplay /usr/share/sounds/alsa/Front_Center.wav

# clone calls project (phony) within VA project
cd ~
sudo apt-get install python-dev python-setuptools python-gobject python-dbus rfkill
# if phony is not in ~/Intellihelm/.
git clone https://github.com/littlecraft/phony.git
cd phony
sudo python setup.py install
# otherwise
#unzip phony-master
#cd phony-master
#sudo python setup.py install

# blueooth debug:
sudo apt-get install bluetooth
/etc/init.d/bluetooth status

# run call example code
python ./phony/test/example_phony_service.py

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#At the start of a new terminal session
#start pulseaudio
pulseaudio --start

# start ofono
systemctl start ofono

#configure bluetooth
hciconfig

#check for bluetooth-related errors
dmesg | grep -i bluetooth

#check your source and sink devices
pacmd list-sources | grep -e 'index:' -e device.string -e 'name:' 
pacmd list-sinks | grep -e 'name:' -e 'index:'

#set your source and sink devices
pacmd set-default-source "enter your microphone device from the result of the command in line 141" #keep the quotation marks 
pacmd set-default-sink "enter your speaker device name from the result of the command in line 142" #keep the quotation marks

#test the speakers
speaker-test -c2 -twav #if it doesn't work, run "sudo reboot" then run lines 129-138 in the new session. Then run this line again

# pair RPi to bluetooth device
bluetoothctl
power on
agent on
scan on
# wait for Device 00:9A:CD:E3:5B:CC HUAWEI SCL-L04 to show
pair {MAC Address}
trust {MAC Address}
# accept pairing request on connecting device
connect {MAC Address}
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

