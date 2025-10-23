# HB Tools

A Rust-based Integrated Development Environment (IDE) that copies the setup and functionality of PeopleTools 7.

## Overview

HB Tools provides a desktop application with tools similar to Oracle's PeopleTools, including:

- **Application Designer**: Visual design interface for applications
- **PeopleCode Editor**: Code editor for scripting
- **Data Mover**: Data import/export functionality
- **Query Tool**: Query building and execution
- **Process Scheduler**: Batch process management

## Prerequisites

- Rust (installed via rustup)
- Visual Studio Build Tools 2022 with C++ workload (for MSVC linker on Windows)

## Installation

1. Install Rust:
   ```powershell
   Invoke-WebRequest -Uri https://win.rustup.rs -OutFile rustup-init.exe
   .\rustup-init.exe -y
   ```

2. Install Visual Studio Build Tools:
   - Download and install Visual Studio Build Tools 2022
   - Select the "Desktop development with C++" workload

3. Clone the repository:
   ```bash
   git clone https://github.com/James-HoneyBadger/HB_Tools
   cd HB_Tools
   ```

4. Build and run:
   ```bash
   cargo build --release
   cargo run --release
   ```

## Development

The application uses [egui](https://github.com/emilk/egui) for the GUI framework, providing an immediate mode interface.

### Project Structure

- `src/main.rs`: Main application logic
- `Cargo.toml`: Dependencies and project configuration

## Features

- Tabbed interface for different tools
- Basic text editor for PeopleCode
- Placeholder interfaces for other tools
- Windows-native desktop application

## Building

Ensure the Visual Studio environment is set up:

```powershell
& "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1"
cargo build
```

## Troubleshooting

### Linker Errors on Windows

If you encounter `linker 'link.exe' not found` errors:

1. Ensure Visual Studio Build Tools 2022 is installed with the "Desktop development with C++" workload
2. For ARM64 Windows systems, the MSVC linker may not be available. Consider:
   - Using Windows Subsystem for Linux (WSL) with GNU toolchain
   - Cross-compiling from an x86_64 Windows machine
   - Using an alternative Rust target if available

### Environment Setup

To verify the build environment:

```powershell
# Check Rust installation
rustc --version
cargo --version

# Check if linker is available
where link.exe
```

## License

[Add license information]