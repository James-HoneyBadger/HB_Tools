# HB Tools

A Python-based Integrated Development Environment (IDE) that copies the setup and functionality of PeopleTools 7.

## Overview

HB Tools provides a desktop application with tools similar to Oracle's PeopleTools, including:

- **Application Designer**: Visual design interface for applications
- **PeopleCode Editor**: Code editor for scripting
- **Data Mover**: Data import/export functionality
- **Query Tool**: Query building and execution
- **Process Scheduler**: Batch process management

## Prerequisites

- Python 3.8 or higher
- PyQt5 (installed via pip)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/James-HoneyBadger/HB_Tools
   cd HB_Tools
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Features

- **Application Designer**: Visual form designer with toolbar to add labels, text edits, and buttons to a design canvas
- **PeopleCode Editor**: Code editor with Python syntax highlighting
- **Data Mover**: Import/export data from CSV and JSON files, displayed in a table
- **Query Tool**: Query builder with table selection, SQL generation, and mock execution with sample results
- **Process Scheduler**: Add and manage scheduled tasks with manual execution

## Features

- Tabbed interface for different tools
- Basic implementations of PeopleTools-inspired functionality
- Windows-native desktop application using PyQt5

## Development

The application uses [PyQt5](https://pypi.org/project/PyQt5/) for the GUI framework.

### Project Structure

- `main.py`: Main application logic
- `requirements.txt`: Python dependencies

## Building

No build step required - run directly with Python after installing dependencies.

## License

[Add license information]