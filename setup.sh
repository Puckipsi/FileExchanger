
#run on debian based

sudo apt-get update

yes | sudo apt-get install python3-venv

yes | sudo apt install python3-pip

git clone https://github.com/Puckipsi/FileExchanger.git

cd FileExchanger

source venv/bin/activate

echo 'instal requirements'
sudo pip3 install -r requirements.txt

echo 'run app'
sudo python3 app.py  >> log.txt