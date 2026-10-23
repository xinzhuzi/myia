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
            for name in ("identity_observer_4115.py", "run_identity_observer_4115.py", "process_status", "cleanup_fixture", "newsendmsg_identity_4115.py")}


def preflight_live():
    qualified = json.loads((ROOT / "identity-cleanup-qualification.json").read_text())
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
    authorization = json.loads((ROOT.parent / "task-tiers.json").read_text())["tiers"][2].get("identity_observation_authorization")
    if authorization is None:
        raise RuntimeError("new explicit identity-snapshot authorization is missing")
    if authorization["consumed"] or authorization["max_seconds"] != 30:
        raise RuntimeError("single observation authorization unavailable")
    return before


def supervise(mode, case):
    os.umask(0o077)
    before = preflight_live() if mode == "live" else None
    folder = Path(tempfile.mkdtemp(prefix=mode + "-" + case + "-", dir=ROOT))
    if mode == "live":
        with (ROOT / "identity-window-consumed.json").open("x") as handle:
            json.dump({"authorization_source": "task-tiers.json L3.identity_observation_authorization", "before": before,
                       "folder": str(folder), "purpose": "fixed 80-byte service identity snapshot only"}, handle)
    started = time.clock_gettime(time.CLOCK_MONOTONIC)
    total = 30.0 if mode == "live" else 6.0
    config = {"mode": mode, "case": case, "pid": before["pid"] if before else None,
              "executable": WECHAT if mode == "live" else str(ROOT / "cleanup_fixture"),
              "library": LIBRARY, "observe_until": started + (20.0 if mode == "live" else 3.0)}
    server = child = None
    cancelled = False
    report = {"mode": mode, "case": case, "folder": str(folder), "deadline_seconds": total}

    def cancel(_signum, _frame):
        nonlocal cancelled
        cancelled = True

    handlers = {s: signal.signal(s, cancel) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
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
        command = [LLDB, "--no-lldbinit", "--batch", "-o", "command script import " + str(ROOT / "identity_observer_4115.py"),
                   "-o", "script identity_observer_4115.run(lldb.debugger, " + repr(str(folder / "config.json")) + ")",
                   "-o", "quit"]
        with (folder / "lldb.log").open("xb") as log:
            child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log, stderr=log)
        while child.poll() is None:
            connected = folder / "connected.json"
            if before is None and connected.is_file():
                before = json.loads(connected.read_text())["identity"]
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
        after = status(before["pid"]) if before else None
        report.update({"before": before, "after": after, "elapsed_seconds": round(time.clock_gettime(time.CLOCK_MONOTONIC) - started, 3),
                       "target_recovered": clean_identity(before, after),
                       "helpers_remaining": int(child is not None and child.poll() is None)
                                            + int(server is not None and server.poll() is None)})
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
