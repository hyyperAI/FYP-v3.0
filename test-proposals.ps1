try {
    Write-Host "=== Getting all proposals ===" -ForegroundColor Cyan
    $response = Invoke-WebRequest -Uri "http://localhost:8000/proposals/" -Method Get -UseBasicParsing
    $json = $response.Content | ConvertFrom-Json
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Total: $($json.total)"
    Write-Host ""
    Write-Host "Proposals:"
    $json.proposals | ForEach-Object { $_ | ConvertTo-Json -Depth 5 | Write-Host }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
