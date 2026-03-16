#!/usr/bin/env python3
"""
code-roast: Static analysis engine for roasting codebases.

Scans a repo and emits a JSON report with metrics across 9 shame categories.
Claude reads this JSON + roast-rubric.md to synthesize the final roast.

Usage:
    uv run analyze.py [path]          # analyze repo at path (default: cwd)
    uv run analyze.py [path] --debug  # pretty-print JSON to stdout
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.php',
    '.cs', '.cpp', '.c', '.h', '.swift', '.kt', '.rs', '.scala',
    '.vue', '.svelte', '.sh', '.bash', '.dart', '.ex', '.exs', '.lua',
    '.r', '.R', '.m', '.mm', '.pl', '.pm', '.groovy', '.tf',
}

IGNORE_DIRS = {
    'node_modules', '.git', 'vendor', '.venv', 'venv', '__pycache__',
    'dist', 'build', '.next', '.nuxt', 'coverage', '.nyc_output',
    'target', '.gradle', 'pods', 'Pods', '.cache', '.parcel-cache',
    'out', '.svelte-kit', '.turbo', 'tmp', '.tmp', '.idea', '.vscode',
    'static', 'public', 'assets', 'migrations', 'fixtures',
}

TEST_PATTERNS = re.compile(
    r'(test_|_test\.|\.test\.|\.spec\.|_spec\.|__tests__|/tests?/|/specs?/)',
    re.IGNORECASE,
)

# -- Shame patterns --

SHAME_COMMENTS = re.compile(
    r'(?://|#|/\*)\s*(TODO|FIXME|HACK|XXX|BUG|TEMP|WTF|WORKAROUND|KLUDGE|BODGE'
    r'|NOCOMMIT|DO NOT MERGE|DO NOT SUBMIT)',
    re.IGNORECASE,
)

DEBUG_CALLS = re.compile(
    r'\b(console\.log|console\.error|console\.warn|console\.debug'
    r'|debugger\b'
    r'|print\s*\('
    r'|pprint\s*\('
    r'|binding\.pry'
    r'|byebug'
    r'|breakpoint\s*\('
    r'|import\s+pdb'
    r'|pdb\.set_trace'
    r'|dd\s*\(|dump\s*\(|var_dump\s*\('
    r'|fmt\.Print(?:ln|f)?\s*\()\b',
)

EMPTY_CATCH = re.compile(
    r'catch\s*\([^)]*\)\s*\{\s*\}'          # JS/Java: catch(e) {}
    r'|except\s*(?:[^:]+)?:\s*\n\s*pass\b',   # Python: except: pass
    re.DOTALL,
)

COMMENTED_CODE = re.compile(
    r'^\s*(?://|#)\s*(?:'
    r'(?:if|else|for|while|switch|return|import|from|require|const|let|var|def |function |class |async )'
    r')',
    re.MULTILINE,
)

MAGIC_NUMBERS = re.compile(
    r'(?<!["\'\w.#-])(?<!0x)(?<!0b)(?<!0o)'
    r'\b(?!0\b|1\b|2\b|10\b|100\b|1000\b)(\d{2,})\b'
    r'(?!["\'\w%])',
)

LONG_LINE = 120  # chars — above this is a style crime

SHAME_COMMIT_WORDS = re.compile(
    r'\b(wip|fix|fixes|fixup|fixup|temp|tmp|hack|lol|oops|typo|test|'
    r'testing|cleanup|todo|revert|undo|whoops|mistake|'
    r'sorry|hotfix|bandaid|asdf|asdfjkl|'
    r'debug|idk|wtf|nope|nah|meh)\b',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def walk_code_files(root: Path):
    """Yield (path, content) for all code files, skipping ignored dirs."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith('.')]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() in CODE_EXTENSIONS:
                try:
                    content = fpath.read_text(encoding='utf-8', errors='replace')
                    yield fpath, content
                except (OSError, PermissionError):
                    pass


def is_test_file(path: Path) -> bool:
    return bool(TEST_PATTERNS.search(str(path)))


