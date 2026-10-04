"""10-04-windows-build 冒烟(dry 逻辑面):workflow 自身 run 块的本地演练。

零外网、零 CI:从 desktop-release.yml 提取**原文 run 块**,在临时目录的
fixture 产物树上按场景执行,断言行为与产物名。覆盖:

  D1 版本解析四场景(tag / 分支无参回退 conf / 分支带参 / 预发布 tag)
  D2 Windows 产物 ASCII 改名(msi-updater/世事_*_x64_en-US.msi → myia_<v>_x64.msi)
  D3 macOS 产物 ASCII 改名(世事.app.tar.gz → myia.app.tar.gz 等)
  D4 latest.json 生成两分支(win 产物在 → 并入;缺席 → 仅 mac 条目)
  D5 build-sidecar.sh 守卫 dry(darwin 主机拒 windows 目标;SKIP 快路径)
  D6 uv.lock/uv export 静态面(ocrmac marker + tsinghua URL 体系)

跑法(仓库根):
    uv run --no-sync python .trellis/tasks/10-04-windows-build/evidence/win_build_dry_logic.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
WF = ROOT / ".github" / "workflows" / "desktop-release.yml"

fails = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global fails
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fails += 1


def run_blocks() -> dict[str, str]:
    """从 workflow 提取原文 run 块(以步骤名定位)."""
    doc = yaml.safe_load(WF.read_text(encoding="utf-8"))
    jobs = doc["jobs"]
    blocks: dict[str, str] = {}
    for step in jobs["macos-dmg"]["steps"]:
        if "产物改 ASCII 名" in str(step.get("name", "")):
            blocks["ascii-mac"] = step["run"]
    for step in jobs["windows-msi"]["steps"]:
        if "产物改 ASCII 名" in str(step.get("name", "")):
            blocks["ascii-win"] = step["run"]
    for step in jobs["release-finalize"]["steps"]:
        name = str(step.get("name", ""))
        if "解析版本" in name:  # 归聚版含 TAG 推导,最全
            blocks["version"] = step["run"]
        if "生成 latest.json" in name:
            blocks["latest"] = step["run"]
    return blocks


def bash(script: str, cwd: Path, env_extra: dict[str, str]) -> tuple[int, str]:
    env = {**os.environ, **env_extra, "GITHUB_ENV": str(cwd / "github_env")}
    proc = subprocess.run(
        ["bash", "-c", script], cwd=cwd, env=env, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return proc.returncode, proc.stdout + proc.stderr


def read_github_env(cwd: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    path = cwd / "github_env"
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                out[key] = value
    return out


def scenario_version(blocks: dict[str, str], workdir: Path) -> None:
    """D1:四场景演练 release-finalize 版本解析块(最全:含 TAG)."""
    conf = workdir / "desktop" / "src-tauri"
    conf.mkdir(parents=True)
    (conf / "tauri.conf.json").write_text(json.dumps({"version": "0.0.1"}), encoding="utf-8")
    cases = [
        # (label, INPUT_VERSION, REF_NAME, GITHUB_REF, expected_version, expected_tag)
        ("tag 推送:v1.2.3 → 1.2.3", "", "v1.2.3", "refs/tags/v1.2.3", "1.2.3", "v1.2.3"),
        ("分支 dispatch 无参:分支名非 semver → 回退 conf 0.0.1",
         "", "10-04-windows-build", "refs/heads/10-04-windows-build", "0.0.1", "v0.0.1"),
        ("分支 dispatch 带参 0.0.2", "0.0.2", "10-04-windows-build",
         "refs/heads/10-04-windows-build", "0.0.2", "v0.0.2"),
        ("预发布 tag:v1.2.3-rc.1 → 1.2.3-rc.1", "", "v1.2.3-rc.1",
         "refs/tags/v1.2.3-rc.1", "1.2.3-rc.1", "v1.2.3-rc.1"),
    ]
    for label, input_v, ref_name, github_ref, want_v, want_tag in cases:
        env_dir = workdir / "github_env"
        env_dir.write_text("", encoding="utf-8")
        code, output = bash(
            blocks["version"], workdir,
            {"INPUT_VERSION": input_v, "REF_NAME": ref_name,
             "GITHUB_REF": github_ref, "GITHUB_REF_NAME": ref_name.split("/")[-1]},
        )
        got = read_github_env(workdir)
        ok = code == 0 and got.get("MYIA_VERSION") == want_v and got.get("MYIA_TAG") == want_tag
        check(f"D1 {label}", ok,
              f"version={got.get('MYIA_VERSION')} tag={got.get('MYIA_TAG')} rc={code}")
        if "回退" in label:
            check("D1 回退路径发 ::warn:: 提示", "::warn::" in output, output.strip()[:80])


def scenario_ascii(blocks: dict[str, str], workdir: Path) -> None:
    """D2/D3:fake bundle 树上演练两平台的 ASCII 改名块."""
    win_root = workdir / "win"
    updater = win_root / "desktop/src-tauri/target/release/bundle/msi-updater"
    updater.mkdir(parents=True)
    (updater / "世事_0.0.2_x64_en-US.msi").write_bytes(b"MSI-PAYLOAD")
    (updater / "世事_0.0.2_x64_en-US.msi.sig").write_text("WINSIG", encoding="utf-8")
    code, output = bash(blocks["ascii-win"], win_root, {"MYIA_VERSION": "0.0.2"})
    bundle = win_root / "desktop/src-tauri/target/release/bundle"
    msi, sig = bundle / "myia_0.0.2_x64.msi", bundle / "myia_0.0.2_x64.msi.sig"
    check("D2 windows 改名 exit 0", code == 0, output.strip()[:80])
    check("D2 myia_0.0.2_x64.msi 产出(ASCII)", msi.exists() and msi.read_bytes() == b"MSI-PAYLOAD")
    check("D2 myia_0.0.2_x64.msi.sig 产出", sig.exists() and sig.read_text() == "WINSIG")
    check("D2 源文件保留(cp 非 mv,原非 ASCII 名仍在)",
          (updater / "世事_0.0.2_x64_en-US.msi").exists())
    check("D2 ASCII 名可作 release 资产(纯 ASCII)",
          all(ord(c) < 128 for c in msi.name))

    mac_root = workdir / "mac"
    macos = mac_root / "desktop/src-tauri/target/release/bundle/macos"
    dmg = mac_root / "desktop/src-tauri/target/release/bundle/dmg"
    macos.mkdir(parents=True)
    dmg.mkdir(parents=True)
    (macos / "世事.app.tar.gz").write_bytes(b"TAR")
    (macos / "世事.app.tar.gz.sig").write_text("MACSIG", encoding="utf-8")
    (dmg / "世事_0.0.2_aarch64.dmg").write_bytes(b"DMG")
    code, output = bash(blocks["ascii-mac"], mac_root, {"MYIA_VERSION": "0.0.2"})
    check("D3 mac 改名 exit 0", code == 0, output.strip()[:80])
    check("D3 myia.app.tar.gz{,.sig} 产出",
          (macos / "myia.app.tar.gz").exists() and (macos / "myia.app.tar.gz.sig").exists())
    check("D3 myia_0.0.2_aarch64.dmg 产出", (dmg / "myia_0.0.2_aarch64.dmg").exists())


def scenario_latest(blocks: dict[str, str], workdir: Path) -> None:
    """D4:latest.json 生成块两分支(win 在 / 缺席)."""
    def run_case(subdir: str, with_win: bool) -> dict:
        case = workdir / subdir
        mac = case / "dist/mac-updater"
        mac.mkdir(parents=True)
        (mac / "myia.app.tar.gz.sig").write_text("MACSIG-XYZ", encoding="utf-8")
        if with_win:
            win = case / "dist/win-msi"
            win.mkdir(parents=True)
            (win / "myia_0.0.2_x64.msi").write_bytes(b"MSI")
            (win / "myia_0.0.2_x64.msi.sig").write_text("WINSIG-XYZ", encoding="utf-8")
        code, output = bash(
            blocks["latest"], case,
            {"MYIA_VERSION": "0.0.2", "MYIA_TAG": "v0.0.2", "REPO": "xinzhuzi/myia"},
        )
        data = json.loads((case / "latest.json").read_text(encoding="utf-8")) if code == 0 else {}
        return {"code": code, "output": output, "data": data}

    both = run_case("both", True)
    check("D4 win 在:生成 exit 0", both["code"] == 0, both["output"].strip()[:80])
    platforms = both["data"].get("platforms", {})
    check("D4 darwin-aarch64 恒在(signature=.sig 内容)",
          platforms.get("darwin-aarch64", {}).get("signature") == "MACSIG-XYZ")
    check("D4 darwin URL 指 ASCII 资产",
          platforms.get("darwin-aarch64", {}).get("url")
          == "https://github.com/xinzhuzi/myia/releases/download/v0.0.2/myia.app.tar.gz")
    check("D4 windows-x86_64 并入(signature=.sig 内容)",
          platforms.get("windows-x86_64", {}).get("signature") == "WINSIG-XYZ")
    check("D4 windows URL 指 ASCII 资产(myia_0.0.2_x64.msi)",
          platforms.get("windows-x86_64", {}).get("url")
          == "https://github.com/xinzhuzi/myia/releases/download/v0.0.2/myia_0.0.2_x64.msi")
    check("D4 notes/version 形态", both["data"].get("version") == "0.0.2"
          and both["data"].get("notes") == "世事 0.0.2")
    check("D4 pub_date 为 ISO8601", "T" in str(both["data"].get("pub_date", "")))

    mac_only = run_case("maconly", False)
    platforms = mac_only["data"].get("platforms", {})
    check("D4 win 缺席:生成 exit 0(不炸)", mac_only["code"] == 0, mac_only["output"].strip()[:80])
    check("D4 win 缺席:仅 darwin 条目,windows 键不出现",
          "windows-x86_64" not in platforms and "darwin-aarch64" in platforms)
    check("D4 win 缺席:发 ::warn:: 提示", "::warn::" in mac_only["output"])


def scenario_sidecar_guard(workdir: Path) -> None:
    """D5:build-sidecar.sh 守卫 dry(零 venv/零网络即退出)."""
    proc = subprocess.run(
        ["bash", "desktop/build-sidecar.sh", "x86_64-pc-windows-msvc"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
        encoding="utf-8", errors="replace",
    )
    check("D5 darwin 主机 + windows 目标 → 拒绝(exit 1)", proc.returncode == 1,
          f"rc={proc.returncode}")
    check("D5 拒绝理由 = PyInstaller 不支持交叉编译", "交叉编译" in proc.stderr,
          proc.stderr.strip().splitlines()[0][:80] if proc.stderr else "")
    proc = subprocess.run(
        ["bash", "desktop/build-sidecar.sh", "aarch64-apple-darwin"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
        env={**os.environ, "MYIA_SIDECAR_SKIP": "1"},
        encoding="utf-8", errors="replace",
    )
    check("D5 MYIA_SIDECAR_SKIP=1 + 产物在 → 零工作快路径(exit 0)",
          proc.returncode == 0 and "跳过" in proc.stdout, proc.stdout.strip()[:80])


def scenario_lock() -> None:
    """D6:uv.lock/uv export 静态面(ocrmac marker + tsinghua URL 体系)."""
    lock = (ROOT / "uv.lock").read_text(encoding="utf-8")
    check("D6 vision extra 的 ocrmac 条目带 darwin marker",
          '{ name = "ocrmac", marker = "sys_platform == \'darwin\'" }' in lock)
    proc = subprocess.run(
        ["uv", "export", "--frozen", "--no-dev", "--extra", "vision"],
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    line = [ln for ln in proc.stdout.splitlines() if ln.strip().startswith("ocrmac==")]
    check("D6 uv export(锁内冻结集)ocrmac 行带 marker",
          proc.returncode == 0 and any("sys_platform == 'darwin'" in ln for ln in line),
          line[0] if line else "无 ocrmac 行")
    ocrmac_urls = [
        ln.strip() for ln in lock.splitlines()
        if "url =" in ln and "ocrmac" in ln
    ]
    check("D6 ocrmac URL 体系仍 tsinghua 镜像",
          ocrmac_urls and all("pypi.tuna.tsinghua.edu.cn" in u for u in ocrmac_urls),
          f"{len(ocrmac_urls)} 条 URL 全 tsinghua" if ocrmac_urls else "无 url 行")


if __name__ == "__main__":
    print(f"win_build_dry_logic @ {ROOT}(workflow 原文 run 块本地演练,零外网)\n")
    blocks = run_blocks()
    check("run 块提取齐备(version/ascii-win/ascii-mac/latest)",
          set(blocks) == {"version", "ascii-win", "ascii-mac", "latest"}, str(sorted(blocks)))
    with tempfile.TemporaryDirectory(prefix="myia-win-dry-") as tmp:
        workdir = Path(tmp)
        print("== D1 版本解析四场景 ==")
        scenario_version(blocks, workdir)
        print("== D2/D3 产物 ASCII 改名(win/mac)==")
        scenario_ascii(blocks, workdir)
        print("== D4 latest.json 生成两分支 ==")
        scenario_latest(blocks, workdir)
    print("== D5 build-sidecar.sh 守卫 dry ==")
    scenario_sidecar_guard(Path("/tmp"))
    print("== D6 uv.lock / uv export 静态面 ==")
    scenario_lock()
    print(f"\n== 结果:{'ALL PASS' if fails == 0 else f'{fails} 项 FAIL'} ==")
    sys.exit(1 if fails else 0)
