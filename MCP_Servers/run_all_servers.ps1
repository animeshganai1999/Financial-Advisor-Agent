# Run All MCP Servers
# This script starts all MCP servers in separate background processes

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*59) -ForegroundColor Cyan
Write-Host "Starting All MCP Servers..." -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*59) -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Fundamentals MCP Server
Write-Host "[INFO] Starting Fundamentals MCP Server on port 8000..." -ForegroundColor Yellow
$fundamentals = Start-Process -FilePath "python" `
    -ArgumentList "$scriptDir\fundamentals_mcp\server.py" `
    -WorkingDirectory "$scriptDir\fundamentals_mcp" `
    -PassThru `
    -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Market Data MCP Server
Write-Host "[INFO] Starting Market Data MCP Server on port 8001..." -ForegroundColor Yellow
$marketData = Start-Process -FilePath "python" `
    -ArgumentList "$scriptDir\market_data_mcp\server.py" `
    -WorkingDirectory "$scriptDir\market_data_mcp" `
    -PassThru `
    -WindowStyle Minimized

Start-Sleep -Seconds 2

# Uncomment when news_sentiment_mcp is ready
# Write-Host "[INFO] Starting News Sentiment MCP Server on port 8002..." -ForegroundColor Yellow
# $news = Start-Process -FilePath "python" `
#     -ArgumentList "$scriptDir\news_sentiment_mcp\server.py" `
#     -WorkingDirectory "$scriptDir\news_sentiment_mcp" `
#     -PassThru `
#     -WindowStyle Minimized

Write-Host ""
Write-Host "[OK] All MCP servers started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Server URLs:" -ForegroundColor Cyan
Write-Host "  - Fundamentals MCP: http://127.0.0.1:8000/mcp" -ForegroundColor White
Write-Host "  - Market Data MCP:  http://127.0.0.1:8001/mcp" -ForegroundColor White
# Write-Host "  - News Sentiment MCP: http://127.0.0.1:8002/mcp" -ForegroundColor White
Write-Host ""
Write-Host "Process IDs:" -ForegroundColor Cyan
Write-Host "  - Fundamentals: $($fundamentals.Id)" -ForegroundColor White
Write-Host "  - Market Data:  $($marketData.Id)" -ForegroundColor White
# Write-Host "  - News Sentiment: $($news.Id)" -ForegroundColor White
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*59) -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to stop all servers..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Stop all servers
Write-Host ""
Write-Host "[INFO] Stopping all MCP servers..." -ForegroundColor Yellow
Stop-Process -Id $fundamentals.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $marketData.Id -Force -ErrorAction SilentlyContinue
# Stop-Process -Id $news.Id -Force -ErrorAction SilentlyContinue

Write-Host "[OK] All servers stopped" -ForegroundColor Green
