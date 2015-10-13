#!/bin/bash
sudo rm -rf /usr/lib/harryplotter
sudo rm -rf ~/Desktop/Harry\ Plotter.desktop
sudo rm -rf /usr/share/applications/Harry\ Plotter.desktop
rm -rf ~/Desktop/Harry\ Plotter.desktop

sudo -E apt-get purge imagemagick 
sudo -E pip uninstall PyOpenGL PyOpenGL_accelerate

#pyqt-4
sudo -E apt-get remove -y --force-yes --purge python-qt4
# sudo -E apt-get clean
sudo -E apt-get purge -y --force-yes python-qt4
echo "pyqt-4 done!!\n"

sudo -E pip uninstall qdarkstyle

#numexpr
#deb http://us.archive.ubuntu.com/ubuntu precise main universe
# sudo apt-get update
sudo -E apt-get purge -y --force-yes python-numexpr

echo "numexpr done!!\n"

sudo -E apt-get purge -y --force-yes python-pip
sudo -E apt-get purge -y --force-yes python-dev libxml2-dev libxslt-dev


#sympy
# sudo -E pip purge sympy
# sudo -E apt-get install python-sympy
# echo "sympy done!!\n"

#mathtex
# apt-get install mathtex
# echo "mathtex done!!"

#pyqtgraph
sudo apt-get purge python-opengl

sudo -E apt-get purge -y --force-yes python-qt4-gl
# apt-get install python-pyqtgraph
#wget http://www.pyqtgraph.org/downloads/python-pyqtgraph_0.9.10-1_all.deb
#sudo -E dpkg -i python-pyqtgraph_0.9.10-1_all.deb
echo "pyqtgraph done!!\n"
sudo -E apt get purge python-pyqtgraph
#sudo -E apt-get install -y --force-yes python-opengl python-numpy
sudo -E apt-get purge python-numpy