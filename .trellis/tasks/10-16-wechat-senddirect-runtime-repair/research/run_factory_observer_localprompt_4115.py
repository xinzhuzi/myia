"""Foreground, single-window supervisor; research only, no product integration."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
LLDB = "/Applications/Xcode.app/Contents/Developer/usr/bin/lldb"
SERVER = "/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/A/Resources/debugserver"
WECHAT = "/Applications/WeChat.app/Contents/MacOS/WeChat"
LIBRARY = "/Applications/WeChat.app/Contents/Resources/wechat.dylib"


def status(pid):
    probe = subprocess.run([str(ROOT / "process_status"), str(pid)],
                           capture_output=True, text=True, timeout=0.75)
    if probe.returncode:
        return None
    fields = probe.stdout.rstrip("\n").split("\t", 5)
    return {"pid": int(fields[0]), "flags": int(fields[1]), "state": int(fields[2]),
            "start_sec": int(fields[3]), "start_usec": int(fields[4]), "executable": fields[5]}


def clean_identity(before, after):
    return bool(before and after
                and all(before[k] == after[k] for k in ("pid", "start_sec", "start_usec", "executable"))
                and not after["flags"] & 0x800 and after["state"] not in (4, 5))


def source_hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("factory_observer_4115.py", "run_factory_observer_localprompt_4115.py", "process_status", "factory_snapshot_fixture_4115", "newsendmsg_identity_4115.py", "newsendmsg_factory_snapshot_4115.py", "factory_window_prompt_4115.swift", "factory_window_prompt_4115")}


def preflight_live():
    qualified = json.loads((ROOT / "factory-localprompt-cleanup-qualification.json").read_text())
    if qualified["passed"] is not True or qualified["hashes"] != source_hashes():
        raise RuntimeError("cleanup qualification missing or source changed")
    for name in ("lldb", "debugserver"):
        if subprocess.run(["pgrep", "-x", name], capture_output=True).returncode != 1:
            raise RuntimeError("another debugger exists; refusing to compete")
    raw = subprocess.check_output(["pgrep", "-x", "WeChat"], text=True, timeout=1)
    pids = raw.split()
    if len(pids) != 1:
        raise RuntimeError("WeChat PID is not unique")
    before = status(int(pids[0]))
    if not clean_identity(before, before) or before["executable"] != WECHAT:
        raise RuntimeError("WeChat already stopped/traced or identity differs")
    with Path("/Applications/WeChat.app/Contents/Info.plist").open("rb") as handle:
        info = plistlib.load(handle)
    if (info["CFBundleShortVersionString"], info["CFBundleVersion"]) != ("4.1.15", "270135"):
        raise RuntimeError("authorized WeChat version differs")
    sys.path.insert(0, str(REPO / "plugins/wechat-bridge"))
    from wechat_bridge import senddirect
    table = senddirect.load_anchor_table(Path.home() / "Library/Application Support/MYIA")
    if senddirect._validate_disk_anchor(table)["anchored"] != "ok":
        raise RuntimeError("disk identity failed")
    authorization = json.loads((ROOT.parent / "task-tiers.json").read_text())["tiers"][2].get("factory_observation_localprompt_authorization")
    if authorization is None:
        raise RuntimeError("new explicit factory-observation authorization is missing")
    if authorization["consumed"] or authorization["max_seconds"] != 30:
        raise RuntimeError("single observation authorization unavailable")
    required = {
        "target": "WeChat 4.1.15 (270135)",
        "purpose": "one factory hit: manual filehelper test digests and thread stack",
        "recipient": "filehelper", "content": "今天真是个好日子",
        "single_foreground_window": True,
        "no_native_calls": True, "no_automatic_send": True,
    }
    if any(authorization.get(key) != value for key, value in required.items()):
        raise RuntimeError("authorization target/purpose/test scope mismatch")
    if (ROOT / "factory-window-localprompt-consumed.json").exists():
        raise RuntimeError("second factory window already consumed")
    return before


def supervise(mode, case):
    os.umask(0o077)
    before = preflight_live() if mode == "live" else None
    folder = Path(tempfile.mkdtemp(prefix=mode + "-" + case + "-", dir=ROOT))
    if mode == "live":
        with (ROOT / "factory-window-localprompt-consumed.json").open("x") as handle:
            json.dump({"authorization_source": "task-tiers.json L3.factory_observation_localprompt_authorization", "before": before,
                       "folder": str(folder), "purpose": "single factory hit: declared test digests and thread stack only"}, handle)
    started = time.clock_gettime(time.CLOCK_MONOTONIC)
    total = 30.0 if mode == "live" else 6.0
    config = {"mode": mode, "case": case, "pid": before["pid"] if before else None,
              "executable": WECHAT if mode == "live" else str(ROOT / "factory_snapshot_fixture_4115"),
              "library": LIBRARY, "observe_until": started + (20.0 if mode == "live" else 3.0)}
    if mode == "live":
        config["recipient_sha256"] = hashlib.sha256(b"filehelper").hexdigest()
        config["content_sha256"] = hashlib.sha256("今天真是个好日子".encode()).hexdigest()
    server = child = prompt = None
    cancelled = False
    report = {"mode": mode, "case": case, "folder": str(folder), "deadline_seconds": total}

    def cancel(_signum, _frame):
        nonlocal cancelled
        cancelled = True

    handlers = {s: signal.signal(s, cancel) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        with (folder / "prompt.log").open("xb") as log:
            prompt = subprocess.Popen([str(ROOT / "factory_window_prompt_4115"), str(folder),
                                       str(started + total - 1), mode],
                                      stdin=subprocess.DEVNULL, stdout=log, stderr=log)
        while not (folder / "prompt-visible.json").is_file():
            if cancelled or prompt.poll() is not None or time.clock_gettime(time.CLOCK_MONOTONIC) >= started + 1:
                raise RuntimeError("local prompt unavailable; no debugger started")
            try:
                prompt.wait(timeout=0.02)
            except subprocess.TimeoutExpired:
                pass
        visible = json.loads((folder / "prompt-visible.json").read_text())
        if not all(visible.get(key) is True for key in ("visible", "nonactivating", "focus_preserved")):
            raise RuntimeError("local prompt visibility/focus validation failed; no debugger started")
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            port = reservation.getsockname()[1]
        config["url"] = f"connect://127.0.0.1:{port}"
        with (folder / "server.log").open("xb") as log:
            server = subprocess.Popen([SERVER, f"127.0.0.1:{port}"],
                                      stdin=subprocess.DEVNULL, stdout=log, stderr=log)
        listening = False
        while not listening:
            if cancelled or server.poll() is not None or time.clock_gettime(time.CLOCK_MONOTONIC) >= started + 2:
                raise RuntimeError("empty debugserver did not listen in setup budget")
            sockets = subprocess.run(["/usr/sbin/lsof", "-nP", "-a", "-p", str(server.pid),
                                      "-iTCP", "-sTCP:LISTEN", "-Fn"],
                                     capture_output=True, text=True, timeout=0.75)
            listening = f"127.0.0.1:{port}" in sockets.stdout
        (folder / "config.json").write_text(json.dumps(config))
        command = [LLDB, "--no-lldbinit", "--batch", "-o", "command script import " + str(ROOT / "factory_observer_4115.py"),
                   "-o", "script factory_observer_4115.run(lldb.debugger, " + repr(str(folder / "config.json")) + ")",
                   "-o", "quit"]
        with (folder / "lldb.log").open("xb") as log:
            child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log, stderr=log)
        announced = False
        while child.poll() is None:
            if prompt.poll() is not None:
                raise RuntimeError("local prompt exited during observation")
            connected = folder / "connected.json"
            if before is None and connected.is_file():
                before = json.loads(connected.read_text())["identity"]
            if mode == "live" and not announced and (folder / "ready.json").is_file():
                print("READY: 请手动向文件传输助手发送约定正文一次。", flush=True)
                announced = True
            if mode == "fixture" and case == "cancel" and before and not cancelled:
                os.kill(os.getpid(), signal.SIGTERM)
            if cancelled or time.clock_gettime(time.CLOCK_MONOTONIC) >= started + (24.0 if mode == "live" else 4.0):
                report["cancelled"] = cancelled
                report["watchdog_triggered"] = not cancelled
                break
            try:
                child.wait(timeout=0.05)
            except subprocess.TimeoutExpired:
                pass
    except BaseException as error:
        report["supervisor_error"] = str(error)
    finally:
        # Cleanup below always runs in this same foreground process.
        for signum in handlers:
            signal.signal(signum, signal.SIG_IGN)
        if child is not None and child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=0.6)
            except subprocess.TimeoutExpired:
                child.kill()  # Close the verified detach-on-error connection.
                child.wait(timeout=0.5)
        if child is not None:
            report["lldb_exit"] = child.returncode
        if before is None and (folder / "connected.json").is_file():
            before = json.loads((folder / "connected.json").read_text())["identity"]
        if server is not None:
            try:
                server.wait(timeout=0.8)
            except subprocess.TimeoutExpired:
                if before is None or clean_identity(before, status(before["pid"])):
                    server.terminate()
                    server.wait(timeout=0.5)
            report["server_exit"] = server.poll()
        if prompt is not None:
            (folder / "prompt-stop.json").write_text("{}")
            if prompt.poll() is None:
                try:
                    prompt.wait(timeout=0.7)
                except subprocess.TimeoutExpired:
                    prompt.terminate()
                    try:
                        prompt.wait(timeout=0.3)
                    except subprocess.TimeoutExpired:
                        prompt.kill()
                        prompt.wait(timeout=0.3)
            report["prompt_exit"] = prompt.poll()
            report["local_prompt_visible"] = (folder / "prompt-visible.json").is_file()
            report["local_prompt_ready"] = (folder / "prompt-ready.json").is_file()
        after = status(before["pid"]) if before else None
        report.update({"before": before, "after": after, "elapsed_seconds": round(time.clock_gettime(time.CLOCK_MONOTONIC) - started, 3),
                       "target_recovered": clean_identity(before, after),
                       "helpers_remaining": int(child is not None and child.poll() is None)
                                            + int(server is not None and server.poll() is None)
                                            + int(prompt is not None and prompt.poll() is None)})
        report["cleanup_ok"] = (report["helpers_remaining"] == 0 and report["elapsed_seconds"] <= total
                                and (report["target_recovered"] or case in ("prelaunch_error", "nonexistent_pid")))
        if (folder / "observer.json").is_file():
            report["observer"] = json.loads((folder / "observer.json").read_text())
        for signum, handler in handlers.items():
            signal.signal(signum, signal.SIG_DFL if handler is None else handler)
        (folder / "supervisor.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("fixture", "live"), required=True)
    parser.add_argument("--case", choices=("observe", "timeout", "cancel", "raised_error", "prelaunch_error",
                                         "client_death_stopped", "client_death_running", "watchdog",
                                         "nonexistent_pid", "snapshot"), default="observe")
    arguments = parser.parse_args()
    if arguments.mode == "live" and arguments.case != "observe":
        parser.error("live mode permits observation only")
    value = supervise(arguments.mode, arguments.case)
    print(json.dumps(value))
    raise SystemExit(0 if value["cleanup_ok"] else 2)
