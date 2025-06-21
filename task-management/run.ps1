# run.ps1

# Path to your venv activate script
$venvActivate = ".\task_env\Scripts\Activate.ps1"

# Activate virtual environment in this session
& $venvActivate

# Run migrations
# python manage.py migrate

# Start Tailwind watcher in a new PowerShell window with venv activated
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { . $pwd\$venvActivate; cd theme; npm run dev }"

# Run Django server in current window
python manage.py runserver




# # run.ps1
# $venvActivate = ".\task_env\Scripts\Activate.ps1"

# Start-Job -ScriptBlock {
#     param($activatePath)
#     & $activatePath
#     python manage.py tailwind start
# } -ArgumentList $venvActivate

# python manage.py runserver

