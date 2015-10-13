#!/bin/bash
export http_proxy=http://10.3.100.207:8080
export ftp_proxy=http://10.3.100.207:8080
export https_proxy=http://10.3.100.207:8080

sudo rm -rf /usr/lib/harryplotter
sudo rm -rf ~/Desktop/Harry\ Plotter.desktop
sudo rm -rf /usr/share/applications/Harry\ Plotter.desktop

sudo -E apt-get install imagemagick 

sudo -E apt-get install -y --force-yes python-pip
sudo -E apt-get install -y --force-yes python-dev libxml2-dev libxslt-dev

#pyqt-4
sudo -E apt-get remove -y --force-yes --purge python-qt4
# sudo -E apt-get clean
sudo -E apt-get install -y --force-yes python-qt4
echo "pyqt-4 done!!\n"

sudo -E pip install qdarkstyle

#numexpr
deb http://us.archive.ubuntu.com/ubuntu precise main universe
# sudo apt-get update
sudo -E apt-get install -y --force-yes python-numexpr
echo "numexpr done!!\n"

#sympy
# sudo -E pip install sympy
# sudo -E apt-get install python-sympy
# echo "sympy done!!\n"

#mathtex
# apt-get install mathtex
# echo "mathtex done!!"

#pyqtgraph
sudo apt-get purge python-opengl
sudo -E pip install PyOpenGL PyOpenGL_accelerate
sudo -E apt-get install -y --force-yes python-qt4-gl
# apt-get install python-pyqtgraph
wget http://www.pyqtgraph.org/downloads/python-pyqtgraph_0.9.10-1_all.deb
sudo -E dpkg -i python-pyqtgraph_0.9.10-1_all.deb
echo "pyqtgraph done!!\n"

#sudo -E apt-get install -y --force-yes python-opengl python-numpy
sudo -E apt-get install -y --force-yes python-numpy

sudo cp -R harryplotter/ /usr/lib/
sudo cp /usr/lib/harryplotter/Harry\ Plotter.desktop /usr/share/applications/
sudo chmod +x /usr/share/applications/Harry\ Plotter.desktop
sudo ln -s /usr/share/applications/Harry\ Plotter.desktop  ~/Desktop
sudo chmod +x ~/Desktop/Harry\ Plotter.desktop

# wget http://www.pyqtgraph.org/downloads/python-pyqtgraph_0.9.10-1_all.deb