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

## License

[Add license information]