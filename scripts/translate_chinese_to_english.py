#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate Chinese markdown and code comments to English."""

import argparse
import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Iterable, List

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
except ImportError:
    raise SystemExit("Please install deep-translator with pip before running this script.")


class TranslationCache:
    """Cache translations to avoid repeated API calls."""
    
    def __init__(self, cache_file: str = '.translation_cache.json'):
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


class GlobalRateLimiter:
    """Enforce a global request rate limit to avoid backend throttling."""
    
    def __init__(self, min_interval_seconds: float = 2.0):
        self.min_interval_seconds = min_interval_seconds
        self.last_request_time = datetime.now() - timedelta(seconds=min_interval_seconds)
    
    def wait_if_needed(self) -> None:
        """Block until enough time has passed since the last request."""
        elapsed = (datetime.now() - self.last_request_time).total_seconds()
        if elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self.last_request_time = datetime.now()


GLOBAL_RATE_LIMITER = GlobalRateLimiter(min_interval_seconds=2.0)
TRANSLATION_CACHE = TranslationCache('.translation_cache.json')


def make_translators() -> list[tuple[object, str]]:
    """Create a prioritized list of working translator backends."""
    translators = []
    try:
        translators.append((MyMemoryTranslator(source='chinese simplified', target='english'), 'MyMemoryTranslator'))
    except Exception as e:
        print(f'Warning: MyMemoryTranslator unavailable: {e}')
    try:
        translators.append((GoogleTranslator(source='zh-CN', target='en'), 'GoogleTranslator'))
    except Exception as e:
        print(f'Warning: GoogleTranslator unavailable: {e}')
    if not translators:
        raise SystemExit('No translation backend available.')
    return translators

TRANSLATORS = make_translators()
print('Using translator backend(s):', ', '.join(name for _, name in TRANSLATORS))

# Matches Chinese characters with digits/letters and punctuation used in Chinese sentences.
CHINESE_SPAN_RE = re.compile(r'([\u4e00-\u9fffA-Za-z0-9]+(?:[，。？！；：、“”‘’（）《》【】…、]+[\u4e00-\u9fffA-Za-z0-9]+)*)')

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
    '皮肤科': 'dermatology',
    '骨科': 'orthopedics',
    '外科': 'surgery',
    '影像检查': 'imaging examination',
    '生化检查': 'biochemical examination',
    '手术记录': 'surgery records',
    '出院小结': 'discharge summary',
    '最近7天': 'last 7 days',
    '最近30天': 'last 30 days',
    '最近 7 天': 'last 7 days',
    '最近 30 天': 'last 30 days',
    '必带': 'must bring',
    '一般': 'general',
    '建议': 'recommend',
    '症状': 'symptom',
    '科室': 'department',
    '检查': 'examination',
    '就诊': 'medical visit',
    '准备指南': 'preparation guide',
    '就医': 'seek medical treatment',
    '高血压': 'hypertension',
    '糖尿病': 'diabetes',
}

CHINESE_PUNCTUATION_MAP = {
    '，': ',',
    '。': '.',
    '；': ';',
    '：': ':',
    '？': '?',
    '！': '!',
    '、': ',',
    '（': '(',
    '）': ')',
    '【': '[',
    '】': ']',
    '“': '"',
    '”': '"',
    '‘': "'",
    '’': "'",
    '《': '<',
    '》': '>',
    '…': '...',
}

CODE_FENCE_RE = re.compile(r'^(?P<fence>```|~~~)')
INLINE_CODE_RE = re.compile(r'(`+)(.+?)(\1)')

COMMENT_REPLACERS: Dict[str, Callable[[str], str]] = {}


def translate_text(text: str) -> str:
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

    translated_segments = None
    for translator, name in TRANSLATORS:
        try:
            translated_segments = translate_segments(translator, segments)
            break
        except Exception as e:
            print(f'Warning: {name} failed for segments batch -> {e}')
            continue

    if translated_segments is None:
        translated_segments = segments

    translated_iter = iter(translated_segments)
    return ''.join(part if part is not None else next(translated_iter) for part in parts)


