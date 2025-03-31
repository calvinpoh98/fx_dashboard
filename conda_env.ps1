# ---- Configurable Variables ----
$envName = "streamlit"  # Change to your preferred environment name
$pythonVersion = "3.10"  # Set your desired Python version
$requirementsPath = "requirements.txt"  # Path to your requirements.txt file

# ---- Set Conda Paths ----
$condaPath = "$env:USERPROFILE\Miniconda3\Scripts\conda.exe"
$condaActivate = "$env:USERPROFILE\Miniconda3\condabin\conda.bat"

# ---- Create Conda Env ----
Write-Host "Creating conda environment '$envName' with Python $pythonVersion..."
& $condaPath create -n $envName python=$pythonVersion -y

# ---- Activate and Install Requirements ----
Write-Host "Installing packages from $requirementsPath..."
cmd /c "`"$condaActivate`" activate $envName && pip install -r $requirementsPath"

Write-Host "Environment '$envName' is ready."
