Lab 6 : Déploiement K8s d’un système MLOps Churn


Étape 1 : Préparer l’environnement Kubernetes
Instructions :
Démarrer Minikube (driver Docker) :
minikube start --driver=docker --kubernetes-version=v1.28.3

<img width="946" height="474" alt="image" src="https://github.com/user-attachments/assets/2a40ab7c-40b5-49af-a9a9-cead1e8edab6" />

Créer un namespace dédié au lab :
kubectl create namespace churn-mlops
Basculer le contexte courant sur ce namespace :
kubectl config set-context --current --namespace=churn-mlops

<img width="818" height="73" alt="image" src="https://github.com/user-attachments/assets/baf5f38f-beb5-4d84-95b3-b55ecb95d1ec" />

Vérifier :
kubectl get ns
kubectl get pods

<img width="538" height="175" alt="image" src="https://github.com/user-attachments/assets/8619d198-13db-4f35-ba47-31e18cfd3f23" />


Étape 2 : Préparer l’image Docker de l’API churn
Instructions :
Préparer l’environnement Python
Python 3.12 obligatoire
Vérifier la version de Python :
python --version
 La version doit être Python 3.12.x
(Si plusieurs versions sont installées, Python 3.12 doit être disponible.)
Si la version de Python utilisée par votre environnement virtuel n’est pas Python 3.12.x, supprimez l’environnement virtuel et recréez-le avec Python 3.12.
Créer un environnement virtuel avec Python 3.12
Windows / PowerShell :
py -3.12 -m venv venv_mlops
.\venv_mlops\Scripts\activate
Mettre pip à jour :
python -m pip install --upgrade pip
Préciser les dépendances dans requirements.txt
(afin d’éviter toute incompatibilité entre entraînement et prédiction)
Créer ou éditer le fichier requirements.txt et y mettre :
fastapi            # Framework web rapide pour créer des APIs Python
uvicorn[standard]  # Serveur ASGI pour exécuter FastAPI
pydantic           # Validation et typage des données
scikit-learn==1.7.2 # Entraînement et inférence des modèles ML
pandas==2.2.3      # Manipulation de données tabulaires
numpy==2.1.3       # Calcul numérique
joblib==1.4.2      # Sérialisation et chargement des modèles
Installer les dépendances :
pip install -r requirements.txt
 Cette étape est obligatoire pour :
éviter les erreurs de compatibilité scikit-learn,
garantir que le modèle chargé par l’API correspond exactement aux versions installées.


<img width="1141" height="620" alt="image" src="https://github.com/user-attachments/assets/9644a50c-452b-45a8-bbdf-3f25ec27096a" />

Étape 3 : Créer le dossier des manifests Kubernetes
Instructions :
Sous PowerShell :
New-Item -ItemType Directory -Name k8s

<img width="765" height="176" alt="image" src="https://github.com/user-attachments/assets/1e10ab90-1b56-4ea0-99a8-3ed78c47bd4d" />

Sous Ubuntu:
mkdir k8s
Vérifier :
Get-ChildItem
ls -ll
Tu dois voir :
mlops-lab-01/
 ├── src/
 ├── data/
 ├── models/
 ├── logs/
 ├── registry/
 ├── k8s/
 └── ...


 <img width="600" height="524" alt="image" src="https://github.com/user-attachments/assets/8934abae-cb20-4f81-b66f-de1fbd081e44" />


Étape 4 : Construire l’image Docker (tag versionné)
Instructions :
Se placer dans le dossier du projet :
cd ./mlops-lab-01
Construire l’image Docker avec un tag versionné (jamais latest) :
# Construire l’image du projet avec un tag de version (v1, v2, ...)
docker build -t churn-api:v1 .


<img width="1141" height="428" alt="image" src="https://github.com/user-attachments/assets/fb21f361-3b52-41cb-bb9b-f298049f2982" />

Vérifier l’image localement :
# Linux/Unix
docker images | grep churn-api
# PowerShell
docker images | Select-String churn-api

<img width="780" height="128" alt="image" src="https://github.com/user-attachments/assets/56c9f496-4d9e-4d67-9d70-5fcef738614c" />

Étape 5 : Charger explicitement l’image dans Minikube
Instructions :
Sauvegarder l’image Docker :
docker save churn-api:v1 -o churn-api_v1.tar
Charger l’image dans Minikube :
minikube image load churn-api_v1.tar
Vérifier que l’image est disponible dans Minikube :
#Unix
minikube image ls | grep churn-api
# PowerShell
minikube image ls | Select-String churn-api

