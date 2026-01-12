Lab 7 : Gestion du cycle de vie des modèles avec MLflow

Étape 1 : Initialisation de l’environnement et installation de MLflow
Instruction :
Initialiser un environnement Python isolé pour le projet et installer la bibliothèque MLflow.
py -3.12 -m venv venv_mlops
Activer l’environnement :
Windows (PowerShell)
.\venv_mlops\Scripts\Activate.ps1
Linux / macOS
source venv_mlops/bin/activate
Mettre à jour pip puis installer MLflow :
pip install mlflow==2.20.1

<img width="1132" height="502" alt="image" src="https://github.com/user-attachments/assets/d5bb33aa-ebe5-4340-96b4-b509afbabb2f" />

Étape 2 : Création explicite de l’espace de stockage MLflow
Instruction :
Créer une structure dédiée au stockage MLflow.
Commandes
À la racine du projet :
mkdir mlflow/artifacts
Résultat attendu :
mlops-lab-01/
 ├── mlflow/
 │   ├── artifacts/
Explication pédagogique :
On prépare explicitement la séparation :
métadonnées (base de données),
artefacts (modèles, fichiers).

<img width="815" height="550" alt="image" src="https://github.com/user-attachments/assets/0c745ec7-a2b4-46be-97e3-5b0063262c7f" />

Étape 3 : Configuration du client MLflow
Instruction :
Configurer l’URI du tracking server pour le projet.
Commande (recommandée)
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000   # Linux / macOS
setx MLFLOW_TRACKING_URI http://127.0.0.1:5000     # Windows
Vérification :
#Powershell 
$Env:MLFLOW_TRACKING_URI
Ubuntu
echo $MLFLOW_TRACKING_URI
Tous les scripts MLflow enverront désormais leurs runs vers le serveur central, et non en local.

<img width="811" height="87" alt="image" src="https://github.com/user-attachments/assets/548188f7-9559-4128-b2b7-6298c22bd657" />

<img width="748" height="89" alt="image" src="https://github.com/user-attachments/assets/4f91e774-b85b-434c-a4f8-5eab8b0874f9" />

Étape 4 : Démarrage du serveur MLflow (tracking server)
Instruction :
Démarrer un serveur MLflow local avec SQLite et un artifact store dédié.
Commande
mlflow server --backend-store-uri sqlite:///mlflow/mlflow.db --default-artifact-root ./mlflow/artifacts --host 127.0.0.1 --port 5000
Résultat attendu :
un fichier mlflow/mlflow.db est créé,
l’interface MLflow est accessible sur
- http://127.0.0.1:5000
Le tracking server devient la source centrale de vérité pour les expérimentations et les modèles.

<img width="1132" height="367" alt="image" src="https://github.com/user-attachments/assets/86bdfa37-168a-4e07-8726-4b8a886838d6" />

<img width="198" height="92" alt="image" src="https://github.com/user-attachments/assets/b0c263db-f48b-45e8-aa9a-a9506066c065" />

<img width="1322" height="493" alt="image" src="https://github.com/user-attachments/assets/b4545601-bf50-46e6-bfb4-eae89676589f" />

Étape 5 : Instrumentation réelle de train.py
Instruction :
Modifier src/train.py afin qu’une exécution d’entraînement enregistre automatiquement :
(1) les paramètres et métriques, (2) le fichier modèle exporté, (3) une version du modèle dans le Model Registry MLflow.


1) Ajout des imports MLflow
Dans le bloc des imports en haut du fichier, ajouter :
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

<img width="496" height="192" alt="image" src="https://github.com/user-attachments/assets/b618e5d6-031d-4f46-ba63-63aad7ae5b3c" />

3) Constante globale
Dans le bloc des constantes globales, ajouter :
MODEL_NAME: Final[str] = "churn_model

<img width="658" height="260" alt="image" src="https://github.com/user-attachments/assets/5cbfee3b-0bf7-4247-b0b8-24a47e8186fd" />

2) Insertion du bloc MLflow à l’endroit exact dans main()
Dans main(), repérer la ligne où le modèle est déjà sauvegardé sur disque :
joblib.dump(pipe, stable_model_path)

