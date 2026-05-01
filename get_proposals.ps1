$result = Invoke-RestMethod -Uri "http://159.65.225.228:8000/proposals/?user_id=550e8400-e29b-41d4-a716-446655440000" -Method GET

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "PROPOSALS FOR USER" -ForegroundColor Cyan
Write-Host "User ID: 550e8400-e29b-41d4-a716-446655440000" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Total Proposals:" $result.total -ForegroundColor Yellow
Write-Host ""

if ($result.total -gt 0) {
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "PROPOSAL DETAILS" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    
    $i = 1
    foreach ($proposal in $result.proposals) {
        Write-Host ""
        Write-Host "--- Proposal #$i ---" -ForegroundColor Magenta
        Write-Host "ID:       " $proposal.proposal_id
        Write-Host "Name:     " $proposal.proposal_name
        Write-Host "Title:    " $proposal.title
        Write-Host "Template: " $proposal.template
        Write-Host "AI Model: " $proposal.ai_model
        Write-Host "Hourly:   $" $proposal.hourly_rate
        Write-Host "Fixed:    $" $proposal.fixed_rate
        Write-Host "Created:  " $proposal.created_at
        
        if ($proposal.instructions) {
            Write-Host "Instructions: " $proposal.instructions.Substring(0, [Math]::Min(100, $proposal.instructions.Length)) "..."
        }
        
        $i++
    }
} else {
    Write-Host "No proposals found for this user." -ForegroundColor Red
}
