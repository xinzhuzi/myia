"""Offline V2 image acceptance; never attaches, provisions keys or writes images."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import struct
import warnings
from pathlib import Path

from PIL import Image

importlib.import_module('cryptography.hazmat.primitives.ciphers')  # Require in-process AES.

MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_PIXELS = 40_000_000
MAX_TOTAL_PIXELS = 160_000_000
MAX_FRAMES = 128
MIN_SAMPLES = 3
MAX_SAMPLES = 32
IMAGE_FORMATS = {'jpg': 'JPEG', 'png': 'PNG', 'gif': 'GIF', 'webp': 'WEBP'}


def load_component():
    path = Path(__file__).resolve().parents[4] / 'scripts' / 'wechat-bridge-mediadecrypt.py'
    spec = importlib.util.spec_from_file_location('offline_media_component', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def image_metadata(payload, extension):
    """verify() alone does not decode JPEG pixels; reopen and load every frame."""
    expected = IMAGE_FORMATS.get(extension)
    if expected is None:
        raise ValueError('Unsupported image format')
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(payload)) as image:
            if image.format != expected:
                raise ValueError('Format mismatch')
            image.verify()
        with Image.open(io.BytesIO(payload)) as image:
            frames = getattr(image, 'n_frames', 1)
            if not 1 <= frames <= MAX_FRAMES:
                raise ValueError('Frame limit')
            size = image.size
            pixels = 0
            for index in range(frames):
                image.seek(index)
                width, height = image.size
                pixels += width * height
                if not 0 < width * height <= MAX_PIXELS or pixels > MAX_TOTAL_PIXELS:
                    raise ValueError('Pixel limit')
                image.load()
    return {'format': expected, 'width': size[0], 'height': size[1], 'frames': frames}


def verify_samples(paths, component, keys):
    """Safe report only: no secret values, private paths, digests or plaintext."""
    report = {'success': False, 'status': 'failed', 'provided': len(paths),
              'required': MIN_SAMPLES, 'verified': 0, 'samples': []}
    if not MIN_SAMPLES <= len(paths) <= MAX_SAMPLES:
        report['status'] = 'sample_count_out_of_range'
        return report
    try:
        parsed_key = component._parse_aes_key(keys.get('aes_key'))
    except (ValueError, UnicodeError, AttributeError, TypeError):
        parsed_key = None
    if parsed_key is None:
        report['status'] = 'invalid_key' if keys.get('aes_key') else 'blocked_missing_key'
        return report
    encrypted_seen = set()
    plain_seen = set()
    for index, path in enumerate(paths, 1):
        row = {'sample': index, 'status': 'failed'}
        report['samples'].append(row)
        try:
            path = Path(path)
            if not path.is_file() or not 47 <= path.stat().st_size <= MAX_FILE_BYTES:
                row['status'] = 'invalid_file'
                continue
            # Bound read even if the source grows after stat.
            with path.open('rb') as stream:
                data = stream.read(MAX_FILE_BYTES + 1)
            if len(data) > MAX_FILE_BYTES:
                row['status'] = 'invalid_file'
                continue
            if data[:6] != component._DAT_V2_MAGIC or data[14] != component._DAT_HEADER_VER:
                row['status'] = 'not_v2'
                continue
            aes_size, xor_size = struct.unpack_from('<II', data, 6)
            if aes_size <= 0 or xor_size <= 0 or 15 + (aes_size + 15) // 16 * 16 > len(data) - xor_size:
                row['status'] = 'invalid_container'
                continue
            digest = hashlib.sha256(data).digest()
            if digest in encrypted_seen:
                row['status'] = 'duplicate_input'
                continue
            encrypted_seen.add(digest)
            plain = component.decrypt_dat(data, keys)
            metadata = image_metadata(plain, component.guess_ext(plain))
            plain_digest = hashlib.sha256(plain).digest()
            if plain_digest in plain_seen:
                row['status'] = 'duplicate_image'
                continue
            plain_seen.add(plain_digest)
            row.update(metadata, status='verified')
            report['verified'] += 1
        except (OSError, ValueError, SyntaxError, EOFError, struct.error,
                Image.DecompressionBombError, Image.DecompressionBombWarning,
                component.DecryptError):
            # Library error text may contain source data; deliberately omit it.
            row['status'] = 'decrypt_or_image_invalid'
    report['success'] = report['verified'] == len(paths)
    report['status'] = 'verified' if report['success'] else 'failed'
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description='Offline acceptance of >=3 independent V2 images; no debugger.')
    parser.add_argument('--key-file', help='Existing private JSON key file; never pass a key value as an argument.')
    parser.add_argument('samples', nargs='+', type=Path, help='Explicit V2 dat sample files (3..32).')
    args = parser.parse_args(argv)
    component = load_component()
    # Existing key intake can emit diagnostics; never surface private input text.
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            keys = component.load_keys(args.key_file)
    except (OSError, ValueError, SystemExit):
        report = {'success': False, 'status': 'key_source_error'}
    else:
        report = verify_samples(args.samples, component, keys)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report['success'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
