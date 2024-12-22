import threading
import traceback
import socket
import os
from MaintienClient import MaintienClient as mc
from Request import Lecteur


#   le serveur
class monHTTPServeur:
    def __init__(s):
        s.repertoire="serveur/projet"
        s.port=1213
        s.ip="0.0.0.0"
        s.php=False
        
        s.initialiseur()

#   lecture du fichier
    def initialiseur(s):
        with open("config/rakApache.ini","r") as file :
            content=file.read().split("\n")
            for i in content:
                if i.startswith(";"):
                    continue
                else :
                    if i.startswith("PORT"):
                        s.port=int(i.split(": ")[1].strip())
                        # print(s.port)
                        continue
                    elif i.startswith("PATH"):
                        s.repertoire=i.split(": ")[1].strip()
                        if (i.endswith("/")):
                            s.repertoire=s.repertoire[:-1]
                        # print(s.repertoire)
                        continue
                    elif i.startswith("IP"):
                        s.ip=i.split(": ")[1].strip()
                        # print(s.ip)
                        continue

                    elif i.startswith("PHP"):
                        test="True"
                        s.php=test.lower()==(i.split(": ")[1].strip()).lower()
                        # print(s.php)
                        continue
#   lancement du serveur
    def serve_forever(s):
        s.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.s_socket.bind((s.ip,s.port))
        s.s_socket.listen(3)
        print("Serveur en marche sur le port {}".format(s.port))
        while True : 
#       Acceptation d'un client
            c_socket,addr = s.s_socket.accept()
#           creation de thread pour son maintient
            c_thread = threading.Thread(target=s.client,args=(c_socket,)) 
            c_thread.start()
#   fermeture du serveur    
    def close(s):
        s.s_socket.close()
#   traitement d'un client apres acception du client    
    def client(s,c_socket):
        try:
            control=mc(c_socket)
            lect=Lecteur(control,s.repertoire,s.php)
            c_socket.close()
        except Exception as e:
            traceback.print_exc()            


serveur = monHTTPServeur()
try:
    serveur.serve_forever()
    serveur.close()
except KeyboardInterrupt :
    serveur.close()

