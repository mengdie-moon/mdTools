# mdTools

中文|[English](README_EN.md)

mdTools是一个基于Python语言编写的多功能开源工具库，旨在提供便捷的开发工具集，提升开发效率。该工具库集成了多个常用功能，可以大大简化开发过程中的重复性工作，帮助开发者更专注于核心业务逻辑的实现。

## 适用场景

1. **快速开发场景**
   - 需要快速实现基础功能而不想重复造轮子
   - 多个项目中经常需要使用相似的工具函数
   - 希望统一管理和维护常用工具代码

2. **自动化测试和脚本**
   - 需要模拟用户操作进行自动化测试
   - 批量处理文件和数据
   - 需要截图记录或自动化UI测试

3. **桌面应用开发**
   - 需要进行鼠标和键盘控制
   - 需要创建用户交互界面和提示框
   - 需要进行屏幕截图和图像处理

## 功能特点

目前该工具库包含四个主要模块(未更新完)：

1. **主工具类 (mdTools_main)**

2. **鼠标操作类 (mdTools_mouse)**

3. **弹窗类 (mdTools_popup)**

4. **截图类 (mdTools_screenshot)**

## 安装方法

```bash
pip install mdTools
```

## 使用示例

```python
from mdTools import mdTools

# 创建工具实例
tool = mdTools()

# 生成随机密码
password = tool.randomPassword(length=12, isNumber=True, isStr=True, isNotation=True)
print(f"生成的随机密码: {password}")

# Base64编码
encoded = tool.base64_encode("Hello World")
print(f"Base64编码结果: {encoded}")

# 鼠标操作
tool.mouse_move(100, 100)  # 移动鼠标到指定位置
tool.mouse_click()         # 点击鼠标

# 显示消息框
tool.MPopup_messagebox("操作成功", "提示", "info")

# 截取屏幕
tool.md_screenshot(0, 0, 800, 600, "screenshot.png")
```

## 环境要求

- Python >= 3.6
- 操作系统：Windows/Linux/MacOS

## 依赖包

- pillow
- pyperclip
- keyboard
- mouse
- pywin32 (Windows)
- xdotool (Linux)
- pyobjc-framework-Quartz (MacOS)

## 许可证

Apache License 2.0

## 作者信息

- 作者：梦蝶
- 邮箱：3257053519@qq.com
- 作者说明：原本想上传pypi后来一直Error就之间上传到github了
