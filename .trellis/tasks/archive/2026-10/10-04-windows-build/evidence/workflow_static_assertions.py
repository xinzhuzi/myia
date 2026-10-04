"""10-04-windows-build 冒烟(静态面):desktop-release.yml yaml parse + 矩阵静态断言。

断言口径 = prd F3/D1-D10 + implement 阶段 3 设计:
  W1 yaml 可解析 + 三 job 清单
  W2 windows-msi:正式目标(无 continue-on-error)、timeout 60、windows-latest、
     版本底座(Python 3.11/Node 22/Rust stable)、产物清单诊断步、ASCII 改名、
     win-msi artifact(if-no-files-found: error)、job 内零 Release 上传步
  W3 macos-dmg:macos-14、--bundles app,dmg、latest.json 生成步不在本 job、
     mac-updater artifact、softprops 步 tag 门
  W4 release-finalize:ubuntu-latest、needs [macos-dmg, windows-msi]、
     if always() && mac result 门、latest.json 单写者(win 条件并入)、
     latest-json artifact 无条件、两 softprops 步 tag 门(win 步另加 result 门)
  W5 workflow_dispatch.version 入参存在且 required: false

跑法(仓库根):python3 .trellis/tasks/10-04-windows-build/evidence/workflow_static_assertions.py
"""

from __future__ import annotations

import sys
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


def step_names(job: dict) -> list[str]:
    return [s.get("name") or s.get("uses", "?") for s in job["steps"]]


def steps_with(job: dict, needle: str) -> list[dict]:
    return [s for s in job["steps"] if needle in str(s)]


