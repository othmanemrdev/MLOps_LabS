Lab 1 : Du notebook au mini-système production-ready

Étape 1 : Initialiser la structure du projet
Crée un dossier de travail :
 <img width="975" height="402" alt="image" src="https://github.com/user-attachments/assets/5fb64dec-be47-44ff-9391-fc8a3a21b4f9" />

Crée les dossiers suivants :
<img width="452" height="365" alt="image" src="https://github.com/user-attachments/assets/835432bb-7e77-498a-8748-ef4894895453" />
<img width="514" height="363" alt="image" src="https://github.com/user-attachments/assets/dec01cf3-02b5-465f-b97d-6880042346a8" />


   
Crée le fichier identifiant le modèle actif :
<img width="975" height="32" alt="image" src="https://github.com/user-attachments/assets/7cf964c3-3f76-4f0c-9869-eaaecaf13b42" />

 
Étape 2 : Préparer l'environnement Python
Instructions :
Créer un environnement virtuel (Windows PowerShell) :
Mettre à jour pip :
Installer les dépendances :
 
 <img width="975" height="373" alt="image" src="https://github.com/user-attachments/assets/085afa55-1844-48fc-ab6c-1f24a06ab1a2" />
<img width="975" height="506" alt="image" src="https://github.com/user-attachments/assets/5f5c3181-bd2e-4184-9cc8-a22e0d2249d4" />



Étape 3 : Générer le dataset
Instructions :
Créer le fichier :

<img width="975" height="255" alt="image" src="https://github.com/user-attachments/assets/515085c2-fad6-46f8-9eb6-cd9dd697643a" />

 
L’objectif de cette étape est de créer un dataset synthétique qui servira de base à l’ensemble du pipeline MLOps qui contrend entraînement, évaluation, déploiement et monitoring du modèle. Le script generate_data.py produit un fichier data/raw.csv contenant des données clients liées à un service d’abonnement.
Étape 4 : Préparer les données + quality checks
Instructions :
Créer le fichier :

<img width="975" height="260" alt="image" src="https://github.com/user-attachments/assets/9f794af0-7dbf-4315-a3e3-ea78f3a736e7" />

 
Cette étape on a  transformer les données brutes en données exploitables par un modèle de machine learning, c’est la phase de prétraitement et validation des données dans un pipeline MLOps. L’objectif principal est d’éviter que des données incorrectes, incohérentes ou non conformes n’entrent dans la phase d’entraînement, ce qui pourrait dégrader les performances du modèle ou rendre le pipeline instable.
Les etapes que le script suit sont :
1.	Chargement et nettoyage des données
2.	Correction des valeurs numériques incohérentes
3.	Normalisation des variables catégorielles
4.	Contrôles de qualité des données 
5.	Vérification du schéma des données
6.	Contrôle du taux de valeurs manquantes
7.	Validation des types de données
8.	Sauvegarde des données prétraitées
9.	Calcul et traçabilité des statistiques d’entraînement

Étape 5 : Entraîner, versionner et valider le modèle
Instructions :
Créer le fichier :

<img width="975" height="176" alt="image" src="https://github.com/user-attachments/assets/c1043bb9-309a-4247-8f9f-0748980be8ae" />

 
Dans cette etapes on fait l’entraînement du modèle de machine learning, sa comparaison à une baseline, on lui donne un statut de modèle courant. L’objectif c’est de garantir que seuls les modèles présentant une qualité suffisante puissent être utilisés en production, grâce à un mécanisme de validation automatique qui est le deployment gate. Le script utilise la régression logistique binaire et une séparation train / test , et une evaluation des performances du modèle ou plusieurs métriques sont calculées afin d’obtenir une évaluation complète :
•	Accuracy : performance globale
•	Precision : qualité des prédictions positives
•	Recall : capacité à détecter les churns
•	F1-score : compromis entre précision et rappel
Un mécanisme de deployment gate est implémenté afin de contrôler la promotion du modèle. Un modèle est accepté uniquement si son F1-score est supérieur ou égal au seuil défini et à celui de la baseline. 
Étape 6 : Inspecter la registry et le modèle courant
Instructions :
Créer le fichier :

<img width="975" height="215" alt="image" src="https://github.com/user-attachments/assets/3483e110-fa80-4cee-8688-32bc124369e8" />

 
L’objectif de cette étape est de mettre en place et d’inspecter une registry de modèles, c’est-à-dire un mécanisme permettant de conserver l’historique des modèles entraînés, stocker leurs performances et métadonnées et identifier clairement quel modèle est considéré comme le modèle courant en production. Donc nous avons mis en place une registry de modèles minimale avec les fichiers :
•	metadata.json qui contient l’historique de tous les modèles entraînés, avec :
1.	la version du modèle ;
2.	la date d’entraînement ;
3.	les métriques (accuracy, precision, recall, F1) ;
4.	la valeur de la baseline ;
5.	le seuil du gate (gate_f1) ;
6.	le statut du modèle (validé ou refusé).
•	current_model.txt qui contient le nom du modèle officiellement actif, c’est-à-dire celui autorisé à être utilisé en production.
Même si un modèle est entraîné et sauvegardé, il n’est pas automatiquement déployé car le déploiement dépend d’un quality gate basé sur la métrique F1, grâce au fichier current_model.txt, il est possible de savoir quel modèle est actif à un instant donné, éviter toute ambiguïté sur la version réellement utilisée et faciliter les audits, le monitoring et les rollbacks. Si aucun modèle ne passe le gate, aucun modèle n’est activé, ce qui est un comportement souhaitable en MLOps, donc un modèle ML ne doit pas être déployé uniquement parce qu’il fonctionne et la notion de registry est essentielle pour la traçabilité des modèles, la reproductibilité des expériences, la gouvernance des déploiements, les quality gates sont un élément clé de la mise en production industrielle des modèles ML.