<img width="813" height="263" alt="image" src="https://github.com/user-attachments/assets/05c438c6-affe-4cd0-979d-1b19f4306118" />

Étape 6 : Deployment Kubernetes pour l’API churn
Instructions :
Créer le fichier :
#Powershell
New-Item -ItemType Directory k8s
New-Item k8s/deployment.yaml
#Unix/Lunix
mkdir -p k8s
touch k8s/deployment.yaml

<img width="853" height="363" alt="image" src="https://github.com/user-attachments/assets/3f38d7a9-87f0-4382-a843-cd08cf5b7f1e" />

Coller le contenu suivant dans k8s/deployment.yaml :
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: churn-api
  template:
    metadata:
      labels:
        app: churn-api
    spec:
      containers:
        - name: api
          image: churn-api:v1 # v1 presente le tag de l'image cible
          ports:
            - containerPort: 8000

<img width="614" height="441" alt="image" src="https://github.com/user-attachments/assets/1e00fc8b-c2ec-4e41-9c67-4a19bb4e2c4d" />

Appliquer le manifest :
kubectl apply -f k8s/deployment.yaml
Suivre le rollout :
kubectl rollout status deployment churn-api
Vérifier :
kubectl get pods -l app=churn-api -o wide

<img width="873" height="167" alt="image" src="https://github.com/user-attachments/assets/be7f968c-b57a-479b-ad4d-699ebb1f4249" />

Étape 7 : Exposer l’API via un Service NodePort
Instructions :
Créer le fichier :
New-Item k8s/service.yaml
Ubuntu
touch k8s/service.yaml
Coller le contenu suivant dans k8s/service.yaml :
apiVersion: v1
kind: Service
metadata:
  name: churn-api-service
spec:
  type: NodePort
  selector:
    app: churn-api
  ports:
    - port: 80
      targetPort: 8000
      nodePort: 30080

<img width="865" height="665" alt="image" src="https://github.com/user-attachments/assets/4583c579-e0c6-422f-8826-97adee8256f8" />

Appliquer :
kubectl apply -f k8s/service.yaml
Visualiser la création du Service :
kubectl get svc churn-api-service
Afficher les détails du Service :
kubectl describe svc churn-api-service
Ouvrir l’accès à la communication avec le cluster (Windows / Minikube driver Docker) :
kubectl port-forward svc/churn-api-service 30080:80

<img width="857" height="517" alt="image" src="https://github.com/user-attachments/assets/6dc13c77-6b67-473a-a043-60d6c24e0dd4" />


Tester l’API, via Postman :
POST http://127.0.0.1:30080/predict
{
  "tenure_months": 48,
  "num_complaints": 0,
  "avg_session_minutes": 60,
  "plan_type": "premium",
  "region": "EU",
  "request_id": "req-safe"
}

<img width="1304" height="683" alt="image" src="https://github.com/user-attachments/assets/8c2b2840-0410-4e3b-916a-94a7e8c1268f" />


<img width="1255" height="586" alt="image" src="https://github.com/user-attachments/assets/955042d3-d546-4e68-8b73-e83de6081f93" />

Étape 8 : Injecter la configuration MLOps via ConfigMap
Instructions :
Créer :
New-Item k8s/configmap.yaml
Ubuntu
touch k8s/configmap.yaml
Coller :
apiVersion: v1
kind: ConfigMap
metadata:
  name: churn-config
data:
  MODEL_NAME: "churn_model_v1"
  LOG_LEVEL: "info"

<img width="863" height="491" alt="image" src="https://github.com/user-attachments/assets/8e5502af-ca71-4bb1-a3cc-970c24d5fdd1" />

Appliquer :
kubectl apply -f k8s/configmap.yaml
Visualiser la création du ConfigMap :
kubectl get configmap churn-config
Afficher le contenu du ConfigMap :
kubectl describe configmap churn-config
Modifier k8s/deployment.yaml pour injecter ces variables dans le conteneur :
Dans la section containers: - name: api, ajouter :
env:
  - name: MODEL_NAME
    valueFrom:
      configMapKeyRef:
        name: churn-config
        key: MODEL_NAME
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: churn-config
        key: LOG_LEVEL

<img width="378" height="668" alt="image" src="https://github.com/user-attachments/assets/fdb0aa86-4106-47b9-8be0-930f6fd2eddd" />

