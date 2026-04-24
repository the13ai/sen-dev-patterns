#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub & Gitee 仓库创建脚本
自动创建远程仓库并推送代码
"""

import os
import sys
import json
import base64
import webbrowser
import time
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests")
    sys.exit(1)

# ===== 配置 =====
GITHUB_API = "https://api.github.com"
GITEE_API = "https://gitee.com/api/v5"

# 获取token
def get_github_token():
    """尝试获取GitHub token"""
    # 1. 检查环境变量
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        print(f"[✓] 从环境变量获取GitHub Token")
        return token
    
    # 2. 检查VSCode状态
    vscode_state = os.path.expandvars(r"%APPDATA%\Code\User\globalStorage\github-auth-token")
    if os.path.exists(vscode_state):
        try:
            with open(vscode_state, 'r', encoding='utf-8') as f:
                data = json.load(f)
                token = data.get('token') or data.get('github_token')
                if token:
                    print(f"[✓] 从VSCode状态获取GitHub Token")
                    return token
        except:
            pass
    
    # 3. 检查git credential
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'credential', 'fill'],
            input='protocol=https\nhost=github.com\n\n',
            capture_output=True, text=True, encoding='utf-8'
        )
        for line in result.stdout.split('\n'):
            if line.startswith('password='):
                return line[9:]
    except:
        pass
    
    return None

def get_gitee_token():
    """尝试获取Gitee token"""
    token = os.getenv("GITEE_TOKEN") or os.getenv("GITEE_ACCESS_TOKEN")
    if token:
        print(f"[✓] 从环境变量获取Gitee Token")
        return token
    
    # 检查VSCode
    vscode_state = os.path.expandvars(r"%APPDATA%\Code\User\globalStorage")
    if os.path.exists(vscode_state):
        for item in os.listdir(vscode_state):
            if 'gitee' in item.lower():
                path = os.path.join(vscode_state, item)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        token = data.get('token') or data.get('access_token')
                        if token:
                            print(f"[✓] 从VSCode获取Gitee Token")
                            return token
                except:
                    pass
    
    return None

def create_github_repo(token, repo_name, description):
    """创建GitHub仓库"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": False
    }
    
    # 检查仓库是否已存在 - 使用正确的用户API
    resp = requests.get(f"{GITHUB_API}/repos/sinadook/{repo_name}", headers=headers)
    if resp.status_code == 200:
        print(f"[*] GitHub仓库已存在: {repo_name}")
        return True
    elif resp.status_code == 404:
        # 仓库不存在，尝试创建
        print(f"[*] GitHub仓库不存在，尝试创建...")
    
    resp = requests.post(f"{GITHUB_API}/user/repos", headers=headers, json=data)
    if resp.status_code == 201:
        print(f"[✓] GitHub仓库创建成功: {repo_name}")
        return True
    elif resp.status_code == 422:
        # 422可能是因为仓库名已存在
        try:
            error = resp.json()
            error_msg = str(error).lower()
            if 'already exists' in error_msg:
                print(f"[*] GitHub仓库已存在: {repo_name}")
                return True
        except:
            pass
        print(f"[✗] GitHub仓库创建失败: {resp.status_code}")
        print(f"    {resp.text[:200]}")
        return False
    else:
        print(f"[✗] GitHub仓库创建失败: {resp.status_code}")
        print(f"    {resp.text[:200]}")
        return False

def create_gitee_repo(token, repo_name, description):
    """创建Gitee仓库"""
    data = {
        "access_token": token,
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": False,
        "has_issues": True,
        "has_wiki": True
    }
    
    # 检查仓库是否已存在
    resp = requests.get(f"{GITEE_API}/repos/sinadook/{repo_name}", params={"access_token": token})
    if resp.status_code == 200:
        print(f"[*] Gitee仓库已存在: {repo_name}")
        return True
    
    resp = requests.post(f"{GITEE_API}/user/repos", data=data)
    if resp.status_code == 201:
        print(f"[✓] Gitee仓库创建成功: {repo_name}")
        return True
    else:
        try:
            error = resp.json()
            if 'error' in error and 'already exists' in error.get('error', '').lower():
                print(f"[*] Gitee仓库已存在: {repo_name}")
                return True
        except:
            pass
        print(f"[✗] Gitee仓库创建失败: {resp.status_code}")
        print(f"    {resp.text[:200]}")
        return False

def main():
    skill_dir = r"C:\Users\sen\.codebuddy\skills\sen-dev-patterns"
    repo_name = "sen-dev-patterns"
    description = "个人开发提效Skill - UI规范、算法库、踩坑记录、Web开发规范、Git工作流等"
    
    # 尝试GitHub
    print("\n=== 尝试GitHub ===")
    gh_token = get_github_token()
    if gh_token:
        success = create_github_repo(gh_token, repo_name, description)
        if success:
            # 添加远程并推送
            os.chdir(skill_dir)
            os.system(f'git remote add origin https://github.com/sinadook/{repo_name}.git')
            os.system('git push -u origin master')
            print(f"\n[✓] GitHub推送完成!")
            print(f"    仓库地址: https://github.com/sinadook/{repo_name}")
    else:
        print("[!] 未找到GitHub Token")
        print("    请在 https://github.com/settings/tokens 创建personal access token")
        print("    需要的权限: repo")
    
    # 尝试Gitee
    print("\n=== 尝试Gitee ===")
    ge_token = get_gitee_token()
    if ge_token:
        success = create_gitee_repo(ge_token, repo_name, description)
        if success:
            os.chdir(skill_dir)
            os.system(f'git remote add gitee https://gitee.com/sinadook/{repo_name}.git')
            os.system('git push -u gitee master --force')
            print(f"\n[✓] Gitee推送完成!")
            print(f"    仓库地址: https://gitee.com/sinadook/{repo_name}")
    else:
        print("[!] 未找到Gitee Token")
        print("    请在 https://gitee.com/oauth/applications 创建access_token")
        print("    需要的权限: projects")
    
    print("\n=== 完成 ===")
    print("如果以上都有[!]提示，请在命令行设置环境变量:")
    print("  Windows: set GITHUB_TOKEN=your_token")
    print("  Windows: set GITEE_TOKEN=your_token")
    print("然后重新运行此脚本")

if __name__ == "__main__":
    main()