<img width="451" height="126" alt="image" src="https://github.com/user-attachments/assets/1998365b-4bb2-445b-8015-6bb58d478bdd" />

Immédiatement après cette ligne, insérer le bloc suivant :
#Associe le run à une expérience logique. Les exécutions seront regroupées sous ce nom dans l’interface MLflow.
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("mlops-lab-01")

#Crée une exécution traçable correspondant à l’entraînement courant. Le nom du run porte ici la version logique passée au script.
with mlflow.start_run(run_name=f"train-{version}") as run:
    run_id = run.info.run_id
    #Enregistre le contexte de l’entraînement. Les paramètres sont essentiels pour comprendre et reproduire une exécution.
    mlflow.log_param("version", version)
    mlflow.log_param("seed", seed)
    mlflow.log_param("gate_f1", gate_f1)
    #Enregistre l’ensemble des métriques calculées par le script (F1, accuracy, etc.). 
    #Chaque métrique devient comparable entre runs dans l’UI.
    mlflow.log_metrics(metrics)
    #Ajoute des informations descriptives (métadonnées) destinées à faciliter la lecture humaine 
    #quel fichier de données a été utilisé, quel fichier modèle a été produit.
    mlflow.set_tag("data_file", DATA_PATH.name)
    mlflow.set_tag("model_file", model_filename)
    #Attache le fichier modèle exporté (celui déjà généré via joblib.dump) au run MLflow. Il apparaît dans la section Artifacts du run.
    mlflow.log_artifact(str(model_path), artifact_path="exported_models")
    #Enregistre le pipeline entraîné comme un modèle MLflow et le publie dans le Model Registry sous un nom stable (churn_model). 
    #Chaque exécution crée une nouvelle version (v1, v2, …) associée au run.
    mlflow.sklearn.log_model(
        sk_model=pipe,
        artifact_path="model",
        registered_model_name="churn_model",
    )

<img width="1147" height="599" alt="image" src="https://github.com/user-attachments/assets/e597ed4b-cee4-4dd6-8688-a45e180205f8" />

4) Exécution
python src/train.py
5) Résultat attendu
Dans l’interface MLflow, un run apparaît dans l’expérience mlops-lab-01 avec :
les paramètres version, seed, gate_f1,
les métriques du dictionnaire metrics,
un artefact exported_models/<fichier_joblib>.
Dans le Model Registry, un modèle churn_model apparaît avec une nouvelle version créée par l’exécution.

<img width="1317" height="539" alt="image" src="https://github.com/user-attachments/assets/3865c7e0-6b0d-435e-acfa-36dfba5498f7" />

<img width="1312" height="551" alt="image" src="https://github.com/user-attachments/assets/465efff1-71bd-4128-bd64-9b4e81ce5f3f" />

<img width="1133" height="285" alt="image" src="https://github.com/user-attachments/assets/eaa95e87-aca4-4994-83ba-7f3851334f99" />

Étape 6 : Observation du registry MLflow
Instruction :
Observer le modèle enregistré dans l’UI.
Action
Ouvrir : http://127.0.0.1:5000
Onglet Models
Sélectionner churn_model
Résultat attendu :
Version 1 créée
Lien vers le run d’origine
Explication pédagogique :
Le registry MLflow remplit maintenant le rôle conceptuel étudié dans le cours.

<img width="1300" height="531" alt="image" src="https://github.com/user-attachments/assets/788f54c1-ff99-4ee5-81b1-37aaa5a0ee7b" />

Étape 7 : Promotion d’un modèle (activation)
Instruction :
Créer un script de promotion.
Fichier src/promote.py
import mlflow
from mlflow.tracking import MlflowClient


MODEL_NAME = "churn_model"
ALIAS = "production"


mlflow.set_tracking_uri("http://127.0.0.1:5000")
client = MlflowClient()


# Cherche toutes les versions et prend la plus récente
mvs = client.search_model_versions(f"name='{MODEL_NAME}'")
if not mvs:
    raise SystemExit(f"Aucune version trouvée pour {MODEL_NAME}. Lance train.py d'abord.")


latest_version = max(int(mv.version) for mv in mvs)


