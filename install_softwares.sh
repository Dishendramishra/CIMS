#!/bin/bash

unset HISTFILE

RED='\033[1;31m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
Color_Off="\033[0m"

# =======================================================================
#                       getting root previliges
# =======================================================================
if [ $EUID != 0 ]; then
   sudo "$0" "$@"
   exit $?
fi
# =======================================================================


echo -e ${BLUE}"\n+----------------------------------------------------+"
echo -e ${BLUE}"|                 Configuring Proxy                  |"
echo -e "+----------------------------------------------------+" ${Color_Off}
read -p "Enter proxy username: " PROXY_USER
read -p "Enter proxy password: " PROXY_PASSWD


export http_proxy="http://${PROXY_USER}:${PROXY_PASSWD}@172.16.0.1:3128/"
export https_proxy="http://${PROXY_USER}:${PROXY_PASSWD}@172.16.0.1:3128/"
export ftp_proxy="http://${PROXY_USER}:${PROXY_PASSWD}@172.16.0.1:3128/"
# =======================================================================

echo $http_proxy

echo -e ${BLUE}"\n+----------------------------------------------------+"
echo -e ${BLUE}"|       updating & upgrading package lists           |"
echo -e "+----------------------------------------------------+" ${Color_Off}
sudo http_proxy=$http_proxy apt update -y
sudo http_proxy=$http_proxy apt upgrade -y


echo -e ${BLUE}"\n+----------------------------------------------------+"
echo -e ${BLUE}"|             Installing Basic Utilities             |"
echo -e "+----------------------------------------------------+" ${Color_Off}
sudo http_proxy=$http_proxy apt install -y git curl wget gparted apt-transport-https build-essential vlc htop easystroke intltool unrar-free unzip gdebi net-tools


echo -e ${RED}"\n adding Google chrome" ${Color_Off}
wget -e use_proxy=yes -e https_proxy=$https_proxy -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'


echo -e ${RED}"\n adding VS Code" ${Color_Off}
curl -x $http_proxy https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'


echo -e ${RED}"\n adding LibreOffice" ${Color_Off}
sudo -E add-apt-repository -y ppa:libreoffice/ppa


echo -e ${BLUE}"\n+----------------------------------------------------+"
echo -e ${BLUE}"|              updating package lists                |"
echo -e "+----------------------------------------------------+" ${Color_Off}
sudo http_proxy=$http_proxy apt update -y


echo -e ${GREEN}"\n+----------------------------------------------------+"
echo -e ${GREEN}"|               Installing Softwares                 |"
echo -e "+----------------------------------------------------+" ${Color_Off}

echo -e ${RED}"\n Thunderbird" ${Color_Off}
sudo http_proxy=$http_proxy apt install -y thunderbird


echo -e ${RED}"\n VS Code" ${Color_Off}
sudo http_proxy=$http_proxy apt install -y code


echo -e ${RED}"\n Google Chrome" ${Color_Off}
sudo http_proxy=$http_proxy apt install -y google-chrome-stable


echo -e ${RED}"\n Libreoffice" ${Color_Off}
sudo http_proxy=$http_proxy apt install -y libreoffice


echo -e ${RED}"\n BlueJeans" ${Color_Off}
wget -e use_proxy=yes -e https_proxy=$https_proxy -O bluejeans.deb "https://swdl.bluejeans.com/desktop-app/linux/2.25.0/BlueJeans_2.25.0.78.deb"
sudo dpkg -i ./bluejeans.deb


echo -e ${RED}"\n openssh-server" ${Color_Off}
sudo http_proxy=$http_proxy apt install -y openssh-server
sudo ufw allow ssh
sudo ufw enable


echo -e ${RED}"\n XRDP" ${Color_Off}
sudo http_proxy=$http_proxy apt install -y xrdp
sudo systemctl enable --now xrdp
sudo ufw allow from any to any port 3389 proto tcp

# echo -e ${RED}"\n Citrix Receiver" ${Color_Off}
# wget -e use_proxy=yes -e https_proxy=$https_proxy -O iclient.deb "https://downloads.citrix.com/20234/icaclient_21.12.0.18_amd64.deb?__gda__=exp=1642449285~acl=/*~hmac=19d3b5faf1abe55a64b3485700caf1de84de1bd63dee7e60e0181913061d7683"
# sudo dpkg -i ./iclient.deb
