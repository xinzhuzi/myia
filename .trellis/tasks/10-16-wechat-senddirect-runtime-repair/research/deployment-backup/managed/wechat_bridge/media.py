"""聊天媒体寻径与解密编排(task 10-14-wechat-media-sns R1/R2)。

R1 外部媒体解密件(协议 v1 = docs/wechat-mediadecrypt.md,形态照取钥器协议):

- MYIA 产品代码**零解密算法实现**:V4 `.dat` 与朋友圈 CDN 流的解密能力整体
  外包给用户自备的外部可执行件(`media_decrypt_path` 配置,管理命令
  ``localdb media-decrypt set|get|clear`` 代写)。桥 spawn 件 → stdin 单行
  JSON → stdout NDJSON(progress + result 恰一次)→ 退出码矩阵 → 产物
  magic 校验 → 原子落媒体缓存。
- **钥匙边界**:V4 媒体钥桥零接触零落盘(件内自理);`decrypt_stream` 的
  CDN key(库内 XML 明文数字串)仅内存过手——**stdin 载荷零日志**,诊断
  只承载 action 与路径名。
- 未配置/不可执行 = exit 23 ``media_unavailable``(媒体面结构化降级,文本链
  query/sns feed/导出正文零影响);解密失败 = 既有 exit 22
  ``decrypt_failed``。

R2 聊天媒体寻径(纯只读,复用 localdb_query 已交付的 ``Msg_<md5>`` 分表/
``real_sender_id`` 反解):

- local_type 3=图:key(消息行 ``packed_info_data`` protobuf 内的 32-hex 串)
  → ``msg/attach/<dir1>/<yyyy-mm>/Img/<key>.dat``(正图)+
  ``<key>_t.dat``(缩略图,**缩略图优先呈现**;本轮实测近 40 条 _t 命中
  40/40、正图 27/40)。dir1 与 username 推导关系未实证 → glob 兜底合法。
- local_type 43=视频:``msg/video/<yyyy-mm>/<key>.mp4`` + ``<key>_thumb.jpg``,
  **全明文直读零解密**。
- 其余类型只报形状(status=null)。

解密编排与缓存(G5 同族纪律):

- 缓存 = 数据根私有区 ``wechat-localdb/media-cache/<sha256(源路径+源mtime+
  源size) 前16>.<ext>``,tmp+rename 原子落位,文件 600/目录 700。幂等:
  键命中零再 spawn;源 mtime/size 变 = 新键重解。容量治理 = 配置
  ``media_cache_capacity_mb``(缺省 2048,LRU 按 mtime)。
- **media-cache 同时是 C6(HTTP 媒体端点)的指定读取落点**(allowlist 限定
  仅该目录;docs/wechat-mediadecrypt.md §7 注记)。

私有数据红线:媒体内容/钥材料不入日志——错误消息只承载形状(计数/路径名)。
微信侧文件零写入、微信进程零接触;本模块零出网(CDN GET 豁免归 sns_export
``--with-media``,缺省关)。
"""

from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

from .codes import DECRYPT_FAILED, EXIT_USAGE, BridgeError
from .config import myssia_home
from .localdb import LOCALDB_PRIVATE_DIR, _proto_length_delimited, ensure_decrypted_copies
from .localdb_query import (
    MSG_TYPE_NAMES,
    _columns,
    _open_copy,
    _pick,
    _sender_name,
    find_message_tables,
    name2id_maps,
)

try:  # codes 表封闭(先改 design §6 再进表);接线批由集成员统一落码
    from .codes import MEDIA_UNAVAILABLE
except ImportError:  # pragma: no cover - codes.py 未含 23 号码期间
    #: exit 23 media_unavailable(design §6 修订 2026-10-14;AC1 法定语义)。
    MEDIA_UNAVAILABLE = 23

__all__ = [
    "MEDIA_CACHE_DIR_NAME",
    "MEDIA_DECRYPT_UNCONFIGURED_MESSAGE",
    "MEDIA_PROVIDER_TIMEOUT_SECONDS",
    "PROVIDER_ACTION_DECRYPT_DAT",
    "PROVIDER_ACTION_DECRYPT_STREAM",
    "MAGIC_SIGS",
    "STATUS_DECRYPTED",
    "STATUS_FILE_MISSING",
    "STATUS_PENDING_DECRYPT",
    "STATUS_PLAINTEXT_VIDEO",
    "STATUS_PROVIDER_UNCONFIGURED",
    "STATUS_WXGF",
    "cache_dir",
    "cache_key_for",
    "decrypt_dat_file",
    "decrypt_stream_file",
    "ensure_cache_capacity",
    "media_decrypt_command",
    "media_extract_key",
    "media_provider_path",
    "media_scan_history",
    "media_status",
    "run_media_provider",
    "scan_chat_media",
    "verify_output_magic",
]

