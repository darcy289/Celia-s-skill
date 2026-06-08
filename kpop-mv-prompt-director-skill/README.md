# K-pop MV Prompt Director Skill

一个面向 AI 助手的 K-pop MV 风格提示词自动生成 Skill。用户输入 K-pop 团体名、音乐风格或视觉想法后，Skill 会自动匹配内置风格 DNA，并生成适用于 Seedance 2.0 / 千问视频模型的 13 镜 MV 分镜提示词。

## 这个 Skill 做什么

它不是直接生成视频，而是生成 **完整 MV Prompt Package**：

- 风格识别
- 导演阐述
- 全局 Prompt
- 13 镜 Shot List
- Seedance 标签式提示词
- 千问自然语言提示词
- 负面 Prompt
- 使用建议

## 仓库结构

```text
kpop-mv-prompt-director-skill/
├─ SKILL.md                         # 给 AI 助手读取的 Skill 使用说明
├─ README.md                        # 仓库说明
├─ data/
│  ├─ style_dna.json                 # 20 个 K-pop 风格 DNA
│  └─ shot_templates.json            # 13 镜通用 MV 模板
├─ src/
│  └─ kpop_mv_prompt_generator.py    # 可运行生成器
├─ examples/
│  ├─ aespa_seedance.md
│  └─ bigbang_qwen.md
└─ tests/
   └─ test_generator.py
```

## 快速开始

```bash
python src/kpop_mv_prompt_generator.py "aespa 风格" --tool seedance
python src/kpop_mv_prompt_generator.py "BIGBANG 街头传奇" --tool qwen
python src/kpop_mv_prompt_generator.py "Y2K 青春低保真" --tool both --character "上传图片中的同一个人物"
```

## 作为 AI 助手 Skill 使用

把整个文件夹放进你的 AI 助手可读取的 skills / tools / prompt library 目录中，让助手优先读取 `SKILL.md`。当用户要求生成 K-pop MV 视频提示词时，助手按 `SKILL.md` 的流程调用 `data/style_dna.json` 与 `data/shot_templates.json`。

## 输入示例

```text
我上传了角色图，帮我生成一个 aespa 风格的 45 秒 K-pop MV prompt，适配 Seedance。
```

## 输出示例

见 `examples/`。

## 注意

本 Skill 使用“风格 DNA”作为提示词生成变量，不声称复刻任何官方 MV，也不输出官方素材。建议在产品中使用“受某类视觉语言启发”的表述。
