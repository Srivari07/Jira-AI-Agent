# 🚀 Using UV with JIRA AI Agent

This guide covers using `uv` - a fast Python package installer and resolver written in Rust.

## Why Use uv?

- ⚡ **10-100x faster** than pip
- 🔒 **Better dependency resolution**
- 💾 **Disk space efficient** with global cache
- 🎯 **Drop-in replacement** for pip
- 🔄 **Compatible** with existing projects

## Installation

### Windows
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux/Mac
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Using pip
```bash
pip install uv
```

### Verify Installation
```bash
uv --version
```

## Quick Start with uv

### 1. Create Virtual Environment
```bash
# Create .venv directory
uv venv

# This creates a .venv folder (standard Python venv)
```

### 2. Activate Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install project dependencies
uv pip install -e .

# This reads pyproject.toml and installs everything
```

## Common uv Commands

### Package Management
```bash
# Install a package
uv pip install package-name

# Install specific version
uv pip install package-name==1.2.3

# Install from requirements.txt
uv pip install -r requirements.txt

# Install in editable mode (development)
uv pip install -e .

# Upgrade a package
uv pip install --upgrade package-name

# Uninstall a package
uv pip uninstall package-name
```

### List & Search
```bash
# List installed packages
uv pip list

# Show package details
uv pip show package-name

# Search for packages (not yet supported, use pip)
pip search package-name
```

### Sync & Compile
```bash
# Compile requirements (faster installs)
uv pip compile pyproject.toml -o requirements.txt

# Sync environment to match requirements
uv pip sync requirements.txt
```

### Cache Management
```bash
# Clear uv cache
uv cache clean

# Show cache info
uv cache dir
```

## JIRA AI Agent Setup with uv

### Complete Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/Jira-AI-Agent.git
cd Jira-AI-Agent

# 2. Create virtual environment
uv venv

# 3. Activate environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Install dependencies
uv pip install -e .

# 5. Copy environment file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 6. Edit .env with your credentials
notepad .env  # Windows
nano .env     # Linux/Mac

# 7. Start the application
python main.py backend   # Terminal 1
python main.py frontend  # Terminal 2
```

### Fast Reinstall
```bash
# If you need to reinstall everything
uv pip install -e . --refresh
```

### Install Dev Dependencies
```bash
# Install development tools
uv pip install pytest black flake8 mypy
```

## Comparing uv vs pip

| Feature | uv | pip |
|---------|----|----|
| Speed | ⚡ 10-100x faster | ✓ Standard |
| Dependency Resolution | ✓ Modern resolver | ✓ Good |
| Global Cache | ✓ Yes | ❌ No |
| Disk Usage | ✓ Efficient | ❌ Duplicates |
| Compatibility | ✓ Drop-in replacement | ✓ Standard |
| Installation | Separate install | ✓ Built-in |

## Troubleshooting

### uv command not found
```bash
# Make sure uv is in PATH
# Windows: Add to System Environment Variables
# Linux/Mac: Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.cargo/bin:$PATH"
```

### Permission errors
```bash
# Windows: Run as Administrator
# Linux/Mac: Don't use sudo with uv venv
uv venv  # Creates .venv in current directory
```

### Slow downloads
```bash
# uv uses your pip config automatically
# To configure mirrors, edit pip config:
pip config set global.index-url https://pypi.org/simple
```

### Clear cache and reinstall
```bash
# If you have issues
uv cache clean
uv pip install -e . --refresh
```

## Performance Comparison

Example: Installing JIRA AI Agent dependencies

| Tool | Time | Notes |
|------|------|-------|
| uv | ~5-10 seconds | With cache |
| uv | ~20-30 seconds | No cache |
| pip | ~2-3 minutes | Standard install |

## Advanced Usage

### Lock Files
```bash
# Generate lock file for reproducible builds
uv pip compile pyproject.toml -o requirements.lock

# Install from lock file
uv pip install -r requirements.lock
```

### Multiple Python Versions
```bash
# Create venv with specific Python version
uv venv --python 3.10
uv venv --python 3.11
```

### Offline Installation
```bash
# Download packages for offline use
uv pip download -r requirements.txt -d ./packages

# Install offline
uv pip install --no-index --find-links ./packages -r requirements.txt
```

## Migration from pip

If you're currently using pip, migrating to uv is simple:

```bash
# 1. Install uv
pip install uv

# 2. Replace pip with uv pip in all commands
pip install package  →  uv pip install package
pip list            →  uv pip list
pip uninstall       →  uv pip uninstall

# That's it! Everything else stays the same
```

## Configuration

uv respects pip configuration files:

**Windows:** `%APPDATA%\pip\pip.ini`
**Linux/Mac:** `~/.config/pip/pip.conf`

Example config:
```ini
[global]
index-url = https://pypi.org/simple
timeout = 60
```

## Best Practices

1. **Always use virtual environments**
   ```bash
   uv venv  # Create new environment for each project
   ```

2. **Use lock files for production**
   ```bash
   uv pip compile pyproject.toml -o requirements.lock
   ```

3. **Leverage the cache**
   ```bash
   # uv automatically caches packages globally
   # No need to download the same package twice
   ```

4. **Regular updates**
   ```bash
   # Keep uv updated
   pip install --upgrade uv
   ```

5. **Use with CI/CD**
   ```yaml
   # GitHub Actions example
   - name: Install uv
     run: pip install uv
   - name: Install dependencies
     run: uv pip install -e .
   ```

## Resources

- **Official Docs:** https://github.com/astral-sh/uv
- **Installation Guide:** https://astral.sh/uv
- **PyPI:** https://pypi.org/project/uv/

## FAQ

**Q: Can I use both pip and uv?**
A: Yes! They're compatible. uv pip is a drop-in replacement.

**Q: Does uv work with conda?**
A: uv works best with venv. For conda environments, use conda/mamba.

**Q: Is uv production-ready?**
A: Yes! It's stable and widely used. It respects pip standards.

**Q: Will uv replace pip?**
A: uv is a faster alternative. pip remains the standard, but uv offers better performance.

**Q: Does uv work on Windows?**
A: Yes! Full Windows support with PowerShell/CMD.

---

**Tip:** For the best experience with JIRA AI Agent, use uv for all package operations. It's faster and more reliable!
