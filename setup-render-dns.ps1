# Render DNS Setup Script for SelfMode Platform
# Run as Administrator

Write-Host "🌐 Setting up Render DNS for SelfMode Platform..." -ForegroundColor Green

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Add Render DNS entries to hosts file
Write-Host "Adding Render DNS entries to hosts file..." -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"

$renderEntries = @"

# SelfMode Platform - Render Production
216.24.57.7 selfmode.app
216.24.57.7 www.selfmode.app
216.24.57.251 selfmode.app
216.24.57.251 www.selfmode.app

# Alternative: CNAME resolution
# selfmode.app -> selfmode-platform.onrender.com
"@

# Check if entries already exist
$existingContent = Get-Content $hostsPath -Raw
if ($existingContent -notlike "*216.24.57.7*") {
    Add-Content $hostsPath $renderEntries
    Write-Host "✅ Hosts file updated with Render IPs" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Render entries already exist" -ForegroundColor Yellow
}

# Flush DNS cache
Write-Host "Flushing DNS cache..." -ForegroundColor Yellow
ipconfig /flushdns

Write-Host ""
Write-Host "🎉 Render DNS setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Your SelfMode Platform is now accessible at:" -ForegroundColor White
Write-Host "  - http://selfmode.app (via hosts file)" -ForegroundColor White
Write-Host "  - https://selfmode-platform.onrender.com (direct)" -ForegroundColor White
Write-Host ""
Write-Host "🌐 For production, add this CNAME record in your DNS provider:" -ForegroundColor Yellow
Write-Host "   Type: CNAME" -ForegroundColor White
Write-Host "   Name: @ (or www)" -ForegroundColor White
Write-Host "   Value: selfmode-platform.onrender.com" -ForegroundColor White
Write-Host "   TTL: 300" -ForegroundColor White
Write-Host ""
Write-Host "Note: You may need to restart your browser for changes to take effect." -ForegroundColor Yellow
