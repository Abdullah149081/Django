# ========== CONFIG ==========
$venvDir = "venv"
$venvActivate = Join-Path $PWD "$venvDir\Scripts\Activate.ps1"
$requirementsFile = Join-Path $PWD "requirements.txt"
$tailwindDir = Join-Path $PWD "theme"
$tailwindScript = "dev" # npm script name
$djangoPort = 8000

# ========== UTILS ==========
function Fail($msg) {
    Write-Host "`n❌ ERROR: $msg" -ForegroundColor Red
    exit 1
}

function Run-Cmd($cmd, $desc) {
    Write-Host "▶ $desc..." -ForegroundColor Yellow
    try {
        Invoke-Expression $cmd
    } catch {
        Fail "$desc failed: $_"
    }
}

# ========== CHECK PYTHON ==========
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "Python is not installed or not in PATH"
}

# ========== VENV SETUP ==========
if (-Not (Test-Path $venvActivate)) {
    Write-Host "🔧 Creating virtual environment in '$venvDir'..." -ForegroundColor Cyan
    Run-Cmd "python -m venv $venvDir" "Create venv"
    if (-Not (Test-Path $venvActivate)) {
        Fail "Virtual environment creation failed"
    }
}

# ========== ACTIVATE VENV ==========
Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
. $venvActivate

# ========== INSTALL PYTHON DEPENDENCIES ==========
if (Test-Path $requirementsFile) {
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
    Run-Cmd "python -m pip install --upgrade pip" "Upgrade pip"
    Run-Cmd "pip install -r `"$requirementsFile`"" "Install requirements"
} else {
    Write-Host "⚠ No requirements.txt found — skipping Python dependency install" -ForegroundColor Yellow
}

# ========== START TAILWIND WATCHER ==========
Write-Host "🎨 Starting Tailwind watcher in a new PowerShell window..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { . '$venvActivate'; cd '$tailwindDir'; npm run $tailwindScript }"

# ========== START DJANGO SERVER ==========
Write-Host "🚀 Starting Django development server on http://127.0.0.1:$djangoPort/ ..." -ForegroundColor Green
Run-Cmd "python manage.py runserver $djangoPort" "Run Django server"

# ========== DONE ==========
Write-Host "`n✅ Setup complete! Visit http://127.0.0.1:$djangoPort/ to view your app."

# ========== KEEP ALIVE ==========
while ($true) {
    Start-Sleep -Seconds 60
}
