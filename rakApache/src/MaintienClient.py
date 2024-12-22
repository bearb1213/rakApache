import os
import secrets
#   traitement des requetes des clients
class MaintienClient:

    def __init__(s,c_socket):

        s.c_socket = c_socket
        s.requete = c_socket.recv(1024).decode()
#       traitement du requete
        s.traitementRequete()
        s.reponse={}
#       assignation de base des reponse
        s.reponse['code']=200
        s.reponse['message']="OK"
        s.content_type= "text/html"
        s.length = 0
        s.serveur = "Rakotoson/2.13"
        s.other_header = ""
        s.create_header()

#   traitement des requetes 
    def traitementRequete(s):
        request = s.requete.split("\r\n")
    #   assignation de la requete du client a un table cle valeur
        s.content={}
        indice=0
        for i in request :
            if i: 
                if indice==0:
                    
                    s.method = request[0].split(" ")[0]
                    s.chemin = request[0].split(" ")[1]
                    s.version = request[0].split(" ")[2]
                    
                    
                elif len(i.split(": "))==2 :                
                    key , value = i.split(": ")
                    s.content[key]=value.strip()
                elif s.method=="POST" and len(request)==indice+1:
                    s.value=i.strip()
            
            indice+=1

        


#   creation de l'entete    
    def create_header(s)->None :
        s.reponse['code']=200
        s.reponse['message']="OK"
        s.content_type= "text/html"
        s.length = 0
        s.serveur = "Rakotoson/2.13"
        s.other_header = ""
#   envoie des reponse avec son message
    def send_response(s,code:int , message:str="OK"):
        s.reponse['code']=code
        s.reponse['message']=message
#      envoie de l'entete
    def send_header(s,titre:str, contenu:str):
        if titre == "Content-Type":
            s.content_type=contenu
        elif titre == "Content-Length":
            s.length = int(contenu)
        elif titre == "Server":
            s.serveur = contenu
        else :
            s.other_header+=((titre)+": "+str(contenu)+"\r\n")
#       fermeture de l'entete
    def end_headers(s):
        s.other_header+="\r\n"
#      envoie de l'entete
    def create_header(s) -> str:
        header=""
        header+="HTTP/1.1 "+str(s.reponse['code'])+" "+s.reponse["message"]+"\r\n"
        header+="Content-Type: "+s.content_type+"\r\n"
        header+="Content-Length: "+str(s.length)+"\r\n"
        header+="Server: "+s.serveur+"\r\n"
        header+=s.other_header
        return header

#       ecriture du fichier
    def write(s,contenu:bytes):
        s.send_header("Content-Length",str(len(contenu)))
        header=s.create_header()
        header+="\r\n"
        s.c_socket.send(header.encode())
        s.c_socket.send(contenu)     
        print("{} {} {}".format(s.method,s.chemin,s.reponse['code']))






    