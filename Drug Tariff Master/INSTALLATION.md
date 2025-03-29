# Installation Guide for Drug Tariff Master

This guide explains how to install and use the Drug Tariff Master package, which follows modern Python packaging standards.

## Installation Options

### Development Installation

If you're working on the code or want to make changes:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd drug-tariff-master
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

   This creates an "editable" installation that allows you to modify the code without reinstalling.

3. Set up your TRUD API key:
   - Create a `.env` file based on `.env.example`
   - Add your TRUD API key: `TRUD_API_KEY=your_actual_key_here`

### Regular Installation

To install the package for regular use:

```bash
pip install git+<repository-url>
```

And set your TRUD API key:
- Linux/macOS: `export TRUD_API_KEY=your_key_here`
- Windows: `set TRUD_API_KEY=your_key_here`

## Verifying Installation

After installation, you should be able to run:

```bash
dmd --help
```

This will display the available commands.

## Running Commands

The main command-line interface provides the following commands:

```bash
# Download dm+d files
dmd download
```

## Using as a Python Package

You can also use the package programmatically in your Python code:

```python
from drug_tariff_master import download_dmd

# Download dm+d files
result = download_dmd.main()
```

## Running Tests

Run all tests:
```bash
python -m unittest discover tests
```

Run a specific test:
```bash
python -m unittest tests.unit.test_download
```

## Package Structure

The package follows a modern Python project structure:

- `pyproject.toml`: Project metadata and build configuration
- `setup.cfg`: Package configuration
- `src/drug_tariff_master/`: Main package source code

This structure ensures the package can be properly installed, dependencies are managed, and entry points are correctly defined. 