Start-Process powershell -ArgumentList "docker-compose up --build"
Start-Sleep -Seconds 5
Start-Process "http://localhost:8000/login"