client.set_registered_model_alias(MODEL_NAME, ALIAS, str(latest_version))
print(f"Modèle activé : {MODEL_NAME}@{ALIAS} -> v{latest_version}")

<img width="953" height="537" alt="image" src="https://github.com/user-attachments/assets/7214186f-c1d7-441f-b404-f720f5735eb5" />

Commande
python src/promote.py
Résultat attendu :
alias production visible dans l’UI MLflow.
Uploaded Image
L’activation devient une décision explicite, indépendante de l’entraînement.

<img width="704" height="128" alt="image" src="https://github.com/user-attachments/assets/4fde553a-b5f5-4fea-b257-0bfb024d2c95" />

<img width="1129" height="201" alt="image" src="https://github.com/user-attachments/assets/77e9aa27-06ef-41cf-8f60-4de6c6e51a38" />

Étape 8 : Rollback via MLflow Model Registry
Instruction :
Modifier src/rollback.py afin qu’il n’écrive plus dans registry/current_model.txt, mais qu’il mette à jour l’alias MLflow production vers une version antérieure du modèle churn_model.


Code à placer dans src/rollback.py (version MLflow)
from __future__ import annotations


"""
Script utilitaire de gestion du Model Registry via MLflow.


Objectif principal :
- Lister les versions du modele enregistre dans MLflow.
- Mettre a jour l'alias "production" pour activer :
  - une version specifique (via target),
  - ou, par defaut, la version precedente (rollback).


Le registry local (metadata.json, current_model.txt) n'est plus utilise.
MLflow devient la source de verite.
"""


from typing import Optional


import mlflow
from mlflow.tracking import MlflowClient



MODEL_NAME = "churn_model"
ALIAS = "production"



def _list_versions(client: MlflowClient) -> list[int]:
    """Retourne la liste des versions existantes (triees)."""
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    out = sorted({int(v.version) for v in versions})
    return out



def _get_current_version(client: MlflowClient) -> Optional[int]:
    """
    Retourne la version actuellement pointee par l'alias production.
    Retourne None si l'alias n'existe pas.
    """
    try:
        mv = client.get_model_version_by_alias(MODEL_NAME, ALIAS)
        return int(mv.version)
    except Exception:
        return None



def _set_alias(client: MlflowClient, version: int) -> None:
    """Fait pointer l'alias production vers la version demandee."""
    client.set_registered_model_alias(MODEL_NAME, ALIAS, str(version))



def main(target: Optional[str] = None) -> None:
    """
    Active une version specifique ou effectue un rollback vers la version precedente.


    Parametres
    ----------
    target : str, optionnel
        Version a activer explicitement (ex: "3").
        Si None, effectue un rollback vers la version precedente de l'alias production.
    """
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    client = MlflowClient()


    versions = _list_versions(client)
    if not versions:
        raise FileNotFoundError(
            f"Aucune version MLflow trouvee pour le modele '{MODEL_NAME}'. "
            "Lancer train.py au moins une fois."
        )


    # Activation explicite : target = numero de version
    if target is not None:
        try:
            v = int(target)
        except ValueError as e:
            raise ValueError(
                "target doit etre un numero de version (ex: '2')."
            ) from e


        if v not in versions:
            raise ValueError(
                f"Version inconnue : v{v}. Versions disponibles : {versions}"
            )


        _set_alias(client, v)
        print(f"[OK] activation => {MODEL_NAME}@{ALIAS} = v{v}")
        return


    # Rollback automatique : version precedente par rapport a l'alias courant
    current = _get_current_version(client)


    # Si l'alias n'existe pas encore, on considere la derniere version comme courante
    if current is None:
        current = versions[-1]


    idx = versions.index(current)
    if idx == 0:
        raise ValueError(
            f"Rollback impossible : {MODEL_NAME}@{ALIAS} est deja sur "
            f"la plus ancienne version (v{current})."
        )


    previous = versions[idx - 1]
    _set_alias(client, previous)
    print(
        f"[OK] rollback => {MODEL_NAME}@{ALIAS} : v{current} -> v{previous}"
    )



if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)

<img width="627" height="659" alt="image" src="https://github.com/user-attachments/assets/1f3d3620-de41-433f-8802-b05dd87a43f3" />

