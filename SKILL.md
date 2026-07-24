---
name: sen-dev-patterns
description: |
  个人开发提效Skill - 沉淀页面布局、样式风格、代码模块、算法库、踩坑记录。
  适用于用户需要复用个人开发经验、遵循统一规范、调用已沉淀的计算口径或模块的场景。
  当用户讨论邮件系统调试、Excel处理、GUI界面开发、数据分析流程时触发。
---

# 个人开发经验沉淀

## 核心原则

### 1. 调试工作流（DEBUG流程）

```
1. 运行程序观察实际输出 → 2. 分析日志/错误信息 → 3. 定位问题代码 → 4. 修复并验证
```

**关键经验：**
- 不要猜测问题，直接运行看日志
- 日志中的 `[调试]` 信息是分析问题的钥匙
- 先修复阻断性问题，再处理其他

### 2. 代码迭代易错点

#### enumerate误用
```python
# ❌ 错误：tables是List[DataFrame]，不能直接解包
for idx, df in tables:
    ...

# ✅ 正确：使用enumerate
for idx, df in enumerate(tables):
    ...
```

#### 变量作用域
```python
# ❌ 错误：result不在_save_extracted_keywords的作用域内
def _save_extracted_keywords(self, extracted, subject, mail):
    result['saved_files'].append(file_path)  # NameError!

# ✅ 正确：直接追加到saved_files
def _save_extracted_keywords(self, extracted, subject, mail):
    saved_files = []
    saved_files.append(file_path)
    return saved_files
```

#### 编码问题
```python
# ❌ 错误：特殊字符在Windows GBK环境无法输出
self._log(f"✓ [规则:{rule_name}] 匹配邮件", "SUCCESS")

# ✅ 正确：使用ASCII兼容字符
self._log(f"[√] [规则:{rule_name}] 匹配邮件", "SUCCESS")
```

---

## 邮件抓取系统架构

### 核心模块 (`email_fetcher.py`)

| 类名 | 职责 |
|------|------|
| `EmailConnector` | IMAP连接、邮件搜索、邮件内容获取 |
| `RuleEngine` | 关键词匹配、动作执行 |
| `EmailParser` | HTML解析、表格提取 |
| `AttachmentHandler` | 附件下载、Excel解析 |
| `DataSaver` | 文件夹管理、Excel保存 |
| `MailDatabase` | 已处理邮件记录 |
| `EmailFetcherWorker` | 协调各模块，主流程控制 |

### 动作类型
```python
ACTION_DOWNLOAD_ATTACHMENT = "download_attachment"  # 下载附件
ACTION_EXTRACT_TABLE = "extract_table"              # 提取正文表格
ACTION_EXTRACT_KEYWORD = "extract_keyword"          # 提取关键字
```

### 规则配置 (config.json)
```json
{
  "mail_rules": [
    {
      "name": "规则名称",
      "keywords": ["关键词1", "关键词2"],
      "match_field": "subject",  // subject/sender/both
      "actions": ["download_attachment", "extract_table", "extract_keyword"],
      "keyword_rules": [
        {
          "keyword": "提取锚点",
          "ctrl1": "之后",      // 之后/之前/从关键词开始
          "ctrl2_keyword": "%", // 控制二关键词
          "ctrl2": "截止"       // 之前/截止
        }
      ]
    }
  ]
}
```

### 文件夹命名逻辑 (`DataSaver._get_table_folder`)
```
1. 优先使用邮件标题作为文件夹名
2. 如果文件夹已存在且有内容，加上前一天日期
3. 使用 safe_filename() 清理非法字符
```

---

## GUI界面开发模式

### 按钮布局模式
```python
# 顶部按钮栏布局
top = QHBoxLayout()
top.addWidget(icon_label)
top.addWidget(title_label)
top.addStretch(1)  # 弹性空间，推按钮到右边
top.addWidget(btn_split)
top.addWidget(btn_settings)
```

### 水晶质感按钮样式
```python
crystal_style = """
    QPushButton {
        color: #ffffff;
        font-weight: 700;
        font-size: 13px;
        border-radius: 14px;
        padding: 10px 16px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #00d4aa, stop:0.5 #00c896, stop:1 #00b882);
        border-top: 1px solid #ffffff;
        border-left: 1px solid #ffffff;
        border-right: 1px solid #000000;
        border-bottom: 2px solid #000000;
    }
"""
```

### 危险操作确认模式
```python
def on_clear_mail_data(self):
    reply = QMessageBox.question(
        self, "确认", "确定要清除吗？此操作不可恢复！",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if reply != QMessageBox.Yes:
        return
    # 执行删除...
```

---

## 数据处理模式

### 表格提取 (`EmailParser.extract_tables_from_html`)
```python
def extract_tables_from_html(self, html_content: str) -> List[pd.DataFrame]:
    soup = BeautifulSoup(html_content, 'html.parser')
    table_elements = soup.find_all('table')
    tables_dfs = []
    for idx, table in enumerate(table_elements):
        df = self._parse_single_table(table, idx)
        if df is not None and not df.empty:
            tables_dfs.append(df)
    return tables_dfs
```

### Excel格式化保存
```python
def _apply_table_format(self, df: pd.DataFrame, file_path: str) -> None:
    df.to_excel(file_path, index=False)
    wb = load_workbook(file_path)
    ws = wb.active
    for row in ws.iter_rows():
        for cell in row:
            cell.font = Font(name='微软雅黑', size=9)
            cell.alignment = Alignment(horizontal='center', vertical='center')
    wb.save(file_path)
```

---

## 踩坑记录

### 1. pandas read_html 需要 StringIO
```python
# ❌ 错误
dfs = pd.read_html(html_content)

# ✅ 正确
from io import StringIO
dfs = pd.read_html(StringIO(html_content))
```

### 2. 文件路径中的特殊字符
使用 `safe_filename()` 清理邮件标题中的非法字符：
```python
def safe_filename(name: str) -> str:
    invalid = '<>:"/\\|?*'
    for c in invalid:
        name = name.replace(c, '_')
    return name.strip()
```

### 3. 多线程/Worker中的信号连接
```python
# ❌ 错误：在Worker中直接发射信号到主窗口
self.finished.connect(self.on_finished)  # Worker内部

# ✅ 正确：Worker发射信号，调用者连接
worker.finished.connect(self.on_finished)  # 主窗口内
```

### 4. HTML表格解析注意rowspan/colspan
邮件HTML表格可能包含合并单元格，需要特殊处理。

---

## 调试技巧

### 1. 添加调试日志
```python
self._log(f"    [调试] 附件数量: {len(attachments)}, body_html长度: {len(body_html)}", "INFO")
```

### 2. 保存HTML到文件分析
```python
with open('debug_email.html', 'w', encoding='utf-8') as f:
    f.write(body_html)
```

### 3. 分步验证
```python
# 1. 验证HTML有表格
soup = BeautifulSoup(html_content, 'html.parser')
print(f"table数量: {len(soup.find_all('table'))}")

# 2. 验证解析成功
tables = parser.extract_tables_from_html(html_content)
print(f"提取表格: {len(tables)}")

# 3. 验证保存成功
saved_files = data_saver.save_tables_to_excel(tables, subject, date)
print(f"保存文件: {saved_files}")
```
