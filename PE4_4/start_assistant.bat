@echo off
echo === Запуск Flask ассистента ===
start "" cmd /k "cd /d C:\Users\ergon73\PycharmProjects\Zerocoder_PE\PE4_4 && python main.py"

timeout /t 5 >nul

echo === Запуск ngrok на порт 8085 ===
start "" cmd /k "C:\Tools\ngrok.exe http 8085"

echo === Готово. После запуска ngrok скопируй ссылку и вставь в Voiceflow. ===
pause
