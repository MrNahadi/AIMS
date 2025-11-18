@echo off
echo ========================================
echo AIMS Project Cleanup
echo ========================================
echo.

REM Backend cleanup
echo [1/4] Cleaning backend artifacts...
if exist backend\artifacts rmdir /s /q backend\artifacts
if exist backend\__pycache__ rmdir /s /q backend\__pycache__
if exist backend\.pytest_cache rmdir /s /q backend\.pytest_cache
if exist backend\models\__pycache__ rmdir /s /q backend\models\__pycache__
if exist backend\services\__pycache__ rmdir /s /q backend\services\__pycache__
if exist backend\tests\__pycache__ rmdir /s /q backend\tests\__pycache__
echo    ✅ Backend cleaned

REM Frontend cleanup
echo [2/4] Cleaning frontend build artifacts...
if exist frontend\build rmdir /s /q frontend\build
if exist frontend\node_modules rmdir /s /q frontend\node_modules
echo    ✅ Frontend cleaned

REM Notebook cleanup
echo [3/4] Cleaning notebook checkpoints...
if exist notebooks\.ipynb_checkpoints rmdir /s /q notebooks\.ipynb_checkpoints
echo    ✅ Notebooks cleaned

REM Test artifacts cleanup
echo [4/4] Cleaning test artifacts...
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist __pycache__ rmdir /s /q __pycache__
del /q *.pyc 2>nul
echo    ✅ Test artifacts cleaned

echo.
echo ========================================
echo Cleanup complete!
echo ========================================
pause
