# Troubleshooting

This guide provides solutions to common issues you may encounter while setting up or using the Design Your Chip 2027 development environment.

## Need Help? Open an Issue!

If your question or problem is not covered in this guide, please don't hesitate to [open an issue](https://github.com/hm-aemy/design-your-chip-2627/issues/new) in this repository.

When reporting an issue, please describe the problem, your operating system, the steps to reproduce it, and any relevant error messages.

**Your feedback and contributions are valuable!** We count on your help to improve this repository and make the learning experience better, not only for this year's course but also for future students.

## openFPGAloader and GNU make installation

Follow the instructions for your operating system.

<details>
<summary>Linux (Ubuntu/Debian)</summary>

Open a terminal on your Linux host and execute:

```
sudo apt update
sudo apt install make openfpgaloader
```

Verify the installation:

```
make --version
openFPGALoader --version
```

</details>

<details>
<summary>macOS</summary>

Install Homebrew if it is not already available.

Install openFPGALoader:

```
brew install openfpgaloader
```

GNU Make is normally available after installing the Xcode Command Line Tools.

If make is not installed, execute:

```
xcode-select --install
```

Verify both tools:

```
make --version
openFPGALoader --version
```

</details>

<details>
<summary>Windows</summary>

For Windows, we recommend using MSYS2 to install openFPGALoader and GNU Make.

Step 1: Install MSYS2

Download and install MSYS2 from:

```
https://www.msys2.org/
```

Step 2: Open the MSYS2 UCRT64 terminal

From the Windows Start menu, launch:

MSYS2 UCRT64

Step 3: Update MSYS2

```
pacman -Syu
```

If the terminal asks you to close and reopen it, do so and run the update again.

Step 4: Install the required tools

```
pacman -S make mingw-w64-ucrt-x86_64-openFPGALoader
```

Verify the installation:

```
make --version
openFPGALoader --version
```

Step 5: USB drivers

Depending on the FPGA board and the installed Windows drivers, additional USB driver configuration may be necessary.

If openFPGALoader cannot detect the connected FPGA, check the USB driver configuration and consult the openFPGALoader documentation.

Important: Run the FPGA programming commands from the MSYS2 UCRT64 terminal, outside the Dev Container.

</details>

## Updating the Dev Container Docker Image

If your Dev Container is using an outdated Docker image, you may encounter missing tools, commands, or features.

The Dev Container uses the following Docker image:

```bash
ghcr.io/hm-aemy/librelane-base-image:latest
```

Even though the image is tagged as `latest`, Docker does not automatically download newer versions if the image already exists locally.

To update your environment, follow one of the methods below.

<details>
<summary>Option 1: Using VS Code</summary>

1. Open your project in VS Code.
2. Open the Command Palette (`Ctrl+Shift+P` on Linux/Windows or `Cmd+Shift+P` on macOS).
3. Run **Dev Containers: Rebuild Container Without Cache**.
4. Wait for the container to be recreated.

**Note:** If VS Code continues using the old image, manually download the latest version using:

```bash
docker pull ghcr.io/hm-aemy/librelane-base-image:latest
```

Then run **Dev Containers: Rebuild Container** from the Command Palette.

</details>

<details>
<summary>Option 2: Using Dev Container CLI</summary>

Open a terminal **outside the Dev Container**, in your project directory.

First, download the latest Docker image:

```bash
docker pull ghcr.io/hm-aemy/librelane-base-image:latest
```

Then recreate the Dev Container:

```bash
devcontainer up \
  --workspace-folder . \
  --config .devcontainer/linux/devcontainer.json \
  --remove-existing-container
```

Replace `linux` with `macos` or `windows` depending on your operating system.

Finally, enter the updated container:

```bash
devcontainer exec \
  --workspace-folder . \
  --config .devcontainer/linux/devcontainer.json \
  bash
```

</details>

### Important Notes

- **Rebuilding or recreating the container does not delete your project files**, provided they are stored in the mounted project workspace.
- Changes made directly inside the container, outside persistent volumes, may be lost.
- You do not need to delete the old Docker image manually.
- Always execute `docker pull` from your host operating system, not from inside the Dev Container.
