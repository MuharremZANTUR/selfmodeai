#!/bin/bash

echo "🔍 SelfMode Platform Deployment Verification"
echo "============================================="
echo ""

echo "📁 Checking project structure:"
echo "Frontend build exists: $([ -d ./frontend/build ] && echo "✅ YES" || echo "❌ NO")"
echo "Backend server exists: $([ -f ./backend/server.js ] && echo "✅ YES" || echo "❌ NO")"
echo "Root package.json exists: $([ -f ./package.json ] && echo "✅ YES" || echo "❌ NO")"
echo ""

echo "📦 Frontend build files:"
if [ -d ./frontend/build ]; then
    ls -la ./frontend/build/
else
    echo "❌ Frontend build directory not found"
fi
echo ""

echo "⚙️ Environment configuration:"
echo "NODE_ENV: ${NODE_ENV:-'not set'}"
echo "PORT: ${PORT:-'not set'}"
echo ""

echo "🚀 Starting server..."
cd backend && npm start