<img width="805" height="360" alt="image" src="https://github.com/user-attachments/assets/0b401f6f-6570-415a-9036-e65ef209b485" />Étape 1 : Vérifier l’installation de Docker
Instructions :
Ouvrez un terminal (PowerShell ou bash).
Vérifiez la version de Docker :
docker --version
Vérifiez que le démon Docker fonctionne :
docker ps

<img width="681" height="135" alt="image" src="https://github.com/user-attachments/assets/3a8cb435-a219-433a-a017-86d5fd2db6b3" />

Étape 2 : Lancer un serveur Nginx dans un conteneur
Instructions :
Lancez un conteneur Nginx en arrière-plan :
docker run -d -p 8080:80 --name demo-nginx nginx

<img width="724" height="309" alt="image" src="https://github.com/user-attachments/assets/685777c0-c762-4d3b-8177-651e3e44b293" />

Ouvrez un navigateur et accédez à :
http://localhost:8080
Vérifiez que la page par défaut de Nginx s’affiche.

<img width="1114" height="306" alt="image" src="https://github.com/user-attachments/assets/88021e97-c36f-4015-92e5-0e04dce42869" />

Listez les conteneurs en cours d’exécution :
docker ps

<img width="1089" height="122" alt="image" src="https://github.com/user-attachments/assets/50e17a30-2fc3-4c6d-9993-9bf9bc19a6e4" />

Arrêtez puis supprimez le conteneur :
docker stop demo-nginx
docker rm demo-nginx

<img width="397" height="106" alt="image" src="https://github.com/user-attachments/assets/0b7166fc-e8da-497c-9c6d-71a29a06239c" />


Étape 3 : Ouvrir un shell Linux isolé dans un conteneur
Instructions :
Lancez un conteneur Linux interactif (exemple avec ubuntu) :
docker run -it --name demo-ubuntu ubuntu bash

Dans le shell à l’intérieur du conteneur, exécutez quelques commandes :
ls
cat /etc/os-release
pwd

<img width="940" height="480" alt="image" src="https://github.com/user-attachments/assets/4fb5a8a3-2a13-4f91-8c7f-e244984748e8" />

Installez un paquet (exemple) :
apt-get update
apt-get install -y curl

<img width="999" height="579" alt="image" src="https://github.com/user-attachments/assets/b94a8ad7-7cae-446a-b7df-9ecd33f03b65" />


Quittez le shell :
exit
Vérifiez que le conteneur existe toujours mais est arrêté :
docker ps -a
Supprimez ce conteneur :
docker rm demo-ubuntu


<img width="1087" height="578" alt="image" src="https://github.com/user-attachments/assets/a8d6de76-4d48-4fb3-8ee6-0064c05ff269" />

Étape 4 : Comprendre la structure d’une commande docker run
Instructions :
Notez la structure générale :
docker run [options] image [commande] [arguments]
Lancez de nouveau Nginx avec des options clairement visibles :
docker run -d \
  --name demo-nginx \
  -p 8080:80 \
  nginx
Identifiez le rôle de chaque élément :
-d : détaché (arrière-plan)
--name demo-nginx : nom du conteneur
-p 8080:80 : port hôte 8080 → port conteneur 80
nginx : image utilisée
Arrêtez et supprimez encore une fois le conteneur :
docker stop demo-nginx
docker rm demo-nginx


<img width="1095" height="217" alt="image" src="https://github.com/user-attachments/assets/5cb05304-ad84-48a9-9106-2e7c1a879ed4" />



Étape 5 : Conteneuriser l’API churn du projet mlops-lab-01
Instructions :
Ouvrez un terminal.
Placez-vous dans le dossier du projet MLOps précédent :
cd mlops-lab-01
Vérifiez que l’arborescence contient au minimum :
mlops-lab-01/
 ├── data/
 ├── logs/
 ├── models/
 ├── registry/
 └── src/
