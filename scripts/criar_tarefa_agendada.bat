@echo off
REM ==========================================================================
REM  Cria (ou atualiza) a tarefa diaria "Scraper Leilao Caixa" no
REM  Agendador de Tarefas do Windows.
REM  Uso:  scripts\criar_tarefa_agendada.bat [HH:MM]     (padrao: 08:00)
REM  - Roda todo dia no horario escolhido, com o seu usuario conectado.
REM  - Se o PC estiver desligado no horario, roda assim que for ligado.
REM ==========================================================================
setlocal

set "HORA=%~1"
if "%HORA%"=="" set "HORA=08:00"
set "TAREFA=Scraper Leilao Caixa"
set "SCRIPT=%~dp0agendar_scraper.bat"

if not exist "%SCRIPT%" (
    echo [ERRO] Nao encontrei "%SCRIPT%".
    exit /b 1
)

echo Criando a tarefa "%TAREFA%" para rodar todo dia as %HORA%...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$acao = New-ScheduledTaskAction -Execute '%SCRIPT%';" ^
  "$gatilho = New-ScheduledTaskTrigger -Daily -At '%HORA%';" ^
  "$config = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 1);" ^
  "Register-ScheduledTask -TaskName '%TAREFA%' -Description 'Busca diaria de imoveis da Caixa (Scraper-leilao-caixa)' -Action $acao -Trigger $gatilho -Settings $config -Force | Out-Null"

if errorlevel 1 (
    echo [ERRO] Nao foi possivel criar a tarefa.
    exit /b 1
)

echo.
echo [OK] Tarefa criada. Ela roda todo dia as %HORA%.
echo.
echo   Testar agora:  schtasks /Run /TN "%TAREFA%"
echo   Ver o log:     type logs\agendador.log
echo   Remover:       schtasks /Delete /TN "%TAREFA%" /F
echo.
exit /b 0