Interprétation du script
Le script ne lit plus registry/metadata.json et n’écrit plus registry/current_model.txt.
La “source de vérité” devient le Model Registry MLflow.
client.search_model_versions(...) récupère toutes les versions disponibles de churn_model.
L’alias production remplace conceptuellement “current_model” :
changer d’alias revient à changer de modèle actif, sans toucher au code ni aux fichiers.
Deux modes :
python src/rollback.py : rollback automatique vers la version précédente.
python -c "from src.rollback import main; main('3')" : activation explicite de la version 3.

Après avoir entraîné au moins deux versions (v1, v2), exécuter :
python src/rollback.py
python src/rollback.py 2
Résultat attendu :
L’alias MLflow production pointe vers la version précédente du modèle churn_model.
Uploaded Image

Uploaded Image

<img width="719" height="128" alt="image" src="https://github.com/user-attachments/assets/b5289297-3c8c-44fc-99e0-579545f83bee" />

<img width="1157" height="145" alt="image" src="https://github.com/user-attachments/assets/3f023665-eeea-4a71-bac4-873b876f700a" />

<img width="1314" height="225" alt="image" src="https://github.com/user-attachments/assets/2fcec211-42fe-46e6-ad52-92d89d2a7627" />

<img width="1285" height="155" alt="image" src="https://github.com/user-attachments/assets/9733c029-6795-4d3e-80af-b9d8d7c29b7c" />

<img width="1180" height="119" alt="image" src="https://github.com/user-attachments/assets/d4ad683d-a6ff-4842-906d-2ee0d11abe01" />

Étape 9 : API : chargement du modèle actif
Instruction :
Adapter l’API pour charger le modèle actif depuis MLflow.


Imports à ajouter en src/api.py
En haut :
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

<img width="432" height="162" alt="image" src="https://github.com/user-attachments/assets/347b1f74-737d-49a7-8800-b4f38cea490e" />

Ajoute ces constantes (près de tes constantes)
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
MODEL_NAME = "churn_model"
ALIAS = "production"
MODEL_URI = f"models:/{MODEL_NAME}@{ALIAS}"

<img width="538" height="203" alt="image" src="https://github.com/user-attachments/assets/fefd27b1-174b-4ba3-af67-d642b04f0996" />

Remplace get_current_model_name() par ceci
def get_current_model_name() -> str:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()
    mv = client.get_model_version_by_alias(MODEL_NAME, ALIAS)
    return f"{MODEL_NAME}@{ALIAS} (v{mv.version})"

<img width="672" height="384" alt="image" src="https://github.com/user-attachments/assets/cd1f8dff-273d-41e5-8003-3ee7df680cc3" />

Remplace load_model_if_needed() par ceci
def load_model_if_needed() -> tuple[str, Any]:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Cache key = model URI (alias), not local filename
    cache_key = MODEL_URI

    if _model_cache["name"] == cache_key and _model_cache["model"] is not None:
        return cache_key, _model_cache["model"]

    model = mlflow.sklearn.load_model(MODEL_URI)

    _model_cache["name"] = cache_key
    _model_cache["model"] = model
    return cache_key, model

<img width="708" height="554" alt="image" src="https://github.com/user-attachments/assets/fa5d4951-5dad-4559-a00e-b1bbdf65dc77" />

Start the FastApi server
uvicorn src.api:app --host 0.0.0.0 --port 8000
Résultat attendu :
l’API sert toujours la version active,
même après promotion ou rollback.
Uploaded Image

<img width="859" height="158" alt="image" src="https://github.com/user-attachments/assets/8498eadb-b21d-4296-8e44-3c54a8673fcd" />

<img width="499" height="142" alt="image" src="https://github.com/user-attachments/assets/17978bd5-b878-4258-b560-d861d6f99877" />

<img width="832" height="261" alt="image" src="https://github.com/user-attachments/assets/ac0c9aa3-0494-4a4f-88a4-f3c2dcce976c" />

<img width="544" height="194" alt="image" src="https://github.com/user-attachments/assets/5231992b-3f7d-453e-821a-894e4553748a" />




