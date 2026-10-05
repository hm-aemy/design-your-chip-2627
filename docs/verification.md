# Development Environment Verification

This guide explains how to verify that the Design Your Chip 2027 development environment is working correctly.

Complete the steps below **inside the Dev Container**, after following the setup instructions for your operating system.

## 1. Verify Digital Design Tools

From the root directory of the course repository, execute:

```bash
bash verification/verify-image.sh
```

This script checks the required digital design tools and dependencies provided by the Docker image.

Make sure all verification tests pass before continuing.

## 2. Verify LibreLane

LibreLane and its physical-design tools are provided through Nix.

Activate the LibreLane development environment:

```bash
nix develop librelane/
```

Once inside the Nix development shell, execute:

```bash
librelane --smoke-test
```
> **Note:** Some warnings may appear at the end of the smoke test. These are expected and can be safely ignored, as long as the smoke test completes successfully.

The smoke test checks that the LibreLane environment is working correctly.

After it finishes, exit the Nix shell:

```bash
exit
```

## 3. Verify Graphical Applications

The following tests verify that graphical applications can communicate with the desktop environment.

### Surfer

From the regular Dev Container terminal, execute:

```bash
surfer
```

> **Note** Surfer is having problems in MacOS, if you are in MacOS please use ```gtkwave``` instead of surfer until we fix the problem c:

The Surfer waveform viewer should open in a graphical window.

Close Surfer after verifying that it works.

### OpenROAD

Activate the LibreLane environment:

```bash
nix develop path:/opt/librelane
```

Then launch OpenROAD:

```bash
openroad -gui
```

The OpenROAD graphical interface should appear on your desktop.

Close OpenROAD after verifying that it works.

## Verification Checklist

- [ ] The digital tools verification script passes.
- [ ] LibreLane's smoke test completes successfully.
- [ ] Surfer opens its graphical interface.
- [ ] OpenROAD opens its graphical interface.

If all checks pass, the development environment is ready for the course.

If a test fails, consult the [Troubleshooting Guide](troubleshooting.md).
