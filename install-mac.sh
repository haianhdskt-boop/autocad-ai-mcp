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

# Build MCP config JSON snippet
MCP_ENTRY="{\"autocad-ai\":{\"command\":\"$PYTHON_BIN\",\"args\":[\"-m\",\"autocad_ai.servers.mac_server\"]}}"

# 1. Antigravity IDE Configuration
ANTIGRAVITY_CONFIG_DIR="$HOME/.gemini/config"
if [ -d "$ANTIGRAVITY_CONFIG_DIR" ]; then
    MCP_CONF="$ANTIGRAVITY_CONFIG_DIR/mcp_config.json"
    if [ -f "$MCP_CONF" ]; then
        # Merge into existing config using python
        python3 -c "
import json, sys
with open('$MCP_CONF','r') as f: cfg=json.load(f)
cfg.setdefault('mcpServers',{})['autocad-ai']={'command':'$PYTHON_BIN','args':['-m','autocad_ai.servers.mac_server']}
with open('$MCP_CONF','w') as f: json.dump(cfg,f,indent=2)
" 2>/dev/null && echo "   ✅ Đã ghi cấu hình vào Antigravity ($MCP_CONF)" || echo "   ⚠️  Không thể ghi Antigravity config, hãy cấu hình thủ công"
    else
        echo "{\"mcpServers\":$MCP_ENTRY}" | python3 -m json.tool > "$MCP_CONF" 2>/dev/null
        echo "   ✅ Đã tạo cấu hình Antigravity ($MCP_CONF)"
    fi
fi

# 2. Claude Desktop Configuration
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
if [ -d "$CLAUDE_CONFIG_DIR" ]; then
    CLAUDE_CONF="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    if [ -f "$CLAUDE_CONF" ]; then
        python3 -c "
import json
with open('$CLAUDE_CONF','r') as f: cfg=json.load(f)
cfg.setdefault('mcpServers',{})['autocad-ai']={'command':'$PYTHON_BIN','args':['-m','autocad_ai.servers.mac_server']}
with open('$CLAUDE_CONF','w') as f: json.dump(cfg,f,indent=2)
" 2>/dev/null && echo "   ✅ Đã ghi cấu hình vào Claude Desktop ($CLAUDE_CONF)" || echo "   ⚠️  Không thể ghi Claude Desktop config, hãy cấu hình thủ công"
    else
        echo "{\"mcpServers\":$MCP_ENTRY}" | python3 -m json.tool > "$CLAUDE_CONF" 2>/dev/null
        echo "   ✅ Đã tạo cấu hình Claude Desktop ($CLAUDE_CONF)"
    fi
fi

echo "✅ [4/4] Cài đặt hoàn tất thành công 100%!"
echo ""
echo "=============================================================================="
echo "🎉 AUTOCAD AI MCP ĐÃ SẴN SÀNG SỬ DỤNG TRÊN MACOS!"
echo "=============================================================================="
echo "Trọn bộ 8 lệnh nghiệp vụ KTS tiếng Việt đã được kích hoạt:"
echo " 1. cad_ve_moi             : Vẽ mặt bằng kiến trúc mới"
echo " 2. cad_chinh_sua          : Sửa đổi, dịch tường, đảo cửa"
echo " 3. cad_hoan_thien_ho_so   : Hoàn thiện bộ bản vẽ thi công TKTC"
echo " 4. cad_du_toan            : Lập bảng dự toán chi tiết ra Excel/CSV"
echo " 5. cad_kiem_tra           : Kiểm tra quy chuẩn & dọn rác bản vẽ"
echo " 6. cad_gui_lenh           : Gửi lệnh AutoCAD gốc"
echo " 7. cad_in_pdf             : In ấn hồ sơ PDF A3 chuẩn nét"
echo " 8. cad_tra_cuu_quy_chuan  : Tra cứu quy chuẩn kiến trúc tức thì"
echo ""
echo "Để chạy thủ công server: $PYTHON_BIN -m autocad_ai.servers.mac_server"
echo "=============================================================================="