Étape 7 : Créer une API /predict qui utilise le modèle courant
Instructions : Créer le fichier :

<img width="895" height="218" alt="image" src="https://github.com/user-attachments/assets/8573537f-0983-48f2-8640-2d0cc9384eae" />

 
Lancer l’API et Tester :
•	GET http://127.0.0.1:8000/health
•	POST http://127.0.0.1:8000/predict (avec un JSON d’exemple)

<img width="975" height="279" alt="image" src="https://github.com/user-attachments/assets/a3fe562e-5ae4-47c9-9f1c-cb6aa2491b70" />

 <img width="975" height="471" alt="image" src="https://github.com/user-attachments/assets/07ab2e7f-e258-4f9b-9cb0-1c620928ae80" />

 <img width="975" height="472" alt="image" src="https://github.com/user-attachments/assets/f4ad723a-cfbe-4815-9c63-78399ee4ceab" />
<img width="975" height="476" alt="image" src="https://github.com/user-attachments/assets/e71ab492-1221-4e08-842e-7ee5d114a0fe" />

 <img width="975" height="237" alt="image" src="https://github.com/user-attachments/assets/25989f5f-5c82-4ad7-8e31-322d3083f43a" />

 <img width="975" height="231" alt="image" src="https://github.com/user-attachments/assets/29bcf155-2b22-46ef-950f-94a098719542" />

 
 
Étape 8 : Détecter une dérive des données via les logs
Instructions :
Créer le fichier :

<img width="975" height="197" alt="image" src="https://github.com/user-attachments/assets/a2bd2766-61b3-4d17-b36b-910a06ecd608" />

 
L’objectif de cette étape est de surveiller le comportement du modèle en production, en détectant une éventuelle dérive des données d’entrée (data drift) car même un modèle performant peut devenir inefficace dans le temps si les données reçues en production ne suivent plus la même distribution que celles utilisées à l’entraînement. Cette étape correspond à la phase Monitor d’un pipeline MLOps.
Conclusion du monitoring
Résultat : 3 alerte(s) de drift.
Analyse recommandée + retraining possible.
Cela signifie que :
•	les données en production ne ressemblent plus aux données d’entraînement ;
•	les prédictions du modèle peuvent devenir peu fiables ;
•	une analyse approfondie est nécessaire.



Étape 9 : Gérer les versions du modèle et revenir en arrière
Instructions :
Entraîner une nouvelle version (v2) :
Créer le script de rollback
Effectuer un rollback automatique vers la version précédente :
Ou rollback vers une version précise (remplacer le nom par un vrai fichier existant) :

<img width="975" height="292" alt="image" src="https://github.com/user-attachments/assets/0457c93c-efc5-4786-b641-0abfbb2d17e9" />

 
Dans cette etape notre objectif est de mettre en place une gestion de versions des modèles (model versioning) et à permettre un retour rapide vers un modèle précédent en cas de problème après un déploiement. Nous avons entraîné une nouvelle version du modèle (v2) et le script rollback.py agit comme un outil de gestion du model registry, il permet de, lire la liste des modèles enregistrés dans registry/metadata.json, définir quel modèle est actuellement actif via current_model.txt et revenir automatiquement à la version précédente si nécessaire.

Conclusion :
Ce lab a permis de mettre en pratique l’ensemble du cycle de vie d’un modèle machine learning dans un contexte MLOps minimal mais réaliste, depuis la préparation des données jusqu’au déploiement et au monitoring en production.
Nous avons appris à :
•	Structurer un projet ML avec des dossiers clairs et une séparation des responsabilités (données, modèles, logs, scripts).
•	Préparer et valider les données, en appliquant des contrôles qualité pour garantir la fiabilité du pipeline.
•	Entraîner, évaluer et versionner les modèles, en utilisant un mécanisme de quality gate pour ne déployer que des modèles performants.
•	Mettre en place une registry de modèles, permettant de tracer l’historique des modèles, de connaître le modèle actif et de faciliter les audits et le suivi des performances.
•	Créer une API de prédiction pour servir le modèle en production, illustrant la phase Serve d’un pipeline MLOps.
•	Surveiller les données et détecter un drift, afin de garantir la performance du modèle dans le temps et anticiper les besoins de ré-entraînement.
•	Gérer les versions et effectuer des rollbacks, assurant un déploiement sécurisé et réversible en cas de problème avec une nouvelle version.
En résumé, ce lab a démontré comment transformer un notebook expérimental en un mini-système production-ready, intégrant toutes les étapes clés d’un pipeline MLOps : Train, Serve, Monitor et Manage. Il illustre l’importance de la traçabilité, de la reproductibilité et de la robustesse dans la mise en production des modèles ML.
