Need to run the following command to forward the port to the local machine:

```bash
kubectl apply -f ./de-secret.yaml
kubectl apply -f ./web/deployment.yaml
others
kubectl port-forward deployment/agrosentry-web 8000:8000
```
