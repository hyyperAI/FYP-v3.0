$body = @{
    "currentPrompt" = "React.js Developer needed for building a modern e-commerce website with payment gateway integration, inventory management, and responsive design. Budget: $500-$1000. Client has 5 previous hires with 4.9 rating."
    "systemPrompt" = "You are an expert Upwork freelancer specializing in web development. Create professional, compelling proposal introductions that highlight relevant skills, show understanding of client needs, and end with a call to action. Keep it under 200 words."
} | ConvertTo-Json

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "TESTING AI GENERATE-INSTRUCTIONS ENDPOINT" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "URL: http://159.65.225.228:8000/ai/generate-instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "Request Body:" -ForegroundColor Yellow
$body | ConvertTo-Json | Write-Host
Write-Host ""
Write-Host "Sending request..." -ForegroundColor Cyan
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://159.65.225.228:8000/ai/generate-instructions" -Method POST -Body $body -ContentType "application/json"
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Response Received" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Generated Instructions:" -ForegroundColor Yellow
    Write-Host ""
    $response.instructions | Write-Host
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host "ERROR!" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}