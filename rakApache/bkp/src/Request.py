import urllib.parse
import subprocess
import os
import MaintienClient
import mimetypes



# Reponse au requete des clients 

#       Liste de fichier au cas ou un repertoire est choisit et qu il n'y a pas de fichier index dans ce repertoire

def listeFile(chemin:str):
    retour="<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n"
    filename=chemin.split("/")[-1]
    
    if filename:
        retour+="<h1>Repertoire "+filename+"</h1>\n"
    else :
        retour+="<h1>Repertoire /</h1>\n"
    retour+="<h3>Voici la liste des fichiers </h3>"
    contenu = os.listdir(chemin)
    for i in contenu:
        retour+='<a href="'+i+'">'+i+'</a><br>\n'
    retour+="</body>\n</html>\n"    
    return retour

#       prends les parametres dans l'url en cas de get

def getParmGet(path):
    tapaka=path.split("?")
    if len(tapaka)<2:
        return 
    else :
        return urllib.parse.parse_qs(tapaka[1])

#       lecture de fichier si c'est un ".html" ou un ".php"

def readFile(path,param=None):
    parm=getParmGet(path)
    file_name=path.split("?")[0]

    #       s'il n'y a pas de paramtre deriere "?"
    
    if parm==None:
        #       get sans parametre
        if param==None:
            #       j'utilise juste l'interpreteur php meme si c'est un ".html"
            prompt="php {file}".format(file=file_name)
            result = subprocess.run(prompt, capture_output= True ,text=True,check=True,shell=True )
            return result.stdout
        #       post 
        else :
            query=param
            #       je cree un script a interpreter
            #           parse_str assigne les parametre en un tableau cle valeur dans 
            prompt="php -r \"parse_str('{query}',\\$_POST); include '{file}';\"".format(query=query,file=file_name)
            result = subprocess.run(prompt , capture_output= True ,text=True , shell=True ,check=True)
            return result.stdout
    #       s'il y a des parametre deriere "?"
    #       get avec paramtre
    else :  
        query=urllib.parse.urlparse(path).query
            #       je fais la meme chose que post mais j'utilise un variable $_GET
        prompt="php -r \" parse_str('{query}',\\$_GET); include '{file}';\"".format(query=query,file=file_name)
        result = subprocess.run(prompt, capture_output= True ,text=True,check=True,shell=True )
        return result.stdout

#       pour avoir les content type des fichiers
def getContentType(path):
    ct,ecd=mimetypes.guess_type(path)
    if ct is None:
        if path.endswith(".php"):
            return "text/html"
        elif path.endswith(".html"):
            return "text/html"  
    return ct

#       la classe qui renvoi les requetes des clients
class Lecteur:
    def __init__(s,mc,path):
#           la classe maintien client qui prend le client et son requete
        s.mc=mc
#           pour les respecter le chemin pour mettre les projets
        s.path=path+s.mc.chemin
#           utilisation des methodes get ou  post
        if (s.mc.method=="GET"):
            s.do_GET()  
        if (s.mc.method=="POST"):
            s.do_POST()

#           envoie d'un reponse
    def send_response(s,code:int,message:str="OK"):
        s.mc.send_response(code,message)
#           envoie d'une nouvelle entete 
    def send_header(s,titre:str, contenu:str):
        s.mc.send_header(titre,contenu)
#           mise en place de 2 "\r\n" pour terminer l'entete
    def end_headers(s):
        s.mc.end_headers


#           traitement de la methode get
    def do_GET(s):
        #       redirection au cas ou repertoire le izy 
        if s.path.endswith("/") or os.path.isdir(s.path):
        #           si il y a un fichier qui index il le redirige vers ce fichier
            if (os.path.exists(s.path+"index.php") or os.path.exists(s.path+"index.html") or os.path.exists(s.path+"/index.php") or os.path.exists(s.path+"/index.html")):
                if os.path.exists(s.path+"index.php"):
                    s.path+="index.php"
                elif os.path.exists(s.path+"/index.php"):
                    s.path+="/index.php"
                elif os.path.exists(s.path+"/index.html"):
                    s.path+="/index.html"
                else :
                    s.path+="index.html"
        #           si il n'y a pas de fichier index , il liste les fichier dans le repertoire
            else :
                content=listeFile(s.path)
                s.send_response(200)
                s.send_header("Content-Type" , "text/html")
                s.end_headers()
                s.mc.write(content.encode())
                directory=True
        #       si le fichier existe
        if os.path.exists(s.path.split("?")[0] ) and not os.path.isdir(s.path):
        #           si c'est un fichier en ".php"
            if s.path.split("?")[0].endswith(".php") :
                #       lecture du fichier 
                content=readFile(s.path)
                #       envoi de la reponse
                s.send_response(200)
                #       envoi du type
                s.send_header("Content-Type" , "text/html")
                s.end_headers()
                #       ecriture de la reponse de la requete 
                s.mc.write(content.encode())
        #           autre extension du fichier
            else :
                #       lecture du fichier
                with open(s.path.split("?")[0],"rb") as fichier:
                    content=fichier.read() 
                #   comme celui d'en haut
                s.send_response(200)
                s.send_header("Content-Type" , getContentType(s.path.split("?")[0]))
                s.end_headers()
                s.mc.write(content)
        #       si le fichier n'existe pas
        else :
            s.send_error(404,"No Such File")
    
    def do_POST(s):
        #   test d'existance de fichier sinon erreur 404
        if os.path.exists(s.path.split("?")[0]):
            if s.path.split("?")[0].endswith(".php") or s.path.split("?")[0].endswith(".html"):
        #       prise des parametre envoyer dans le body
                post = s.mc.value
        #       comme get sauf les argument qui son envoyer
                content=readFile(s.path,str(post))
                s.send_response(200)
                s.send_header("Content-Type" , "text/html")
                s.end_headers()
                s.mc.write(content.encode())

        else :
            s.send_error(404,"No Such File")

#       envoie des erreurs
    def send_error(s,code,message=None):
        
        if code ==404:
            s.send_response(404 )
            s.send_header("Content-type" , "text/html")
            s.end_headers()
            s.mc.write(b"<h1>404 Not Found</h1><h3>Ce fichier n'existe pas </h3><p>Veuillez verifier l'existance du fichier</p>")
        elif code==500:
            s.send_response(500)
            s.send_header("Content-type" , "text/html")
            s.end_headers()
            message="<h1>500 Internal Server Error</h1><h3>{message}</h3>".format(message=message)
            s.mc.write(message.encode())
        
            