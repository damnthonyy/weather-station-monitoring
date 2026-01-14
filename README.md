# Station Météo

Application de station météorologique composée de trois services principaux : une base de données PostgreSQL, un collecteur de données et une application web de visualisation.

## 📋 Architecture

### Composants

1. **Base de données (PostgreSQL)**
   - Stocke les mesures de température
   - Table `mesures` avec les champs : `id`, `ville`, `temperature`, `date`

2. **Collector** (`collector/`)
   - Collecte et enregistre des données météorologiques (température)
   - Insère des mesures toutes les 10 secondes dans la base de données
   - Script Python utilisant `psycopg2`

3. **Webapp** (`webapp/`)
   - Application Flask pour visualiser les données
   - Affiche les 10 dernières mesures
   - Accessible via un navigateur web

### Schéma de l'architecture

```
┌─────────────┐
│  Collector  │──┐
└─────────────┘  │
                 │
┌─────────────┐  │    ┌──────────────┐
│   Webapp    │──┼───▶│  PostgreSQL  │
│   (Flask)   │  │    │   Database   │
└─────────────┘  │    └──────────────┘
```

## 🚀 Déploiement

### Prérequis

- Docker et Docker Compose (pour le déploiement local)
- Kubernetes et kubectl (pour le déploiement en cluster)
- Fichier `.env` avec les variables d'environnement

### Configuration

Créez un fichier `.env` à la racine du projet :

```env
POSTGRES_USER=user_meteo
POSTGRES_PASSWORD=password123!
POSTGRES_DB=db_meteo
```

**Important :** Ne mettez pas d'espaces autour du signe `=` dans le fichier `.env`.

---

## 🐳 Déploiement avec Docker Compose

### Commandes usuelles

#### Démarrer tous les services
```bash
docker-compose up -d
```

#### Démarrer avec reconstruction des images
```bash
docker-compose up -d --build
```

#### Voir les logs
```bash
# Tous les services
docker-compose logs -f

# Un service spécifique
docker-compose logs -f collector
docker-compose logs -f webapp
docker-compose logs -f db
```

#### Arrêter les services
```bash
docker-compose down
```

#### Arrêter et supprimer les volumes (⚠️ supprime les données)
```bash
docker-compose down -v
```

#### Voir l'état des conteneurs
```bash
docker-compose ps
```

#### Redémarrer un service spécifique
```bash
docker-compose restart collector
docker-compose restart webapp
```

### Accès aux services

- **Webapp** : http://localhost:8080
- **Base de données** : localhost:5432

### Connexion à la base de données

```bash
docker-compose exec db psql -U user_meteo -d db_meteo
```

Commandes SQL utiles :
```sql
-- Voir toutes les mesures
SELECT * FROM mesures ORDER BY date DESC;

-- Compter les mesures
SELECT COUNT(*) FROM mesures;

-- Voir les 10 dernières mesures
SELECT * FROM mesures ORDER BY date DESC LIMIT 10;
```

---

## ☸️ Déploiement avec Kubernetes

### Architecture Kubernetes

- **Deployments** :
  - `db-deployment` : Base de données PostgreSQL
  - `display-deployment` : Application collector/webapp

- **Services** :
  - `postgres-db-service` : Service pour la base de données
  - `display-service` : Service pour l'application web (type LoadBalancer)

- **PersistentVolumeClaim** :
  - `postgres-db-pvc` : Stockage persistant pour la base de données

### Commandes usuelles

#### Déployer tous les composants
```bash
# Créer le PVC (stockage)
kubectl apply -f k8s/db-pvc.yaml

# Déployer la base de données
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/db-service.yaml

# Déployer l'application
kubectl apply -f k8s/display-deployment.yaml
kubectl apply -f k8s/display-service.yaml
```

#### Voir l'état des ressources
```bash
# Voir les pods
kubectl get pods

# Voir les services
kubectl get services

# Voir les deployments
kubectl get deployments

# Voir les PVC
kubectl get pvc
```

#### Voir les logs
```bash
# Logs du collector/webapp
kubectl logs -f -l app=display-pod

# Logs de la base de données
kubectl logs -f -l app=postgres-db-pod

# Logs d'un pod spécifique
kubectl logs -f <nom-du-pod>

# Logs du déploiement
kubectl logs -f deployment/display-deployment
```

