# ========== CONFIG ==========
$venvDir = "venv"
$venvActivate = Join-Path $PWD "$venvDir\Scripts\Activate.ps1"
$requirementsFile = Join-Path $PWD "requirements.txt"
$tailwindApp = "theme"
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

# ========== LOAD ENV FROM .env FILE ==========
$envFile = ".env"
$exampleEnvFile = ".env.example"
if (Test-Path $envFile) {
    Write-Host "🌍 Loading environment variables from .env..." -ForegroundColor DarkCyan
    Get-Content $envFile | ForEach-Object {
        $_ = $_.Trim()
        if ($_ -match "^\s*([^#=]+)\s*=\s*(.*)$") {
            $key = $matches[1].Trim()
            $val = $matches[2].Trim('"')
            ${env:$key} = $val
        }
    }
} else {
    Write-Host "⚠ No .env file found — skipping environment loading." -ForegroundColor Yellow
    if (-not (Test-Path $exampleEnvFile)) {
        Write-Host "ℹ️ Creating a sample '.env.example' file..." -ForegroundColor Cyan
        @"
# Sample environment variables for your Django project
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
"@ | Out-File $exampleEnvFile -Encoding UTF8
    } else {
        Write-Host "ℹ️ '.env.example' already exists." -ForegroundColor Green
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

# ========== INSTALL TAILWIND IF NEEDED ==========
$tailwindNodeModules = Join-Path $PWD "$tailwindApp/static_src/node_modules"
if (-Not (Test-Path $tailwindNodeModules)) {
    Write-Host "📦 Tailwind not found — installing..." -ForegroundColor Cyan
    Run-Cmd "python manage.py tailwind install" "Tailwind install"
} else {
    Write-Host "✅ Tailwind already installed — skipping install" -ForegroundColor Green
}

# ========== ENSURE MIGRATIONS INIT IN ALL APPS ==========
Write-Host "🔍 Ensuring all apps have a 'migrations/__init__.py'..." -ForegroundColor Cyan
Get-ChildItem -Recurse -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "models.py")
} | ForEach-Object {
    $migrationsDir = Join-Path $_.FullName "migrations"
    $initFile = Join-Path $migrationsDir "__init__.py"
    if (-Not (Test-Path $migrationsDir)) {
        New-Item -ItemType Directory -Path $migrationsDir | Out-Null
        Write-Host "📁 Created migrations/ in '$($_.Name)'"
    }
    if (-Not (Test-Path $initFile)) {
        New-Item -ItemType File -Path $initFile | Out-Null
        Write-Host "📄 Created __init__.py in '$($_.Name)/migrations'"
    }
}

# ========== MAKE MIGRATIONS IF NEEDED ==========
Write-Host "🛠 Checking for model changes (makemigrations)..." -ForegroundColor Cyan
try {
    $pendingMigrations = python manage.py makemigrations --check --dry-run 2>&1
    if ($pendingMigrations -match "No changes detected") {
        Write-Host "✅ No new migrations needed." -ForegroundColor Green
    } else {
        Run-Cmd "python manage.py makemigrations" "Make migrations"
    }
} catch {
    Fail "makemigrations failed: $_"
}

# ========== AUTO SQUASH ==========
Write-Host "🔧 Checking for squashable apps..." -ForegroundColor Cyan
Get-ChildItem -Recurse -Directory | Where-Object {
    (Test-Path (Join-Path $_.FullName "models.py")) -and
    (Test-Path (Join-Path $_.FullName "migrations"))
} | ForEach-Object {
    $migrations = Get-ChildItem -Path (Join-Path $_.FullName "migrations") -Filter "*.py" | Where-Object {
        $_.Name -notmatch "^__init__\.py$" -and $_.Name -notmatch "squash"
    }
    if ($migrations.Count -gt 10) {
        Write-Host "🔁 Squashing: $($_.Name) ($($migrations.Count) migrations)"
        try {
            Run-Cmd "python manage.py squashmigrations $($_.Name) --noinput" "Squash migrations for $($_.Name)"
        } catch {
            Write-Host "⚠ Could not squash $($_.Name)" -ForegroundColor DarkYellow
        }
    }
}

# ========== SHOW UNAPPLIED MIGRATIONS ==========
Write-Host "📋 Listing migrations..." -ForegroundColor Cyan
Run-Cmd "python manage.py showmigrations" "Show migrations"

# ========== APPLY MIGRATIONS ==========
Write-Host "🗄️ Applying migrations..." -ForegroundColor Cyan
try {
    Run-Cmd "python manage.py migrate" "Run migrate"
} catch {
    Fail "migrate failed: $_"
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

# ========== START DJANGO DEV SERVER ==========
Write-Host "🚀 Starting Django development server on http://127.0.0.1:$djangoPort/ ..." -ForegroundColor Green
try {
    Run-Cmd "python manage.py runserver $djangoPort" "Start Django server"
} finally {
    Write-Host "`n🛑 Stopping Tailwind watcher..." -ForegroundColor Magenta
    if ($tailwindJob.State -eq 'Running') {
        Stop-Job $tailwindJob | Out-Null
    }
    Remove-Job $tailwindJob | Out-Null
}

Write-Host "`n✅ Setup complete!"
Read-Host -Prompt "Press Enter to exit"
