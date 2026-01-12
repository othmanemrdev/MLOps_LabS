Lab2 : Code Source management
Étape 1 : Initialiser Git dans mlops-lab-01
Instructions :
Aller dans le dossier du projet :
Initialiser le dépôt Git :

<img width="975" height="220" alt="image" src="https://github.com/user-attachments/assets/fe6bb42c-0cda-448d-8b5b-b32292857ea7" />

 
Afficher les dossiers cachés:

<img width="763" height="335" alt="image" src="https://github.com/user-attachments/assets/cd2ac9fb-07b3-4cc8-9599-56f708f5c4c2" />

 
Créer le fichier .gitignore :

<img width="505" height="322" alt="image" src="https://github.com/user-attachments/assets/a9e47311-2748-4b49-84f8-60917d413947" />

 
Vérifier l’état du dépôt :

<img width="875" height="361" alt="image" src="https://github.com/user-attachments/assets/213b78a9-dbda-47e6-99bc-c18852072274" />

 
Ici on doit initier un dépôt Git local pour versionner l’ensemble du projet MLOps et préparer un historique traçable des changements.
Étape 2 : Premier commit du projet MLOps
Instructions :
Ajouter les dossiers et fichiers principaux (code + configuration) :
Créer le premier commit :
Afficher l’historique :

<img width="975" height="435" alt="image" src="https://github.com/user-attachments/assets/c181f053-6354-48b1-b752-b7cde995ead2" />

 
On remarque que le dossier data n’est pas ajouter car on la mit dans le fichier .gitignore pour etre ignoré
Étape 3 : Observer une modification avec git diff
Instructions :
Modifier un script existant, par exemple dans src/monitor_drift.py :

<img width="578" height="252" alt="image" src="https://github.com/user-attachments/assets/a8b6146c-a0b7-4b4d-8835-fd791dc97304" />

 
Afficher les différences par rapport au dernier commit :
Ajouter le fichier modifié à l’index :
Afficher les différences en staging :
Créer un commit :

<img width="1055" height="706" alt="image" src="https://github.com/user-attachments/assets/f3471144-7297-4935-a9bd-6ff2f10263ed" />

 
Ici on doit inspecter les changements locaux avant de les valider dans l’historique.
Étape 4 : Créer une branche de fonctionnalité liée au lab
Instructions :
Créer une branche :

<img width="975" height="91" alt="image" src="https://github.com/user-attachments/assets/dafd8885-827a-48c4-8c3e-e56668f58d4f" />

 
Modifier src/api.py (par exemple ajouter une gestion de request_id automatique) :

<img width="602" height="529" alt="image" src="https://github.com/user-attachments/assets/7339a00b-4b84-42c9-bca6-f7b52016f47c" />

 
Ajouter et committer :
Lister les branches :
Revenir sur la branche principale :

<img width="975" height="199" alt="image" src="https://github.com/user-attachments/assets/cafb7305-73c2-4598-8e82-a32210f85e91" />

 
Ici on doit isoler la nouvelle fonctionnalité de gestion automatique de request_id dans une branche dédiée pour développer sans perturber master.
Étape 5 : Fusionner la branche feature dans la branche principale
Instructions :
Depuis la branche principale :
Fusionner la branche :
Vérifier l’historique :

<img width="975" height="261" alt="image" src="https://github.com/user-attachments/assets/6cc986a1-fc5c-4a35-b73d-be632d27d619" />

 
Ici on doit intégrer la fonctionnalité testée dans la branche principale après validation.
Étape 6 : Créer un conflit de merge sur src/train.py
Instructions :
Créer une nouvelle branche :

<img width="969" height="92" alt="image" src="https://github.com/user-attachments/assets/b7113f42-45b5-4178-9b21-e40b1977f5b9" />

 
Modifier src/train.py (par exemple gate_f1 à 0.60) :

<img width="1007" height="266" alt="image" src="https://github.com/user-attachments/assets/9d507840-d4a1-4b5d-aec4-c08bccd8de68" />

 
Ajouter et committer :
Revenir sur la branche principale :

<img width="975" height="157" alt="image" src="https://github.com/user-attachments/assets/9cf91aed-e836-48a8-a1ff-90b0333e842c" />

 
Modifier la même ligne dans src/train.py (par exemple gate_f1 à 0.75) :

<img width="975" height="249" alt="image" src="https://github.com/user-attachments/assets/68b79920-2443-4300-bfbd-e64562589983" />

 
Ajouter et committer :
Une erreur de conflix est apparu que j’ai resulut en acceptant les modification uncomming
Tenter la fusion :

<img width="938" height="100" alt="image" src="https://github.com/user-attachments/assets/8343bb31-58f0-4923-afe0-c154168d4c94" />

 
Résoudre le conflit dans src/train.py (choisir une valeur, par exemple 0.70), puis :

