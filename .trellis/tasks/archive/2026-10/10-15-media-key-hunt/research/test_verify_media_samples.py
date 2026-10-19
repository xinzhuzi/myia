"""Real codec images in synthetic V2 containers; no private WeChat fixtures."""
import hashlib
import importlib.util
import io
import json
import struct
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PIL import Image

SYNTHETIC_KEY = 'unit-test-key-01'
KEYS = {'aes_key': SYNTHETIC_KEY, 'xor_key': '0x5A'}


@pytest.fixture
def verifier():
    path = Path(__file__).with_name('verify_media_samples.py')
    spec = importlib.util.spec_from_file_location('verify_media_samples', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def component(verifier):
    return verifier.load_component()


def plain_image(seed, fmt='PNG'):
    width, height = 17 + seed, 19
    pixels = bytes((i * 37 + seed * 11) % 256 for i in range(width * height * 3))
    image = Image.frombytes('RGB', (width, height), pixels)
    stream = io.BytesIO()
    image.save(stream, format=fmt)
    return stream.getvalue()


def container(plain, xor_key=0x5A):
    aes_size = 32
    encryptor = Cipher(algorithms.AES(SYNTHETIC_KEY.encode()), modes.ECB()).encryptor()
    cipher = encryptor.update(plain[:aes_size]) + encryptor.finalize()
    middle, tail = plain[aes_size:aes_size + 16], plain[aes_size + 16:]
    return (b'\x07\x08V2\x08\x07' + struct.pack('<II', aes_size, len(tail)) + b'\x01'
            + cipher + middle + bytes(value ^ xor_key for value in tail))


def write_samples(tmp_path, plains=None):
    plains = plains if plains is not None else [plain_image(i) for i in range(3)]
    result = []
    for index, plain in enumerate(plains):
        path = tmp_path / f'private-sample-{index}.dat'
        path.write_bytes(container(plain))
        result.append(path)
    return result


def test_three_decodable_images_pass(verifier, component, tmp_path):
    paths = write_samples(tmp_path, [plain_image(0, 'PNG'), plain_image(1, 'JPEG'), plain_image(2, 'GIF')])
    report = verifier.verify_samples(paths, component, KEYS)
    assert report['success'] and report['verified'] == 3
    assert [row['format'] for row in report['samples']] == ['PNG', 'JPEG', 'GIF']
    assert [row['width'] for row in report['samples']] == [17, 18, 19]


@pytest.mark.parametrize('keys,status', [({}, 'blocked_missing_key'), ({'aes_key': 'short'}, 'invalid_key'),
                                        ({'aes_key': '\u2603' * 16}, 'invalid_key')])
def test_key_intake_failure(verifier, component, tmp_path, keys, status):
    report = verifier.verify_samples(write_samples(tmp_path), component, keys)
    assert not report['success'] and report['status'] == status


def test_wrong_aes_key_rejected(verifier, component, tmp_path):
    report = verifier.verify_samples(write_samples(tmp_path), component,
                                     {'aes_key': 'wrong-key-123456', 'xor_key': '0x5A'})
    assert not report['success'] and report['verified'] == 0


def test_duplicates_do_not_count(verifier, component, tmp_path):
    paths = write_samples(tmp_path)
    paths[2].write_bytes(paths[0].read_bytes())
    report = verifier.verify_samples(paths, component, KEYS)
    assert not report['success'] and report['verified'] == 2
    assert report['samples'][2]['status'] == 'duplicate_input'


def test_reencrypted_same_image_does_not_count(verifier, component, tmp_path):
    paths = write_samples(tmp_path)
    # Different tail encoding, same clear image; omit XOR override to derive it.
    paths[2].write_bytes(container(plain_image(0), xor_key=0xE9))
    report = verifier.verify_samples(paths, component, {'aes_key': SYNTHETIC_KEY})
    assert not report['success'] and report['verified'] == 2
    assert report['samples'][2]['status'] == 'duplicate_image'


@pytest.mark.parametrize('invalid', [b'\xff\xd8\xff' + b'\x00' * 100, plain_image(1)[:-5]])
def test_magic_only_or_corrupt_image_rejected(verifier, component, tmp_path, invalid):
    report = verifier.verify_samples(write_samples(tmp_path, [plain_image(0), plain_image(2), invalid]), component, KEYS)
    assert not report['success'] and report['verified'] == 2


def test_one_bad_sample_prevents_success_even_with_three_valid(verifier, component, tmp_path):
    paths = write_samples(tmp_path)
    invalid = tmp_path / 'bad.dat'
    invalid.write_bytes(b'x' * 100)
    report = verifier.verify_samples(paths + [invalid], component, KEYS)
    assert not report['success'] and report['verified'] == 3
    assert report['samples'][3]['status'] == 'not_v2'


def test_fewer_than_three_rejected(verifier, component, tmp_path):
    report = verifier.verify_samples(write_samples(tmp_path)[:2], component, KEYS)
    assert not report['success'] and report['status'] == 'sample_count_out_of_range'


def test_oversized_image_rejected_before_load(verifier, component, tmp_path, monkeypatch):
    monkeypatch.setattr(verifier, 'MAX_PIXELS', 100)
    report = verifier.verify_samples(write_samples(tmp_path), component, KEYS)
    assert not report['success'] and report['verified'] == 0


def test_report_does_not_leak_input_or_key(verifier, tmp_path, monkeypatch, capsys):
    paths = write_samples(tmp_path)
    key_file = tmp_path / 'private-keys.json'
    key_file.write_text(json.dumps(KEYS))
    monkeypatch.setenv('WX_MEDIA_SKIP_COMPONENT', '1')
    monkeypatch.delenv('WX_MEDIA_AES_KEY', raising=False)
    monkeypatch.delenv('WX_MEDIA_XOR_KEY', raising=False)
    assert verifier.main(['--key-file', str(key_file), *map(str, paths)]) == 0
    captured = capsys.readouterr()
    assert SYNTHETIC_KEY not in captured.out + captured.err
    assert str(tmp_path) not in captured.out + captured.err
    assert hashlib.sha256(paths[0].read_bytes()).hexdigest() not in captured.out
    assert captured.err == ''
    assert json.loads(captured.out)['success'] is True
    assert len(list(tmp_path.iterdir())) == 4  # No clear image outputs.


def test_key_file_parse_error_is_sanitized(verifier, tmp_path, monkeypatch, capsys):
    paths = write_samples(tmp_path)
    key_file = tmp_path / 'keys.json'
    key_file.write_text('not json ' + SYNTHETIC_KEY)
    monkeypatch.setenv('WX_MEDIA_SKIP_COMPONENT', '1')
    assert verifier.main(['--key-file', str(key_file), *map(str, paths)]) == 2
    captured = capsys.readouterr()
    assert captured.err == ''
    assert SYNTHETIC_KEY not in captured.out
    assert json.loads(captured.out)['status'] == 'key_source_error'


def test_bad_container_length_is_rejected(verifier, component, tmp_path):
    paths = write_samples(tmp_path)
    data = paths[0].read_bytes()
    paths[0].write_bytes(data[:6] + struct.pack('<II', 2**31, 1) + data[14:])
    report = verifier.verify_samples(paths, component, KEYS)
    assert report['samples'][0]['status'] == 'invalid_container'
    assert not report['success']


def test_file_size_limit(verifier, component, tmp_path, monkeypatch):
    paths = write_samples(tmp_path)
    monkeypatch.setattr(verifier, 'MAX_FILE_BYTES', 50)
    report = verifier.verify_samples(paths, component, KEYS)
    assert report['verified'] == 0
    assert all(row['status'] == 'invalid_file' for row in report['samples'])


def test_animation_frame_limit(verifier, component, tmp_path, monkeypatch):
    frames = [Image.new('RGB', (20, 20), color) for color in ('red', 'green', 'blue')]
    stream = io.BytesIO()
    frames[0].save(stream, format='GIF', save_all=True, append_images=frames[1:], duration=100)
    paths = write_samples(tmp_path, [plain_image(0), plain_image(1), stream.getvalue()])
    monkeypatch.setattr(verifier, 'MAX_FRAMES', 2)
    report = verifier.verify_samples(paths, component, KEYS)
    assert not report['success'] and report['verified'] == 2


def test_missing_input_file(verifier, component, tmp_path):
    paths = write_samples(tmp_path)
    paths[0] = tmp_path / 'missing.dat'
    report = verifier.verify_samples(paths, component, KEYS)
    assert not report['success'] and report['samples'][0]['status'] == 'invalid_file'
