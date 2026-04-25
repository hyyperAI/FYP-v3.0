$body = @{
    currentPrompt = "Write a proposal intro for a web development job"
    systemPrompt = "You are an expert Upwork proposal writer AI."
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/ai/generate-instructions" -Method Post -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 120
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host ""
    Write-Host "Response:"
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
