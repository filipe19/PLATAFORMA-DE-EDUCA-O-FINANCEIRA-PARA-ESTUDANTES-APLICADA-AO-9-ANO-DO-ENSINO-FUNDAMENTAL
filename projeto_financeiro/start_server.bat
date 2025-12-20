@echo off
echo ========================================
echo   Iniciando Servidor - Meu Futuro Financeiro
echo ========================================
echo.
cd /d "%~dp0"
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat
echo.
echo Iniciando servidor na porta 8000...
echo Acesse: http://localhost:8000
echo.
echo Pressione CTRL+C para parar o servidor
echo ========================================
echo.
python backend\app.py
pause
