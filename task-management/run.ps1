# ========== CONFIG ==========
$venvDir = "venv"
$venvActivate = Join-Path $PWD "$venvDir\Scripts\Activate.ps1"
$requirementsFile = Join-Path $PWD "requirements.txt"
$tailwindScript = "start"
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

function Check-Command($cmd, $desc) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Fail "$desc is not installed or not in PATH"
    }
}

# ========== CHECK PYTHON & PIP ==========
Check-Command python "Python"
Check-Command pip "pip"

# ========== VENV SETUP ==========
if (-Not (Test-Path $venvActivate)) {
    Write-Host "🔧 Creating virtual environment in '$venvDir'..." -ForegroundColor Cyan
    Run-Cmd "python -m venv `"$venvDir`"" "Create venv"
    if (-Not (Test-Path $venvActivate)) {
        Fail "Virtual environment creation failed"
    }
}

# ========== ACTIVATE VENV ==========
Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
. $venvActivate

# ========== CHECK DJANGO ==========
try {
    python -m django --version | Out-Null
} catch {
    Write-Host "📦 Installing Django..." -ForegroundColor Cyan
    Run-Cmd "pip install django" "Install Django"
}

# ========== INSTALL PYTHON DEPENDENCIES ==========
if (Test-Path $requirementsFile) {
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
    Run-Cmd "python -m pip install --upgrade pip" "Upgrade pip"
    Run-Cmd "pip install -r `"$requirementsFile`"" "Install requirements"
} else {
    Write-Host "⚠ No requirements.txt found — skipping Python dependency install" -ForegroundColor Yellow
}

# ========== RUN MIGRATIONS ==========
Write-Host "🗄️ Running Django migrations..." -ForegroundColor Cyan
try {
    Run-Cmd "python manage.py migrate" "Run migrations"
} catch {
    Fail "Django migrations failed: $_"
}

# ========== START TAILWIND WATCHER ==========
Write-Host "🎨 Starting Tailwind watcher in background..." -ForegroundColor Blue
$tailwindJob = Start-Job -ScriptBlock {
    param($activatePath)
    & $activatePath
    python manage.py tailwind start
} -ArgumentList $venvActivate

Start-Sleep -Seconds 2
if ($tailwindJob.State -ne 'Running') {
    Receive-Job $tailwindJob -ErrorAction SilentlyContinue
    Fail "Tailwind watcher failed to start"
}

# ========== START DJANGO SERVER ==========
Write-Host "🚀 Starting Django development server on http://127.0.0.1:$djangoPort/ ..." -ForegroundColor Green
try {
    Run-Cmd "python manage.py runserver $djangoPort" "Run Django server"
} finally {
    Write-Host "`n🛑 Stopping Tailwind watcher..." -ForegroundColor Magenta
    if ($tailwindJob.State -eq 'Running') {
        Stop-Job $tailwindJob | Out-Null
    }
    Remove-Job $tailwindJob | Out-Null
}

# ========== DONE ==========
Write-Host "`n✅ Setup complete! Visit http://127.0.0.1:$djangoPort/ to view your app."
Read-Host -Prompt "Press Enter to exit"