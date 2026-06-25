#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate Chinese markdown and code comments to English using Ollama LLM."""

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
    
    def __init__(self, cache_file: str = '.translation_cache_ollama.json'):
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


TRANSLATION_CACHE = TranslationCache('.translation_cache_ollama.json')

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
    '健康': 'health',
    '记录': 'record',
    '数据': 'data',
    '分析': 'analysis',
    '报告': 'report',
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

COMMENT_REPLACERS: Dict[str, Callable[[str], str]] = {}


def translate_with_ollama(text: str, model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Use local Ollama LLM to translate Chinese to English."""
    if not text.strip():
        return text
    
    # Check cache first
    cached = TRANSLATION_CACHE.get(text)
    if cached:
        return cached
    
    prompt = f"""Translate the following Chinese text to English. Keep the translation concise and accurate.
Respond with only the translated text, nothing else.

Chinese: {text}
English:"""
    
    try:
        response = requests.post(ollama_url, json={
            'model': model,
            'prompt': prompt,
            'stream': False,
        }, timeout=120)
        
        if response.status_code == 200:
            result = response.json().get('response', '').strip()
            if result:
                TRANSLATION_CACHE.put(text, result)
                return result
    except Exception as e:
        print(f'Warning: Ollama translation failed for "{text}": {e}')
    
    return text


def translate_segments_ollama(segments: List[str], model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> List[str]:
    """Translate segments using Ollama LLM, checking cache first."""
    if not segments:
        return []
    
    results: List[str] = []
    for segment in segments:
        try:
            result = translate_with_ollama(segment, model, ollama_url)
            results.append(result)
        except Exception as e:
            print(f'Failed to translate "{segment}": {e}')
            results.append(segment)
    
    return results


def translate_text(text: str, model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Translate Chinese text to English."""
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


def translate_markdown_file(path: Path, model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
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
        
        output.append(translate_text(line, model, ollama_url))
    
    return ''.join(output)


def translate_python_file(path: Path, model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Translate Chinese comments in Python files."""
    text = path.read_text(encoding='utf-8')
    if not re.search(r'[\u4e00-\u9fff]', text):
        return text

    def repl_comment(match: re.Match) -> str:
        return translate_text(match.group(0), model, ollama_url)

    # Replace line comments
    text = re.sub(r'#[^\n]*', repl_comment, text)
    # Replace docstrings (triple-quoted strings)
    text = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', lambda m: translate_text(m.group(0), model, ollama_url), text, flags=re.DOTALL)
    
    return text


def translate_c_style_file(path: Path, model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Translate Chinese comments in C-style files (C, C++, Java, Go, etc)."""
    text = path.read_text(encoding='utf-8')
    if not re.search(r'[\u4e00-\u9fff]', text):
        return text

    def repl_line(match: re.Match) -> str:
        return translate_text(match.group(0), model, ollama_url)

    def repl_block(match: re.Match) -> str:
        return translate_text(match.group(0), model, ollama_url)

    # Replace line comments //
    text = re.sub(r'//[^\n]*', repl_line, text)
    # Replace block comments /* */
    text = re.sub(r'/\*.*?\*/', repl_block, text, flags=re.DOTALL)
    
    return text


def translate_js_ts_file(path: Path, model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> str:
    """Translate Chinese comments in JavaScript/TypeScript files."""
    return translate_c_style_file(path, model, ollama_url)


FILE_HANDLERS: Dict[str, Callable[[Path, str, str], str]] = {
    '.md': lambda p, m, u: translate_markdown_file(p, m, u),
    '.py': lambda p, m, u: translate_python_file(p, m, u),
    '.js': lambda p, m, u: translate_js_ts_file(p, m, u),
    '.ts': lambda p, m, u: translate_js_ts_file(p, m, u),
    '.tsx': lambda p, m, u: translate_js_ts_file(p, m, u),
    '.jsx': lambda p, m, u: translate_js_ts_file(p, m, u),
    '.java': lambda p, m, u: translate_c_style_file(p, m, u),
    '.go': lambda p, m, u: translate_c_style_file(p, m, u),
    '.c': lambda p, m, u: translate_c_style_file(p, m, u),
    '.cpp': lambda p, m, u: translate_c_style_file(p, m, u),
    '.h': lambda p, m, u: translate_c_style_file(p, m, u),
}


def find_target_files(root: Path, patterns: Iterable[str]) -> List[Path]:
    """Find all files with Chinese text matching the given extensions."""
    files: List[Path] = []
    for path in root.rglob('*'):
        if path.is_file() and path.suffix in patterns:
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            if re.search(r'[\u4e00-\u9fff]', content):
                files.append(path)
    return sorted(files)


def process_files(files: List[Path], dry_run: bool = True, backup: bool = False, model: str = 'qwen3:4b', ollama_url: str = 'http://localhost:11434/api/generate') -> tuple[int, list[Path]]:
    """Process files and translate Chinese text."""
    changed = 0
    updated_files: list[Path] = []
    for i, path in enumerate(files):
        handler = FILE_HANDLERS.get(path.suffix)
        if not handler:
            continue
        
        print(f'Processing {i+1}/{len(files)}: {path}...')
        try:
            new_text = handler(path, model, ollama_url)
            old_text = path.read_text(encoding='utf-8')
            if new_text != old_text:
                changed += 1
                updated_files.append(path)
                print(f'  ✓ Would update: {path}' if dry_run else f'  ✓ Updated: {path}')
                if not dry_run:
                    if backup:
                        backup_path = path.with_suffix(path.suffix + '.bak')
                        backup_path.write_text(old_text, encoding='utf-8')
                        print(f'    - Backup saved: {backup_path}')
                    path.write_text(new_text, encoding='utf-8')
            else:
                print(f'  - No changes needed')
        except Exception as e:
            print(f'  ✗ Error processing {path}: {e}')
    
    return changed, updated_files


def main() -> None:
    parser = argparse.ArgumentParser(description='Translate Chinese text using local Ollama LLM.')
    parser.add_argument('--model', type=str, default='qwen3:4b', help='Ollama model to use (default: qwen3:4b)')
    parser.add_argument('--ollama-url', type=str, default='http://localhost:11434/api/generate', help='Ollama API URL')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dry-run', dest='dry_run', action='store_true', help='Show files that would be updated without writing changes.')
    group.add_argument('--write', dest='dry_run', action='store_false', help='Write translated files back to disk.')
    parser.set_defaults(dry_run=True)
    parser.add_argument('--backup', action='store_true', default=False, help='Create .bak backups before writing files.')
    parser.add_argument('--root', type=str, default='.', help='Root directory to scan.')
    parser.add_argument('--extensions', type=str, default='.md,.py,.js,.ts,.tsx,.jsx,.java,.go,.c,.cpp,.h', help='Comma-separated file extensions to process.')
    args = parser.parse_args()

    # Verify Ollama is running
    try:
        response = requests.get(args.ollama_url.replace('/api/generate', '/api/tags'), timeout=5)
        if response.status_code != 200:
            raise SystemExit(f'Ollama service not responding correctly (status {response.status_code})')
    except Exception as e:
        raise SystemExit(f'Cannot connect to Ollama at {args.ollama_url}: {e}. Make sure to run "ollama serve" first.')

    root = Path(args.root)
    extensions = {ext.strip() for ext in args.extensions.split(',') if ext.strip()}
    files = find_target_files(root, extensions)
    print(f'Found {len(files)} files containing Chinese characters.')
    print(f'Using model: {args.model}')
    print(f'Dry-run mode: {args.dry_run}')
    print()
    
    changed, updated_files = process_files(files, dry_run=args.dry_run, backup=args.backup, model=args.model, ollama_url=args.ollama_url)
    print(f'\nFiles updated: {changed}')
    if changed and args.dry_run:
        print('The following files would be written:')
        for path in updated_files:
            print(f'  - {path}')
    elif changed and not args.dry_run:
        print('The following files were written:')
        for path in updated_files:
            print(f'  - {path}')
    TRANSLATION_CACHE.save()
    print(f'Saved {len(TRANSLATION_CACHE.cache)} translations to cache.')


if __name__ == '__main__':
    main()
