# Data Science 3A App

This is a simple Streamlit-based application deployed with Kubernetes using ArgoCD. It includes a chat interface (`conversation`) and a sidebar component (`sidebar`), and is styled with a basic custom CSS.

## Project Structure

```
.
├── components/
│   ├── conversation.py       # Chat UI and logic
│   └── sidebar.py            # Sidebar UI
├── manifests/
│   ├── deployment.yaml       # Kubernetes deployment manifest
│   ├── service.yaml          # Kubernetes service manifest
├── main.py                   # Streamlit app entry point
├── main.css                  # Custom CSS styles
├── application.yaml          # ArgoCD application manifest
├── Dockerfile                # Docker image definition
├── LICENSE
```

## Getting Started

### Prerequisites

- Python 3
- Docker
- (Optional) Kubernetes cluster with ArgoCD
- Credentials to SSP Cloud required.

### Setup the environment

In order to access the database, you have to create a .env file and write your credentials:
```bash
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=...
```

### Setup with Python

```bash
python3 -m venv .myenv
source .myenv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

### Setup with Docker

```bash
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

### Setup with Kubernetes + ArgoCD (Optional)

```bash
minikube start
export KUBECONFIG=`ls ~/.kube/config`

# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Port forward and login
kubectl get pods -n argocd
kubectl port-forward svc/argocd-server 8080:443 -n argocd

export PASSWORD=`argocd admin initial-password -n argocd`
argocd login localhost:8080 --username admin --password $PASSWORD -y

# Deploy application
kubectl apply -f application.yaml
```

Open ArgoCD UI at [http://localhost:8080](http://localhost:8080) to monitor your deployment.

## Kubernetes Manifests

- **Deployment**: Runs the app container on port 8080.
- **Service**: Exposes the app within the cluster on port 8080.
- **Application**: ArgoCD definition for syncing with the Git repo and deploying manifests.

## Components

- `conversation.py`: Handles chat message input/output.
- `sidebar.py`: Renders a sidebar UI with interactive elements.
- `main.css`: Contains styles for layout and hover effects of chat bubbles and buttons.

## License

This project is licensed under the terms of the [MIT license](./LICENSE).