Réappliquer le Deployment :
kubectl apply -f k8s/deployment.yaml
Suivre le rollout :
kubectl rollout restart deployment churn-api
kubectl rollout status deployment churn-api
Vérifier que les variables sont bien injectées dans un Pod :
kubectl exec -it deploy/churn-api -- printenv MODEL_NAME
kubectl exec -it deploy/churn-api -- printenv LOG_LEVEL

<img width="897" height="207" alt="image" src="https://github.com/user-attachments/assets/0e41e5ba-cfb7-473f-9190-be271db67d81" />

Étape 9 : Gérer les secrets (MONITORING_TOKEN)
Instructions :
Encoder une valeur simple en base64 (exemple "abc123") :
Depuis PowerShell :
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("abc123"))
Ubuntu
echo -n "abc123" | base64
Garder la valeur obtenue, par ex : YWJjMTIz
Créer le fichier :
New-Item k8s/secret.yaml
Ubuntu
touch k8s/secret.yaml
Coller :
apiVersion: v1
kind: Secret
metadata:
  name: churn-secret
type: Opaque
data:
  MONITORING_TOKEN: "YWJjMTIz"

<img width="1131" height="510" alt="image" src="https://github.com/user-attachments/assets/c91b34e3-2502-4a8e-bb53-dc2179dc2032" />

Appliquer :
kubectl apply -f k8s/secret.yaml
Visualiser la création du Secret :
kubectl get secret churn-secret
Afficher les détails (sans afficher les valeurs en clair) :
kubectl describe secret churn-secret

<img width="792" height="295" alt="image" src="https://github.com/user-attachments/assets/6066243e-474a-476c-8dbc-909d30e4eab9" />

Ajouter la variable d’environnement dans k8s/deployment.yaml (dans env: déjà présent) :
- name: MONITORING_TOKEN
  valueFrom:
    secretKeyRef:
      name: churn-secret
      key: MONITORING_TOKEN

<img width="664" height="557" alt="image" src="https://github.com/user-attachments/assets/403e3e18-7427-40b3-9e8a-45d535aa7069" />

Réappliquer :
kubectl apply -f k8s/deployment.yaml
Vérifier le redémarrage et l’état des Pods :
kubectl get pods
Vérifier que la variable d’environnement est bien injectée dans un Pod :
kubectl exec -it deploy/churn-api -- printenv MONITORING_TOKEN

<img width="930" height="189" alt="image" src="https://github.com/user-attachments/assets/b33e800b-af44-43b4-85f9-bca261724243" />

Étape 10 : Mise en place des endpoints de santé et des probes Kubernetes pour l’API Churn
Instructions :
Ajouter les endpoints nécessaires aux probes Kubernetes dans l’API.
Ouvrir le fichier contenant la définition de l’API FastAPI (par exemple src/api.py).
Ajouter les endpoints suivants :
@app.get("/health")
def health() -> dict[str, Any]:
    """
    Endpoint de santé de l'API.


    Vérifie simplement qu'un modèle courant est bien configuré.


    Retour
    ------
    dict
        - status : "ok" ou "error"
        - current_model : nom du modèle courant (si OK)
        - detail : message d'erreur (si error)
    """
    try:
        model_name = get_current_model_name()
        return {"status": "ok", "current_model": model_name}
    except Exception as exc:  # pragma: no cover - simple endpoint de debug
        return {"status": "error", "detail": str(exc)}

@app.get("/startup")
def startup() -> dict[str, Any]:
    """
    Endpoint utilisé par Kubernetes startupProbe.

    L'application est considérée comme démarrée UNIQUEMENT si :
    - le registry existe,
    - le fichier current_model.txt existe,
    - le fichier n'est pas vide.
    """
    if not REGISTRY_DIR.exists():
        raise HTTPException(
            status_code=503,
            detail="Registry non monté (PVC absent ou incorrect).",
        )

    if not CURRENT_MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Aucun modèle courant. Lancer train.py (avec gate) d'abord.",
        )

    name = CURRENT_MODEL_PATH.read_text(encoding="utf-8").strip()
    if not name:
        raise HTTPException(
            status_code=503,
            detail="current_model.txt vide.",
        )

    return {
        "status": "ok",
        "current_model": name,
    }


@app.get("/ready")
def ready() -> dict[str, Any]:
    try:
        model_name = get_current_model_name()
        return {"status": "ready", "current_model": model_name}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))


