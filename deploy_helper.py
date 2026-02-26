#!/usr/bin/env python3
"""
Deployment Helper Script for College Blind Date App
Run this script to prepare your app for production deployment.
"""

import secrets
import os
import subprocess
import sys

def generate_secret_key():
    """Generate a cryptographically strong secret key."""
    return secrets.token_hex(32)

def check_git():
    """Check if git is initialized."""
    return os.path.exists('.git')

def init_git():
    """Initialize git repository."""
    try:
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize git repository")
        return False

def create_env_file():
    """Create .env file with secure settings."""
    secret_key = generate_secret_key()
    env_content = f"""# Production Environment Variables
SECRET_KEY={secret_key}
FLASK_ENV=production
PORT=5000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with secure secret key")
    print(f"🔑 Your secret key: {secret_key}")
    return secret_key

def main():
    print("🚀 College Blind Date App - Deployment Helper")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    print("📋 Pre-deployment checklist:")
    
    # 1. Check git
    if check_git():
        print("✅ Git repository found")
    else:
        print("⚠️  Git not initialized. Initializing...")
        if not init_git():
            sys.exit(1)
    
    # 2. Create .env file
    if os.path.exists('.env'):
        print("⚠️  .env file already exists")
        choice = input("Do you want to create a new one? (y/n): ")
        if choice.lower() == 'y':
            secret_key = create_env_file()
        else:
            print("ℹ️  Keeping existing .env file")
            secret_key = "existing-key"
    else:
        secret_key = create_env_file()
    
    # 3. Check requirements
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt found")
    else:
        print("❌ requirements.txt missing")
        sys.exit(1)
    
    # 4. Check Procfile
    if os.path.exists('Procfile'):
        print("✅ Procfile found")
    else:
        print("❌ Procfile missing")
        sys.exit(1)
    
    print("\n🎉 Your app is ready for deployment!")
    print("\n📝 Next Steps:")
    print("1. Choose a hosting platform (see DEPLOYMENT.md)")
    print("2. For Heroku deployment, run:")
    print("   git add .")
    print("   git commit -m 'Ready for deployment'")
    print("   heroku create your-app-name")
    print(f"   heroku config:set SECRET_KEY={secret_key}")
    print("   git push heroku main")
    print("\n📖 See DEPLOYMENT.md for detailed instructions!")

if __name__ == "__main__":
    main()