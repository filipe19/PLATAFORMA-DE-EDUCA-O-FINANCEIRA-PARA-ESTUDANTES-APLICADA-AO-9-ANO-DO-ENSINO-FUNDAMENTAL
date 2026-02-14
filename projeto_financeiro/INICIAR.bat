@echo off
chcp 65001 >nul
title 💰 Meu Futuro Financeiro - Iniciando...

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  💰 MEU FUTURO FINANCEIRO - PLATAFORMA EDUCACIONAL ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo 🚀 Iniciando servidores...
echo.

echo [1/2] Iniciando Backend (porta 5000)...
start "Backend - Porta 5000" cmd /k "cd backend && python servidor_dados.py"
timeout /t 2 >nul

echo [2/2] Iniciando Frontend (porta 8080)...
start "Frontend - Porta 8080" cmd /k "python servidor.py"
timeout /t 2 >nul

echo.
echo ✅ Sistema iniciado!
echo.
echo 📍 Acesse: http://localhost:8080
echo.
echo 💡 Não feche as janelas que abriram!
echo.
echo Pressione qualquer tecla para abrir no navegador...
pause >nul

start http://localhost:8080

exit