#: 媒体缓存目录名(数据根私有区 wechat-localdb/ 下)。
MEDIA_CACHE_DIR_NAME = "media-cache"
#: 解密件子进程硬上限(协议 §6:120 秒全程预算,超时 kill 进程组)。
MEDIA_PROVIDER_TIMEOUT_SECONDS = 120.0
#: 未配置媒体解密件的法定错误文案(协议 §8;AC1 锚文本)。
MEDIA_DECRYPT_UNCONFIGURED_MESSAGE = "未配置媒体解密件,请在设置中指定可执行文件路径"
#: 协议 v1 两动作(桥只发这两个;未知动作属件侧事务)。
PROVIDER_ACTION_DECRYPT_DAT = "decrypt_dat"
PROVIDER_ACTION_DECRYPT_STREAM = "decrypt_stream"

#: 产物魔数表(协议 §7:ext 与首字节一致才收;wxgf 免对照)。
#: 形状 = ext → [(offset, magic), ...](任一签名组全对即过;webp 双段)。
MAGIC_SIGS: dict[str, list[tuple[int, bytes]]] = {
    "jpg": [(0, b"\xff\xd8\xff")],
    "png": [(0, b"\x89PNG\r\n\x1a\n")],
    "webp": [(0, b"RIFF"), (8, b"WEBP")],
    "gif": [(0, b"GIF87a"), (0, b"GIF89a")],
    "mp4": [(4, b"ftyp")],
}
#: 同格式别名规整(缓存后缀统一,防 jpeg/jpg 双份)。
_EXT_ALIASES = {"jpeg": "jpg"}

# —— 状态词面(R2/R3 词汇判例,全人话)——
STATUS_PLAINTEXT_VIDEO = "明文直读(视频)"
STATUS_PENDING_DECRYPT = "待解密"
STATUS_FILE_MISSING = "文件缺失"
STATUS_PROVIDER_UNCONFIGURED = "未配置解密件"
STATUS_DECRYPTED = "已解密"
STATUS_WXGF = "实况格式,暂不支持预览"
STATUS_DECRYPT_FAILED = "解密失败"

_HEX32 = set("0123456789abcdefABCDEF")


# =====================================================================
# 配置 duck-type(config.py 键接线批归集成员;getattr 容错与 key_provider 同判例)
# =====================================================================


def media_provider_path(config: Any) -> str:
    """已配置的媒体解密件路径(空白 = 未配置;duck-type 容错测试替身)。"""
    return str(getattr(config, "media_decrypt_path", "") or "").strip()


def media_capacity_mb(config: Any) -> int:
    """媒体缓存容量上限 MB(config ``media_cache_capacity_mb``,缺省 2048)。"""
    raw = getattr(config, "media_cache_capacity_mb", None)
    if isinstance(raw, int) and not isinstance(raw, bool) and raw > 0:
        return raw
    return 2048


