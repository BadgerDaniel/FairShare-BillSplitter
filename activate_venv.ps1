# FairShare Bill Splitter - Virtual Environment Activation Script
Write-Host "Activating FairShare Bill Splitter Virtual Environment..." -ForegroundColor Green
Write-Host ""

# Activate the virtual environment
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Virtual environment activated! You can now:" -ForegroundColor Yellow
Write-Host "- Run the Streamlit app: streamlit run FairShareSplitUI1.py" -ForegroundColor Cyan
Write-Host "- Run tests: python test_standalone.py" -ForegroundColor Cyan
Write-Host "- Install packages: pip install package_name" -ForegroundColor Cyan
Write-Host ""
Write-Host "To deactivate, type: deactivate" -ForegroundColor Yellow
Write-Host ""
Write-Host "Current Python path: $(Get-Command python | Select-Object -ExpandProperty Source)" -ForegroundColor Green
Write-Host ""