#### Appliquer une modification de configuration
```bash
# Après modification d'un fichier YAML
kubectl apply -f k8s/display-deployment.yaml

# Kubernetes redéploiera automatiquement les pods
```

#### Redémarrer un deployment
```bash
kubectl rollout restart deployment/display-deployment
kubectl rollout restart deployment/db-deployment
```

#### Supprimer les ressources
```bash
# Supprimer un composant spécifique
kubectl delete -f k8s/display-deployment.yaml

# Supprimer tout
kubectl delete -f k8s/
```

#### Accéder à un pod (debug)
```bash
# Ouvrir un shell dans un pod
kubectl exec -it <nom-du-pod> -- /bin/bash

# Exécuter une commande dans un pod
kubectl exec <nom-du-pod> -- psql -U user_meteo -d db_meteo -c "SELECT * FROM mesures;"
```

#### Voir les événements
```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### Obtenir l'URL du service LoadBalancer
```bash
kubectl get service display-service
```

### Connexion à la base de données depuis un pod

```bash
# Trouver le nom du pod de la base de données
kubectl get pods -l app=postgres-db-pod

# Se connecter à la base de données
kubectl exec -it <nom-du-pod-db> -- psql -U user_meteo -d db_meteo
```

---

## 🔧 Développement

### Structure du projet

```
station-meteo/
├── collector/           # Service de collecte de données
│   ├── main.py         # Script principal
│   ├── Dockerfile      # Image Docker
│   └── requirements.txt # Dépendances Python
├── webapp/             # Application web Flask
│   ├── app.py         # Application Flask
│   └── Dockerfile     # Image Docker
├── k8s/                # Manifests Kubernetes
│   ├── db-deployment.yaml
│   ├── db-service.yaml
│   ├── db-pvc.yaml
│   ├── display-deployment.yaml
│   └── display-service.yaml
├── docker-compose.yml  # Configuration Docker Compose
├── .env               # Variables d'environnement (à créer)
└── README.md          # Ce fichier
```

### Variables d'environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `DB_HOST` | Nom d'hôte de la base de données | `localhost` (Docker) / `db` (K8s) |
| `POSTGRES_USER` | Utilisateur PostgreSQL | `user_meteo` |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `password123!` |
| `POSTGRES_DB` | Nom de la base de données | `db_meteo` |

### Modifier le code

1. **Modifier le code Python** : Éditez les fichiers dans `collector/` ou `webapp/`
2. **Reconstruire l'image** (Docker Compose) :
   ```bash
   docker-compose up -d --build
   ```
3. **Reconstruire et déployer** (Kubernetes) :
   ```bash
   # 1. Reconstruire l'image Docker et la pousser vers votre registry
   # 2. Mettre à jour l'image dans le deployment YAML
   # 3. Appliquer le changement
   kubectl apply -f k8s/display-deployment.yaml
   ```

---

## 🐛 Dépannage

### Erreur d'authentification PostgreSQL

**Symptôme :** `password authentication failed for user "user_meteo"`

**Solution :**
1. Vérifiez que le fichier `.env` existe et contient les bonnes valeurs
2. Vérifiez qu'il n'y a pas d'espaces autour du `=` dans le `.env`
3. Pour Docker Compose : supprimez le volume et redémarrez
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```
4. Pour Kubernetes : vérifiez que les variables d'environnement sont bien définies dans les deployments

### Le service ne peut pas résoudre le nom de la base de données (Kubernetes)

**Symptôme :** `could not translate host name "db-service" to address`

**Solution :** Vérifiez que :
- Le nom du service dans `db-service.yaml` correspond à la valeur de `DB_HOST` dans le deployment
- Le service est bien créé : `kubectl get services`
- Les pods sont dans le même namespace

### Les logs ne s'affichent pas

**Solution :** Utilisez `-f` pour suivre les logs en temps réel :
```bash
kubectl logs -f -l app=display-pod
docker-compose logs -f collector
```

---

## 📝 Notes

- Le collector insère des données toutes les 10 secondes
- La webapp affiche les 10 dernières mesures
- Les données sont persistantes (volume Docker ou PVC Kubernetes)
- En production, changez les mots de passe par défaut !
