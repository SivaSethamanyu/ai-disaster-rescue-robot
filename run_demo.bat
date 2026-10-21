@echo off
title AI Disaster Rescue Robot Using A* and Multi-Agent Planning
color 0b
echo =====================================================================
echo    AI DISASTER RESCUE ROBOT USING A* AND MULTI-AGENT PLANNING
echo    AI Case Study Project - VIT Vellore
echo    Presented by: Haritha (24BCE0412)
echo =====================================================================
echo.
echo Starting Pygame simulation...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Simulation exited with an error. Please verify python and pygame are installed.
    pause
)