<img width="975" height="115" alt="image" src="https://github.com/user-attachments/assets/585118ae-ac17-4779-8a15-b6ff19553e94" />

 
Ici on a tout simplement rencontrer un conflit Git et on a appris a le resoudre correctement
Étape 7 : Utiliser git stash dans le contexte du lab
Instructions :
Modifier un fichier sans vouloir committer (par exemple src/rollback.py) :

<img width="324" height="220" alt="image" src="https://github.com/user-attachments/assets/7eaa1aef-c2f3-4721-9c2f-172f468004fd" />

 
Afficher l’état :
Mettre de côté les modifications :
Lister les stash :
Récupérer les modifications :
(Option alternative pour appliquer + supprimer) :

<img width="789" height="530" alt="image" src="https://github.com/user-attachments/assets/93135801-eaaf-4be8-8a95-473efe4a2554" />

 
Ici on doit apprendre à mettre temporairement de côté des modifications non terminées pour pouvoir switcher facilement de branche sans probleme.
Étape 8 : Tester git reset sur un fichier d’expérimentation
Instructions :

Créer un dossier d’expérimentation :
Créer un fichier de test :
Modifier puis committer deux fois :
Effectuer un reset soft :
Effectuer un reset mixed :
Effectuer un reset hard :

<img width="975" height="699" alt="image" src="https://github.com/user-attachments/assets/2e1b7011-58ce-4064-8ed3-a6988b9922db" />
<img width="975" height="368" alt="image" src="https://github.com/user-attachments/assets/50eb01b7-d2cd-46f7-a97e-4226906b2fe0" />

 
 
Ici on a Comprendris les différents types de git reset : soft, mixed et hard et leur effet sur l’index et le working tree.
Étape 9 : Annuler un commit avec git revert
Instructions :
Ajouter un changement non souhaité dans src/api.py :
Lister les commits :
Revert du dernier commit :
Vérifier le contenu du fichier :

<img width="975" height="408" alt="image" src="https://github.com/user-attachments/assets/7970ccbb-e6d1-498d-b083-3f0efe643f4f" />

 
Étape 10 : Rebase d’une branche feature sur la branche principale
Instructions :
Créer une branche :

<img width="975" height="28" alt="image" src="https://github.com/user-attachments/assets/172daf96-1f2f-4eb4-a043-a7adf78e3a08" />

 
Modifier src/monitor_drift.py (changer last_n, par exemple 500) :

<img width="975" height="261" alt="image" src="https://github.com/user-attachments/assets/34e6b806-92ba-4219-add9-a15bf5d89712" />

Ajouter et committer :
Revenir sur la branche principale et créer un nouveau commit sur un autre fichier (par exemple src/generate_data.py) :
Revenir sur la branche feature :
Rebaser la branche feature sur la branche principale :
Vérifier l’historique :

<img width="975" height="593" alt="image" src="https://github.com/user-attachments/assets/876f9a46-32bb-4042-a199-e3b2905d1b63" />

 
Ici on doit apprendre à annuler un commit 

Conclusion : 
Ce deuxième lab a permis de maîtriser les fondamentaux de la gestion de code source avec Git, un outil indispensable dans les projets MLOps et plus généralement en ingénierie logicielle et data. À travers des manipulations progressives et réalistes, nous avons appris à structurer un dépôt, versionner correctement le code, et gérer l’évolution d’un projet de manière contrôlée et traçable. L’utilisation de .gitignore nous a sensibilisés à l’importance de ne pas versionner des artefacts non reproductibles ou volumineux tels que les données, les modèles entraînés et les environnements virtuels, ce qui est crucial dans un contexte MLOps. Les commandes git diff, git add et git commit ont renforcé la discipline de validation incrémentale des changements, favorisant des commits clairs, atomiques et compréhensibles. Le travail avec les branches de fonctionnalité, leur fusion dans la branche principale, ainsi que la résolution de conflits, a mis en évidence les problématiques réelles du travail collaboratif. La création volontaire d’un conflit de merge a permis de comprendre en profondeur les mécanismes de Git et d’adopter une démarche réfléchie lors de la résolution, plutôt qu’une acceptation aveugle des changements. Les commandes avancées telles que git stash, git reset, git revert et git rebase ont permis de distinguer clairement les opérations sûres de celles potentiellement destructrices, et d’identifier les bonnes pratiques à adopter selon que l’on travaille localement ou sur une branche partagée. En particulier, la différence entre reset et revert est essentielle pour préserver l’intégrité de l’historique dans un environnement collaboratif.
En conclusion, ce laboratoire ne se limite pas à l’apprentissage de commandes Git, mais constitue une mise en situation réaliste des workflows utilisés en MLOps, où la reproductibilité, la collaboration et la traçabilité sont critiques. Les compétences acquises dans ce lab forment une base solide pour la gestion de pipelines de données et de modèles à grande échelle, et sont directement applicables dans des projets professionnels et industriels.
