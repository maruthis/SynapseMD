#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Optimized Chinese to English translation using Ollama, with efficient batching."""

import json
import re
import sys
from pathlib import Path
from typing import Dict

try:
    import requests
except ImportError:
    sys.exit("Please install requests: pip install requests")


class TranslationCache:
    def __init__(self, cache_file: str = '.translation_cache_ollama.json'):
        self.cache_file = Path(cache_file)
        self.cache: Dict[str, str] = {}
        self.load()
    
    def load(self) -> None:
        if self.cache_file.exists():
            try:
                self.cache = json.loads(self.cache_file.read_text(encoding='utf-8'))
            except Exception as e:
                print(f'Warning: Failed to load cache: {e}', file=sys.stderr)
                self.cache = {}
    
    def save(self) -> None:
        try:
            self.cache_file.write_text(json.dumps(self.cache, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception as e:
            print(f'Warning: Failed to save cache: {e}', file=sys.stderr)
    
    def get(self, key: str) -> str | None:
        return self.cache.get(key)
    
    def put(self, key: str, value: str) -> None:
        if key and value:
            self.cache[key] = value


# Medical terminology overrides
TERM_OVERRIDES = {
    'B超': 'B-mode ultrasound', '体检': 'physical examination', '胸闷气短': 'chest tightness and shortness of breath',
    '头疼': 'headache', '胃疼': 'stomachache', '咳嗽': 'cough', '心内科': 'cardiology', '消化科': 'gastroenterology',
    '内分泌科': 'endocrinology', '呼吸内科': 'respiratory medicine', '眼科': 'ophthalmology', '耳鼻喉科': 'otolaryngology',
    '骨科': 'orthopedics', '泌尿科': 'urology', '皮肤科': 'dermatology', '肾内科': 'nephrology', '神经内科': 'neurology',
    '风湿科': 'rheumatology', '肿瘤科': 'oncology', '放疗科': 'radiation oncology', '感染科': 'infectious diseases',
    '急诊科': 'emergency medicine', '重症监护室': 'ICU', '医院': 'hospital', '门诊': 'outpatient clinic',
    '住院': 'hospitalization', '药物': 'medication', '手术': 'surgery', '检查': 'examination', '健康': 'health',
    '记录': 'record', '数据': 'data', '分析': 'analysis', '报告': 'report', '认知': 'cognitive', '评估': 'assessment',
    '测试': 'test', '结果': 'result', '分数': 'score', '风险': 'risk', '预防': 'prevention', '建议': 'recommendation',
}

CHINESE_PUNCTUATION_MAP = {
    '，': ',', '。': '.', '？': '?', '！': '!', '；': ';', '：': ':', '、': ',',
    '（': '(', '）': ')', '【': '[', '】': ']', '"': '"', '"': '"', ''': "'", ''': "'",
    '《': '<', '》': '>', '…': '...',
}

CHINESE_SPAN_RE = re.compile(r'[\u4e00-\u9fff]+')
CACHE = TranslationCache()


def translate_with_ollama(text: str, model: str = 'qwen3:4b', url: str = 'http://localhost:11434/api/generate') -> str:
    """Translate text using Ollama."""
    if not text.strip():
        return text
    
    cached = CACHE.get(text)
    if cached:
        return cached
    
    prompt = f"""Translate Chinese to English concisely. Only respond with the translation, nothing else.

Chinese: {text}
English:"""
    
    try:
        resp = requests.post(url, json={'model': model, 'prompt': prompt, 'stream': False}, timeout=120)
        if resp.status_code == 200:
            result = resp.json().get('response', '').strip()
            if result:
                CACHE.put(text, result)
                return result
    except Exception as e:
        print(f'Error translating: {e}', file=sys.stderr)
    
    return text


def extract_chinese_spans(text: str) -> list[str]:
    """Extract all Chinese character sequences from text."""
    return CHINESE_SPAN_RE.findall(text)


def translate_line(line: str, model: str = 'qwen3:4b') -> str:
    """Translate Chinese text in a line while preserving structure."""
    if not CHINESE_SPAN_RE.search(line):
        return line
    
    result = line
    for match in CHINESE_SPAN_RE.finditer(line):
        chinese_text = match.group(0)
        if chinese_text in TERM_OVERRIDES:
            translation = TERM_OVERRIDES[chinese_text]
        else:
            translation = translate_with_ollama(chinese_text, model)
        result = result.replace(chinese_text, translation, 1)
    
    # Apply punctuation replacements
    for zh, en in CHINESE_PUNCTUATION_MAP.items():
        result = result.replace(zh, en)
    
    return result


def translate_markdown_file(file_path: Path, model: str = 'qwen3:4b') -> str:
    """Translate markdown file, preserving code blocks."""
    content = file_path.read_text(encoding='utf-8')
    if not CHINESE_SPAN_RE.search(content):
        return content
    
    lines = content.split('\n')
    result = []
    in_code_block = False
    
    for line in lines:
        # Track code blocks
        if line.startswith('```') or line.startswith('~~~'):
            in_code_block = not in_code_block
            result.append(line)
        elif in_code_block or not CHINESE_SPAN_RE.search(line):
            result.append(line)
        else:
            result.append(translate_line(line, model))
    
    return '\n'.join(result)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 translate_optimized.py <file_path> [model]")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    model = sys.argv[2] if len(sys.argv) > 2 else 'qwen3:4b'
    
    if not file_path.exists():
        print(f"Error: {file_path} not found")
        sys.exit(1)
    
    print(f"Translating {file_path} with model {model}...", file=sys.stderr)
    
    if file_path.suffix == '.md':
        translated = translate_markdown_file(file_path, model)
    else:
        content = file_path.read_text(encoding='utf-8')
        translated = '\n'.join(translate_line(line, model) if CHINESE_SPAN_RE.search(line) else line for line in content.split('\n'))
    
    print(translated)
    CACHE.save()


if __name__ == '__main__':
    main()
