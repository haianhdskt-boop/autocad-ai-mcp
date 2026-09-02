# ==============================================================================
# AutoCAD AI MCP - 1-Click Automated Installer for Windows
# Compatible with: Antigravity, Claude Code, Claude Desktop, VS Code, Cursor
# ==============================================================================

Write-Host "🚀 [1/4] Đang khởi tạo cài đặt AutoCAD AI MCP cho Windows..." -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Lỗi: Máy tính chưa cài Python. Vui lòng cài Python từ python.org trước." -ForegroundColor Red
    exit 1
}

Write-Host "📦 [2/4] Thiết lập môi trường Python và cài đặt pywin32, fastmcp..." -ForegroundColor Cyan
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
& .\.venv\Scripts\python.exe -m pip install pywin32 --quiet
& .\.venv\Scripts\python.exe -m pip install -e . --quiet

$PythonBin = Join-Path $ScriptDir ".venv\Scripts\python.exe"

Write-Host "⚙️  [3/4] Tự động cấu hình MCP vào các AI Client trên Windows..." -ForegroundColor Cyan

# Build MCP config entry
$McpEntry = @{
    "command" = $PythonBin
    "args" = @("-m", "autocad_ai.servers.win_server")
}

# 1. Claude Desktop Configuration
$ClaudeConfigDir = Join-Path $env:APPDATA "Claude"
$ClaudeConf = Join-Path $ClaudeConfigDir "claude_desktop_config.json"
if (Test-Path $ClaudeConfigDir) {
    try {
        if (Test-Path $ClaudeConf) {
            $cfg = Get-Content $ClaudeConf -Raw | ConvertFrom-Json
        } else {
            $cfg = @{ mcpServers = @{} }
        }
        if (-not $cfg.mcpServers) { $cfg | Add-Member -NotePropertyName mcpServers -NotePropertyValue @{} }
        $cfg.mcpServers | Add-Member -NotePropertyName "autocad-ai" -NotePropertyValue $McpEntry -Force
        $cfg | ConvertTo-Json -Depth 10 | Set-Content $ClaudeConf -Encoding UTF8
        Write-Host "   ✅ Đã ghi cấu hình vào Claude Desktop ($ClaudeConf)" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  Không thể ghi Claude Desktop config, hãy cấu hình thủ công" -ForegroundColor Yellow
    }
}

# 2. Antigravity IDE Configuration
$AntigravityDir = Join-Path $env:USERPROFILE ".gemini\config"
$AntigravityConf = Join-Path $AntigravityDir "mcp_config.json"
if (Test-Path $AntigravityDir) {
    try {
        if (Test-Path $AntigravityConf) {
            $cfg = Get-Content $AntigravityConf -Raw | ConvertFrom-Json
        } else {
            $cfg = @{ mcpServers = @{} }
        }
        if (-not $cfg.mcpServers) { $cfg | Add-Member -NotePropertyName mcpServers -NotePropertyValue @{} }
        $cfg.mcpServers | Add-Member -NotePropertyName "autocad-ai" -NotePropertyValue $McpEntry -Force
        $cfg | ConvertTo-Json -Depth 10 | Set-Content $AntigravityConf -Encoding UTF8
        Write-Host "   ✅ Đã ghi cấu hình vào Antigravity ($AntigravityConf)" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  Không thể ghi Antigravity config, hãy cấu hình thủ công" -ForegroundColor Yellow
    }
}

Write-Host "✅ [4/4] Cài đặt hoàn tất thành công 100%!" -ForegroundColor Green
Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Yellow
Write-Host "🎉 AUTOCAD AI MCP ĐÃ SẴN SÀNG SỬ DỤNG TRÊN WINDOWS (COM ACTIVEX)!" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Yellow
Write-Host "Trọn bộ 8 lệnh nghiệp vụ KTS tiếng Việt đã được kích hoạt:" -ForegroundColor White
Write-Host " 1. cad_ve_moi             : Vẽ mặt bằng kiến trúc mới"
Write-Host " 2. cad_chinh_sua          : Sửa đổi, dịch tường, đảo cửa"
Write-Host " 3. cad_hoan_thien_ho_so   : Hoàn thiện bộ bản vẽ thi công TKTC"
Write-Host " 4. cad_du_toan            : Lập bảng dự toán chi tiết ra Excel/CSV"
Write-Host " 5. cad_kiem_tra           : Kiểm tra quy chuẩn & dọn rác bản vẽ"
Write-Host " 6. cad_gui_lenh           : Gửi lệnh AutoCAD gốc"
Write-Host " 7. cad_in_pdf             : In ấn hồ sơ PDF A3 chuẩn nét"
Write-Host " 8. cad_tra_cuu_quy_chuan  : Tra cứu quy chuẩn kiến trúc tức thì"
Write-Host ""
Write-Host "Để chạy thủ công server: $PythonBin -m autocad_ai.servers.win_server" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Yellow
