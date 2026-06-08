from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kpop_mv_prompt_generator import generate_package


def test_generate_aespa_seedance():
    output = generate_package("aespa 风格", "seedance")
    assert "匹配风格：aespa" in output
    assert "Seedance Prompt" in output
    assert "镜头13" in output


def test_generate_bigbang_qwen():
    output = generate_package("BigBang 街头传奇", "qwen", "上传图片中的同一个人物")
    assert "匹配风格：BIGBANG" in output
    assert "千问 Prompt" in output
    assert "上传图片中的同一个人物" in output
