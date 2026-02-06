# Contributing to Smart Crop Planning System

First off, thank you for considering contributing to the Smart Crop Planning System! It's people like you that make this tool better for farmers everywhere.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```
**Description:**
A clear and concise description of the bug.

**Steps to Reproduce:**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior:**
What you expected to happen.

**Screenshots:**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 10]
- Python version: [e.g. 3.9]
- Django version: [e.g. 6.0.2]
- Browser: [e.g. Chrome 120]

**Additional Context:**
Any other relevant information.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide:

- **Clear title** and description
- **Use case** - Why is this enhancement useful?
- **Proposed solution** - How should it work?
- **Alternatives considered**
- **Screenshots/mockups** if applicable

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Simple issues for beginners
- `help wanted` - Issues that need attention

### Pull Requests

1. **Fork** the repo and create your branch from `main`
2. **Follow** the existing code style
3. **Add tests** if you've added functionality
4. **Update documentation** if you've changed APIs
5. **Ensure** all tests pass
6. **Create** a pull request

**Pull Request Template:**
```
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] I have tested these changes locally
- [ ] All existing tests pass
- [ ] I have added new tests

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
```

## Development Process

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/smart-crop-planner.git
cd smart-crop-planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Coding Standards

**Python/Django:**
- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

**Example:**
```python
def calculate_crop_score(crop_name: str, field: Field, 
                         soil_analysis: SoilAnalysis) -> int:
    """
    Calculate suitability score for a crop based on field conditions.
    
    Args:
        crop_name: Name of the crop to score
        field: Field object with location and characteristics
        soil_analysis: Latest soil analysis for the field
    
    Returns:
        Integer score between 0-100
    """
    score = 50  # Base score
    # ... calculation logic
    return score
```

**Templates:**
- Use semantic HTML5
- Keep templates DRY (Don't Repeat Yourself)
- Use template inheritance
- Follow accessibility best practices
- Mobile-first responsive design

**CSS:**
- Use BEM naming convention
- Keep styles modular
- Avoid !important unless absolutely necessary
- Use CSS variables for theming

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(rotation): add 10-year rotation planning support

Added capability to generate rotation plans for up to 10 years
instead of the previous 5-year limit. Updated UI and validation.

Closes #123
```

```
fix(soil): correct NPK calculation for sandy soil

The phosphorus calculation was using incorrect conversion factor
for sandy soil types. Fixed formula in utils.py.

Fixes #456
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test fields

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

**Writing Tests:**
```python
from django.test import TestCase
from fields.models import Field

class FieldModelTests(TestCase):
    def setUp(self):
        self.field = Field.objects.create(
            name="Test Field",
            size_acres=10,
            soil_type="loam"
        )
    
    def test_field_creation(self):
        """Test field is created correctly"""
        self.assertEqual(self.field.name, "Test Field")
        self.assertEqual(self.field.size_acres, 10)
    
    def test_field_str_representation(self):
        """Test string representation"""
        self.assertEqual(str(self.field), "Test Field")
```

### Documentation

- Update README.md for major features
- Add docstrings to all functions
- Update inline comments when logic changes
- Create/update wiki pages for complex features

## Project Structure Guidelines

### Adding a New App

```bash
python manage.py startapp newapp
```

**Required files:**
- `models.py` - Database models
- `views.py` - View functions/classes
- `urls.py` - URL routing
- `forms.py` - Django forms
- `admin.py` - Admin interface configuration
- `tests.py` - Unit tests

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Check migration SQL
python manage.py sqlmigrate app_name migration_number

# Apply migrations
python manage.py migrate
```

**Migration Best Practices:**
- Always create migrations after model changes
- Review migration files before committing
- Never edit migration files after they're committed
- Use data migrations for complex data transformations

## Areas Needing Contribution

### High Priority
- [ ] Hindi language support
- [ ] Mobile app development
- [ ] Advanced ML yield prediction
- [ ] Market price integration
- [ ] Government scheme notifications

### Medium Priority
- [ ] Additional crop types (vegetables, fruits)
- [ ] Pest and disease tracking
- [ ] Irrigation scheduling
- [ ] Cost-benefit analysis tools
- [ ] Community forum

### Low Priority
- [ ] Dark mode UI
- [ ] Export to more formats
- [ ] Integration with IoT sensors
- [ ] Social media sharing

## Community

- **GitHub Discussions:** Ask questions, share ideas
- **Discord:** Real-time chat with other developers
- **Monthly Calls:** Community sync meetings

## Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Invited to community calls
- Eligible for contributor badge

## Questions?

Feel free to ask questions by:
- Opening a GitHub issue
- Joining our Discord
- Emailing: dev@smartcropplanner.com

---

**Thank you for contributing! 🌾**

Together, we're building something that helps farmers grow better crops and manage their farms more efficiently.
