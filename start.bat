@echo off
echo ========================================
echo AIMS Project Startup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/5] Setting up Python virtual environment...
if not exist venv (
    echo    Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo    ✅ Virtual environment created
) else (
    echo    ✅ Virtual environment already exists
)

echo [2/5] Installing backend dependencies...
echo    Activating virtual environment and installing packages...
call venv\Scripts\activate.bat
python -m pip install --quiet --upgrade pip
python -m pip install --quiet --requirement backend\requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
echo    ✅ Backend dependencies installed

echo [3/5] Installing frontend dependencies...
cd frontend
if not exist node_modules (
    echo    Installing npm packages...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        cd ..
        pause
        exit /b 1
    )
) else (
    echo    ✅ Dependencies already installed
)
cd ..

echo [4/5] Running Jupyter notebooks to generate ML artifacts...
if not exist backend\artifacts\lgbm_model.pkl (
    echo    Executing notebook pipeline...
    cd backend
    python run_notebooks.py
    if errorlevel 1 (
        echo ERROR: Failed to execute notebooks
        echo You can run them manually with: cd backend ^&^& python run_notebooks.py
        cd ..
        pause
        exit /b 1
    )
    cd ..
) else (
    echo    ✅ ML artifacts already exist (skipping notebook execution)
    echo    To regenerate artifacts, delete backend\artifacts\ and restart
)

echo [5/5] Starting backend server...
start "AIMS Backend" cmd /k "call venv\Scripts\activate.bat && cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

echo [6/6] Starting frontend development server...
start "AIMS Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo AIMS Project Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Note: To regenerate ML artifacts, run:
echo   cd backend ^&^& python run_notebooks.py
echo   or delete backend\artifacts\ and restart
echo.
echo Press any key to exit (servers will keep running)...
pause >nul
