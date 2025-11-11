#!/bin/bash

# MCP 서버 설정 스크립트
# Talk to Figma MCP를 위한 Bun 설치 및 기본 설정

set -e

echo "🚀 MCP 서버 설정을 시작합니다..."

# Bun 설치 확인
if ! command -v bun &> /dev/null; then
    echo "📦 Bun이 설치되어 있지 않습니다. 설치를 시작합니다..."
    curl -fsSL https://bun.sh/install | bash
    
    # PATH 업데이트
    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    elif [ -f ~/.zshrc ]; then
        source ~/.zshrc
    fi
    
    echo "✅ Bun 설치 완료"
else
    echo "✅ Bun이 이미 설치되어 있습니다: $(bun --version)"
fi

# MCP 설정 파일 확인
if [ ! -f ".cursor/mcp.json" ]; then
    echo "📝 MCP 설정 파일을 생성합니다..."
    if [ -f ".cursor/mcp.json.example" ]; then
        cp .cursor/mcp.json.example .cursor/mcp.json
        echo "✅ .cursor/mcp.json.example을 복사했습니다"
        echo "⚠️  .cursor/mcp.json 파일을 열어서 필요한 토큰을 설정하세요"
    else
        echo "❌ .cursor/mcp.json.example 파일을 찾을 수 없습니다"
        exit 1
    fi
else
    echo "✅ MCP 설정 파일이 이미 존재합니다"
fi

echo ""
echo "🎉 설정 완료!"
echo ""
echo "다음 단계:"
echo "1. .cursor/mcp.json 파일을 열어서 GitHub/Brave API 키를 설정하세요 (선택사항)"
echo "2. 별도 터미널에서 WebSocket 서버를 시작하세요:"
echo "   bunx cursor-talk-to-figma-mcp@latest socket"
echo "3. Figma에서 'Cursor Talk to Figma MCP' 플러그인을 설치하세요"
echo "4. Cursor IDE를 재시작하세요"
echo ""
echo "자세한 내용은 MCP_SETUP.md를 참고하세요."



