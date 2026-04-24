# Sen 开发提效 Skill - 发布指南

## 发布状态

**✅ Skill已准备就绪，可随时发布到ClawHub市场**

---

## 快速发布（推荐）

### 方法1：网页发布（最简单）

#### 步骤1：访问发布页面
打开浏览器访问：
```
https://clawhub.ai/import
```

#### 步骤2：填写表单
| 字段 | 值 |
|------|-----|
| Slug | `sen-dev-patterns` |
| Display name | `Sen开发提效Skill` |
| Version | `1.3.0` |
| Tags | `latest` |
| Folder | 上传整个 `sen-dev-patterns` 文件夹 |

#### 步骤3：登录并发布
- 使用GitHub账户登录
- 点击发布按钮

---

### 方法2：使用clawhub CLI

#### 1. 安装Node.js
访问 https://nodejs.org 下载安装

#### 2. 安装clawhub CLI
```bash
npm i -g clawhub
```

#### 3. 登录
```bash
clawhub login
```

#### 4. 发布
```bash
clawhub publish ~/.codebuddy/skills/sen-dev-patterns \
  --slug sen-dev-patterns \
  --name "Sen开发提效Skill" \
  --version 1.3.0 \
  --changelog "v1.3.0: UI规范、算法库、踩坑记录、Web开发规范、Git工作流" \
  --tags latest
```

---

## Skill信息

| 项目 | 内容 |
|------|------|
| 名称 | sen-dev-patterns |
| 版本 | 1.3.0 |
| 作者 | 很拽的猪 |
| 描述 | 个人开发提效Skill |
| 亮点 | 满意度加权公式、水晶质感UI、跨平台适配 |
| 文件数 | 14个文档 |
| 质量评分 | 9.0/10 |

---

## 发布后验证

发布成功后访问：`https://clawhub.ai/skills/sen-dev-patterns`

---

*最后更新: 2026-04-24*