<img width="820" height="620" alt="image" src="https://github.com/user-attachments/assets/51eae14b-9632-480a-ad77-a4daf4b986ad" />

<img width="751" height="484" alt="image" src="https://github.com/user-attachments/assets/ce47b934-7828-4989-b988-165fe3bd104b" />

  <img width="601" height="616" alt="image" src="https://github.com/user-attachments/assets/3cb9814d-098f-4209-a1f3-dbdc4dfacf08" />

Sauvegarder le fichier.
Reconstruire l’image Docker de l’API :
docker build -t churn-api:v1 .
Exporter l’image Docker :
docker save churn-api:v1 -o churn-api_v1.tar
Charger l’image dans Minikube :
minikube image load churn-api_v1.tar

<img width="891" height="451" alt="image" src="https://github.com/user-attachments/assets/039cec6b-cd80-4f96-bbd3-0e9d33585387" />

Étape 11 : Ajouter les probes (liveness / readiness / startup)
Instructions :
Dans k8s/deployment.yaml, compléter le conteneur :
- name: api
  image: churn-api:v1
  ports:
    - containerPort: 8000
  env:
    - name: MODEL_NAME
      valueFrom:
        configMapKeyRef:
          name: churn-config
          key: MODEL_NAME

    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: churn-config
          key: LOG_LEVEL

    - name: MONITORING_TOKEN
      valueFrom:
        secretKeyRef:
          name: churn-secret
          key: MONITORING_TOKEN

  livenessProbe:
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 10
    periodSeconds: 30

  readinessProbe:
    httpGet:
      path: /ready
      port: 8000
    initialDelaySeconds: 5
    periodSeconds: 10

  startupProbe:
    httpGet:
      path: /startup
      port: 8000
    failureThreshold: 30
    periodSeconds: 5
  
<img width="560" height="652" alt="image" src="https://github.com/user-attachments/assets/5de1fd1c-305f-4815-ad2f-fe959397be06" />

  Réappliquer :
kubectl apply -f k8s/deployment.yaml
kubectl describe pod -l app=churn-api

<img width="872" height="619" alt="image" src="https://github.com/user-attachments/assets/b905237c-927c-43ea-ba46-e9bb2a1b0cfd" />

Redéployer l’application dans le cluster Kubernetes :
kubectl rollout restart deployment churn-api
kubectl rollout status deployment churn-api
Vérifier l’état des Pods :
kubectl get pods
Objectif :
Kubernetes redémarre un Pod si /health ne répond plus,
et n’envoie du trafic qu’aux Pods ready.

<img width="903" height="630" alt="image" src="https://github.com/user-attachments/assets/c8b04bd7-b56d-4a11-bc79-716f0bc2666d" />

Étape 12 : Volume persistant pour registry + logs
Instructions :
Créer le PVC (PersistentVolumeClaim) : ce volume persistant permet de conserver les fichiers du modèle et des logs même si les Pods sont recréés.
Créer le fichier :
New-Item k8s/pvc.yaml
Ubuntu
touch k8s/pvc.yaml
Coller :
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: churn-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi

<img width="809" height="526" alt="image" src="https://github.com/user-attachments/assets/a196df09-36ed-4465-9804-c4a04a845755" />

Appliquer :
kubectl apply -f k8s/pvc.yaml
Vérifier que le PVC est bien créé et associé à un volume :
kubectl get pvc
Créer et exécuter le Job d’entraînement : ce Job initialise le contenu du PVC en entraînant un premier modèle et en écrivant les artefacts dans /app/registry.
Créer le fichier :
New-Item k8s/job-train.yaml
Ubuntu
touch k8s/job-train.yaml
Coller :
apiVersion: batch/v1
kind: Job
metadata:
  name: churn-train
spec:
  backoffLimit: 1
  template:
    spec:
      restartPolicy: Never
      volumes:
        - name: churn-volume
          persistentVolumeClaim:
            claimName: churn-storage
      containers:
        - name: train
          image: churn-api:v1
          command: ["python", "src/train.py"]
          volumeMounts:
            - name: churn-volume
              mountPath: /app/models
              subPath: models
            - name: churn-volume
              mountPath: /app/registry
              subPath: registry

<img width="876" height="646" alt="image" src="https://github.com/user-attachments/assets/1a0c545e-6181-4623-b9c5-e7df21d719d1" />

Appliquer le Job :
kubectl apply -f k8s/job-train.yaml
Attendre la fin du Job :
kubectl wait --for=condition=complete job/churn-train

