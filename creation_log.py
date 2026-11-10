import random as rd 
import datetime

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
    'ip_pirates': ['35.246.233.229', '45.33.32.156', '103.21.244.8',
               '185.220.101.4', '198.51.100.23', '203.0.113.77'],
}


# Fonction pour cré l'attaque 
def crea_attaque(fichier, date):
    
    ip_pirate = rd.choice(data_log['ip_pirates'])
    cible = rd.choice(data_log['utilisateur'])
    nb_tentatives = rd.randint(5, 8)

    for i in range(nb_tentatives):
        ecart = datetime.timedelta(seconds=rd.randint(1, 3))
        date = date + ecart
        ligne = f"{date} | ERROR | {ip_pirate} | {cible} | Mot de passe incorrect | 22 | SSH"
        fichier.write(ligne + '\n')
    return date


  #Création des fichiers 

def creation_fichier(nom_fichier,date): #N nombre de fichier attendue 
    with open(f'logs/{nom_fichier}.txt', 'w',encoding='utf-8') as fichier: #encoding= garantit que les accents (é, à, ç…) s’enregistrent et se relisent correctement sur n’importe quel ordinateur.
          
         
         for i in range(1_000_000):
                
                n=rd.randint(1,60)
                ecart= datetime.timedelta(seconds=n)
                date= date+ecart

                evenement = rd.choice(data_log['evenement'])
                niveau, message = evenement 
                ip = rd.choice(data_log['ip'])
                utilisateur = rd.choice(data_log['utilisateur'])
                porte = rd.choice(data_log['porte'])
                port, protocole = porte

                if rd.randint(1, 20) == 1:
                     niveau = niveau.lower()           
                     utilisateur = utilisateur.upper() 

                ligne= f"{date} | {niveau} | {ip} | {utilisateur} | {message} | {port} | {protocole}"

                if rd.randint(1, 100) == 1:
                    ligne = ligne[:rd.randint(10, 40)]  # ligne coupée pour tester le filtre lambda
                                    
                fichier.write(ligne + '\n')

               
                
                if rd.randint(1, 20) == 1:
                    fichier.write('\n') #ligne vide pour module 2 

                if rd.randint(1, 1000) == 1:
                     date = crea_attaque(fichier, date)               


  

creation_fichier('logs_jour', datetime.datetime(2026, 10, 12, 8, 0, 0))



