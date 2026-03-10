# py-01-first

A Python project designed to test development workflows within Dev Containers, specifically focusing on Podman integration on systems like Fedora Silverblue.

## Development

This project is configured to run in a VS Code Dev Container. 

### Podman Specifics
When using Podman for dev containers, the following configurations in `devcontainer.json` are used to handle rootless user namespaces and SELinux on Silverblue:
- `--userns=keep-id`: Maps the user inside the container to the same UID as the host user.
- `--security-opt label=disable`: Disables SELinux labeling for the container to avoid permission issues with volume mounts.

## Deployment

The project uses a standard `Dockerfile` that is compatible with both Docker and Podman.

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Usage

| Tool | Build | Run |
| :--- | :--- | :--- |
| **Docker** | `docker build -t myapp .` | `docker run -p 8000:8000 myapp` |
| **Podman** | `podman build -t myapp .` | `podman run -p 8000:8000 myapp` |
| **Docker Compose** | — | `docker compose up` |
| **Podman Compose** | — | `podman-compose up` |

### Key Differences from Dev Container
* **No `--userns=keep-id`**: Not needed for production images.
* **No `--reload`**: The production command excludes the `--reload` flag used during development.
* **Root User**: The production `Dockerfile` runs as root inside the container by default. Host isolation provides the necessary security, unlike the development environment which often requires specific user mapping.

### Orchestration
An optional `docker-compose.yml` (also compatible with `podman-compose`) can be used:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    restart: unless-stopped
```
