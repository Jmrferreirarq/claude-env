@echo off
rem Backup semanal do ambiente Claude: sync + push. Corrido pelo Agendador de Tarefas.
"C:\Program Files\Git\bin\bash.exe" "C:\Users\JOSFER~1\claude-env\sync.sh" >> "C:\Users\JOSFER~1\claude-env\backup.log" 2>&1
cd /d "C:\Users\JOSFER~1\claude-env"
git push origin main >> "C:\Users\JOSFER~1\claude-env\backup.log" 2>&1