def run_git(args: list, cwd: Path) -> str:
    try:
        result = subprocess.run(
            ['git'] + args, cwd=cwd,
            capture_output=True, text=True, timeout=15,
        )
        return result.stdout.strip()
    except Exception:
        return ''


def count_functions(content: str, ext: str) -> int:
    """Rough function/method count using language-appropriate patterns."""
    patterns = {
        '.py':   r'^\s*(?:async\s+)?def\s+\w+',
        '.js':   r'(?:function\s+\w+|\w+\s*[:=]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
        '.ts':   r'(?:function\s+\w+|\w+\s*[:=]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
        '.jsx':  r'(?:function\s+\w+|\w+\s*[:=]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
        '.tsx':  r'(?:function\s+\w+|\w+\s*[:=]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
        '.java': r'(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+\w+\s*\(',
        '.go':   r'^\s*func\s+',
        '.rb':   r'^\s*def\s+\w+',
        '.swift':r'^\s*func\s+\w+',
        '.kt':   r'^\s*fun\s+\w+',
        '.rs':   r'^\s*(?:pub\s+)?fn\s+\w+',
    }
    pattern = patterns.get(ext)
    if not pattern:
        return 0
    return len(re.findall(pattern, content, re.MULTILINE))


def max_indent_depth(content: str) -> int:
    """Approximate max nesting depth via leading spaces/tabs."""
    max_depth = 0
    for line in content.splitlines():
        if not line.strip():
            continue
        leading = len(line) - len(line.lstrip())
        spaces = leading if '\t' not in line[:leading] else leading * 4
        depth = spaces // 4
        if depth > max_depth:
            max_depth = depth
    return max_depth


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyze(root: Path) -> dict:
    metrics = {
        'repo_path': str(root),
        'analyzed_at': datetime.now(timezone.utc).isoformat(),
        'summary': {},
        'shame_comments': {'total': 0, 'by_type': {}, 'worst_files': []},
        'debug_statements': {'total': 0, 'worst_files': []},
        'long_files': [],
        'god_files': [],
        'deep_nesting': {'max_depth': 0, 'worst_file': None},
        'empty_catches': {'total': 0, 'files': []},
        'commented_code': {'total': 0, 'worst_files': []},
        'magic_numbers': {'total': 0, 'worst_files': []},
        'git': {
            'shame_commits': [],
            'total_commits': 0,
            'shame_ratio': 0.0,
            'available': False,
        },
        'test_coverage': {
            'source_files': 0,
            'test_files': 0,
            'ratio': 0.0,
            'grade': 'unknown',
        },
    }

    total_lines = 0
    total_files = 0
    source_files = 0
    test_files_count = 0

    # Per-file accumulations
    shame_by_file: dict[str, int] = defaultdict(int)
    debug_by_file: dict[str, int] = defaultdict(int)
    comment_code_by_file: dict[str, int] = defaultdict(int)
    magic_by_file: dict[str, int] = defaultdict(int)
    nesting_by_file: dict[str, int] = {}

    for fpath, content in walk_code_files(root):
        rel = str(fpath.relative_to(root))
        lines = content.count('\n') + 1
        total_lines += lines
        total_files += 1

        if is_test_file(fpath):
            test_files_count += 1
        else:
            source_files += 1

        # --- Shame comments ---
        for m in SHAME_COMMENTS.finditer(content):
            kw = m.group(1).upper()
            metrics['shame_comments']['by_type'][kw] = \
                metrics['shame_comments']['by_type'].get(kw, 0) + 1
            metrics['shame_comments']['total'] += 1
            shame_by_file[rel] += 1

        # --- Debug statements ---
        count = len(DEBUG_CALLS.findall(content))
        if count:
            metrics['debug_statements']['total'] += count
            debug_by_file[rel] += count

        # --- Long files ---
        if lines > 300:
            metrics['long_files'].append({'file': rel, 'lines': lines})

        # --- God files (many functions) ---
        fn_count = count_functions(content, fpath.suffix.lower())
        if fn_count >= 10:
            metrics['god_files'].append({'file': rel, 'functions': fn_count})

        # --- Deep nesting ---
        depth = max_indent_depth(content)
        nesting_by_file[rel] = depth
        if depth > metrics['deep_nesting']['max_depth']:
            metrics['deep_nesting']['max_depth'] = depth
            metrics['deep_nesting']['worst_file'] = rel

        # --- Empty catches ---
        ec = len(EMPTY_CATCH.findall(content))
        if ec:
            metrics['empty_catches']['total'] += ec
            metrics['empty_catches']['files'].append({'file': rel, 'count': ec})

        # --- Commented-out code ---
        cc = len(COMMENTED_CODE.findall(content))
        if cc:
            metrics['commented_code']['total'] += cc
            comment_code_by_file[rel] += cc

        # --- Magic numbers ---
        mn = len(MAGIC_NUMBERS.findall(content))
        if mn:
            metrics['magic_numbers']['total'] += mn
            magic_by_file[rel] += mn

    # Sort and cap worst-file lists
    def top5(d: dict) -> list:
        return [{'file': k, 'count': v}
                for k, v in sorted(d.items(), key=lambda x: -x[1])[:5]]

    metrics['shame_comments']['worst_files'] = top5(shame_by_file)
    metrics['debug_statements']['worst_files'] = top5(debug_by_file)
    metrics['commented_code']['worst_files'] = top5(comment_code_by_file)
    metrics['magic_numbers']['worst_files'] = top5(magic_by_file)

    # Sort long_files / god_files descending
    metrics['long_files'].sort(key=lambda x: -x['lines'])
    metrics['long_files'] = metrics['long_files'][:10]
    metrics['god_files'].sort(key=lambda x: -x['functions'])
    metrics['god_files'] = metrics['god_files'][:10]

    # Deep nesting top 5
    top_nesting = sorted(nesting_by_file.items(), key=lambda x: -x[1])[:5]
    metrics['deep_nesting']['top_files'] = [
        {'file': f, 'depth': d} for f, d in top_nesting
    ]

    # --- Test coverage ratio ---
    metrics['test_coverage']['source_files'] = source_files
    metrics['test_coverage']['test_files'] = test_files_count
    if source_files > 0:
        ratio = test_files_count / source_files
        metrics['test_coverage']['ratio'] = round(ratio, 2)
        if ratio >= 0.8:
            grade = 'A'
        elif ratio >= 0.5:
            grade = 'B'
        elif ratio >= 0.2:
            grade = 'C'
        elif ratio >= 0.05:
            grade = 'D'
        else:
            grade = 'F'
        metrics['test_coverage']['grade'] = grade

    # --- Git shame ---
    git_log = run_git(['log', '--oneline', '--no-merges', '-500'], root)
    if git_log:
        metrics['git']['available'] = True
        lines_git = [l.strip() for l in git_log.splitlines() if l.strip()]
        metrics['git']['total_commits'] = len(lines_git)
        shame = []
        for line in lines_git:
            parts = line.split(' ', 1)
            sha = parts[0] if parts else ''
            msg = parts[1] if len(parts) > 1 else ''
            if SHAME_COMMIT_WORDS.search(msg):
                shame.append({'sha': sha, 'message': msg})
        metrics['git']['shame_commits'] = shame[:20]  # cap at 20
        if lines_git:
            metrics['git']['shame_ratio'] = round(len(shame) / len(lines_git), 2)

    # --- Summary ---
    metrics['summary'] = {
        'total_files': total_files,
        'total_lines': total_lines,
        'source_files': source_files,
        'test_files': test_files_count,
    }

    return metrics


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    debug = '--debug' in args
    paths = [a for a in args if not a.startswith('--')]

    root = Path(paths[0]).resolve() if paths else Path.cwd()

    if not root.exists():
        print(f'Error: path not found: {root}', file=sys.stderr)
        sys.exit(1)

    data = analyze(root)

    if debug:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data))


if __name__ == '__main__':
    main()