def translate_segments(translator: object, segments: List[str]) -> List[str]:
    """Translate a batch of Chinese segments, checking cache first, splitting on failure and retrying on rate limits."""
    if not segments:
        return []

    # Check cache first
    results: List[str | None] = []
    uncached_segments: List[tuple[int, str]] = []
    for i, segment in enumerate(segments):
        cached = TRANSLATION_CACHE.get(segment)
        if cached:
            results.append(cached)
        else:
            results.append(None)
            uncached_segments.append((i, segment))
    
    # If all segments are cached, return immediately
    if not uncached_segments:
        return [r for r in results if r is not None]
    
    # Translate only uncached segments
    batch_fn = getattr(translator, 'translate_batch', None)
    if batch_fn is None:
        uncached_translations = [translate_segment(translator, segment) for _, segment in uncached_segments]
    else:
        retries = 3
        backoff = 5.0  # Start with 5 seconds backoff
        uncached_translations = None
        for attempt in range(1, retries + 1):
            try:
                GLOBAL_RATE_LIMITER.wait_if_needed()
                uncached_translations = batch_fn([segment for _, segment in uncached_segments])
                break
            except Exception as e:
                message = str(e).lower()
                if 'too many requests' in message or 'rate limit' in message or 'retry after' in message:
                    if len(uncached_segments) == 1:
                        uncached_translations = [translate_segment(translator, uncached_segments[0][1])]
                        break
                    if attempt == retries:
                        raise
                    print(f'Rate limit hit on batch of {len(uncached_segments)} uncached segments. Waiting {backoff}s before retry.')
                    time.sleep(backoff)
                    backoff *= 2  # Exponential backoff: 5s, 10s, 20s
                    continue
                if len(uncached_segments) > 1:
                    mid = len(uncached_segments) // 2
                    first_half = translate_segments(translator, [s for _, s in uncached_segments[:mid]])
                    second_half = translate_segments(translator, [s for _, s in uncached_segments[mid:]])
                    uncached_translations = first_half + second_half
                    break
                raise
        
        if uncached_translations is None:
            uncached_translations = [segment for _, segment in uncached_segments]
    
    # Cache and merge results
    cache_updates = {}
    for (orig_idx, segment), translation in zip(uncached_segments, uncached_translations):
        results[orig_idx] = translation
        cache_updates[segment] = translation
    
    TRANSLATION_CACHE.put_many(cache_updates)
    
    return [r for r in results if r is not None]


def translate_segment(translator: object, segment: str) -> str:
    """Translate a single Chinese segment with aggressive exponential backoff on rate limits. Uses cache first."""
    # Check cache first
    cached = TRANSLATION_CACHE.get(segment)
    if cached:
        return cached
    
    retries = 5
    backoff = 5.0  # Start with 5 seconds backoff
    for attempt in range(1, retries + 1):
        try:
            GLOBAL_RATE_LIMITER.wait_if_needed()
            result = translator.translate(segment)
            TRANSLATION_CACHE.put(segment, result)
            return result
        except Exception as e:
            message = str(e).lower()
            if 'too many requests' in message or 'rate limit' in message or 'retry after' in message:
                if attempt == retries:
                    raise
                print(f'Rate limit on segment. Waiting {backoff}s before retry (attempt {attempt}/{retries}).')
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff: 5s, 10s, 20s, 40s, 80s
                continue
            raise



def translate_markdown_line(line: str) -> str:
    if not re.search(r'[\u4e00-\u9fff]', line):
        return line

    # Protect inline code segments from translation.
    segments = []
    pos = 0
    for match in INLINE_CODE_RE.finditer(line):
        segments.append(translate_text(line[pos:match.start()]))
        segments.append(match.group(0))
        pos = match.end()
    segments.append(translate_text(line[pos:]))
    return ''.join(segments)


def translate_markdown_file(path: Path) -> str:
    output_lines: List[str] = []
    in_code_block = False
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if CODE_FENCE_RE.match(line):
                in_code_block = not in_code_block
                output_lines.append(line)
                continue
            if in_code_block:
                output_lines.append(line)
                continue
            output_lines.append(translate_markdown_line(line))
    return ''.join(output_lines)


