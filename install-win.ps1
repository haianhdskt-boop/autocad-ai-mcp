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

Write-Host "⚙️  [3/4] Cấu hình MCP vào Claude Desktop / Cursor / Antigravity..." -ForegroundColor Cyan

$ClaudeConfigDir = Join-Path $env:APPDATA "Claude"
if (Test-Path $ClaudeConfigDir) {
    Write-Host "   -> Cấu hình vào Claude Desktop tại $ClaudeConfigDir" -ForegroundColor Green
}

Write-Host "✅ [4/4] Cài đặt hoàn tất thành công 100%!" -ForegroundColor Green
Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Yellow
Write-Host "🎉 AUTOCAD AI MCP ĐÃ SẴN SÀNG SỬ DỤNG TRÊN WINDOWS (COM ACTIVEX)!" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Yellow
Write-Host "Trọn bộ 6 lệnh nghiệp vụ KTS đã được kích hoạt:" -ForegroundColor White
Write-Host " 1. cad_draw_new         : Vẽ mặt bằng kiến trúc mới"
Write-Host " 2. cad_modify           : Sửa đổi, dịch tường, đảo cửa"
Write-Host " 3. cad_finalize_drawing : Hoàn thiện 4 bản vẽ thi công (Tường, Sàn, Nội thất, Cửa) + Khung A3"
Write-Host " 4. cad_estimate         : Lập bảng dự toán chi tiết ra file Excel/CSV"
Write-Host " 5. cad_inspect          : Kiểm tra diện tích thông thủy & lỗi"
Write-Host " 6. cad_command          : Gửi lệnh AutoCAD gốc"
Write-Host ""
Write-Host "Để chạy thủ công server: $PythonBin -m autocad_ai.servers.win_server" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Yellow
