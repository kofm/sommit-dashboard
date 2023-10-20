# Navigate to the directory containing the docker-compose.yml file
Set-Location -Path $PSScriptRoot

# Run docker-compose up command
docker-compose up -d
