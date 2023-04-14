
#run on debian based

#run manual:
# 1. git clone https://github.com/Puckipsi/FileExchanger.git
# 2. cd FileExchanger
# 3. bash setup.sh --verbose

yes | sudo apt-get update

yes | sudo apt install redis-server

yes | sudo apt-get install python3-venv

yes | sudo apt install python3-pip

source venv/bin/activate

echo 'instal requirements'
sudo pip3 install -r requirements.txt

echo 'run app'
sudo python3 app.py  >> log.txt