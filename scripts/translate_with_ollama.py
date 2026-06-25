#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate Chinese markdown and code comments using Ollama local LLM (faster, no rate limits)."""

import argparse
import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Iterable, List

try:
    import requests
except ImportError:
    raise SystemExit("Please install requests: pip install requests")


class TranslationCache:
    """Cache translations to avoid repeated API calls."""
    
    def __init__(self, cache_file: str = '.ollama_translation_cache.json'):
        self.cache_file = Path(cache_file)
        self.cache: Dict[str, str] = {}
        self.load()
    
    def load(self) -> None:
        """Load the cache from disk."""
        if self.cache_file.exists():
            try:
                self.cache = json.loads(self.cache_file.read_text(encoding='utf-8'))
            except Exception as e:
                print(f'Warning: Failed to load cache: {e}')
                self.cache = {}
    
    def save(self) -> None:
        """Save the cache to disk."""
        try:
            self.cache_file.write_text(json.dumps(self.cache, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception as e:
            print(f'Warning: Failed to save cache: {e}')
    
    def get(self, key: str) -> str | None:
        """Get a translation from the cache, or None if not cached."""
        return self.cache.get(key)
    
    def put(self, key: str, value: str) -> None:
        """Store a translation in the cache."""
        if key and value:
            self.cache[key] = value
    
    def put_many(self, items: Dict[str, str]) -> None:
        """Store multiple translations in the cache."""
        for key, value in items.items():
            self.put(key, value)


TRANSLATION_CACHE = TranslationCache('.ollama_translation_cache.json')

# Matches Chinese characters with digits/letters and punctuation used in Chinese sentences.
CHINESE_SPAN_RE = re.compile(r'([\u4e00-\u9fffA-Za-z0-9]+(?:[，。？！；：、""''（）《》【】…、]+[\u4e00-\u9fffA-Za-z0-9]+)*)')

TERM_OVERRIDES = {
    'B超': 'B-mode ultrasound',
    '体检': 'physical examination',
    '胸闷气短': 'chest tightness and shortness of breath',
    '头疼': 'headache',
    '胃疼': 'stomachache',
    '咳嗽': 'cough',
    '心内科': 'cardiology',
    '消化科': 'gastroenterology',
    '内分泌科': 'endocrinology',
    '呼吸内科': 'respiratory medicine',
    '眼科': 'ophthalmology',
    '耳鼻喉科': 'otolaryngology',
    '骨科': 'orthopedics',
    '泌尿科': 'urology',
    '皮肤科': 'dermatology',
    '肾内科': 'nephrology',
    '神经内科': 'neurology',
    '风湿科': 'rheumatology',
    '肿瘤科': 'oncology',
    '放疗科': 'radiation oncology',
    '感染科': 'infectious diseases',
    '急诊科': 'emergency medicine',
    '重症监护室': 'ICU',
    '医院': 'hospital',
    '门诊': 'outpatient clinic',
    '住院': 'hospitalization',
    '药物': 'medication',
    '手术': 'surgery',
    '检查': 'examination',
}

CHINESE_PUNCTUATION_MAP = {
    '，': ',',
    '。': '.',
    '？': '?',
    '！': '!',
    '；': ';',
    '：': ':',
    '、': ',',
    '（': '(',
    '）': ')',
    '【': '[',
    '】': ']',
    '"': '"',
    '"': '"',
    ''': "'",
    ''': "'",
    '《': '<',
    '》': '>',
    '…': '...',
}

CODE_FENCE_RE = re.compile(r'^(?P<fence>```|~~~)')
INLINE_CODE_RE = re.compile(r'(`+)(.+?)(\1)')


def translate_with_ollama(text: str, model: str = 'mistral', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Use local Ollama LLM to translate Chinese to English."""
    if not text.strip():
        return text
    
    prompt = f"""Translate the following Chinese text to English. Keep the translation concise and accurate. 
Respond with only the translated text, nothing else.

Chinese: {text}
English:"""
    
    try:
        response = requests.post(ollama_url, json={
            'model': model,
            'prompt': prompt,
            'stream': False,
        }, timeout=60)
        
        if response.status_code == 200:
            result = response.json().get('response', '').strip()
            if result:
                return result
    except Exception as e:
        print(f'Ollama translation failed: {e}')
    
    return text


def translate_segments_ollama(segments: List[str], model: str = 'mistral', ollama_url: str = 'http://localhost:11434/api/generate') -> List[str]:
    """Translate segments using Ollama LLM, checking cache first."""
    if not segments:
        return []
    
    results: List[str | None] = []
    uncached_segments: List[tuple[int, str]] = []
    
    # Check cache first
    for i, segment in enumerate(segments):
        cached = TRANSLATION_CACHE.get(segment)
        if cached:
            results.append(cached)
        else:
            results.append(None)
            uncached_segments.append((i, segment))
    
    # If all cached, return immediately
    if not uncached_segments:
        return [r for r in results if r is not None]
    
    # Translate uncached segments
    cache_updates = {}
    for idx, segment in uncached_segments:
        try:
            translation = translate_with_ollama(segment, model, ollama_url)
            results[idx] = translation
            cache_updates[segment] = translation
        except Exception as e:
            print(f'Failed to translate "{segment}": {e}')
            results[idx] = segment
    
    TRANSLATION_CACHE.put_many(cache_updates)
    return [r for r in results if r is not None]


def translate_text_ollama(text: str, model: str = 'mistral', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Translate Chinese text to English using Ollama."""
    if not re.search(r'[\u4e00-\u9fff]', text):
        return text

    parts: List[str | None] = []
    segments: List[str] = []
    last = 0
    for match in CHINESE_SPAN_RE.finditer(text):
        parts.append(text[last:match.start()])
        segment = match.group(1)
        for zh, en in CHINESE_PUNCTUATION_MAP.items():
            segment = segment.replace(zh, en)
        if segment in TERM_OVERRIDES:
            parts.append(TERM_OVERRIDES[segment])
        else:
            parts.append(None)
            segments.append(segment)
        last = match.end()

    parts.append(text[last:])

    if not segments:
        return ''.join(part if part is not None else '' for part in parts)

    try:
        translated_segments = translate_segments_ollama(segments, model, ollama_url)
    except Exception as e:
        print(f'Warning: Translation failed: {e}')
        translated_segments = segments

    translated_iter = iter(translated_segments)
    return ''.join(part if part is not None else next(translated_iter) for part in parts)


def translate_markdown_file_ollama(path: Path, model: str = 'mistral', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Translate Chinese in markdown file, preserving code blocks."""
    text = path.read_text(encoding='utf-8')
    if not re.search(r'[\u4e00-\u9fff]', text):
        return text

    output: List[str] = []
    in_fence = False
    fence_delim = None
    lines = text.splitlines(keepends=True)
    
    for line in lines:
        if in_fence:
            if fence_delim and line.strip().startswith(fence_delim):
                in_fence = False
            output.append(line)
            continue
        
        fence_match = CODE_FENCE_RE.match(line.lstrip())
        if fence_match:
            fence_delim = fence_match.group('fence')
            in_fence = True
            output.append(line)
            continue
        
        output.append(translate_text_ollama(line, model, ollama_url))
    
    return ''.join(output)


def main() -> None:
    parser = argparse.ArgumentParser(description='Translate Chinese text using local Ollama LLM.')
    parser.add_argument('--model', type=str, default='mistral', help='Ollama model to use (default: mistral)')
    parser.add_argument('--ollama-url', type=str, default='http://localhost:11434/api/generate', help='Ollama API URL')
    parser.add_argument('--test', action='store_true', help='Test translation with a simple phrase')
    args = parser.parse_args()
    
    if args.test:
        print(f'Testing Ollama translation with model "{args.model}"...')
        result = translate_text_ollama('你好，世界', args.model, args.ollama_url)
        print(f'Result: {result}')
        TRANSLATION_CACHE.save()
        return
    
    print('Ollama translation script loaded. Use translate_text_ollama() or translate_segments_ollama() functions.')


if __name__ == '__main__':
    main()
