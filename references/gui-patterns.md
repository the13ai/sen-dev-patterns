# GUI界面开发模式参考

## PySide6按钮样式模板

### 水晶质感按钮
```python
crystal_style = """
    QPushButton {
        color: #ffffff;
        font-weight: 700;
        font-size: 13px;
        border-radius: 14px;
        padding: 10px 16px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #COLOR_START,
            stop:0.5 #COLOR_MID,
            stop:1 #COLOR_END);
        border-top: 1px solid #ffffff;
        border-left: 1px solid #ffffff;
        border-right: 1px solid #000000;
        border-bottom: 2px solid #000000;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #HOVER_START,
            stop:0.5 #HOVER_MID,
            stop:1 #HOVER_END);
    }
    QPushButton:pressed {
        padding-top: 11px;
        padding-left: 17px;
        padding-bottom: 9px;
        padding-right: 15px;
    }
"""
```

### 颜色方案

| 按钮类型 | start | mid | end |
|----------|-------|-----|-----|
| 成功/绿色 | #48bb78 | #38a169 | #2f855a |
| 警告/橙色 | #ed8936 | #dd6b20 | #c05621 |
| 危险/红色 | #fc8181 | #f56565 | #e53e3e |
| 信息/蓝色 | #63b3ed | #4299e1 | #3182ce |

## 布局模式

### 顶部按钮栏
```python
top = QHBoxLayout()
top.setSpacing(12)

icon_label = QLabel("◆")  # 图标
top.addWidget(icon_label)

title_label = QLabel("标题")
top.addWidget(title_label)

top.addStretch(1)  # 弹性空间，推按钮到右侧

# 按钮并排
top.addWidget(btn_split)
top.addWidget(btn_export)
top.addWidget(btn_settings)

root.addLayout(top, 0)  # 0表示非扩展
```

### 主容器毛玻璃效果
```python
container = QFrame()
container.setStyleSheet("""
    QFrame {
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid #667eea;
    }
""")
shadow = QGraphicsDropShadowEffect(
    blurRadius=30, xOffset=0, yOffset=8,
    color=QColor(100, 120, 180, 40)
)
container.setGraphicsEffect(shadow)
```

## 信号槽连接

### Worker模式
```python
# 主窗口
self._worker = SomeWorker(config)
self._worker.progress.connect(self.on_progress)
self._worker.finished.connect(self.on_finished)
self._worker.error.connect(self.on_error)
self._thread = QThread()
self._worker.moveToThread(self._thread)
self._thread.started.connect(self._worker.run)
self._thread.start()
```

### 按钮点击确认
```python
def on_dangerous_action(self):
    reply = QMessageBox.question(
        self, "确认", "确定要执行吗？",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if reply != QMessageBox.Yes:
        return
    # 执行...
```
