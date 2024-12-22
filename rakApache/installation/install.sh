echo "Lancement de l'installation"

echo "Decompresion du fichier"
sudo tar -xJf rakApache.tar.xz -C /opt/

echo "Installation de python"
sudo apt install python3

echo "Installation de php"
sudo apt install php

echo "Fin de l'installation\n lancer l'application avec launch.sh"
