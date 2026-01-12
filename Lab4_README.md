Lab 4 : Mise en place d’un pipeline CI/CD complet pour un projet Machine Learning

Étape 1 : Créer le dépôt GitHub et connecter le remote
Instructions :
Aller sur GitHub → New Repository → nom : mlops-lab-01
Copier l’URL HTTPS du dépôt.
Connecter :
git remote add origin https://github.com/<USER>/mlops-lab-01.git
git branch -M main
git push -u origin main

**Already done in the previous Labs**

Étape 2 : Définir les secrets GitHub
Instructions :
Aller dans :
GitHub → Repository → Settings → Secrets and Variables → Actions → New repository secret
Créer les secrets suivants :
PY_VERSION = 3.10 #variable
F1_GATE_THRESHOLD = 0.70 #variable
DEMO_SECRET = "CI/CD demo secret for students" #secert
APP_ENV = staging #variable

<img width="794" height="142" alt="Screenshot 2025-12-27 122724" src="https://github.com/user-attachments/assets/f1f0e4bd-5cfa-4b22-89bd-7539e5a50ead" />



Étape 3 : Créer le workflow CI/CD
name: MLOps CI/CD manifest


on:
  push:
    branches: ["main"]
  pull_request:


jobs:
  ci:
    runs-on: ubuntu-latest


    steps:
      - uses: actions/checkout@v4


      - uses: actions/setup-python@v5
        with:
          python-version: ${{ vars.PY_VERSION }}


      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ vars.PY_VERSION }}-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            pip-${{ runner.os }}-${{ vars.PY_VERSION }}-


      - name: Installer dépendances
        run: |
          pip install -U pip
          pip install dvc pandas numpy scikit-learn joblib


      - name: Restaurer cache DVC
        uses: actions/cache@v4
        with:
          path: .dvc/cache
          key: dvc-${{ runner.os }}-${{ vars.PY_VERSION }}-${{ github.sha }}
          restore-keys: |
            dvc-${{ runner.os }}-${{ vars.PY_VERSION }}-


      - name: Afficher le DAG DVC
        run: dvc dag


      - name: Générer données brutes
        run: python src/generate_data.py


      - name: Exécuter pipeline ML via DVC
        run: dvc repro


      - name: Vérifier métriques (Quality Gate F1)
        run: |
          python - << 'EOF'
          import json
          threshold = float("${{ vars.F1_GATE_THRESHOLD }}")
          with open("reports/metrics.json", "r", encoding="utf-8") as f:
              metrics = json.load(f)
          f1 = float(metrics.get("f1", 0.0))
          print(f"F1={f1} | seuil={threshold}")
          if f1 < threshold:
              raise SystemExit("Quality Gate échoué : F1 insuffisante")
          print("Quality Gate validé")
          EOF


      - name: Upload artefacts ML
        uses: actions/upload-artifact@v4
        with:
          name: ml-artifacts
          path: |
            models/
            registry/
            reports/


  cd:
    needs: ci
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'


    steps:
      - uses: actions/checkout@v4


      - name: Télécharger artefacts validés
        uses: actions/download-artifact@v4
        with:
          name: ml-artifacts
          path: release_artifacts


      - name: CD simulé (déploiement SSH)
        run: |
          echo "=== Phase CD (simulée) ==="
          echo "ENV               : ${{ vars.APP_ENV }}"
          echo "F1 gate           : ${{ vars.F1_GATE_THRESHOLD }}"
          echo "Secret (demo)     : ${{ secrets.DEMO_SECRET }}"
          echo
          echo "Artefacts prêts :"
          ls -R release_artifacts
          echo
          echo "Simulation SSH : ssh user@server 'deploy release_artifacts/'"



<img width="808" height="496" alt="Screenshot 2025-12-27 122644" src="https://github.com/user-attachments/assets/c6a0385d-663e-4b28-b5e0-7079b247f941" />






Étape 4 : Commit et push
Instructions :
Aller dans :
GitHub → Actions
Résulat:
Uploaded ImageVérifier :
job ci : doit installer Python, exécuter les scripts, uploader les artefacts
job cd : uniquement sur main, doit simuler un déploiement SSH



<img width="813" height="373" alt="Screenshot 2025-12-27 122703" src="https://github.com/user-attachments/assets/877f76f4-d130-4447-9242-21ae777d5fa2" />























