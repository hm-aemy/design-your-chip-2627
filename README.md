# Design Your Chip 2026/2027

Welcome to **Design Your Chip 2027** at Hochschule München!

This repository contains the development environment, exercises, and resources for the course.

Throughout the course, students will explore digital hardware design, simulation, synthesis, FPGA implementation, hardware/software integration, and the ASIC design flow.

## Important Note: Repository Updates

This repository will be continuously updated throughout the course. New learning materials, exercises, and configuration changes may be introduced as needed.

**You must clone this repository using Git. Do not download it as a ZIP file.**

Using Git ensures that you can easily retrieve updates without downloading the entire repository again.

To get the latest course materials, run the following command from your local repository directory:

```bash
git pull
```

Throughout the course, we will explicitly inform you when a git pull is required and provide any additional instructions if necessary.

## Development Environment

To provide a consistent development environment across different operating systems, the course uses **Docker and Dev Containers**.

The environment includes the following tools:

| Tool | Purpose |
|---|---|
| Verilator | SystemVerilog simulation |
| cocotb | Python-based hardware verification |
| Yosys | RTL synthesis |
| Surfer | Waveform visualization |
| OSS CAD Suite | Digital design and FPGA tools |
| LibreLane | RTL-to-GDSII ASIC implementation |
| OpenROAD | Digital physical design |
| KLayout | Layout visualization and inspection |

Digital design tools are provided through OSS CAD Suite, while LibreLane and its physical-design tools are managed using Nix.

**You do not need to install these EDA tools individually on your computer.**

## Getting Started

Follow the setup guide for your operating system:

| Operating System | Setup Guide | Status |
|---|---|---|
| Linux (X11 / Wayland) | [Linux Setup](docs/setup/linux.md) | Tested |
| Windows 11 (WSL2 / WSLg) | [Windows Setup](docs/setup/windows.md) | Testing |
| macOS (XQuartz) | [macOS Setup](docs/setup/macos.md) | Testing |

The development environment supports both Visual Studio Code and terminal-based workflows using Dev Container CLI.

### Verify Your Installation

After completing the setup, follow the **[Verification Guide](docs/verification.md)** to check that the required tools and graphical applications work correctly.

### Troubleshooting

If you encounter problems during installation or verification, consult the [Troubleshooting Guide](docs/troubleshooting.md).

## Resources

- [Dev Containers](https://containers.dev/)
- [Docker](https://docs.docker.com/)
- [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build)
- [LibreLane](https://github.com/librelane/librelane)
- [Nix](https://nixos.org/)
