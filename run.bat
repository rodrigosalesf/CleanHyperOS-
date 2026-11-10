@echo off
setlocal enabledelayedexpansion
title CleanHyperOS - Otimizador Inteligente Xiaomi
cls

echo ======================================================================
echo                 CleanHyperOS - Inicializador Inteligente
echo ======================================================================
echo.

:: 1. Verificar se Python esta instalado
set "PY_CMD="
where python >nul 2>&1 && set "PY_CMD=python"
if not defined PY_CMD (
    where py >nul 2>&1 && set "PY_CMD=py"
)

if not defined PY_CMD (
    echo [!] Python 3 nao foi encontrado no seu computador.
    echo [*] Iniciando instalacao automatica do Python...
    echo.
    where winget >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        echo [*] Instalando Python via winget (Windows Package Manager)...
        winget install --id Python.Python.3.12 -e --silent --accept-source-agreements --accept-package-agreements
    ) else (
        echo [*] Baixando instalador oficial do Python via PowerShell...
        powershell -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe' -OutFile '%TEMP%\python_installer.exe'; Start-Process -FilePath '%TEMP%\python_installer.exe' -ArgumentList '/quiet InstallAllUsers=0 PrependPath=1' -Wait; Remove-Item '%TEMP%\python_installer.exe'"
    )

    :: Tentar localizar o Python recem-instalado
    for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
        if exist "%%D\python.exe" set "PY_CMD=%%D\python.exe"
    )
    if not defined PY_CMD (
        where python >nul 2>&1 && set "PY_CMD=python"
    )
    if not defined PY_CMD (
        echo.
        echo [X] Nao foi possivel detectar o Python recem-instalado nesta sessao.
        echo [*] Por favor, feche e abra novamente este arquivo (run.bat).
        echo.
        pause
        exit /b 1
    )
)

:: 2. Verificar se ADB esta instalado
where adb >nul 2>&1
if !ERRORLEVEL! neq 0 (
    if exist "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" (
        set "PATH=%LOCALAPPDATA%\Android\Sdk\platform-tools;!PATH!"
    ) else (
        echo [!] ADB (Android Debug Bridge) nao foi encontrado no sistema.
        echo [*] Instalando Google Platform Tools via winget...
        where winget >nul 2>&1
        if !ERRORLEVEL! equ 0 (
            winget install Google.PlatformTools --version 37.0.1 -e --silent --accept-source-agreements --accept-package-agreements
            :: Tentar localizar adb instalado pelo winget se ainda nao estiver no PATH atual
            for /d %%P in ("%LOCALAPPDATA%\Microsoft\WinGet\Packages\Google.PlatformTools*") do (
                if exist "%%P\platform-tools\adb.exe" set "PATH=%%P\platform-tools;!PATH!"
                if exist "%%P\adb.exe" set "PATH=%%P;!PATH!"
            )
        ) else (
            echo [AVISO] O gerenciador winget nao foi encontrado para instalar o ADB automaticamente.
        )
    )
)

echo [OK] Ambiente pronto! Iniciando CleanHyperOS...
echo.
"%PY_CMD%" "%~dp0run_clean_hyperos.py" %*

pause
