# Gemini Image Generator Skill

[English](./README.md) | 简体中文

一个基于 Gemini 3 Pro Image API 的 Claude Code Skill，支持文生图和图生图功能。

## 功能特性

### 核心能力

- **文生图 (Text-to-Image)**：通过自然语言描述生成高质量图片
- **图生图 (Image-to-Image)**：基于现有图片进行修改、转换或合并
  - 人脸身份保持
  - 姿势迁移
  - 风格迁移
  - 服装迁移
  - 图片编辑和增强

### 独特优势

- **超高分辨率**：支持 1K/2K/4K 三档分辨率，最高可达 6336×2688 像素
- **多种宽高比**：支持 10 种宽高比，覆盖各类使用场景
- **智能交互**：Claude 自动分析需求，引导用户完善细节
- **结构化 Prompt**：通过 JSON 格式精确控制生成效果
- **灵活部署**：支持自定义 API 端点，可配合代理使用

### 使用场景

**设计工作**
- 网站 LOGO 设计
- Banner 横幅图
- 海报和宣传画
- 社交媒体配图
- 产品展示图

**内容创作**
- 文章配图
- 封面图片
- 头像和个人形象
- 概念艺术图

**商业应用**
- 广告素材
- 电商产品图
- 品牌视觉设计
- PPT 配图

**个人娱乐**
- 桌面壁纸
- 手机壁纸
- AI 艺术创作
- 照片风格转换

## 支持的宽高比和分辨率

| 宽高比 | 1K 分辨率 | 2K 分辨率 | 4K 分辨率 |
|--------|-----------|-----------|-----------|
| 1:1    | 1024×1024 | 2048×2048 | 4096×4096 |
| 2:3    | 848×1264  | 1696×2528 | 3392×5056 |
| 3:2    | 1264×848  | 2528×1696 | 5056×3392 |
| 3:4    | 896×1200  | 1792×2400 | 3584×4800 |
| 4:3    | 1200×896  | 2400×1792 | 4800×3584 |
| 4:5    | 928×1152  | 1856×2304 | 3712×4608 |
| 5:4    | 1152×928  | 2304×1856 | 4608×3712 |
| 9:16   | 768×1376  | 1536×2752 | 3072×5504 |
| 16:9   | 1376×768  | 2752×1536 | 5504×3072 |
| 21:9   | 1584×672  | 3168×1344 | 6336×2688 |

## 安装

### 1. 安装依赖

```bash
pip install -q -U google-genai Pillow
```

### 2. 配置环境变量

```bash
export GEMINI_API_KEY="your-api-key-here"

# 可选：自定义 API 端点
export GEMINI_BASE_URL="https://your-proxy-url.com"
```

### 3. 安装 Skill

先将代码clone下来，然后将 `gemini-image-generator` 目录复制到你的项目的.claude/skills/ 目录下：

```
your-project/
├── .claude/
│   └── skills/
│       └── gemini-image-generator/
│           ├── SKILL.md
│           ├── README.md
│           ├── scripts/
│           │   └── generate_image.py
│           └── references/
│               └── json_schema_reference.md
```

## 使用方法

### 在 Claude Code 中使用

安装完成后，有两种方式调用此 Skill：

**方式一：显式调用（推荐）**

使用 `/gemini-image-generator` 命令显式调用 Skill：

```
/gemini-image-generator 帮我生成一张猫睡觉的图片
```

```
/gemini-image-generator 把这张照片 ./photo.jpg 转换成动漫风格
```

**方式二：自然语言描述**

直接描述你的图片生成需求，Claude 会自动识别并调用此 Skill：

```
帮我生成一张赛博朋克风格的城市夜景图
```

```
把这张照片 ./photo.jpg 转换成动漫风格
```

Claude 会自动：
1. 分析你的需求并询问必要的细节（宽高比、分辨率等）
2. 将需求转换为结构化 JSON 格式
3. 调用生成脚本生成图片


### 输出位置

生成的图片默认保存在 `./generation-image/` 目录，文件名格式为 `generated_YYYYMMDD_HHMMSS.png`。

## JSON Prompt 结构

完整的 JSON prompt 结构参考 `references/json_schema_reference.md`，主要字段包括：

```json
{
  "user_intent": "自然语言描述目标",
  "meta": {
    "aspect_ratio": "16:9",
    "image_size": "1K",
    "quality": "ultra_photorealistic"
  },
  "subject": [{
    "type": "person",
    "description": "视觉特征描述",
    "pose": "动作描述",
    "expression": "表情"
  }],
  "scene": {
    "location": "场景描述",
    "time": "golden_hour",
    "lighting": {"type": "cinematic"}
  },
  "style_modifiers": {
    "medium": "photography",
    "aesthetic": ["cyberpunk"]
  }
}
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| API Key not found | 确保设置了 `GEMINI_API_KEY` 环境变量 |
| 图片生成失败 | 检查 prompt 是否违反内容策略 |
| 图片质量不佳 | 调整 `meta.quality` 和 `meta.image_size` 参数 |
| 宽高比不对 | 检查 `meta.aspect_ratio` 是否为支持的值 |

## 目录结构

```
gemini-image-generator/
├── SKILL.md                    # Skill 定义文件（Claude 读取）
├── README.md                   # 英文文档
├── README_CN.md                # 中文文档（本文件）
├── scripts/
│   └── generate_image.py       # 图片生成脚本
└── references/
    └── json_schema_reference.md # JSON prompt 完整参考
```

## License

MIT
