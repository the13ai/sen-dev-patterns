# 邮件抓取系统调试记录

## 问题排查清单

### 1. 表格提取失败
**症状**: 日志显示"从正文中提取到 N 个表格"但保存失败
**检查项**:
- [ ] `save_tables_to_excel` 函数中是否使用 `enumerate(tables)`
- [ ] 返回值类型是否为 `List[str]`
- [ ] 文件夹是否存在 (`ensure_dir`)

**典型错误**:
```python
# 错误
for idx, df in tables:  # tables是List，直接迭代是DataFrame

# 正确
for idx, df in enumerate(tables):
```

### 2. 编码错误
**症状**: `'gbk' codec can't encode character '\u2713'`
**修复**: 将特殊符号替换为ASCII兼容字符
```python
# ❌
self._log(f"✓ 成功", "SUCCESS")

# ✅
self._log(f"[√] 成功", "SUCCESS")
```

### 3. 变量未定义
**症状**: `NameError: name 'result' is not defined`
**检查**: 确认变量在当前函数作用域内定义

### 4. Excel解析失败
**症状**: `Can't find workbook in OLE2 compound document`
**原因**: 下载的Excel文件可能是HTML格式伪装
**检查**: 使用 `file --mime-type` 确认文件真实类型

## 日志分析要点

```
[调试] HTML特征: table=5, div=53, img=0, pre=0
```
- table > 0: HTML中有表格
- table = 0, pre > 0: 可能需要用pre标签解析
- table = 0, img > 0: 表格可能是图片形式

## 邮件规则动作

| 动作 | 需要的配置 |
|------|-----------|
| download_attachment | 无特殊配置 |
| extract_table | HTML中要有`<table>`标签 |
| extract_keyword | keyword_rules配置 |
