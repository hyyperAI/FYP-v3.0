try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/openapi.json" -Method Get -UseBasicParsing
    $json = $response.Content | ConvertFrom-Json
    Write-Host "Available paths:"
    $json.paths.PSObject.Properties | ForEach-Object { Write-Host $_.Name }
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
