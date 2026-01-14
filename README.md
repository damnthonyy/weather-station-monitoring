# Weather Station

Weather monitoring application consisting of three main services: a PostgreSQL database, a data collector, and a web visualization application.

## 📋 Architecture

### Components

1. **Database (PostgreSQL)**
   - Stores temperature measurements
   - Table `mesures` with fields: `id`, `ville`, `temperature`, `date`

2. **Collector** (`collector/`)
   - Collects and records weather data (temperature)
   - Inserts measurements every 10 seconds into the database
   - Python script using `psycopg2`

3. **Webapp** (`webapp/`)
   - Flask application for data visualization
   - Displays the last 10 measurements
   - Accessible via web browser

### Architecture Diagram

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

## 🚀 Deployment

### Prerequisites

- Docker and Docker Compose (for local deployment)
- Kubernetes and kubectl (for cluster deployment)
- `.env` file with environment variables

### Configuration

Create a `.env` file at the project root:

```env
POSTGRES_USER=user_meteo
POSTGRES_PASSWORD=password123!
POSTGRES_DB=db_meteo
```

**Important:** Do not put spaces around the `=` sign in the `.env` file.

---

## 🐳 Deployment with Docker Compose

### Common Commands

#### Start all services
```bash
docker-compose up -d
```

#### Start with image rebuild
```bash
docker-compose up -d --build
```

#### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f collector
docker-compose logs -f webapp
docker-compose logs -f db
```

#### Stop services
```bash
docker-compose down
```

#### Stop and remove volumes (⚠️ deletes data)
```bash
docker-compose down -v
```

#### Check container status
```bash
docker-compose ps
```

#### Restart a specific service
```bash
docker-compose restart collector
docker-compose restart webapp
```

### Service Access

- **Webapp**: http://localhost:8080
- **Database**: localhost:5432

### Connect to Database

```bash
docker-compose exec db psql -U user_meteo -d db_meteo
```

Useful SQL commands:
```sql
-- View all measurements
SELECT * FROM mesures ORDER BY date DESC;

-- Count measurements
SELECT COUNT(*) FROM mesures;

-- View last 10 measurements
SELECT * FROM mesures ORDER BY date DESC LIMIT 10;
```

---

## ☸️ Deployment with Kubernetes

### Kubernetes Architecture

- **Deployments**:
  - `db-deployment`: PostgreSQL database
  - `display-deployment`: Collector/webapp application

- **Services**:
  - `postgres-db-service`: Database service
  - `display-service`: Web application service (LoadBalancer type)

- **PersistentVolumeClaim**:
  - `postgres-db-pvc`: Persistent storage for the database

### Common Commands

#### Deploy all components
```bash
# Create PVC (storage)
kubectl apply -f k8s/db-pvc.yaml

# Deploy database
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/db-service.yaml

# Deploy application
kubectl apply -f k8s/display-deployment.yaml
kubectl apply -f k8s/display-service.yaml
```

#### View resource status
```bash
# View pods
kubectl get pods

# View services
kubectl get services

# View deployments
kubectl get deployments

# View PVCs
kubectl get pvc
```

#### View logs
```bash
# Collector/webapp logs
kubectl logs -f -l app=display-pod

# Database logs
kubectl logs -f -l app=postgres-db-pod

# Specific pod logs
kubectl logs -f <pod-name>

# Deployment logs
kubectl logs -f deployment/display-deployment
```

#### Apply configuration changes
```bash
# After modifying a YAML file
kubectl apply -f k8s/display-deployment.yaml

# Kubernetes will automatically redeploy pods
```

#### Restart a deployment
```bash
kubectl rollout restart deployment/display-deployment
kubectl rollout restart deployment/db-deployment
```

#### Delete resources
```bash
# Delete specific component
kubectl delete -f k8s/display-deployment.yaml

# Delete everything
kubectl delete -f k8s/
```

#### Access a pod (debugging)
```bash
# Open a shell in a pod
kubectl exec -it <pod-name> -- /bin/bash

# Execute a command in a pod
kubectl exec <pod-name> -- psql -U user_meteo -d db_meteo -c "SELECT * FROM mesures;"
```

#### View events
```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### Get LoadBalancer service URL
```bash
kubectl get service display-service
```

### Connect to Database from a Pod

```bash
# Find database pod name
kubectl get pods -l app=postgres-db-pod

# Connect to database
kubectl exec -it <db-pod-name> -- psql -U user_meteo -d db_meteo
```

### Stop Kubernetes Resources (Keep Data)

To stop pods and services while keeping data for later:

```bash
# Stop deployments and services (data in PVC is preserved)
kubectl delete -f k8s/collector-deployment.yaml \
                -f k8s/display-deployment.yaml \
                -f k8s/db-deployment.yaml \
                -f k8s/display-service.yaml \
                -f k8s/db-service.yaml
```

**Important:** Do NOT delete `db-pvc.yaml` if you want to keep your data.

To restart later:
```bash
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/db-service.yaml
kubectl apply -f k8s/collector-deployment.yaml
kubectl apply -f k8s/display-deployment.yaml
kubectl apply -f k8s/display-service.yaml
```

---

## 🔧 Development

### Project Structure

```
station-meteo/
├── collector/           # Data collection service
│   ├── main.py         # Main script
│   ├── Dockerfile      # Docker image
│   └── requirements.txt # Python dependencies
├── webapp/             # Flask web application
│   ├── app.py         # Flask application
│   └── Dockerfile     # Docker image
├── k8s/                # Kubernetes manifests
│   ├── db-deployment.yaml
│   ├── db-service.yaml
│   ├── db-pvc.yaml
│   ├── collector-deployment.yaml
│   ├── display-deployment.yaml
│   └── display-service.yaml
├── docker-compose.yml  # Docker Compose configuration
├── .env               # Environment variables (create this)
├── .env.example       # Environment variables template
└── README.md          # This file
```

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `DB_HOST` | Database hostname | `localhost` (Docker) / `db` (K8s) |
| `POSTGRES_USER` | PostgreSQL user | `user_meteo` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `password123!` |
| `POSTGRES_DB` | Database name | `db_meteo` |

### Modify Code

1. **Modify Python code**: Edit files in `collector/` or `webapp/`
2. **Rebuild image** (Docker Compose):
   ```bash
   docker-compose up -d --build
   ```
3. **Rebuild and deploy** (Kubernetes):
   ```bash
   # 1. Rebuild Docker image and push to your registry
   # 2. Update image in deployment YAML
   # 3. Apply changes
   kubectl apply -f k8s/display-deployment.yaml
   ```

---

## 🐛 Troubleshooting

### PostgreSQL Authentication Error

**Symptom:** `password authentication failed for user "user_meteo"`

**Solution:**
1. Check that the `.env` file exists and contains correct values
2. Check that there are no spaces around `=` in `.env`
3. For Docker Compose: delete volume and restart
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```
4. For Kubernetes: check that environment variables are properly defined in deployments

### Service Cannot Resolve Database Hostname (Kubernetes)

**Symptom:** `could not translate host name "db-service" to address`

**Solution:** Check that:
- The service name in `db-service.yaml` matches the `DB_HOST` value in the deployment
- The service is created: `kubectl get services`
- Pods are in the same namespace

### Logs Not Displaying

**Solution:** Use `-f` to follow logs in real-time:
```bash
kubectl logs -f -l app=display-pod
docker-compose logs -f collector
```

---

## 📝 Notes

- The collector inserts data every 10 seconds
- The webapp displays the last 10 measurements
- Data is persistent (Docker volume or Kubernetes PVC)
- In production, change default passwords!