def translate_comment_line(line: str, prefix: str) -> str:
    if not re.search(r'[\u4e00-\u9fff]', line):
        return line
    before, sep, comment = line.partition(prefix)
    if not sep:
        return line
    return f'{before}{sep}{translate_text(comment)}'


def translate_python_file(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    if not re.search(r'[\u4e00-\u9fff]', text):
        return text

    output: List[str] = []
    in_triple = False
    triple_delim = None
    lines = text.splitlines(keepends=True)
    for line in lines:
        if in_triple:
            if triple_delim and triple_delim in line:
                # translate within triple-quoted string content
                in_triple = False
                output.append(translate_text(line))
                triple_delim = None
            else:
                output.append(translate_text(line))
            continue

        if line.lstrip().startswith('#'):
            output.append(translate_comment_line(line, '#'))
            continue

        if '"""' in line or "'''" in line:
            delim = '"""' if '"""' in line else "'''"
            if line.count(delim) == 1:
                in_triple = True
                triple_delim = delim
            output.append(translate_text(line))
            continue

        output.append(line)
    return ''.join(output)


def translate_c_style_file(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    if not re.search(r'[\u4e00-\u9fff]', text):
        return text

    # Translate line comments and block comments.
    def repl_line(match: re.Match) -> str:
        prefix = match.group(1)
        comment = match.group(2)
        return f'{prefix}{translate_text(comment)}'

    def repl_block(match: re.Match) -> str:
        content = match.group(1)
        return f'/*{translate_text(content)}*/'

    text = re.sub(r'(//)(.*)$', repl_line, text, flags=re.MULTILINE)
    text = re.sub(r'/\*(.*?)\*/', repl_block, text, flags=re.DOTALL)
    return text


def translate_js_ts_file(path: Path) -> str:
    return translate_c_style_file(path)


FILE_HANDLERS: Dict[str, Callable[[Path], str]] = {
    '.md': translate_markdown_file,
    '.py': translate_python_file,
    '.js': translate_js_ts_file,
    '.ts': translate_js_ts_file,
    '.tsx': translate_js_ts_file,
    '.jsx': translate_js_ts_file,
    '.java': translate_c_style_file,
    '.go': translate_c_style_file,
    '.c': translate_c_style_file,
    '.cpp': translate_c_style_file,
    '.h': translate_c_style_file,
}


def find_target_files(root: Path, patterns: Iterable[str]) -> List[Path]:
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


def process_files(files: List[Path], dry_run: bool = True) -> int:
    changed = 0
    for i, path in enumerate(files):
        handler = FILE_HANDLERS.get(path.suffix)
        if not handler:
            continue
        new_text = handler(path)
        old_text = path.read_text(encoding='utf-8')
        if new_text != old_text:
            changed += 1
            print(f'Updated: {path}')
            if not dry_run:
                path.write_text(new_text, encoding='utf-8')
        # Add a small delay between files to let the backend breathe
        if i < len(files) - 1:
            time.sleep(0.5)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description='Translate Chinese text in markdown and code comments to English.')
    parser.add_argument('--dry-run', action='store_true', default=False, help='Show files that would be updated without writing changes.')
    parser.add_argument('--root', type=str, default='.', help='Root directory to scan.')
    parser.add_argument('--extensions', type=str, default='.md,.py,.js,.ts,.tsx,.jsx,.java,.go,.c,.cpp,.h', help='Comma-separated file extensions to process.')
    args = parser.parse_args()

    root = Path(args.root)
    extensions = {ext.strip() for ext in args.extensions.split(',') if ext.strip()}
    files = find_target_files(root, extensions)
    print(f'Found {len(files)} files containing Chinese characters.')
    changed = process_files(files, dry_run=args.dry_run)
    print(f'Files updated: {changed}')
    TRANSLATION_CACHE.save()
    print(f'Saved {len(TRANSLATION_CACHE.cache)} translations to cache.')



if __name__ == '__main__':
    main()
