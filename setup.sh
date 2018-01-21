cd /root/
apt update
apt install build-essential python-dev git scons swig monit mosquito
systemctl enable mosquitto
systemctl enable monit
systemctl start mosquitto
systemctl start monit
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
python setup.py install
pip install paho-mqtt
cp monit/monit-mqtt-led /etc/monit/conf-available
cd /etc/monit/conf-enabled
ln -s monit-mqtt-led ../conf-available/monit-mqtt-led
