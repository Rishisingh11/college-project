@echo off
echo 🚀 College Blind Date App - Quick Deploy to Heroku
echo ================================================

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Heroku CLI not found. Please install it from: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

REM Check if git is initialized
if not exist ".git" (
    echo 📝 Initializing git repository...
    git init
)

REM Generate secret key and prepare environment
echo 🔑 Generating secure secret key...
python deploy_helper.py

echo.
set /p APP_NAME="🏷️  Enter your Heroku app name (e.g., my-blind-date-app): "

if "%APP_NAME%"=="" (
    echo ❌ App name is required!
    pause
    exit /b 1
)

echo.
echo 📦 Committing files to git...
git add .
git commit -m "Ready for Heroku deployment"

echo.
echo 🌐 Creating Heroku app...
heroku create %APP_NAME%

echo.
echo 🔧 Setting environment variables...
for /f "tokens=2 delims==" %%i in ('findstr "SECRET_KEY" .env') do set SECRET_KEY=%%i
heroku config:set SECRET_KEY=%SECRET_KEY% --app %APP_NAME%

echo.
echo 🚀 Deploying to Heroku...
git push heroku main

echo.
echo 🎉 Deployment complete!
echo 🌍 Your app is live at: https://%APP_NAME%.herokuapp.com
echo.
echo Opening your app...
heroku open --app %APP_NAME%

pause