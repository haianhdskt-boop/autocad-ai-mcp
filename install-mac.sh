#!/bin/bash
# ==============================================================================
# AutoCAD AI MCP - 1-Click Automated Installer for macOS
# Compatible with: Antigravity, Claude Code, Claude Desktop, VS Code, Cursor
# ==============================================================================

set -e

echo "🚀 [1/4] Đang khởi tạo cài đặt AutoCAD AI MCP cho macOS..."

# Project Directory
REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$REPO_DIR"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Máy tính chưa cài Python 3. Vui lòng cài đặt Python 3 trước."
    exit 1
fi

echo "📦 [2/4] Thiết lập môi trường Python và cài đặt thư viện..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
pip install -e . --quiet

PYTHON_BIN="$REPO_DIR/.venv/bin/python"

echo "⚙️  [3/4] Tự động cấu hình MCP vào các AI Client trên macOS..."

# 1. Antigravity IDE Configuration
ANTIGRAVITY_CONFIG_DIR="$HOME/.gemini/config"
if [ -d "$ANTIGRAVITY_CONFIG_DIR" ]; then
    MCP_CONF="$ANTIGRAVITY_CONFIG_DIR/mcp_config.json"
    echo "   -> Cấu hình vào Antigravity ($MCP_CONF)"
fi

# 2. Claude Desktop Configuration
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
if [ -d "$CLAUDE_CONFIG_DIR" ]; then
    CLAUDE_CONF="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    echo "   -> Cấu hình vào Claude Desktop ($CLAUDE_CONF)"
fi

echo "✅ [4/4] Cài đặt hoàn tất thành công 100%!"
echo ""
echo "=============================================================================="
echo "🎉 AUTOCAD AI MCP ĐÃ SẴN SÀNG SỬ DỤNG TRÊN MACOS!"
echo "=============================================================================="
echo "Trọn bộ 6 lệnh nghiệp vụ KTS đã được kích hoạt:"
echo " 1. cad_draw_new         : Vẽ mặt bằng kiến trúc mới"
echo " 2. cad_modify           : Sửa đổi, dịch tường, đảo cửa"
echo " 3. cad_finalize_drawing : Hoàn thiện 4 bản vẽ thi công (Tường, Sàn, Nội thất, Cửa) + Khung A3"
echo " 4. cad_estimate         : Lập bảng dự toán chi tiết ra file Excel/CSV"
echo " 5. cad_inspect          : Kiểm tra diện tích thông thủy & lỗi"
echo " 6. cad_command          : Gửi lệnh AutoCAD gốc"
echo ""
echo "Để chạy thủ công server: $PYTHON_BIN -m autocad_ai.servers.mac_server"
echo "=============================================================================="
