# macOS Setup

This guide explains how to set up the Design Your Chip 2027 development environment on macOS.

The environment uses Docker Desktop to run Linux-based EDA tools. Graphical applications are displayed on the macOS desktop through XQuartz.

Both Apple Silicon and Intel Macs are supported. The Docker image is available natively for both architectures.

**Status:** Under testing.

## 1. Prerequisites

Make sure the following software is installed:

- Git
- Docker Desktop
- XQuartz
- Visual Studio Code with the Dev Containers extension, or Node.js/npm for Dev Container CLI

### Install Git

Git is included with the Xcode Command Line Tools. If Git is not yet available, execute:

```bash
xcode-select --install
```

Alternatively, install Git using [Homebrew](https://brew.sh/):

```bash
brew install git
```

### Install Docker Desktop

Download and install [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/). Select the version that matches your Mac (Apple Silicon or Intel).

Start Docker Desktop and verify that Docker is running:

```bash
docker info
```

## 2. Install and Configure XQuartz

XQuartz is the X11 server for macOS. It displays graphical applications such as Surfer, KLayout, and OpenROAD that run inside the container.

Download and install [XQuartz](https://www.xquartz.org/), or use Homebrew:

```bash
brew install --cask xquartz
```

**Log out and log back in** (or restart your Mac) after the installation.

### Allow Network Connections

The container connects to XQuartz over the network, which is disabled by default.

1. Start XQuartz.
2. Open **XQuartz → Settings → Security**.
3. Enable **Allow connections from network clients**.
4. Quit XQuartz completely (`Cmd+Q`) and start it again. Closing the windows is not enough. The setting only takes effect after a full restart.

Verify that XQuartz now accepts TCP connections on port 6000:

```bash
lsof -nP -iTCP:6000 -sTCP:LISTEN
```

The output should list `X11.bin` listening on `*:6000`. If the output is empty, XQuartz was not fully restarted.

### Allow the Container to Connect

XQuartz rejects connections that are not explicitly allowed. Connections from the container arrive as `localhost`, so allow `localhost` to connect.

This permission is **reset every time XQuartz starts**, including the restart in the previous step. To apply it automatically on each start, create a startup script:

```bash
mkdir -p ~/.xinitrc.d
cat > ~/.xinitrc.d/xhost-localhost.sh << 'EOF'
/opt/X11/bin/xhost +localhost
EOF
chmod +x ~/.xinitrc.d/xhost-localhost.sh
```

Quit and restart XQuartz once more, then verify the setting:

```bash
/opt/X11/bin/xhost
```

The output should include `INET:localhost`.

Alternatively, run the following command manually after each start of XQuartz, before launching graphical applications in the container:

```bash
/opt/X11/bin/xhost +localhost
```

## 3. Clone the Repository

Open a terminal and run:

```bash
git clone <REPOSITORY_URL>
cd design-your-chip-2627
```

## 4. Start the Development Container

Make sure Docker Desktop and XQuartz are running before starting the container.

Choose one of the following methods.

### Option A: Visual Studio Code

1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. Install the **Dev Containers** extension.
3. Ensure Docker Desktop is running.
4. Open the cloned repository in VS Code.
5. Open the Command Palette (`Cmd+Shift+P`).
6. Select **Dev Containers: Reopen in Container**.
7. Select **Design Your Chip 2027 - macOS**, if prompted.

The first launch may require downloading the Docker image.

### Option B: Dev Container CLI

If you prefer working from a terminal, use Dev Container CLI. Install Node.js and npm if required, for example with `brew install node`.

From the repository directory:

```bash
npx --yes @devcontainers/cli up \
  --workspace-folder . \
  --config .devcontainer/macos/devcontainer.json
```

Enter the development container:

```bash
npx --yes @devcontainers/cli exec \
  --workspace-folder . \
  --config .devcontainer/macos/devcontainer.json \
  bash
```

Both approaches use the same Docker image and development tools.

## 5. Next Step: Verification

Once the development container is running, follow the **[Verification Guide](../verification.md)** to verify the digital design tools, LibreLane, and graphical applications.

Graphical applications should appear on the macOS desktop as XQuartz windows.

### Troubleshooting

Inside the container, `DISPLAY` must be set to `host.docker.internal:0`. Check it with `echo $DISPLAY`. If it shows a different value, rebuild the container.

**`Can't open display: host.docker.internal:0`** (without further messages): The container cannot reach XQuartz. Check that:

- XQuartz is running.
- **Allow connections from network clients** is enabled in the XQuartz settings.
- XQuartz was fully restarted afterwards: `lsof -nP -iTCP:6000 -sTCP:LISTEN` must show `X11.bin`.

**`Authorization required, but no authorization protocol specified`**: The container reaches XQuartz, but the connection is rejected. Run `/opt/X11/bin/xhost +localhost` on the Mac, or set up the startup script described in [Allow the Container to Connect](#allow-the-container-to-connect).
