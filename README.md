# py-fastapi

A Python project designed to test development workflows within Dev Containers, specifically focusing on Podman integration on systems like Fedora Silverblue.

![Screenshot](doco/Screenshot%202026-03-10%20at%206.18.55 pm.png)

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

# Dev Container Usage

This project supports multiple Dev Containers for both Docker and Podman. You can select which container to use when opening the workspace in VS Code. When multiple devcontainer configurations are present, VS Code will show a popup allowing you to choose between them (e.g., Docker or Podman). Each configuration is located in its respective folder under `.devcontainer/`.

## Running and Debugging

To run and debug the FastAPI app inside the Dev Container:
- Use the provided launch configuration (`Python: FastAPI (Uvicorn)`) in VS Code. This configuration starts Uvicorn with the debugger attached, enabling breakpoints and interactive debugging.
- Open the Run and Debug panel in VS Code and select the launch config, then click 'Run' or 'Debug'.

## About `postStartCommand`

The `postStartCommand` in the devcontainer configuration (which previously auto-started Uvicorn) is commented out. This is intentional:
- When `postStartCommand` is enabled, Uvicorn starts automatically, but breakpoints in VS Code will not work because the debugger is not attached.
- By commenting it out, you control app startup via the launch configuration, ensuring proper debugging support.

## Quick Steps
1. Open the workspace in VS Code.
2. If prompted, select the desired Dev Container (Docker or Podman).
3. Wait for the container to build and dependencies to install.
4. Open the Run and Debug panel, select `Python: FastAPI (Uvicorn)`, and start debugging.
5. Set breakpoints as needed—these will now be hit during execution.

## Non-Devcontainer Development Using uv (macOS)

If you want to run and debug the FastAPI app natively on macOS without a Dev Container, you can use uv for fast dependency management and execution:

### Setup Steps
1. **Install uv**
   - `brew install uv`

2. **Install dependencies**
   - `uv venv`
   - `uv pip install -r requirements.txt`

Ensure you set the default Python interpreter in VS Code to the one created by uv (`.venv/bin/python`). Hopefully, VS Code will automatically detect it when you open the folder.

4. **Run the FastAPI app**
   - `uvicorn app.main:app --reload --host 0.0.0.0`

5. **Debugging with VS Code**
   - Open VS Code in your project folder.
   - Set breakpoints as needed.
   - Use the existing `Python: FastAPI (Uvicorn)` launch configuration in `.vscode/launch.json`.
   - Start debugging from the Run and Debug panel.

> The launch configuration works for both Dev Container and local development. No changes are needed.

### Example output

When you click the button in the web app to fetch random info, you should see output similar to the following in your terminal where Uvicorn is running:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [6117] using WatchFiles
INFO:     Started server process [6199]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:49595 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /static/style.css HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:49595 - "GET /random-info HTTP/1.1" 200 OK
```

# Appendix: Python 3.14 in Dev Containers

The `mcr.microsoft.com/devcontainers/python:3` image is a floating tag — as of March 2026 it points to Python 3.14, which is not yet supported by the `debugpy` version bundled in the VS Code Python extension. This causes the launch config to silently fail with no useful error message.

Both the devcontainer base image and the `ms-python.debugpy` extension are maintained by Microsoft, but they are not kept in sync — the image was updated to 3.14 before the extension's bundled debugpy supported it.

**Fix:** Pin to a stable version in `devcontainer.json`:

```json
"image": "mcr.microsoft.com/devcontainers/python:3.13"
```

Alternatively, add `debugpy` to `requirements.txt` to install a newer version that overrides the bundled one — but pinning the image is the cleaner fix and prevents the same issue recurring on a future Python bump.


