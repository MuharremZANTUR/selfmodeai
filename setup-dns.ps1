# Windows DNS Setup Script for SelfMode Platform
# Run as Administrator

Write-Host "🌐 Setting up local DNS for SelfMode Platform..." -ForegroundColor Green

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Get current DNS settings
Write-Host "Current DNS settings:" -ForegroundColor Yellow
Get-DnsClientServerAddress | Format-Table -AutoSize

# Set DNS to local server (127.0.0.1) and backup to Google DNS
Write-Host "Setting DNS to local server..." -ForegroundColor Yellow

# Get network adapters
$adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}

foreach ($adapter in $adapters) {
    Write-Host "Configuring adapter: $($adapter.Name)" -ForegroundColor Cyan
    
    # Set DNS servers
    Set-DnsClientServerAddress -InterfaceIndex $adapter.ifIndex -ServerAddresses "127.0.0.1", "8.8.8.8", "8.8.4.4"
    
    Write-Host "✅ DNS configured for $($adapter.Name)" -ForegroundColor Green
}

# Add local hosts entries
Write-Host "Adding local hosts entries..." -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"

$hostsEntries = @"
# SelfMode Platform Local DNS
127.0.0.1 selfmode.local
127.0.0.1 www.selfmode.local
127.0.0.1 selfmode.app
127.0.0.1 www.selfmode.app
127.0.0.1 api.selfmode.local
127.0.0.1 api.selfmode.app
127.0.0.1 admin.selfmode.local
127.0.0.1 admin.selfmode.app
"@

# Check if entries already exist
$existingContent = Get-Content $hostsPath -Raw
if ($existingContent -notlike "*selfmode.local*") {
    Add-Content $hostsPath $hostsEntries
    Write-Host "✅ Hosts file updated" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Hosts entries already exist" -ForegroundColor Yellow
}

# Flush DNS cache
Write-Host "Flushing DNS cache..." -ForegroundColor Yellow
ipconfig /flushdns

Write-Host ""
Write-Host "🎉 DNS setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Your SelfMode Platform is now accessible at:" -ForegroundColor White
Write-Host "  - http://selfmode.local" -ForegroundColor White
Write-Host "  - http://selfmode.app" -ForegroundColor White
Write-Host "  - http://api.selfmode.local" -ForegroundColor White
Write-Host "  - http://admin.selfmode.local" -ForegroundColor White
Write-Host ""
Write-Host "Note: You may need to restart your browser for changes to take effect." -ForegroundColor Yellow
