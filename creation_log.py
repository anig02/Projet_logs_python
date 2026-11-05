import random as rd 
import datetime

#Préparation du fichier log 

  #Création dictionnaire 
data_log = {
    # evenement = (niveau, message) : chaque message va avec un niveau cohérent
    'evenement': [('INFO', 'Connexion reussie'), ('INFO', 'Page consultee'),
                  ('WARNING', 'Disque presque plein'), ('WARNING', 'Reponse lente'),
                  ('ERROR', 'Mot de passe incorrect'), ('ERROR', 'Page introuvable'),
                  ('CRITICAL', 'Serveur arrete'), ('CRITICAL', 'Acces refuse')],
    'ip': ['192.168.0.14', '192.168.0.37', '10.12.4.101', '84.203.17.92',
           '151.6.240.33', '37.165.88.9', '91.68.112.250'],
    'utilisateur': ['user01', 'user02', 'user03', 'user04'],
    # porte = (port, protocole) : par où on entre dans le serveur
    # (22 = contrôler la machine, 80/443 = visiter le site)
    'porte': [(22, 'SSH'), (80, 'HTTP'), (443, 'HTTPS')],
}



# On pioche au hasard une valuer pour chque clé de notre dictionnaire 
'''niveau = rd.choice(data_log['niveau'])
ip = rd.choice(data_log['ip'])
utilisateur = rd.choice(data_log['utilisateur'])
message = rd.choice(data_log['message'])
porte = rd.choice(data_log['porte'])
port, protocole = porte'''

'''print('niveau',niveau)
print('ip',ip)
print('utilisateur',utilisateur)
print('message',message)
print('port',port)
print('protocole',protocole)'''

    # on crée les lignes de notre 'base de donnée'
#date= datetime.datetime(2026,10,10,11,30,0) # date plus heure

'''print(date)
ligne= f" {date} | {niveau} | {ip} | {utilisateur} | {message} | {port}| {protocole} "
print(ligne)'''


# Fonction pour cré l'attaque 
def crea_attaque(fichier, date):
    
    ip_pirate = f'{rd.randint(1, 254)}.{rd.randint(1, 254)}.{rd.randint(1, 254)}.{rd.randint(1, 254)}'
    cible = rd.choice(data_log['utilisateur'])
    nb_tentatives = rd.randint(5, 8)

    for i in range(nb_tentatives):
        ecart = datetime.timedelta(seconds=rd.randint(1, 3))
        date = date + ecart
        ligne = f"{date} | ERROR | {ip_pirate} | {cible} | Mot de passe incorrect | 22 | SSH"
        fichier.write(ligne + '\n')
    return date


  #Création des fichiers 

def creation_fichier(nom_fichier,date,N): #N nombre de fichier attendue 

  for k in range(N):
     
    with open(f'logs/{nom_fichier}{k+1}.txt', 'w',encoding='utf-8') as fichier: #encoding= garantit que les accents (é, à, ç…) s’enregistrent et se relisent correctement sur n’importe quel ordinateur.
        position_attaque = rd.randint(0, 99) 

        for i in range(100):
            
            n=rd.randint(1,60)
            ecart= datetime.timedelta(minutes=n)
            date= date+ecart

            evenement = rd.choice(data_log['evenement'])
            niveau, message = evenement 
            ip = rd.choice(data_log['ip'])
            utilisateur = rd.choice(data_log['utilisateur'])
            porte = rd.choice(data_log['porte'])
            port, protocole = porte

            ligne= f"{date} | {niveau} | {ip} | {utilisateur} | {message} | {port} | {protocole}"
            fichier.write(ligne + '\n')
            
            if rd.randint(1, 20) == 1:
                fichier.write('\n') #ligne vide pour module 2 
            if rd.randint(1, 15) == 1:
                ligne= f"{date} | {niveau} |  | {utilisateur} | {message} | {port} | {protocole}" #ligne dans ip pour module2
                fichier.write(ligne + '\n')

            if i == position_attaque: 
                  date = crea_attaque(fichier, date)                


  

#test creation_fichier('logs_jour', datetime.datetime(2026, 10, 12, 8, 0, 0), 4)
   

# Environnement virtuel (à faire une seule fois) :
#   python -m venv venv                -> crée l'environnement isolé du projet
#   venv\Scripts\activate              -> l'active ("(venv)" s'affiche dans le terminal)
#   Si erreur de sécurité Windows :
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# Puis dans VS Code : Python: Select Interpreter -> choisir "venv"


