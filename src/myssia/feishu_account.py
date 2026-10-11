"""飞书「本身账号」线(user_access_token)——配置组账号卡的领域层。

裁定语义(10-11-platform-account-config):配置组管「本身账号」= 用户对
自建应用的 OAuth 授权态(user_access_token/refresh_token);推送机器人
(App 凭据/tenant_access_token)归设置→推送,两条线不混。App ID/Secret
**复用**推送区同一应用凭据(env→钥匙链回退,``push.base.resolve_channel_
credential`` 惯例),本模块只管「用户授权」那一半:authorize URL 构造 /
code 换 token / 刷新闭环 / 账号枚举 / 删除。

存储(目录即账号,镜像 telegram/web_line.py 配置档惯例):
    <数据根>/feishu-accounts/<账号键>/myssia-login.json   # label+时间(零凭据面)
    keychain myia/<账号键>/user_access_token              # ~2h 有效
    keychain myia/<账号键>/refresh_token                  # ~30 天,无感续期

钥匙链两级命名:scope=账号键(``feishu-<标识>``,恰满足
:mod:`myssia.secrets` 名字正则的品类 id 段),叶名=token 项名。

OAuth 事实(开放平台文档):授权码换
``POST /open-apis/authen/v1/oidc/access_token``;刷新
``POST /open-apis/authen/v1/oidc/refresh_access_token``;应答
``{code:0, data:{access_token, refresh_token, expires_in,...}}``,
``data.access_token`` 即 user_access_token。
"""

from __future__ import annotations

import json
import re
import shutil
import time
from pathlib import Path
from typing import Any

import httpx

from myssia.secrets import delete_secret, get_secret, set_secret

__all__ = [
    "ACCOUNT_KEY_RE",
    "ACCOUNTS_ROOT_DIR",
    "LOGIN_MARKER_NAME",
    "FeishuAccountError",
    "account_dir",
    "accounts_root",
    "authorize_url",
    "delete_account",
    "exchange_code",
    "list_accounts",
    "probe_account",
    "read_login_marker",
    "refresh_tokens",
    "validate_account_key",
    "write_login_marker",
]

#: 账号键全称律(镜像 telegram/web_line.ACCOUNT_KEY_RE 形态,前缀换平台)。
ACCOUNT_KEY_RE = re.compile(r"^feishu-[a-z0-9][a-z0-9_-]{0,62}$")
#: 账号档根目录名(<数据根> 下,镜像 PROFILE_ROOT_DIR 惯例)。
ACCOUNTS_ROOT_DIR = "feishu-accounts"
#: 登录标记文件名(零凭据:label + 授权/刷新时间戳)。
LOGIN_MARKER_NAME = "myssia-login.json"
#: 飞书开放平台 OAuth 端点( accounts 域名发授权页,open 域名换/刷 token)。
AUTHORIZE_ENDPOINT = "https://accounts.feishu.cn/open-apis/authen/v1/authorize"
TOKEN_API_BASE = "https://open.feishu.cn/open-apis/authen/v1/oidc"

_TOKEN_ITEM = "user_access_token"
_REFRESH_ITEM = "refresh_token"


class FeishuAccountError(RuntimeError):
    """账号线结构化错误(code + 中文原因,错误处理规范同款)。"""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def validate_account_key(key: str) -> str:
    """账号键校验(不过 = ``account_key_invalid``):守目录穿越与钥匙链 scope。"""
    if not ACCOUNT_KEY_RE.match(key):
        raise FeishuAccountError(
            "account_key_invalid",
            f"账号键不合规:{key!r}(全称律 feishu-<标识>,小写字母/数字/-/_)",
        )
    return key


def accounts_root(data_root: str | Path) -> Path:
    return Path(data_root) / ACCOUNTS_ROOT_DIR


def account_dir(data_root: str | Path, key: str) -> Path:
    """账号档目录(键先过规约,守目录穿越 —— web_line.profile_dir 同款)。"""
    validate_account_key(key)
    return accounts_root(data_root) / key


def _marker_path(directory: str | Path) -> Path:
    return Path(directory) / LOGIN_MARKER_NAME


