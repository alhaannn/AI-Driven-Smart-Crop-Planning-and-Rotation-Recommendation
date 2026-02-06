# 🚀 Quick Setup Guide - For Your Local Development

## You Need to Do This NOW! ⚠️

Since we removed the hardcoded SECRET_KEY from the code, you need to create your own `.env` file to run the project locally.

---

## Step-by-Step Setup

### 1. Copy the Environment Template

Open PowerShell in your project directory and run:

```powershell
copy .env.example .env
```

### 2. Generate a Secure SECRET_KEY

Run this command to generate a secure key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** - it will look something like:
```
django-insecure-a8d#9f$2m*x@4k&7h^3n!9p-v5q+w2e&8k@3m
```

### 3. Edit the .env File

Open the `.env` file (created in step 1) in any text editor and update it:

```env
# Required: Paste the SECRET_KEY you just generated
SECRET_KEY=django-insecure-a8d#9f$2m*x@4k&7h^3n!9p-v5q+w2e&8k@3m

# Development settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: Configure these if needed
TIME_ZONE=Asia/Kolkata
LANGUAGE_CODE=en-us
```

### 4. Install the New Dependency

Since we added `python-dotenv`, install it:

```powershell
pip install python-dotenv
```

### 5. Restart the Django Server

If the server is running, stop it (Ctrl+C) and restart:

```powershell
python manage.py runserver
```

---

## ✅ That's It!

Your local environment is now secure and properly configured. The server should start normally.

---

## 🔒 Important Notes

- **Never commit the `.env` file** to Git (it's already in `.gitignore`)
- **Never share your SECRET_KEY** publicly
- **Generate a new SECRET_KEY** for production deployments
- **Keep your `.env` file private** - it contains sensitive configuration

---

## 🆘 Troubleshooting

### Error: "No module named 'dotenv'"
**Solution:** Run `pip install python-dotenv`

### Error: "SECRET_KEY not found"
**Solution:** Make sure you created the `.env` file and added the SECRET_KEY

### Server Won't Start
**Solution:** 
1. Check that `.env` file exists in the project root
2. Verify SECRET_KEY is set in `.env`
3. Make sure python-dotenv is installed

---

## 📞 Need Help?

Check the main README.md for detailed installation instructions or refer to DEPLOYMENT_SECURITY.md for more information.

---

**Happy Coding! 🌾**