Vérifiez que l’API fonctionne encore en local (optionnel mais recommandé) :
(.venv) python src/api.py  # ou: uvicorn src.api:app --reload

<img width="559" height="473" alt="image" src="https://github.com/user-attachments/assets/461b817d-e20b-412d-b92b-06914f08ba6c" />


tape 6 : Créer un fichier requirements.txt pour l’image Docker
Instructions :
Dans le dossier mlops-lab-01, créez un fichier requirements.txt.
Ajoutez le contenu suivant (version minimale) :
fastapi
uvicorn[standard]
pydantic
scikit-learn
pandas
numpy
joblib
Enregistrez le fichier.
Remarque : si tu as des libs supplémentaires dans ton lab (par ex. python-dotenv, loguru…), ajoute-les ici.

<img width="460" height="411" alt="image" src="https://github.com/user-attachments/assets/379bcd3d-f4ef-41d6-8881-c446cab8483f" />


Étape 7 : Créer un Dockerfile pour l’API churn
Instructions :
Dans le dossier mlops-lab-01, créez un fichier nommé :
Dockerfile
Collez le contenu suivant :
FROM python:3.10-slim

# 1) Préparer le dossier de travail dans le conteneur
WORKDIR /app

# 2) Copier les dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copier le reste du projet dans l'image
COPY . .

# 4) Exposer le port de l'API (8000 dans notre lab)
EXPOSE 8000

# 5) Commande de lancement de l'API FastAPI
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
Sauvegardez le fichier.

<img width="863" height="433" alt="image" src="https://github.com/user-attachments/assets/7eca6342-d44e-4c09-9210-a7a05ce12864" />

Étape 8 :Préparer un modèle actif avant de construire l’image
Instructions :
Assurez-vous qu’un modèle entraîné existe déjà dans models/ :
ls models
Assurez-vous que registry/current_model.txt contient bien le nom d’un modèle (une ligne du type) :
churn_model_v2_20251209_232031.joblib
Si le fichier est vide, relancez l’entraînement avec un gate acceptable :
(.venv) python -c "from src.train import main; main(version='v1', gate_f1=0.60)"
Vérifiez à nouveau le contenu de :
type registry/current_model.txt        # sous Windows
# ou
cat registry/current_model.txt         # sous Linux/macOS

<img width="699" height="426" alt="image" src="https://github.com/user-attachments/assets/14d35b36-3139-4920-999b-a3a063b913b5" />


Étape 9 : Construire l’image Docker du projet churn
Instructions :
Dans le dossier mlops-lab-01, construisez l’image :
docker build -t churn-api:latest .
Attendez la fin de la construction, vérifiez la présence de l’image :
docker images
Vous devez voir une ligne avec churn-api dans la colonne REPOSITORY.


<img width="1140" height="605" alt="image" src="https://github.com/user-attachments/assets/cff015d5-2a1d-4be0-9f45-b5ff9754259f" />

Étape 10 : Lancer l’API churn dans un conteneur
Instructions :
Lancez un conteneur basé sur l’image :
docker run -d \
  --name churn-api-demo \
  -p 8000:8000 \
  churn-api:latest
Vérifiez que le conteneur est en cours d’exécution :
docker ps

<img width="1128" height="122" alt="image" src="https://github.com/user-attachments/assets/01bfaab5-c55c-4e4a-883a-15eaacf8af8a" />

Testez le endpoint /health avec un client HTTP (Postman, curl, ou navigateur si tu as un GET simplifié) :
Exemple avec curl :
curl http://localhost:8000/health
Testez une requête POST /predict en envoyant un JSON conforme au lab (tenure, complaints, etc.).

<img width="1258" height="552" alt="image" src="https://github.com/user-attachments/assets/707861ec-a626-4b0b-8f9e-054e3fec37b6" />


<img width="1259" height="609" alt="image" src="https://github.com/user-attachments/assets/84398703-4cef-491b-801f-9bc7be28c580" />

