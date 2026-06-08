#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K-pop MV Prompt Director

Generate 13-shot K-pop MV prompt packages from style keywords.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

NEGATIVE_PROMPT = (
    "避免：文字水印、低清晰度、模糊面部、脸部身份漂移、畸形手指、畸形肢体、"
    "多余路人抢戏、廉价舞台、现代 UI 杂讯、过度塑料感、画面脏乱、过曝、过暗。"
)

GLOBAL_RULES = (
    "使用上传图片中的同一个人物作为【角色】，保持脸部身份一致；K-pop MV 质感，"
    "电影级灯光，高级商业影像，主体清晰，服装、妆造、场景与所选风格 DNA 保持一致。"
)


def load_json(name: str) -> Any:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(text: str) -> str:
    return text.lower().replace(" ", "").replace(".", "").replace("-", "")


def score_style(query: str, record: Dict[str, Any]) -> int:
    q = normalize(query)
    score = 0
    names = [record["display_name"], record["id"], *record.get("aliases", [])]
    for name in names:
        n = normalize(name)
        if n and n in q:
            score += 100 if normalize(record["display_name"]) == n else 60
    for value in record["variables"].values():
        for token in str(value).replace("、", ",").replace("/", ",").split(","):
            t = normalize(token.strip())
            if t and t in q:
                score += 8
    return score


def choose_style(query: str, styles: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], int]:
    ranked = sorted(((score_style(query, s), s) for s in styles), key=lambda x: x[0], reverse=True)
    if ranked[0][0] <= 0:
        # Sensible default: current mainstream futuristic K-pop visual language.
        fallback = next(s for s in styles if s["display_name"] == "aespa")
        return fallback, 0
    return ranked[0][1], ranked[0][0]


def fill_template(template: str, variables: Dict[str, str], character: str) -> str:
    result = template.replace("【角色】", character)
    for key, value in variables.items():
        result = result.replace("{" + key + "}", value)
    return result


def build_title(style_name: str, variables: Dict[str, str]) -> str:
    mood = variables.get("风格氛围", "K-pop MV")
    return f"{style_name} 灵感 MV：{mood.split('、')[0]}"


def generate_package(query: str, target_tool: str = "both", character: str = "【角色】") -> str:
    styles = load_json("style_dna.json")
    shots = load_json("shot_templates.json")
    style, score = choose_style(query, styles)
    variables = style["variables"]
    title = build_title(style["display_name"], variables)

    lines: List[str] = []
    lines.append(f"# K-pop MV 风格提示词包：{title}")
    lines.append("")
    lines.append("## 1. 风格识别")
    lines.append(f"- 用户输入：{query}")
    lines.append(f"- 匹配风格：{style['display_name']}")
    lines.append(f"- 匹配置信度：{'默认推荐' if score == 0 else score}")
    lines.append(f"- 风格氛围：{variables['风格氛围']}")
    lines.append(f"- 目标工具：{target_tool}")
    lines.append("")
    lines.append("## 2. 导演阐述")
    lines.append(
        f"这支 MV 以“{variables['风格氛围']}”为核心视觉方向，把{character}包装成一个具有明确舞台身份的 K-pop 主角。"
        f"画面会在{variables['标志场景']}、{variables['标志场景2']}与{variables['标志场景3']}之间切换，"
        f"用{variables['标志运镜']}、{variables['标志特效']}和{variables['标志动作']}建立完整的音乐录像带节奏。"
    )
    lines.append("")
    lines.append("## 3. 全局 Prompt")
    lines.append(GLOBAL_RULES)
    lines.append("")
    lines.append("## 4. Shot List / 分镜提示词")

    for shot in shots:
        lines.append(f"### 镜头{shot['shot_id']}：{shot['name']}")
        lines.append(f"- 时长：{shot['duration']}")
        lines.append(f"- 功能：{shot['function']}")
        if target_tool in ("seedance", "both"):
            lines.append(f"- Seedance Prompt：{fill_template(shot['seedance_template'], variables, character)}")
        if target_tool in ("qwen", "both"):
            lines.append(f"- 千问 Prompt：{fill_template(shot['qwen_template'], variables, character)}")
        lines.append("")

    lines.append("## 5. 负面 Prompt")
    lines.append(NEGATIVE_PROMPT)
    lines.append("")
    lines.append("## 6. 使用建议")
    lines.append("- 如果使用图生视频，把上传角色图作为首帧或角色参考图，并将【角色】替换为“上传图片中的同一个人物”。")
    lines.append("- 如果模型一次只能生成短片，建议每个镜头单独生成 3-5 秒，再后期拼接。")
    lines.append("- 如果要接近 60 秒，把镜头5、7、11、13拉长到 5-6 秒，其余镜头保持 3-4 秒。")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate K-pop MV prompt package.")
    parser.add_argument("query", help="团体名、风格名或自然语言描述")
    parser.add_argument("--tool", choices=["seedance", "qwen", "both"], default="both")
    parser.add_argument("--character", default="【角色】", help="角色占位符，默认【角色】")
    parser.add_argument("--output", "-o", help="输出 Markdown 文件路径")
    args = parser.parse_args()

    result = generate_package(args.query, args.tool, args.character)
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result)


if __name__ == "__main__":
    main()