def main() -> None:
    print(f"workflow_static_assertions @ {WF}")
    doc = yaml.safe_load(WF.read_text(encoding="utf-8"))

    print("== W1 yaml 解析与 job 清单 ==")
    check("yaml.safe_load 解析成功", isinstance(doc, dict))
    jobs = doc["jobs"]
    check("job 清单 = [macos-dmg, release-finalize, windows-msi]",
          sorted(jobs) == ["macos-dmg", "release-finalize", "windows-msi"], str(sorted(jobs)))
    check("触发含 push.tags v* 与 workflow_dispatch",
          doc[True]["push"]["tags"] == ["v*"] and "workflow_dispatch" in doc[True])
    check("permissions.contents = write", doc["permissions"]["contents"] == "write")

    print("== W5 dispatch 版本入参 ==")
    inputs = doc[True]["workflow_dispatch"]["inputs"]
    check("inputs.version 存在且 required=false(分支 dispatch 合法)",
          "version" in inputs and inputs["version"].get("required") is False)

    win, mac, fin = jobs["windows-msi"], jobs["macos-dmg"], jobs["release-finalize"]

    print("== W2 windows-msi(正式目标)==")
    check("无 continue-on-error(转正式)", "continue-on-error" not in win)
    check("timeout-minutes: 60", win.get("timeout-minutes") == 60)
    check("runs-on: windows-latest", win["runs-on"] == "windows-latest")
    uses = " ".join(str(s.get("uses", "")) for s in win["steps"])
    check("版本底座对齐 mac(setup-uv py3.11 / node 22 / rust stable)",
          "setup-uv@v5" in uses and "setup-node@v4" in uses and "rust-toolchain@stable" in uses)
    uv_step = [s for s in win["steps"] if str(s.get("uses", "")).startswith("astral-sh/setup-uv")][0]
    check("Python 3.11(D9)", uv_step["with"]["python-version"] == "3.11")
    node_step = [s for s in win["steps"] if str(s.get("uses", "")).startswith("actions/setup-node")][0]
    check("Node 22(D9)", node_step["with"]["node-version"] == "22")
    check("sidecar 目标 = x86_64-pc-windows-msvc",
          any("x86_64-pc-windows-msvc" in str(s.get("run", "")) for s in win["steps"]))
    names = step_names(win)
    check("产物清单(诊断)步在", any("产物清单" in n for n in names))
    ascii_step = steps_with(win, "msi-updater")[0]
    check("ASCII 改名步:msi-updater/*_x64*.msi → myia_${MYIA_VERSION}_x64.msi(+.sig)",
          "myia_${MYIA_VERSION}_x64.msi" in ascii_step["run"]
          and "msi-updater/*_x64*.msi.sig" in ascii_step["run"])
    up = steps_with(win, "actions/upload-artifact")[0]
    check("win-msi artifact 上传(if-no-files-found: error)",
          up["with"]["name"] == "win-msi" and up["with"]["if-no-files-found"] == "error")
    check("windows job 内零 softprops Release 上传步(挂载归 release-finalize)",
          not steps_with(win, "softprops"))
    check("版本解析步:dispatch 入参 → ref → tauri.conf.json 兜底",
          any("tauri.conf.json" in str(s.get("run", "")) for s in win["steps"] if "解析版本" in str(s.get("name", ""))))

    print("== W3 macos-dmg(主线不回归形态)==")
    check("runs-on: macos-14(arm64)", mac["runs-on"] == "macos-14")
    build = [s for s in mac["steps"] if "tauri build" in str(s.get("run", ""))][0]
    check("--bundles app,dmg(updater 产物链)", "--bundles app,dmg" in build["run"])
    check("latest.json 生成步已移出 mac job(单写者;run 面零 latest.json 写入)",
          not any("latest.json" in str(s.get("run", "")) for s in mac["steps"]))
    mac_up = steps_with(mac, "actions/upload-artifact")[0]
    check("mac-updater artifact(myia.app.tar.gz.sig,if-no-files-found: error)",
          mac_up["with"]["name"] == "mac-updater"
          and "myia.app.tar.gz.sig" in str(mac_up["with"]["path"])
          and mac_up["with"]["if-no-files-found"] == "error")
    mac_softprops = steps_with(mac, "softprops")
    check("mac softprops 步挂 tag 门", all(
        str(s.get("if", "")).strip() == "startsWith(github.ref, 'refs/tags/')" for s in mac_softprops))
    mac_ascii = [s for s in mac["steps"] if "产物改 ASCII 名" in str(s.get("name", ""))][0]
    check("mac ASCII 改名:myia.app.tar.gz{,.sig} + myia_${MYIA_VERSION}_aarch64.dmg",
          "myia.app.tar.gz" in mac_ascii["run"] and "myia_${MYIA_VERSION}_aarch64.dmg" in mac_ascii["run"])

    print("== W4 release-finalize(归聚单写者)==")
    check("runs-on: ubuntu-latest(jq 预装,R2-D6a)", fin["runs-on"] == "ubuntu-latest")
    check("needs = [macos-dmg, windows-msi]", fin["needs"] == ["macos-dmg", "windows-msi"])
    check("if = always() && needs.macos-dmg.result == 'success'(mac 绿即执行,R2-D6b)",
          str(fin["if"]).strip() == "always() && needs.macos-dmg.result == 'success'")
    gen = [s for s in fin["steps"] if "生成 latest.json" in str(s.get("name", ""))][0]
    run = gen["run"]
    check("mac 条目恒在(darwin-aarch64 无条件写入)", '"darwin-aarch64"' in run)
    check("windows 条目按产物存在与否并入(compgen 分支)", "compgen -G 'dist/win-msi/myia_*_x64.msi'" in run)
    check("windows 条目键 = windows-x86_64,URL 指 ASCII 资产名",
          '"windows-x86_64"' in run and "/myia_" + "\" + $v + \"_x64.msi" in run)
    fin_names = step_names(fin)
    latest_up = [s for s in fin["steps"] if str(s.get("uses", "")).startswith("actions/upload-artifact")][0]
    check("latest-json artifact 无条件上传(dispatch 循环可复核)",
          latest_up["with"]["name"] == "latest-json" and "if" not in latest_up)
    win_dl = [s for s in fin["steps"] if str(s.get("uses", "")).startswith("actions/download-artifact") and s["with"]["name"] == "win-msi"]
    check("win-msi 下载步带 result 门(缺席=仅 mac 条目)",
          len(win_dl) == 1 and str(win_dl[0].get("if", "")).strip() == "needs.windows-msi.result == 'success'")
    fin_softprops = steps_with(fin, "softprops")
    check("归聚 job 两 softprops 步均挂 tag 门", len(fin_softprops) == 2 and all(
        str(s.get("if", "")).startswith("startsWith(github.ref, 'refs/tags/')") for s in fin_softprops))
    win_attach = [s for s in fin_softprops if "myia_*_x64.msi" in str(s["with"].get("files", ""))][0]
    check("windows 挂载步另加 result 门", "needs.windows-msi.result == 'success'" in str(win_attach["if"]))
    check("job 本体不整体 tag 门(only steps gated)", "if" not in fin or str(fin["if"]).startswith("always()"))

    print(f"\n== 结果:{'ALL PASS' if fails == 0 else f'{fails} 项 FAIL'} ==")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
