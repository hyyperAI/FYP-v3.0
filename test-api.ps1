$body = @{
    currentPrompt = "Write a proposal intro for a web development job"
    systemPrompt = "You are an expert Upwork proposal writer AI. Your task is to generate highly effective, personalized cover letter instructions for Upwork job proposals.`n`nGuidelines:`n- Write in a professional, engaging tone`n- Focus on the client's specific needs mentioned in their job posting`n- Keep it concise but impactful (3-4 paragraphs max)`n- Include natural opening hooks that grab attention`n- Avoid generic templates - make each response tailored`n- Never reveal you are an AI"
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/ai/generate-instructions" -Method Post -Body $body -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 120
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Response:"
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)"
    }
}
