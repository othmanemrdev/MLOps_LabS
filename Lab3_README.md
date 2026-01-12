Lab3 : Versionnement des données et pipelines ML avec DVC

Étape 1 : Initialisation de DVC dans le projet
Instructions :
Ouvre un terminal dans le dossier du projet :
cd mlops-lab-01

Lance l’initialisation de DVC :
dvc init

<img width="547" height="378" alt="Screenshot 2025-12-27 100649" src="https://github.com/user-attachments/assets/13bd0e3e-7b0e-4d44-ab45-9f978f54bd82" />

Vérifie les fichiers créés :
.dvc/
.dvc/config


<img width="297" height="238" alt="Screenshot 2025-12-27 100704" src="https://github.com/user-attachments/assets/f704d199-f7cc-4008-b691-b0da629d59c1" />


Résultat attendu :
Un projet intégrant Git + DVC, prêt à suivre des fichiers volumineux.


Étape 2 : Versionner les données brutes avec DVC
Instructions :
Supprimer  data/  de votre .gitignore 
Nous allons versionner le fichier généré dans le lab précédent :
data/raw.csv
Instructions :
Ajoute le dataset au suivi DVC :
dvc add data/raw.csv

<img width="537" height="65" alt="Screenshot 2025-12-27 100823" src="https://github.com/user-attachments/assets/f44f0197-4e82-4edb-8272-49d710cf6dfe" />

Cette commande crée automatiquement :
data/raw.csv.dvc
data/.gitignore
Ajoute au versionnement Git :
git add data/raw.csv.dvc data/.gitignore .gitignore
git commit -m "data: suivi du dataset brut via DVC"

<img width="1319" height="666" alt="Screenshot 2025-12-27 101330" src="https://github.com/user-attachments/assets/8b64ad32-009f-4a25-a299-7e5ae304b128" />


Résultat attendu :
data/raw.csv n’est plus suivi par Git
seul raw.csv.dvc est versionné
Git reste léger, DVC gère les gros fichiers


Étape 3 : Configuration d’un remote DVC
Instructions :
Crée un dossier de remote :
mkdir dvc_storage

<img width="524" height="204" alt="Screenshot 2025-12-27 101447" src="https://github.com/user-attachments/assets/36ebc594-7e00-4f8e-a830-39d8f6148739" />


Déclare-le comme remote principal :
dvc remote add -d localremote dvc_storage
# dvc remote add -d storage s3://mybucket/dvcstore cas de cloud storage
Versionne la config :
git add .dvc/config
git commit -m "dvc: configuration du remote local"


<img width="775" height="119" alt="Screenshot 2025-12-27 101536" src="https://github.com/user-attachments/assets/007bb828-4913-4255-8da6-8ab0e939cbb5" />




Étape 4 : Push des données dans le remote DVC
Instructions :
Envoie les données :
dvc push

<img width="463" height="89" alt="Screenshot 2025-12-27 101610" src="https://github.com/user-attachments/assets/73ecb82c-dbec-409c-8abd-74ab9faf1d36" />


Vérifie que le dossier dvc_storage/ contient des fichiers de hash.
Résultat attendu :
La donnée est désormais partagée et récupérable par n’importe quel étudiant via DVC.

<img width="372" height="112" alt="Screenshot 2025-12-27 101615" src="https://github.com/user-attachments/assets/0054adc1-abf6-4f8e-9a0d-567809a4eb69" />


Étape 5 : imulation d’une collaboration : supprimer localement et récupérer depuis DVC
Instructions :
Supprime le dataset local :
del data\raw.csv   # Windows
# ou
rm data/raw.csv    # Linux/Mac
Vérifie qu’il n’y a plus rien :
ls data/
Récupère le dataset via DVC :
dvc pull
Résultat attendu :
Le fichier data/raw.csv réapparaît identique à l’original → preuve que DVC fonctionne.


<img width="598" height="604" alt="Screenshot 2025-12-27 101711" src="https://github.com/user-attachments/assets/bca95975-a490-4aa3-9742-881245bad670" />


Étape 6 : Création d’un pipeline reproductible dvc.yaml
Instructions :
Crée un pipeline :
dvc stage add -n prepare `
  -d src/prepare_data.py `
  -d data/raw.csv `
  -o data/processed.csv `
  -o registry/train_stats.json `
  python src/prepare_data.py
Ajoute l'étape d’entraînement :
dvc stage add -n train  `
  -d src/train.py -d data/processed.csv  `
  -o models/model.joblib  `
  python src/train.py
   4. Evaluation du model :
dvc stage add -n evaluate `
  -d src/evaluate.py `
  -d models/model.joblib `
  -d data/processed.csv `
  -o reports/metrics.json `
  python src/evaluate.py
Versionne :
git add dvc.yaml registry/.gitignore reports/.gitignore
git commit -m "pipeline: ajout des étapes prepare/train/evaluate"
Résultat attendu :
DVC a enregistré dans dvc.yaml :
les dépendances
les sorties
les commandes du pipeline


<img width="993" height="566" alt="Screenshot 2025-12-27 104132" src="https://github.com/user-attachments/assets/045a8094-6618-4422-a7aa-452ec87281fe" />



<img width="998" height="177" alt="Screenshot 2025-12-27 104214" src="https://github.com/user-attachments/assets/2f96ee04-474c-48e3-b8be-3080c09912e6" />



<img width="599" height="479" alt="Screenshot 2025-12-27 110911" src="https://github.com/user-attachments/assets/5c4e135f-d939-46b2-b7b8-361402b2f7f4" />


<img width="1008" height="395" alt="Screenshot 2025-12-27 110939" src="https://github.com/user-attachments/assets/91f210c5-8377-4d1d-8503-a78744d4efc1" />



Étape 7 : Reproduire automatiquement tout le pipeline
Instructions :
Modifie par exemple src/prepare_data.py
(Ajouter un print, changer un seuil…)
Vérifie l’impact :
dvc repro
Versionne :
git add dvc.lock
git commit -m "pipeline: lock after repro"
Résultat attendu :
Seules les étapes impactées sont réexécutées → reproductibilité totale.



<img width="910" height="576" alt="Screenshot 2025-12-27 113351" src="https://github.com/user-attachments/assets/55d40e1a-a2ea-4479-85b4-ae8629956b2c" />


