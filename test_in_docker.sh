#!/bin/bash
# Test script to generate reports inside Docker container

echo "🚀 Testing ESG Report Generation in Docker"
echo "=========================================="

# Run the quick test inside the Docker container
docker-compose exec web python /app/quick_test_report.py

echo ""
echo "✅ Test completed!"
echo "📁 Check the reports/ directory for generated files"
