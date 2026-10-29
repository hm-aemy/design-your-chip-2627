# Troubleshooting

This guide provides solutions to common issues you may encounter while setting up or using the Design Your Chip 2027 development environment.

## Need Help? Open an Issue!

If your question or problem is not covered in this guide, please don't hesitate to [open an issue](https://gitlab.lrz.de/design-your-chip-2027/design-your-chip-environment/-/work_items?sort=created_date&state=opened&first_page_size=20) in this repository.

When reporting an issue, please describe the problem, your operating system, the steps to reproduce it, and any relevant error messages.

**Your feedback and contributions are valuable!** We count on your help to improve this repository and make the learning experience better, not only for this year's course but also for future students.

### 1. openFPGAloader and GNU make installation

Follow the instructions for your operating system.
<details>
    <summary>Linux (Ubuntu/Debian)<summary>

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
    <summary>macOS<summary>

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
    <summary>Windows<summary>

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