def cache_dir(data_root: Path | None = None) -> Path:
    """媒体缓存目录(数据根私有区 wechat-localdb/media-cache)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / LOCALDB_PRIVATE_DIR / MEDIA_CACHE_DIR_NAME


def cache_key_for(source: Path) -> str:
    """缓存键 = sha256(源路径 + 源mtime + 源size) 前 16 hex(幂等判据)。"""
    stat = source.stat()
    digest = hashlib.sha256(
        f"{source}|{stat.st_mtime}|{stat.st_size}".encode("utf-8")
    ).hexdigest()
    return digest[:16]


def normalize_ext(ext: str) -> str:
    """产物格式规整(小写 + jpeg→jpg 别名归一)。"""
    value = ext.strip().lower()
    return _EXT_ALIASES.get(value, value)


def verify_output_magic(path: Path, ext: str, *, is_wxgf: bool = False) -> str:
    """产物 magic 校验(协议 §7):首字节与声明的 ext 一致才收。

    wxgf(微信实况专有容器,无标准魔数)免对照原样保留。未知 ext = 拒收。
    返回规整后的 ext(缓存后缀用)。

    Raises:
        BridgeError: exit 22 ``decrypt_failed``(magic 不符/未知格式/产物缺位)。
    """
    normalized = normalize_ext(ext)
    if is_wxgf or normalized == "wxgf":
        if not path.is_file():
            raise BridgeError(
                DECRYPT_FAILED, f"解密件未产出文件(out_path 缺位): {path.name}"
            )
        return "wxgf"
    sigs = MAGIC_SIGS.get(normalized)
    if sigs is None:
        raise BridgeError(
            DECRYPT_FAILED,
            f"解密件声明了未知产物格式 {ext!r}(合法: {'/'.join(sorted(MAGIC_SIGS))}/wxgf)",
            fix_hint="协议 §5:ext 取 jpg/png/webp/gif/mp4/wxgf;wxgf 须同时报 is_wxgf=true",
        )
    try:
        with path.open("rb") as fh:
            head = fh.read(16)
    except OSError as exc:
        raise BridgeError(
            DECRYPT_FAILED,
            f"解密产物不可读({type(exc).__name__}): {path.name}",
        ) from exc
    for offset, magic in sigs:
        if head[offset : offset + len(magic)] != magic:
            raise BridgeError(
                DECRYPT_FAILED,
                f"产物格式与声明不符(声明 {normalized},首字节不符): {path.name}",
                fix_hint="协议 §7:桥按标准魔数表核对产物;件应校验自产 ext 或修正算法",
            )
    return normalized


# =====================================================================
# R1 外部件协议执行(spawn + NDJSON + 退出码矩阵;stdin 载荷零日志)
# =====================================================================


def _kill_process_group(proc: subprocess.Popen) -> None:
    """kill 解密件进程组(start_new_session spawn → pgid == pid)。"""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except OSError:
        try:
            proc.kill()
        except OSError:
            pass


def _stderr_tail(text: str, limit: int = 500) -> str:
    """stderr 尾部截取(协议 §6:失败场景附入错误信息;只入消息不落盘)。"""
    return text[-limit:]


def run_media_provider(
    provider_path: str,
    request: dict[str, Any],
    *,
    timeout: float = MEDIA_PROVIDER_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """spawn 外部媒体解密件(协议 v1 全链;任何失败 = exit 22/23,无降级)。

    stdin 单行 JSON 请求(**载荷零日志**:诊断只携带 action 与文件名)→
    stdout NDJSON(progress 0..N + result 恰一次;首条 result 即终态)→
    退出码矩阵判定(协议 §6)。成功返回 result 字典(success=true 必含)。

    Raises:
        BridgeError: exit 23(spawn 失败/件不可执行)或 exit 22(件侧一切
            解密失败;消息只承载形状与件自报 error,绝无钥材料)。
    """
    action = str(request.get("action") or "?")
    exe = Path(provider_path).expanduser()
    try:
        proc = subprocess.Popen(  # noqa: S603 - 用户自备外部件,契约=docs/wechat-mediadecrypt.md
            [str(exe)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as exc:
        raise BridgeError(
            MEDIA_UNAVAILABLE,
            f"媒体解密件子进程启动失败({type(exc).__name__}): {exe}",
            fix_hint="核对路径存在且有可执行位(localdb media-decrypt get 可查在位状态)",
        ) from exc
    try:
        out_bytes, err_bytes = proc.communicate(
            json.dumps(request, ensure_ascii=False).encode("utf-8") + b"\n",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        _kill_process_group(proc)
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:  # pragma: no cover - SIGKILL 后罕见
            pass
        raise BridgeError(
            DECRYPT_FAILED,
            f"媒体解密件超时(>{timeout:.0f} 秒已 kill 子进程): {exe.name}(action={action})",
            fix_hint="协议 v1 硬上限 120 秒;预计耗时的步骤应尽早输出 result 或主动失败",
        )

    result: dict[str, Any] | None = None
    progress_lines = 0
    junk_lines = 0
    for raw_line in (out_bytes or b"").decode("utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or result is not None:
            continue  # result 即终态,其后行忽略排空(协议 §5 违例取舍)
        try:
            obj = json.loads(line)
        except ValueError:
            junk_lines += 1
            continue
        if not isinstance(obj, dict):
            junk_lines += 1
            continue
        obj_type = obj.get("type")
        if obj_type == "progress":
            progress_lines += 1
        elif obj_type == "result":
            result = obj
        else:
            junk_lines += 1

    if result is not None and result.get("success") is False:
        provider_error = (
            str(result.get("error") or "").strip()
            or "(解密件未给出人话 error 字段)"
        )
        raise BridgeError(
            DECRYPT_FAILED,
            f"媒体解密件报告失败: {provider_error}(action={action})",
            fix_hint="件自报错误原样透传(协议 §6);排查解密件实现或更换解密件",
        )
    if proc.returncode != 0:
        tail = _stderr_tail((err_bytes or b"").decode("utf-8", errors="replace")).strip()
        detail = f";stderr 尾部: {tail}" if tail else ""
        raise BridgeError(
            DECRYPT_FAILED,
            f"媒体解密件异常退出(exit={proc.returncode}): {exe.name}(action={action}){detail}",
        )
    if result is None:
        raise BridgeError(
            DECRYPT_FAILED,
            f"媒体解密件未返回结果(退出码 0 但无 result 行;progress {progress_lines} 行,"
            f"非协议行 {junk_lines} 行): {exe.name}",
            fix_hint="协议 §6:退出码 0 必须恰有一条 result;调试输出一律走 stderr",
        )
    if result.get("success") is not True:
        raise BridgeError(
            DECRYPT_FAILED,
            f"解密件 result 行形状不符(success 须为布尔): {exe.name}",
        )
    if not str(result.get("ext") or "").strip():
        raise BridgeError(
            DECRYPT_FAILED,
            f"解密件 result 缺 ext 字段: {exe.name}",
            fix_hint="协议 §5:成功形态必含 ext(jpg/png/webp/gif/mp4/wxgf)",
        )
    return result


# =====================================================================
# 解密编排 + 媒体缓存(幂等/原子/LRU)
# =====================================================================


def _cached_entry(directory: Path, key: str) -> Path | None:
    """按缓存键找既有条目(幂等判据:键 = 源路径+mtime+size)。"""
    if not directory.is_dir():
        return None
    matches = sorted(p for p in directory.glob(f"{key}.*") if p.is_file())
    return matches[0] if matches else None


def ensure_cache_capacity(directory: Path, capacity_mb: int) -> dict[str, object]:
    """LRU 容量治理:超上限按 mtime 从旧到新清到限额内(纯派生缓存可安全清)。

    Returns:
        形状级统计:{"files","total_bytes","capacity_mb","removed"}。
    """
    if not directory.is_dir():
        return {"files": 0, "total_bytes": 0, "capacity_mb": capacity_mb, "removed": 0}
    entries: list[tuple[Path, int, float]] = []
    total = 0
    for item in directory.iterdir():
        if not item.is_file() or item.name.startswith("."):
            continue
        try:
            stat = item.stat()
        except OSError:
            continue
        entries.append((item, stat.st_size, stat.st_mtime))
        total += stat.st_size
    removed = 0
    capacity_bytes = capacity_mb * 1024 * 1024
    if total > capacity_bytes and entries:
        entries.sort(key=lambda entry: entry[2])  # LRU:最旧先清
        for item, size, _mtime in entries:
            if total <= capacity_bytes:
                break
            try:
                item.unlink()
            except OSError:
                continue
            total -= size
            removed += 1
    return {
        "files": len(entries) - removed,
        "total_bytes": total,
        "capacity_mb": capacity_mb,
        "removed": removed,
    }


def _result_dims(result: dict[str, Any]) -> dict[str, Any]:
    """result 的 width/height 透传(int 化;形状异常 = None 如实)。"""
    dims: dict[str, Any] = {}
    for field in ("width", "height"):
        value = result.get(field)
        try:
            dims[field] = int(value) if value is not None else None
        except (TypeError, ValueError):
            dims[field] = None
    return dims


def decrypt_dat_file(
    dat_path: str | Path,
    config: Any,
    *,
    data_root: Path | None = None,
    provider_runner: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, object]:
    """``localdb media decrypt`` 全链:外部件解密 + magic 校验 + 原子落缓存。

    幂等:缓存键(sha256 源路径+mtime+size 前 16)命中 = **零 spawn** 直回;
    源 mtime/size 变 = 新键重解。未配置件 = exit 23 法定文案(AC1)。

    Returns:
        ``{"dat_path","cached_path","ext","is_wxgf","width","height",
        "cache": "hit"|"miss"}``(形状级,零内容)。
    """
    provider = media_provider_path(config)
    if not provider:
        raise BridgeError(
            MEDIA_UNAVAILABLE,
            MEDIA_DECRYPT_UNCONFIGURED_MESSAGE,
            fix_hint=(
                "wechat-bridge localdb media-decrypt set <媒体解密件可执行文件路径> "
                "配置后重试(协议文档 docs/wechat-mediadecrypt.md)"
            ),
        )
    source = Path(dat_path).expanduser()
    if not source.is_file():
        raise BridgeError(
            EXIT_USAGE,
            f"待解密的源文件不存在: {source}",
            code="usage",
            fix_hint="给出 .dat 文件的绝对路径(localdb media scan 可查在场文件)",
        )
    directory = cache_dir(data_root)
    directory.mkdir(parents=True, exist_ok=True)
    os.chmod(directory, 0o700)
    key = cache_key_for(source)
    existing = _cached_entry(directory, key)
    if existing is not None:
        return {
            "dat_path": str(source),
            "cached_path": str(existing),
            "ext": existing.suffix.lstrip(".") or None,
            "is_wxgf": existing.suffix == ".wxgf",
            "width": None,
            "height": None,
            "cache": "hit",
        }
    runner = provider_runner if provider_runner is not None else run_media_provider
    tmp_out = directory / f".tmp-{os.getpid()}-{key}"
    try:
        result = runner(
            provider,
            {
                "action": PROVIDER_ACTION_DECRYPT_DAT,
                "dat_path": str(source),
                "out_path": str(tmp_out),
            },
        )
        is_wxgf = bool(result.get("is_wxgf"))
        ext = verify_output_magic(tmp_out, str(result.get("ext")), is_wxgf=is_wxgf)
        target = directory / f"{key}.{ext}"
        os.replace(tmp_out, target)
        os.chmod(target, 0o600)
    finally:
        if tmp_out.exists():
            try:
                tmp_out.unlink()
            except OSError:
                pass
    ensure_cache_capacity(directory, media_capacity_mb(config))
    payload: dict[str, object] = {
        "dat_path": str(source),
        "cached_path": str(target),
        "ext": ext,
        "is_wxgf": is_wxgf,
        "cache": "miss",
    }
    payload.update(_result_dims(result))
    return payload


def decrypt_stream_file(
    in_path: str | Path,
    key: str,
    config: Any,
    out_base: Path,
    *,
    provider_runner: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, object]:
    """``decrypt_stream`` 动作桥侧执行(R4:CDN 下载落盘后交件解密流)。

    ``key`` = sns 库 content XML 的数字串(库内明文字段;stdin 单次透传,
    **零日志零落盘**)。产物写 ``out_base`` 同目录临时文件,magic 校验通过
    后原子改名 ``<out_base>.<ext>``。调用方(sns_export)负责临时密文与
    失败词面。

    Raises:
        BridgeError: exit 23(未配置/不可执行)或 exit 22(件侧失败/magic 不符)。
    """
    provider = media_provider_path(config)
    if not provider:
        raise BridgeError(MEDIA_UNAVAILABLE, MEDIA_DECRYPT_UNCONFIGURED_MESSAGE)
    runner = provider_runner if provider_runner is not None else run_media_provider
    tmp_out = out_base.with_name(f".tmp-{os.getpid()}-{out_base.name}")
    try:
        result = runner(
            provider,
            {
                "action": PROVIDER_ACTION_DECRYPT_STREAM,
                "in_path": str(in_path),
                "key": str(key),
                "out_path": str(tmp_out),
            },
        )
        is_wxgf = bool(result.get("is_wxgf"))
        ext = verify_output_magic(tmp_out, str(result.get("ext")), is_wxgf=is_wxgf)
        target = out_base.with_suffix(f".{ext}")
        os.replace(tmp_out, target)
        os.chmod(target, 0o600)
    finally:
        if tmp_out.exists():
            try:
                tmp_out.unlink()
            except OSError:
                pass
    payload: dict[str, object] = {
        "path": str(target),
        "ext": ext,
        "is_wxgf": is_wxgf,
    }
    payload.update(_result_dims(result))
    return payload


def media_decrypt_command(
    dat_path: str, config: Any, *, data_root: Path | None = None
) -> dict[str, object]:
    """``localdb media decrypt <dat_path>`` 应答载荷(命令壳在 cli.py 接线批)。"""
    inner = decrypt_dat_file(dat_path, config, data_root=data_root)
    return {"media_decrypt": inner}


# =====================================================================
# R2 寻径(纯只读;消息域解密副本 + msg/ 明文树)
# =====================================================================

#: 图片/视频类型(local_type;localdb_query.MSG_TYPE_NAMES 同源锚)。
_TYPE_IMAGE = 3
_TYPE_VIDEO = 43


def media_extract_key(packed_info_data: Any) -> str | None:
    """消息行 ``packed_info_data``(protobuf BLOB)→ 32-hex 媒体 key。

    走读两级 length-delimited 字段(payload 及其嵌套 payload),任一恰好
    32 字符纯 hex 的 ASCII 载荷即认定为 key;解析不出 = None 如实(不猜)。
    """
    if not isinstance(packed_info_data, (bytes, bytearray, memoryview)):
        return None
    blob = bytes(packed_info_data)

    def _hex32(candidate: bytes) -> str | None:
        if len(candidate) != 32:
            return None
        try:
            text = candidate.decode("ascii")
        except UnicodeDecodeError:
            return None
        return text.lower() if all(ch in _HEX32 for ch in text) else None

    for _f, _l, payload in _proto_length_delimited(blob):
        found = _hex32(payload)
        if found:
            return found
        for _f2, _l2, nested in _proto_length_delimited(payload):
            found = _hex32(nested)
            if found:
                return found
    return None


def _month_of(ts: int) -> str:
    """时间戳 → ``YYYY-MM``(媒体目录的月份段;本地时)。"""
    return time.strftime("%Y-%m", time.localtime(ts))


def _first_existing(patterns: list[str]) -> Path | None:
    """glob 模式族 → 首个在场文件(保序确定性:目录序升序)。"""
    import glob as _glob

    for pattern in patterns:
        matches = sorted(_glob.glob(pattern))
        for match in matches:
            path = Path(match)
            if path.is_file():
                return path
    return None


def image_files_for(media_root: Path, key: str, ts: int) -> dict[str, str | None]:
    """图片 key → ``{thumb, full}``(.dat 路径;缩略图与正图独立判在场)。

    目录段:消息月份优先,落空回落全月份 glob 兜底(dir1 推导关系未实证,
    PRD 明示 glob 合法)。两档都缺 = 双 None(词面「文件缺失」如实)。
    """
    month = _month_of(ts)
    for months in ([month], ["*"]):
        thumb = _first_existing(
            [str(media_root / "attach" / dir1 / m / "Img" / f"{key}_t.dat")
             for dir1 in ["*"] for m in months]
        )
        full = _first_existing(
            [str(media_root / "attach" / dir1 / m / "Img" / f"{key}.dat")
             for dir1 in ["*"] for m in months]
        )
        if thumb is not None or full is not None:
            return {"thumb": str(thumb) if thumb else None,
                    "full": str(full) if full else None}
    return {"thumb": None, "full": None}


def video_files_for(media_root: Path, key: str, ts: int) -> dict[str, str | None]:
    """视频 key → ``{video, video_thumb}``(mp4/_thumb.jpg 明文直读零解密)。"""
    month = _month_of(ts)
    for months in ([month], ["*"]):
        video = _first_existing(
            [str(media_root / "video" / m / f"{key}.mp4") for m in months]
        )
        thumb = _first_existing(
            [str(media_root / "video" / m / f"{key}_thumb.jpg") for m in months]
        )
        if video is not None or thumb is not None:
            return {"video": str(video) if video else None,
                    "video_thumb": str(thumb) if thumb else None}
    return {"video": None, "video_thumb": None}


def scan_chat_media(
    copy_dir: Path,
    chat_id: str,
    since_days: int,
    *,
    media_root: Path,
    now: float | None = None,
) -> dict[str, object]:
    """R2 寻径本体(纯只读):会话窗口内媒体消息 → 媒体清单(不解密)。

    复用 localdb_query 的表自适应与发送者反解;按 local_type 分流
    (3=图/43=视频/其余只报形状)。产物每条 = ``{message_ref, type, key,
    files, status}``,status 词面全人话(R2 判例)。

    Returns:
        ``{"media": {chat_id, since_days, items[], stats{}, provider{}}}``。
    """
    con = None
    for rel in ("message/message_0.db", "message/biz_message_0.db"):
        con = _open_copy(copy_dir, rel)
        if con is not None:
            break
    if con is None:
        raise BridgeError(
            DECRYPT_FAILED,
            "message 域解密副本不可用(媒体寻径前置;副本缺失或损坏)",
            fix_hint="重跑 localdb media scan 触发副本重建;持续失败先核密钥与 sqlcipher",
        )
    since_ts = int(time.time() if now is None else now) - since_days * 86400
    items: list[dict[str, object]] = []
    stats = {"messages": 0, "image": 0, "video": 0, "other": 0, "image_file_missing": 0}
    try:
        tables = find_message_tables(con)
        id_to_name: dict[int, str] = {}
        if any(colmap.get("sender_id") for _table, colmap in tables):
            id_to_name = name2id_maps(con)[0]
        for table, colmap in tables:
            columns = _columns(con, table)
            packed_col = _pick(columns, ("packed_info_data",))
            if packed_col is None:
                continue  # 无 packed 列的表无法取媒体 key,如实跳过
            select_cols = [colmap["time"], colmap["type"], packed_col]
            params: tuple[object, ...]
            if colmap.get("sender_id"):
                select_cols.append(colmap["sender_id"])
            if colmap["talker"]:
                sql = (
                    f'SELECT {", ".join(chr(34) + c + chr(34) for c in select_cols)} '
                    f'FROM "{table}" WHERE "{colmap["talker"]}" = ? '
                    f'AND "{colmap["time"]}" >= ?'
                )
                params = (chat_id, since_ts)
            elif colmap.get("chat") == chat_id:
                sql = (
                    f'SELECT {", ".join(chr(34) + c + chr(34) for c in select_cols)} '
                    f'FROM "{table}" WHERE "{colmap["time"]}" >= ?'
                )
                params = (since_ts,)
            else:
                continue
            try:
                rows = con.execute(sql, params).fetchall()
            except Exception:  # noqa: BLE001 - 单表漂移不拖垮整轮(红线 7 降级)
                continue
            for row in rows:
                ts_raw, type_raw, packed = row[0], row[1], row[2]
                sender_id = row[3] if len(row) > 3 else None
                try:
                    local_type = int(type_raw or 0)
                except (TypeError, ValueError):
                    local_type = 0
                try:
                    ts = int(ts_raw)
                except (TypeError, ValueError):
                    ts = 0
                stats["messages"] = int(stats["messages"]) + 1
                sender = _sender_name(sender_id, id_to_name, chat_id)
                message_ref: dict[str, object] = {
                    "ts": ts,
                    "sender": sender,
                    "local_type": local_type,
                }
                base: dict[str, object] = {
                    "message_ref": message_ref,
                    "type": MSG_TYPE_NAMES.get(local_type, f"type_{local_type}"),
                }
                if local_type == _TYPE_IMAGE:
                    stats["image"] = int(stats["image"]) + 1
                    key = media_extract_key(packed)
                    base["key"] = key
                    if not key:
                        # key 解析不出:形状如实(packed 列在场但无 32-hex 载荷)
                        base["files"] = {"thumb": None, "full": None}
                        base["status"] = STATUS_FILE_MISSING
                        stats["image_file_missing"] = (
                            int(stats["image_file_missing"]) + 1
                        )
                        items.append(base)
                        continue
                    files = image_files_for(media_root, key, ts)
                    base["files"] = files
                    if not files["thumb"] and not files["full"]:
                        base["status"] = STATUS_FILE_MISSING
                        stats["image_file_missing"] = (
                            int(stats["image_file_missing"]) + 1
                        )
                    else:
                        base["status"] = STATUS_PENDING_DECRYPT
                    items.append(base)
                elif local_type == _TYPE_VIDEO:
                    stats["video"] = int(stats["video"]) + 1
                    key = media_extract_key(packed)
                    base["key"] = key
                    files: dict[str, str | None]
                    if key:
                        files = video_files_for(media_root, key, ts)
                    else:
                        files = {"video": None, "video_thumb": None}
                    base["files"] = files
                    if files["video"] or files["video_thumb"]:
                        base["status"] = STATUS_PLAINTEXT_VIDEO
                    else:
                        base["status"] = STATUS_FILE_MISSING
                    items.append(base)
                else:
                    stats["other"] = int(stats["other"]) + 1
                    base["key"] = None
                    base["files"] = {}
                    base["status"] = None  # 只报形状:非媒体主干类型
                    items.append(base)
    finally:
        con.close()
    items.sort(key=lambda item: int(item["message_ref"]["ts"]), reverse=True)  # type: ignore[index,union-attr]
    return {
        "media": {
            "chat_id": chat_id,
            "since_days": since_days,
            "items": items,
            "stats": stats,
        }
    }


# =====================================================================
# 编排(命令壳在 cli.py 接线批:media status/decrypt/scan)
# =====================================================================


def media_scan_history(
    config: Any,
    db_storage: Path,
    keys: dict[str, str],
    chat_id: str,
    since_days: int,
    *,
    decrypt: bool = False,
    data_root: Path | None = None,
    now: float | None = None,
    provider_runner: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, object]:
    """``localdb media scan`` 全链编排(寻径;``--decrypt`` = 逐条解密回填)。

    与 query_history 同构:E2 副本(域固定 ``["message"]``)→ R2 寻径 →
    (``--decrypt``)逐条 decrypt_dat 回填 cached_path(缩略图优先)。未配置
    件 + ``--decrypt`` = exit 23 法定文案(AC1);逐条解密失败 = 词面
    「解密失败」+ 计数,不炸整轮(宁缺毋假)。
    """
    provider = media_provider_path(config)
    if decrypt and not provider:
        raise BridgeError(
            MEDIA_UNAVAILABLE,
            MEDIA_DECRYPT_UNCONFIGURED_MESSAGE,
            fix_hint=(
                "wechat-bridge localdb media-decrypt set <媒体解密件可执行文件路径> "
                "配置后重试(协议文档 docs/wechat-mediadecrypt.md)"
            ),
        )
    copy_info = ensure_decrypted_copies(
        db_storage,
        keys,
        domains=["message"],
        ttl_hours=getattr(config, "copy_ttl_hours", 24),
        capacity_mb=getattr(config, "copy_capacity_mb", 512),
        data_root=data_root,
        now=now,
    )
    payload = scan_chat_media(
        Path(str(copy_info["dir"])),
        chat_id,
        since_days,
        media_root=db_storage.parent / "msg",
        now=now,
    )
    inner = payload["media"]
    assert isinstance(inner, dict)
    items = inner["items"]
    assert isinstance(items, list)
    inner["provider"] = {"configured": bool(provider), "path": provider or None}
    if decrypt:
        decrypted = 0
        failed = 0
        for item in items:
            assert isinstance(item, dict)
            if item.get("type") != "image" or item.get("status") != STATUS_PENDING_DECRYPT:
                continue
            files = item.get("files")
            assert isinstance(files, dict)
            source = files.get("thumb") or files.get("full")
            if not source:
                continue
            try:
                outcome = decrypt_dat_file(
                    source, config, data_root=data_root, provider_runner=provider_runner
                )
            except BridgeError:
                item["status"] = STATUS_DECRYPT_FAILED
                failed += 1
                continue
            item["cached_path"] = outcome.get("cached_path")
            item["status"] = (
                STATUS_WXGF if outcome.get("is_wxgf") else STATUS_DECRYPTED
            )
            decrypted += 1
        inner["stats"]["decrypted"] = decrypted
        inner["stats"]["decrypt_failed"] = failed
    return payload


def media_status(
    config: Any = None, *, data_root: Path | None = None
) -> dict[str, object]:
    """``localdb media status``:件配置态 + 缓存统计(状态查询恒不判错)。"""
    import os as _os

    configured = media_provider_path(config)
    if not configured:
        provider = {
            "path": None,
            "state": "unconfigured",
            "message": "未配置媒体解密件;localdb media-decrypt set <path> 配置(协议:docs/wechat-mediadecrypt.md)",
        }
    else:
        path = Path(configured).expanduser()
        if not path.is_file():
            provider = {
                "path": configured,
                "state": "missing_file",
                "message": f"已配置但文件不存在: {path}",
            }
        elif not _os.access(path, _os.X_OK):
            provider = {
                "path": configured,
                "state": "not_executable",
                "message": f"已配置但文件缺可执行位: {path}",
            }
        else:
            provider = {
                "path": configured,
                "state": "configured",
                "message": f"媒体解密件已配置: {path}",
            }
    directory = cache_dir(data_root)
    capacity_mb = media_capacity_mb(config)
    if directory.is_dir():
        files = 0
        total_bytes = 0
        for item in directory.iterdir():
            if not item.is_file() or item.name.startswith("."):
                continue
            try:
                files += 1
                total_bytes += item.stat().st_size
            except OSError:
                continue
        cache = {
            "dir": str(directory),
            "files": files,
            "total_bytes": total_bytes,
            "capacity_mb": capacity_mb,
        }
    else:
        cache = {
            "dir": str(directory),
            "files": 0,
            "total_bytes": 0,
            "capacity_mb": capacity_mb,
        }
    return {"media": {"provider": provider, "cache": cache}}
