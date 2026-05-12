# Compila logistic_churn.exe en la raíz del repo (equivalente a `make main`).
# Requisito: g++ en PATH (p. ej. MSYS2 UCRT64 o MinGW64).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command g++ -ErrorAction SilentlyContinue)) {
    Write-Error "g++ no está en PATH. Instala MSYS2 y abre 'UCRT64' / 'MinGW64', o añade ...\msys64\ucrt64\bin al PATH."
}

$sources = @("main.cpp") + (
    Get-ChildItem -Path "src" -Recurse -Filter "*.cpp" |
        Sort-Object FullName |
        ForEach-Object { $_.FullName }
)

$gppArgs = @(
    "-g", "-std=c++20", "-Wall", "-Iinclude",
    "-o", "logistic_churn.exe"
) + $sources

& g++ @gppArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
Write-Host "OK: logistic_churn.exe generado en la raíz del repositorio."