def read_login_marker(directory: str | Path) -> dict[str, Any] | None:
    """读登录标记(缺/坏 = None;宽容不抛 —— 标记只是展示面)。"""
    try:
        payload = json.loads(_marker_path(directory).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def write_login_marker(
    directory: str | Path,
    *,
    label: str,
    refresh_ok: bool | None = None,
) -> dict[str, Any]:
    """写登录标记(零凭据:label + 授权/刷新时间;刷新探针复写状态位)。"""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    previous = read_login_marker(directory) or {}
    payload = {
        "label": label or previous.get("label") or "",
        "authorized_at": previous.get("authorized_at") or _now_iso(),
        "refresh_ok": refresh_ok,
        "refreshed_at": _now_iso() if refresh_ok is not None else previous.get("refreshed_at"),
    }
    _marker_path(directory).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return payload


def list_accounts(data_root: str | Path) -> list[dict[str, Any]]:
    """账号枚举(目录名即键,排序稳定;坏标记的目录也入列,标记位留 None)。"""
    root = accounts_root(data_root)
    if not root.is_dir():
        return []
    out: list[dict[str, Any]] = []
    for entry in sorted(root.iterdir(), key=lambda p: p.name):
        if not entry.is_dir() or not ACCOUNT_KEY_RE.match(entry.name):
            continue
        marker = read_login_marker(entry)
        out.append(
            {
                "account": entry.name,
                "label": marker.get("label") if marker else None,
                "authorized_at": marker.get("authorized_at") if marker else None,
                "refresh_ok": marker.get("refresh_ok") if marker else None,
                "refreshed_at": marker.get("refreshed_at") if marker else None,
            }
        )
    return out


def authorize_url(app_id: str, redirect_uri: str, state: str) -> str:
    """OAuth 授权页 URL(纯函数;redirect_uri 必须与应用登记完全一致)。"""
    query = httpx.QueryParams(
        {"app_id": app_id, "redirect_uri": redirect_uri, "state": state}
    )
    return f"{AUTHORIZE_ENDPOINT}?{query}"


async def exchange_code(
    app_id: str,
    app_secret: str,
    code: str,
    redirect_uri: str,
    *,
    transport: httpx.AsyncBaseTransport | None = None,
) -> dict[str, Any]:
    """授权码换 token 对(应答非 0 = ``feishu_oauth_exchange_failed``)。"""
    async with httpx.AsyncClient(timeout=30.0, transport=transport) as client:
        response = await client.post(
            f"{TOKEN_API_BASE}/access_token",
            json={
                "grant_type": "authorization_code",
                "app_id": app_id,
                "app_secret": app_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
        )
    return _parse_token_response(response, "feishu_oauth_exchange_failed")


async def refresh_tokens(
    app_id: str,
    app_secret: str,
    refresh_token: str,
    *,
    transport: httpx.AsyncBaseTransport | None = None,
) -> dict[str, Any]:
    """刷新 token 对(应答非 0 = ``feishu_refresh_failed``;失效即重授权)。"""
    async with httpx.AsyncClient(timeout=30.0, transport=transport) as client:
        response = await client.post(
            f"{TOKEN_API_BASE}/refresh_access_token",
            json={
                "grant_type": "refresh_token",
                "app_id": app_id,
                "app_secret": app_secret,
                "refresh_token": refresh_token,
            },
        )
    return _parse_token_response(response, "feishu_refresh_failed")


def _parse_token_response(response: httpx.Response, error_code: str) -> dict[str, Any]:
    """统一解析 OIDC 应答:HTTP 非 200 / 业务非 0 / 缺 token 项同族报错。"""
    try:
        payload = response.json()
    except ValueError as exc:
        raise FeishuAccountError(error_code, f"飞书应答非 JSON:HTTP {response.status_code}") from exc
    if response.status_code != 200 or payload.get("code") != 0:
        msg = payload.get("msg") or f"HTTP {response.status_code}"
        raise FeishuAccountError(error_code, f"飞书开放平台拒绝({payload.get('code')}):{msg}")
    data = payload.get("data") or {}
    token = data.get("access_token")
    refresh = data.get("refresh_token")
    if not token or not refresh:
        raise FeishuAccountError(error_code, "飞书应答缺 access_token/refresh_token")
    return {"access_token": token, "refresh_token": refresh}


def _token_secret_names(key: str) -> tuple[str, str]:
    """钥匙链两级名(scope=账号键;键先过规约)。"""
    validate_account_key(key)
    return f"myia/{key}/{_TOKEN_ITEM}", f"myia/{key}/{_REFRESH_ITEM}"


def store_account_tokens(key: str, token: str, refresh: str) -> None:
    """token 对入钥匙链(scope=账号键;值经 myssia.secrets 规范写入)。"""
    token_name, refresh_name = _token_secret_names(key)
    set_secret(token_name, token)
    set_secret(refresh_name, refresh)


async def probe_account(
    data_root: str | Path,
    key: str,
    app_id: str,
    app_secret: str,
    *,
    transport: httpx.AsyncBaseTransport | None = None,
) -> dict[str, Any]:
    """刷新闭环探针:refresh 可成功 = 账号态有效(新 token 回写 = 续期)。

    结论写进 marker.refresh_ok,不抛探针失败(失败是**状态**不是异常);
    只有两类结构化错上抛:键不合规 / refresh_token 缺(从未授权成功)。
    """
    directory = account_dir(data_root, key)
    _, refresh_name = _token_secret_names(key)
    try:
        refresh = get_secret(refresh_name)
    except Exception:
        refresh = ""
    if not refresh:
        write_login_marker(directory, label=_marker_label(directory), refresh_ok=False)
        raise FeishuAccountError(
            "feishu_refresh_token_missing",
            f"账号 {key} 无 refresh_token(从未授权成功或已被清理),请重新添加授权",
        )
    try:
        tokens = await refresh_tokens(app_id, app_secret, refresh, transport=transport)
    except FeishuAccountError:
        write_login_marker(directory, label=_marker_label(directory), refresh_ok=False)
        raise
    store_account_tokens(key, tokens["access_token"], tokens["refresh_token"])
    write_login_marker(directory, label=_marker_label(directory), refresh_ok=True)
    return {"account": key, "refresh_ok": True, "refreshed_at": _now_iso()}


def delete_account(data_root: str | Path, key: str) -> dict[str, Any]:
    """删除账号:钥匙链两项(缺省容忍)+ 账号目录(护栏在协议层)。"""
    directory = account_dir(data_root, key)
    for name in _token_secret_names(key):
        try:
            delete_secret(name)
        except Exception:
            pass  # 未授权成功的账号可能只有目录,凭据缺省不算错
    if directory.is_dir():
        shutil.rmtree(directory)
    return {"deleted": True, "account": key}


def _marker_label(directory: str | Path) -> str:
    marker = read_login_marker(directory)
    return (marker or {}).get("label") or ""


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())