<img width="1259" height="612" alt="image" src="https://github.com/user-attachments/assets/f1c7f8f2-f31b-4ea2-8cc3-9cc1d8a1a796" />

<img width="1253" height="599" alt="image" src="https://github.com/user-attachments/assets/57191e84-a7d3-4393-b6a1-db45b24d0f7c" />



Étape 11 : Vérifier les logs générés à l’intérieur du conteneur
Instructions :
Listez les fichiers dans le conteneur :
docker exec -it churn-api-demo ls
Vérifiez que l’application écrit des logs à l’exécution :
docker exec -it churn-api-demo ls logs
Affichez quelques lignes du fichier de logs des prédictions :
docker exec -it churn-api-demo head logs/predictions.log
Arrêtez et supprimez le conteneur une fois les tests terminés :
docker stop churn-api-demo
docker rm churn-api-demo


<img width="1139" height="287" alt="image" src="https://github.com/user-attachments/assets/331f8b6b-bff8-4d3e-9a2d-cf78ba5b460e" />


Étape 12 : Orchestration locale avec Docker Compose
Instructions :
Toujours dans le dossier mlops-lab-01, créez un fichier :
docker-compose.yml
Ajoutez le contenu suivant :
version: "3.9"

services:
  churn-api:
    build: .
    image: churn-api:latest
    container_name: churn-api-compose
    ports:
      - "8000:8000"
    environment:
      LOG_LEVEL: "info"
    # Optionnel : monter les logs sur l'hôte pour inspection
    volumes:
      - ./logs:/app/logs
Sauvegardez le fichier.

<img width="805" height="360" alt="image" src="https://github.com/user-attachments/assets/e5580f27-c43b-4fae-9c30-391b978b5a45" />



Étape 13 : Démarrer l’API via Docker Compose
Instructions :
Dans le dossier mlops-lab-01, lancez :
docker compose up
Observez dans le terminal :
la construction éventuelle de l’image
le démarrage du service churn-api
Ouvrez un deuxième terminal et testez :
curl http://localhost:8000/health
Envoyez quelques requêtes /predict comme dans le lab précédent.
Arrêtez tous les services (dans la fenêtre où tourne Compose) avec :
Ctrl + C


<img width="1179" height="556" alt="image" src="https://github.com/user-attachments/assets/d18bd39e-170b-48fa-b680-d67a4ff4decd" />


Étape 14 : lancer les services en arrière-plan et observer les logs
Instructions :
Lancez les services en mode détaché :
docker compose up -d
Vérifiez les conteneurs en cours d’exécution :
docker ps
Affichez les logs du service :
docker compose logs -f churn-api
Testez /health et /predict pendant que les logs défilent.
Arrêtez les services :
docker compose down



<img width="1139" height="547" alt="image" src="https://github.com/user-attachments/assets/21684e0e-eba3-4716-9c96-e63692122a8c" />


<img width="1131" height="572" alt="image" src="https://github.com/user-attachments/assets/6336db3d-0adc-4f2a-806b-6358cca0f8cb" />



Étape 15 : lier Docker Compose au reste du cours (Git + DVC)
Instructions :
Assurez-vous que :
le projet mlops-lab-01 est versionné avec Git (lab Git),
les données et modèles lourds sont suivis par DVC (lab DVC),
l’API est conteneurisée via Docker (lab Docker).
Ajoutez au minimum les fichiers suivants dans Git :
git add Dockerfile docker-compose.yml requirements.txt
git commit -m "feat: ajout conteneurisation Docker de l'API churn"
Notez dans ton cours que l’on a maintenant :
MLOps local : pipeline + API + monitoring
Git : versionnement du code et de la structure
DVC : versionnement des données / modèles (lab suivant)
Docker / Compose : déploiement reproductible de l’API



<img width="847" height="152" alt="image" src="https://github.com/user-attachments/assets/4d88d33f-c10c-4b46-9716-6f8d5dacea12" />












