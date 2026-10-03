# Windows Setup

This guide explains how to set up the Design Your Chip 2027 development environment on Windows 11.

The environment uses WSL2 and Docker Desktop to run Linux-based EDA tools. Graphical applications are displayed directly on Windows through WSLg.

**Status:** Under testing.

## 1. Install WSL2

Open PowerShell and execute:

```powershell
wsl --install -d Ubuntu
```

Restart Windows if requested.

Launch Ubuntu and complete the initial user setup.

Verify that Ubuntu uses WSL2:

```powershell
wsl --list --verbose
```

Update WSL:

```powershell
wsl --update
```

For more information, see the [official WSL documentation](https://learn.microsoft.com/windows/wsl/install).

## 2. Install Docker Desktop

Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Open Docker Desktop and verify the following settings:

**Settings → General**

Enable the WSL2-based engine, if the option is available.

**Settings → Resources → WSL Integration**

Enable integration with your Ubuntu distribution.

Apply the changes if necessary.

From the Ubuntu WSL terminal, verify Docker:

```bash
docker info
```

Docker should be accessible directly from Ubuntu.

## 3. Verify WSLg

WSLg allows Linux graphical applications to display windows directly on the Windows desktop.

From Ubuntu WSL:

```bash
echo "$DISPLAY"
ls -la /mnt/wslg/.X11-unix/
ls -la /tmp/.X11-unix/
```

Optionally, verify that a graphical application works:

```bash
sudo apt update
sudo apt install -y x11-apps
xclock
```

A clock window should appear on the Windows desktop.

Close the application after testing.

## 4. Clone the Repository

Install Git inside Ubuntu if necessary:

```bash
sudo apt update
sudo apt install -y git
```

Clone the repository:

```bash
mkdir -p ~/projects
cd ~/projects

git clone <REPOSITORY_URL>
cd design-your-chip-2627
```

**Important:** Store the project in the WSL Linux filesystem, such as `~/projects/`, rather than under `/mnt/c/`.

## 5. Start the Development Container

### Option A: Visual Studio Code

1. Install [Visual Studio Code](https://code.visualstudio.com/) on Windows.
2. Install the **WSL** and **Dev Containers** extensions.
3. Ensure Docker Desktop is running.

From the Ubuntu WSL terminal:

```bash
cd ~/projects/design-your-chip-2627
code .
```

Ensure VS Code is connected to Ubuntu through WSL.

Open the Command Palette (`Ctrl+Shift+P`) and select:

**Dev Containers: Reopen in Container**

Choose:

**Design Your Chip 2027 - Windows**

The development image will be downloaded if necessary.

### Option B: Dev Container CLI

Install Node.js and npm inside Ubuntu WSL if required.

From the repository directory, execute:

```bash
npx --yes @devcontainers/cli up \
  --workspace-folder . \
  --config .devcontainer/windows/devcontainer.json
```

Enter the container:

```bash
npx --yes @devcontainers/cli exec \
  --workspace-folder . \
  --config .devcontainer/windows/devcontainer.json \
  bash
```

## 6. Next Step: Verification

Once the development container is running, follow the **[Verification Guide](../verification.md)**.

The verification includes graphical applications, which should appear directly on the Windows desktop through WSLg.
