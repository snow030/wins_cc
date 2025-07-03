# 🌐 wins_cc · 免费同声传译工具

**wins_cc** 是一款基于 Python 的英文同声传译程序，它扩展了 Windows 11 内建的 Live Caption（实时字幕）功能，结合 OCR 与翻译引擎，实现英语 ➜ 中文的自动翻译流程。当前仅支持英译中，如需多语言支持可修改源代码适配。

---

## 🧩 第三方工具依赖

- **Live Caption (Windows 11)**：系统自带语音转文字服务
- **Tesseract OCR (需自行安装)**：开源图像识别引擎，用于屏幕文字提取
- **Google Translate API (v1)**：来自 Chrome 的网页翻译接口，无需认证、无调用限制

---

## 📦 Python 第三方库

| 库名           | 用途描述                  |
|----------------|--------------------------|
| `pytesseract`  | Python 接口封装 Tesseract |
| `pywin32`      | 用于识别 & 获取窗口信息    |
| `pillow`       | 用于截取指定屏幕区域       |

---

## 🔍 核心功能亮点

- 🧠 **字幕追踪（LCS）**：使用最长公共子句匹配（Longest Common Subsentence）算法检测新出现字幕段落
- ✨ **新增内容高亮**：仅展示新变化内容，并以黄色字体高亮显示，拥有不错的可读性
- 🌍 **英译中翻译链**：通过 Chrome 内建 Google Translate 接口完成文本翻译（低延迟、零限制）
- 🧱 **模块化设计**：各功能独立封装，可按需替换 OCR / 翻译模块
- 💻 **极简界面（GUI）**：基于 Tkinter，仅显示翻译内容 + 黑色半透明背景
- 📦 **可独立打包运行**：支持 PyInstaller 制作 EXE，便于部署与便携运行

---

## 🚀 使用方式

可以下载 python 源代码在本地上运行，或通过下面的链接下载 .exe 程序。

### ✅ EXE 可执行程序下载：

- [win_cc_1.2.0-scale100.exe](https://www.mediafire.com/file/n7geptx7g0wxdag/wins_cc_1.2.0-scale100.exe/file) - 适配屏幕缩放比例 100% 的用户
- [win_cc_1.2.0-scale125.exe](https://www.mediafire.com/file/wx31qotdfet8pe2/wins_cc_1.2.0-scale125.exe/file) - 适配屏幕缩放比例 125% 的用户

### 🔧 必要的工具：
- 请确保设备上的 Live Capture 能正常使用。程序默认将运行`C:/Windows/System32/LiveCaptions.exe`
- 请额外安装配置 [Tesseract OCR](https://tesseract-ocr.cn/tessdoc/Installation.html) (5.x+)
  - 作者推荐下载[UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)提供的已编译安装包。