<img width="870" height="120" alt="image" src="https://github.com/user-attachments/assets/c9b9e22a-a129-46cc-a755-84cf6a2e18af" />

Monter le PVC dans le Deployment : l’API doit lire le modèle courant et écrire ses logs dans le même stockage persistant.
Modifier k8s/deployment.yaml pour ajouter le volume dans spec.template.spec :
volumes:
  - name: churn-volume
    persistentVolumeClaim:
      claimName: churn-storage

<img width="480" height="640" alt="image" src="https://github.com/user-attachments/assets/ea8ae95c-b62a-4984-ac3f-ae8972ad0f1b" />

Dans la section containers: - name: api, monter ce volume à deux emplacements distincts :
/app/registry pour stocker et lire les modèles,
/app/logs pour écrire les logs applicatifs.
Ajouter :
volumeMounts:
  - name: churn-volume
    mountPath: /app/registry
    subPath: registry
  - name: churn-volume
    mountPath: /app/models
    subPath: models
  - name: churn-volume
    mountPath: /app/logs
    subPath: logs

<img width="538" height="612" alt="image" src="https://github.com/user-attachments/assets/8256647b-e681-43d7-931c-83c3fbe4bafd" />

Réappliquer :
kubectl apply -f k8s/deployment.yaml
Vérifier que les Pods redémarrent correctement :
kubectl get pods
Vérifier que les dossiers sont bien accessibles depuis un Pod :
kubectl exec -it deploy/churn-api -- ls /app/registry
kubectl exec -it deploy/churn-api -- ls /app/logs

<img width="906" height="205" alt="image" src="https://github.com/user-attachments/assets/830ced97-4517-4d3e-a90d-33aa8278278b" />

Étape 12 : NetworkPolicy
Instructions :
Créer le fichier :
New-Item k8s/networkpolicy.yaml
#Ubuntu
touch k8s/networkpolicy.yaml
Coller le contenu suivant :
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-internal-services
spec:
  podSelector:
    matchLabels:
      app: churn-api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector: {}
      ports:
        - port: 8000
          protocol: TCP

<img width="888" height="662" alt="image" src="https://github.com/user-attachments/assets/e8e7a5be-8ba1-43d0-8fc2-82baa980606b" />

Appliquer la configuration :
kubectl apply -f k8s/networkpolicy.yaml
kubectl get networkpolicy

<img width="789" height="121" alt="image" src="https://github.com/user-attachments/assets/3977c1dc-2ec3-4d48-b5b4-772204f91c1a" />

Étape 14 : Vérifications finales
Instructions :
Vérifier les Pods :
kubectl get pods -l app=churn-api
Vérifier les Services :
kubectl get svc
Tester l’endpoint /health :
kubectl port-forward svc/churn-api-service 30080:80

<img width="880" height="225" alt="image" src="https://github.com/user-attachments/assets/9beaba88-5240-4336-ae8a-e7f7fbdb3fc2" />

GET http://127.0.0.1:30080/health

<img width="1297" height="674" alt="Screenshot 2026-01-12 151838" src="https://github.com/user-attachments/assets/171b9fb5-0628-4989-a121-3ea6bafe01c3" />

<img width="1252" height="602" alt="image" src="https://github.com/user-attachments/assets/f1acf426-c3a4-41f0-b693-8e63c494eac9" />



Envoyer quelques requêtes /predict.

<img width="1245" height="512" alt="image" src="https://github.com/user-attachments/assets/398f7c2d-6d2e-4f61-89e8-cfc871688d5b" />

<img width="1246" height="448" alt="image" src="https://github.com/user-attachments/assets/e9c3f147-c310-49ff-ac45-b22ea30535b3" />

<img width="679" height="271" alt="image" src="https://github.com/user-attachments/assets/db59eb49-96e1-4391-bfca-962d10239338" />

<img width="1149" height="459" alt="image" src="https://github.com/user-attachments/assets/1548583a-a8ce-4e47-a04a-0a407e048767" />

Lister les Pods pour choisir un Pod churn :
kubectl get pods -l app=churn-api
Exécuter la détection de drift dans le Pod :
kubectl exec -it <nom_du_pod> -- python src/monitor_drift.py

<img width="1008" height="470" alt="image" src="https://github.com/user-attachments/assets/a25539d8-cfb1-4c50-ad03-0bfbce6c9823" />


