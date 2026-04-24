@echo off
chcp 65001 >nul
echo ==========================================
echo   Sen-Dev-Patterns Skill 发布脚本
echo ==========================================
echo.

cd /d "%~dp0"

REM 检查是否有GitHub token
set GITHUB_TOKEN=
for /f "tokens=2,* delims= " %%a in ('git config --global credential.helper 2^>nul') do (
    echo Found credential helper: %%a
)

REM 尝试从环境变量获取
if defined GITHUB_TOKEN (
    echo [✓] 找到GitHub Token
    goto :github
)

if defined GH_TOKEN (
    set GITHUB_TOKEN=%GH_TOKEN%
    echo [✓] 找到GitHub Token (GH_TOKEN)
    goto :github
)

REM 检查VSCode GitHub扩展token
echo.
echo [*] 正在检查VSCode GitHub扩展...
for /r "%APPDATA%\Code\User\globalStorage" %%i in (*github*) do (
    echo Found: %%i
)

echo.
echo [!] 未找到GitHub Token
echo.
echo 请选择以下方式之一：
echo.
echo 方式1: 在浏览器中创建GitHub Personal Access Token
echo   1. 访问: https://github.com/settings/tokens
echo   2. 点击 "Generate new token (classic)"
echo   3. 勾选 "repo" 权限
echo   4. 复制生成的token
echo   5. 在下方粘贴:
echo.
set /p TOKEN="粘贴Token: "
set GITHUB_TOKEN=%TOKEN%

if not defined GITHUB_TOKEN (
    echo [✗] 未提供Token，退出
    pause
    exit /b 1
)

:github
echo.
echo [✓] 开始创建GitHub仓库...
python -c "
import requests, os
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
resp = requests.get('https://api.github.com/user', headers=headers)
print(f'User: {resp.json().get(\"login\")}')
"

echo.
echo [✓] 推送代码到GitHub...
git push -u origin master

if %errorlevel% neq 0 (
    echo.
    echo [!] 推送失败，可能是仓库不存在
    echo [*] 尝试通过API创建仓库...
    python create_repo.py
)

echo.
echo ==========================================
echo   发布完成！
echo ==========================================
pause
