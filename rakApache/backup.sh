echo "commencement du backup"
sudo tar -xJf bkp.tar.xz -C .

echo "supression desfichier corrompu"
sudo rm -rf src
sudo rm -rf config
sudo rm -f launch.sh


echo "copie de fichier"
cp -r bkp/src .
cp -r bkp/config .
cp  bkp/launch.sh .
sudo rm -rf bkp

echo "votre serveur est revenu a ses config de base"
