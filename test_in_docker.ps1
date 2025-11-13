# Test script to generate reports inside Docker container (PowerShell)

Write-Host "🚀 Testing ESG Report Generation in Docker" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Run the quick test inside the Docker container
docker-compose exec web python /app/quick_test_report.py

Write-Host ""
Write-Host "✅ Test completed!" -ForegroundColor Green
Write-Host "📁 Check the reports/ directory for generated files" -ForegroundColor Cyan
