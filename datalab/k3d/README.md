# Kubernetes on your laptop: k3d

k3d runs k3s (a small Kubernetes) inside Docker Desktop. This guide makes a cluster named `de` with one node, puts your own image into it, and runs a CronJob once. The course uses it in P4 ClearAir.

The cluster needs about 700 MB of memory, so it fits an 8 GB laptop when the other stacks are stopped. Run every command in Git Bash, with Docker Desktop running.

## 1. Install k3d and kubectl

```bash
winget install -e --id k3d.k3d --version 5.9.0
winget install -e --id Kubernetes.kubectl --version 1.35.4
```

Close VS Code and open it again, so Git Bash finds the new commands. Then check:

```bash
k3d version
kubectl version --client
```

`k3d version` shows `v5.9.0` and `k3s version v1.35.5-k3s1 (default)`. `kubectl version --client` shows `v1.35.4`. kubectl works with a cluster one minor version older or newer, so 1.35 suits k3s 1.35.

### Which kubectl runs?

Docker Desktop also installs a `kubectl`, and Git Bash may find Docker Desktop's copy first. See every copy, in the order Git Bash searches them:

```bash
which -a kubectl
```

If `kubectl version --client` shows a version older than 1.34, use the winget copy. Take the folder of the line that contains `WinGet`, for example `/c/Users/asha/AppData/Local/Microsoft/WinGet/Links`, and put it first in your PATH:

```bash
echo 'export PATH="/c/Users/asha/AppData/Local/Microsoft/WinGet/Links:$PATH"' >> ~/.bashrc
source ~/.bashrc
kubectl version --client
```

Use your own folder in place of the example.

## 2. Create the cluster

Stop the data lab's stacks you do not need first. Then:

```bash
k3d cluster create de --api-port 127.0.0.1:6550
kubectl get nodes
```

The first time takes 1 to 2 minutes, while Docker downloads the k3s image. `kubectl get nodes` shows one node, `k3d-de-server-0`, with STATUS `Ready`.

- `de` is the cluster's name. k3d also makes kubectl's context `k3d-de` the current one.
- `--api-port 127.0.0.1:6550` makes kubectl talk to the cluster at `https://127.0.0.1:6550`. Without it, kubectl may use the name `host.docker.internal`, which stops working after your laptop changes Wi-Fi.
- k3d also starts a small container named `k3d-de-serverlb` in front of the node. It is part of the cluster.

If you use another cluster later, come back to this one with `kubectl config use-context k3d-de`.

## 3. Put your own image into the cluster

The cluster cannot see the images on your laptop. Build your image with a version tag, then import it:

```bash
docker build -t clearair:0.1.0 .
k3d image import clearair:0.1.0 -c de
```

In your YAML, write `image: clearair:0.1.0` and `imagePullPolicy: IfNotPresent`.

- Import again after every rebuild. Better: give each build a new tag (`0.1.1`), import it, and change the YAML.
- Never use the tag `latest` for an imported image. With `latest`, Kubernetes tries to download the image from Docker Hub and fails.
- Import only images you built. The cluster downloads images such as `python:3.12-slim` from Docker Hub by itself.

Check that the image is inside the node:

```bash
MSYS_NO_PATHCONV=1 docker exec k3d-de-server-0 crictl images | grep clearair
```

It prints a line with `docker.io/library/clearair` and `0.1.0`. `k3d image import` can say `Successfully imported` even when the image did not arrive: in the course team's test this happened with an image that had only been re-tagged, not built. If the line is missing, import the image through a file:

```bash
docker save --platform linux/amd64 -o clearair.tar clearair:0.1.0
k3d image import clearair.tar -c de
rm clearair.tar
```

## 4. Reaching the data lab from a pod

A pod reaches services on your laptop at the name `host.k3d.internal`. So with the data lab's `core` profile running, a pod reaches PostgreSQL at:

```text
postgresql://de:de@host.k3d.internal:5432/clearair
```

Start PostgreSQL first: `docker compose --profile core up -d` in `~/de-kit/datalab`. Keep settings such as this address in a Secret made from an env file, not in the YAML:

```bash
kubectl create secret generic clearair-env --from-env-file=k8s.env
```

## 5. A CronJob, and running it once

A CronJob starts a Job on a schedule. This example runs `psql` once an hour and prints the database's name. Save it as `lab-check.yaml`:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: lab-check
spec:
  schedule: "15 * * * *"
  timeZone: Etc/UTC
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      backoffLimit: 0
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: check
              image: pgvector/pgvector:0.8.7-pg16
              imagePullPolicy: IfNotPresent
              command: ["psql", "postgresql://de:de@host.k3d.internal:5432/clearair", "-c", "SELECT 'reached ' || current_database() AS result;"]
```

Apply it, then start one Job from it now instead of waiting for the schedule:

```bash
kubectl apply -f lab-check.yaml
kubectl get cronjobs
kubectl create job --from=cronjob/lab-check lab-check-now
kubectl wait --for=condition=complete job/lab-check-now --timeout=120s
kubectl logs job/lab-check-now
```

The last command prints `reached clearair`. `kubectl get jobs` shows `lab-check-now` with COMPLETIONS `1/1`. The first run downloads the image into the cluster, which can take a minute.

To run it again, delete the old Job first: `kubectl delete job lab-check-now`. Remove the example with `kubectl delete -f lab-check.yaml`.

## 6. Stop, start and delete

Stop the cluster when you finish for the day, and start it again the next morning. Its CronJobs, Secrets and imported images stay:

```bash
k3d cluster stop de
k3d cluster start de
```

Delete it when the project is over:

```bash
k3d cluster delete de
```

## Git Bash and paths inside pods

Git Bash changes an argument that starts with `/` into a Windows path. Put `MSYS_NO_PATHCONV=1` in front of a `kubectl` or `docker` command that names a path inside a container, for example a pod of your own:

```bash
MSYS_NO_PATHCONV=1 kubectl exec deploy/<name> -- ls /app
```

Never `export` the variable for the whole terminal.

To see which address `host.k3d.internal` points to, read the cluster's DNS entries (no path, so no prefix needed):

```bash
kubectl get configmap coredns -n kube-system -o jsonpath='{.data.NodeHosts}'
```

With Docker Desktop it prints a line such as `192.168.65.254 host.k3d.internal`.

## Troubleshooting

- **kubectl cannot connect** and the error names `host.docker.internal`: the cluster was made without `--api-port 127.0.0.1:6550`. Point kubectl at `127.0.0.1` once: `sed -i 's/host.docker.internal/127.0.0.1/' ~/.kube/config`, then `kubectl get nodes`.
- **`port is already allocated` for 6550**: another cluster uses the port. Run `k3d cluster list`, then delete the old cluster or use `--api-port 127.0.0.1:6551`.
- **`ErrImagePull` or `ImagePullBackOff` for your own image**: the tag in the YAML differs from the imported tag, or the import failed. Check with `crictl images` (step 3) and import through a file.
- **The Job's log says `connection refused` or `could not translate host name`**: start the data lab's `core` profile, and write `host.k3d.internal`, not `localhost`.
- **`error: timed out waiting for the condition`**: look at the pod: `kubectl describe pod -l job-name=lab-check-now`. The `Events` at the end say what went wrong.
- **The laptop is slow**: stop the other stacks. `docker stats --no-stream` shows the cluster's two containers, `k3d-de-server-0` and `k3d-de-serverlb`.

## Versions

| Tool | Version |
|---|---|
| k3d | 5.9.0 |
| k3s (the cluster) | `rancher/k3s:v1.35.5-k3s1`, k3d 5.9.0's default |
| kubectl | 1.35.4 |
