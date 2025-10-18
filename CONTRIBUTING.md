# Contributing to PyRay

Thank you for your interest in contributing to PyRay! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Om7035/PyRay/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, PyRay version)
   - Code sample if applicable

### Suggesting Features

1. Check if the feature has been suggested in [Issues](https://github.com/Om7035/PyRay/issues)
2. Create a new issue with the "enhancement" label
3. Describe the feature and its use case
4. Provide examples if possible

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/Om7035/PyRay.git
   cd PyRay
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

5. **Run tests**
   ```bash
   python -m pytest tests/
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of changes

## Code Style Guidelines

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Documentation

- Update docstrings for any modified functions
- Update README.md if adding major features
- Add examples for new features
- Keep documentation clear and beginner-friendly

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Test on multiple platforms if possible

## Community Guidelines

- Be respectful and inclusive
- Help others in discussions and issues
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
- Be patient with review process

## Getting Help

- Join our [Discord server](https://discord.gg/pyray)
- Ask questions in [Discussions](https://github.com/Om7035/PyRay/discussions)
- Check the [documentation](docs/)

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- Our website (coming soon)

Thank you for helping make PyRay better!
