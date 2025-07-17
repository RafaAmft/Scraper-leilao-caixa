@echo off
chcp 65001 >nul
echo.
echo 📧 CONFIGURAÇÃO DO GMAIL
echo ================================
echo.
echo Este script configura o email Gmail para envio de relatórios.
echo A senha de app já está configurada: hfvk igne yago hwou
echo.
echo Pressione qualquer tecla para continuar...
pause >nul

python config/configurar_gmail.py

echo.
echo Pressione qualquer tecla para sair...
pause >nul 