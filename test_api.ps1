$headers = @{"Content-Type" = "application/json"}
$body = @{
    "currentPrompt" = "React developer needed for e-commerce website"
    "systemPrompt" = "You are a professional Upwork freelancer"
} | ConvertTo-Json

Write-Host "Testing AI endpoint..."
Write-Host "URL: http://159.65.225.228:8000/ai/generate-instructions"
Write-Host "Body: $body"
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://159.65.225.228:8000/ai/generate-instructions" -Method POST -Body $body -ContentType "application/json"
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
}
