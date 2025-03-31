# Set destination and installer URL
$installerUrl = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
$destination = "$env:TEMP\Miniconda3-latest-Windows-x86_64.exe"

# Download the installer
Invoke-WebRequest -Uri $installerUrl -OutFile $destination

# Install Miniconda silently to default location
Start-Process -FilePath $destination -ArgumentList "/InstallationType=JustMe", "/AddToPath=1", "/RegisterPython=1", "/S", "/D=$env:USERPROFILE\Miniconda3" -Wait

# Initialize conda (optional, helpful for scripting)
& "$env:USERPROFILE\Miniconda3\Scripts\conda.exe" init powershell