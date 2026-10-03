# Linux Setup

This guide explains how to set up the Design Your Chip 2027 development environment on Linux.

The environment supports desktop sessions using X11 (Xorg) or Wayland with XWayland.

## 1. Prerequisites

Make sure the following software is installed:

- Git
- Docker Engine
- Visual Studio Code with the Dev Containers extension, or Node.js/npm for Dev Container CLI
- X11 or XWayland for graphical applications

### Install Docker

Follow the official [Docker Engine installation instructions](https://docs.docker.com/engine/install/) for your Linux distribution.

Verify that Docker is running:

```bash
docker info
```

On Linux, you may need to configure permissions to run Docker without `sudo`. See the [Docker post-installation instructions](https://docs.docker.com/engine/install/linux-postinstall/).

**Note:** Membership in the Docker group grants root-equivalent privileges. Only configure this on a trusted machine.

### Verify the Display Server

The development container uses X11 to display graphical applications such as Surfer, KLayout, and OpenROAD.

Check your graphical environment:

```bash
echo "$XDG_SESSION_TYPE"
echo "$DISPLAY"
ls -la /tmp/.X11-unix/
```

The `DISPLAY` variable should be defined, and an X11 socket should be available.

This works with Xorg and with Wayland desktop environments that provide XWayland.

Some systems may require additional X11 authentication configuration.

## 2. Clone the Repository

Open a terminal and run:

```bash
git clone <REPOSITORY_URL>
cd design-your-chip-2627
```

## 3. Start the Development Container

Choose one of the following methods.

### Option A: Visual Studio Code

1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. Install the **Dev Containers** extension.
3. Ensure Docker is running.
4. Open the cloned repository in VS Code.
5. Open the Command Palette (`Ctrl+Shift+P`).
6. Select **Dev Containers: Reopen in Container**.
7. Select **Design Your Chip 2027 - Linux**, if prompted.

The first launch may require downloading the Docker image.

### Option B: Dev Container CLI

If you prefer working from a terminal, use Dev Container CLI.

From the repository directory:

```bash
npx --yes @devcontainers/cli up \
  --workspace-folder . \
  --config .devcontainer/linux/devcontainer.json
```

Enter the development container:

```bash
npx --yes @devcontainers/cli exec \
  --workspace-folder . \
  --config .devcontainer/linux/devcontainer.json \
  bash
```

Both approaches use the same Docker image and development tools.

## 4. Next Step: Verification

Once the development container is running, follow the **[Verification Guide](../verification.md)** to verify the digital design tools, LibreLane, and graphical applications.
