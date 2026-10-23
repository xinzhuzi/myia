"""Research-only one-hit factory observation. No send, expression, injection, or attach retry."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

import lldb


def run(debugger, config_path):
    config = json.loads(Path(config_path).read_text())
    folder = Path(config_path).parent
    result = {"outcome": "error", "detach_ack": False, "attach_calls": 0,
              "launch_calls": 0, "detached": False, "hit": False}
    process = None
    target = None
    cancelled = False

    def cancel(_signum, _frame):
        nonlocal cancelled
        cancelled = True

    def save(name, value):
        temporary = folder / (name + ".tmp")
        temporary.write_text(json.dumps(value, indent=2) + "\n")
        temporary.replace(folder / name)

    def guard():
        if cancelled:
            raise InterruptedError("window cancelled")
        if time.clock_gettime(time.CLOCK_MONOTONIC) >= config["observe_until"]:
            raise TimeoutError("observation deadline")

    def read(address, length):
        guard()
        error = lldb.SBError()
        data = process.ReadMemory(address, length, error)
        if not error.Success() or len(data) != length:
            raise RuntimeError("bounded memory read failed: " + str(error))
        return data

    def pointer(address):
        value = int.from_bytes(read(address, 8), "little")
        if value < 4096 or value % 8:
            raise RuntimeError("invalid pointer; no masking or scanning")
        return value

    handlers = {s: signal.signal(s, cancel) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        debugger.SetAsync(True)
        interpreter = debugger.GetCommandInterpreter()
        for command in (
            "settings set plugin.process.gdb-remote.packet-timeout 1",
            "settings set target.process.interrupt-timeout 1",
            "settings set target.require-hardware-breakpoint true",
            *(("log enable -f " + str(folder / "packets.log") + " gdb-remote packets",)
              if config["mode"] == "fixture" else ()),
        ):
            response = lldb.SBCommandReturnObject()
            interpreter.HandleCommand(command, response)
            if not response.Succeeded():
                raise RuntimeError(response.GetError())
        guard()
        target = debugger.CreateTarget(config["executable"])
        listener = lldb.SBListener("bounded-observer")
        error = lldb.SBError()
        process = target.ConnectRemote(listener, config["url"], "gdb-remote", error)
        if not error.Success():
            raise RuntimeError("empty server connect failed: " + str(error))
        while process.GetState() != lldb.eStateConnected:
            guard()
            if process.GetState() not in (lldb.eStateUnloaded, lldb.eStateConnected):
                raise RuntimeError("unexpected empty-server state")
            listener.WaitForEvent(1, lldb.SBEvent())
        response = lldb.SBCommandReturnObject()
        interpreter.HandleCommand("process plugin packet send QSetDetachOnError:1", response)
        result["detach_ack"] = response.Succeeded() and "response: OK" in response.GetOutput().splitlines()
        if not result["detach_ack"]:
            raise RuntimeError("detach-on-error was not acknowledged")
        guard()
        if config["case"] == "prelaunch_error":
            raise RuntimeError("intentional isolated prelaunch failure")
        if config["mode"] == "fixture" and config["case"] == "nonexistent_pid":
            absent = subprocess.run([str(Path(__file__).with_name("process_status")), "2147483647"],
                                    capture_output=True, timeout=0.75)
            if absent.returncode != 3:
                raise RuntimeError("invalid-PID fixture was not proven absent")
            result["attach_calls"] += 1
            process.RemoteAttachToProcessWithID(2147483647, error)
            result["outcome"] = "nonexistent_pid_rejected"
            result["invalid_pid_error"] = str(error)
            return
        if config["mode"] == "fixture":
            result["launch_calls"] += 1
            ok = process.RemoteLaunch([config["executable"]], None, "/dev/null", "/dev/null",
                                      "/dev/null", str(folder), lldb.eLaunchFlagDetachOnError,
                                      True, error)
        else:
            result["attach_calls"] += 1
            ok = process.RemoteAttachToProcessWithID(config["pid"], error)
        if not ok or not error.Success():
            raise RuntimeError("single target operation failed: " + str(error))
        while process.GetState() not in (lldb.eStateStopped, lldb.eStateCrashed, lldb.eStateExited):
            guard()
            listener.WaitForEvent(1, lldb.SBEvent())
        if process.GetState() != lldb.eStateStopped:
            raise RuntimeError("target did not stop safely")
        raw = subprocess.check_output([str(Path(__file__).with_name("process_status")),
                                       str(process.GetProcessID())], text=True, timeout=0.75)
        fields = raw.rstrip("\n").split("\t", 5)
        identity = {"pid": int(fields[0]), "flags": int(fields[1]), "state": int(fields[2]),
                    "start_sec": int(fields[3]), "start_usec": int(fields[4]), "executable": fields[5]}
        save("connected.json", {"pid": process.GetProcessID(), "state": "stopped", "identity": identity})
        guard()
        if config["mode"] == "fixture" and config["case"] == "client_death_stopped":
            os._exit(90)  # Only permitted for a newly launched disposable fixture.
        if config["case"] == "raised_error":
            raise RuntimeError("intentional embedded LLDB exception")
        if config["mode"] == "fixture" and config["case"] == "snapshot":
            pc = process.GetThreadAtIndex(0).GetFrameAtIndex(0).GetPC()
            result["fixture_snapshot_read_bytes"] = len(read(pc, 16))
            result["outcome"] = "fixture_snapshot"
            return
        if config["mode"] == "fixture" and config["case"] == "watchdog":
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            while True:
                listener.WaitForEvent(1, lldb.SBEvent())
        if config["mode"] == "fixture":
            breakpoint = target.BreakpointCreateByName("fixture_factory")
        else:
            modules = [target.GetModuleAtIndex(i) for i in range(target.GetNumModules())]
            matches = [m for m in modules if str(m.GetFileSpec()) == config["library"]]
            if len(matches) != 1:
                raise RuntimeError("actual Resources library was not uniquely loaded")
            module = matches[0]
            base = module.GetObjectFileHeaderAddress().GetLoadAddress(target)
            if base == lldb.LLDB_INVALID_ADDRESS:
                raise RuntimeError("missing actual module load address")
            if module.GetUUIDString().upper() != "0C2F01C0-C197-3286-901D-70E1D007A1C0":
                raise RuntimeError("runtime module UUID mismatch")
            if read(base + 0x30c2c1c, 16).hex() != "ff4302d1fa6704a9f85f05a9f65706a9":
                raise RuntimeError("native factory code identity mismatch")
            result["module_uuid"] = module.GetUUIDString()
            import sys
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from newsendmsg_identity_4115 import inspect_service
            result["service_identity"] = inspect_service(read, base)
            breakpoint = target.BreakpointCreateByAddress(base + 0x30c2c1c)

        if not breakpoint.IsValid() or not breakpoint.IsHardware() or breakpoint.GetNumLocations() != 1:
            raise RuntimeError("one hardware breakpoint could not be established")
        breakpoint.SetOneShot(True)
        breakpoint_address = breakpoint.GetLocationAtIndex(0).GetLoadAddress()
        result["hardware_breakpoint"] = True
        if config["mode"] == "fixture" and config["case"] in ("timeout", "cancel", "client_death_running"):
            breakpoint.SetEnabled(False)
        guard()
        initial_stop_id = process.GetStopID()
        error = process.Continue()
        if not error.Success():
            raise RuntimeError("continue failed: " + str(error))
        if config["mode"] == "live":
            save("ready.json", {"ready": True, "deadline": config["observe_until"]})
        if config["mode"] == "fixture" and config["case"] == "client_death_running":
            while process.GetState() != lldb.eStateRunning:
                guard()
                listener.WaitForEvent(1, lldb.SBEvent())
            os._exit(91)
        while True:
            guard()
            listener.WaitForEvent(1, lldb.SBEvent())
            state = process.GetState()
            if state == lldb.eStateRunning:
                continue
            if state == lldb.eStateStopped and process.GetStopID() == initial_stop_id:
                continue  # Initial stop notification can outlive asynchronous Continue.
            if state != lldb.eStateStopped:
                raise RuntimeError("unexpected target state: " + str(state))
            threads = [process.GetThreadAtIndex(i) for i in range(process.GetNumThreads())]
            hits = [t for t in threads if t.GetStopReason() == lldb.eStopReasonBreakpoint
                    and t.GetFrameAtIndex(0).GetPC() == breakpoint_address]
            if len(hits) != 1:
                result["stop_reasons"] = [{"reason": t.GetStopReason(),
                                           "data": [t.GetStopReasonDataAtIndex(j)
                                                    for j in range(t.GetStopReasonDataCount())]}
                                          for t in threads]
                raise RuntimeError("unexpected stop; no resume/retry")
            result["hit"] = True
            import sys
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from newsendmsg_factory_snapshot_4115 import inspect_factory
            thread = hits[0]
            frame = thread.GetFrameAtIndex(0)
            registers = {}
            for name in ("x0", "x1", "x2"):
                register = frame.FindRegister(name)
                if not register.IsValid():
                    raise RuntimeError("factory argument register unavailable")
                registers[name] = register.GetValueAsUnsigned()
            capture_base = base if config["mode"] == "live" else 0x100000000
            service = (int(result["service_identity"]["service_interface"], 16)
                       if config["mode"] == "live" else 0x200000000)
            capture = inspect_factory(read, capture_base, registers, service)
            if config["mode"] == "live":
                matched = (capture["fields"]["1"] is not None
                           and capture["fields"]["2"] is not None
                           and capture["fields"]["1"]["sha256"] == config["recipient_sha256"]
                           and capture["fields"]["2"]["sha256"] == config["content_sha256"])
                result["declared_test_matched"] = matched
                if not matched:
                    raise RuntimeError("first factory hit differs from declared test; no retry")
            result["factory_snapshot"] = capture
            result["thread_id"] = thread.GetThreadID()
            result["thread_name"] = thread.GetName()
            result["stack"] = [{"pc": hex(thread.GetFrameAtIndex(i).GetPC()),
                                "function": thread.GetFrameAtIndex(i).GetFunctionName()}
                               for i in range(min(thread.GetNumFrames(), 24))]
            result["outcome"] = "observed"
            break
    except BaseException as error:
        result["outcome"] = "cancelled" if cancelled else type(error).__name__
        result["error"] = str(error)
    finally:
        if target and target.IsValid():
            target.DeleteAllBreakpoints()
        if process and process.IsValid() and process.GetProcessID() not in (0, lldb.LLDB_INVALID_PROCESS_ID):
            error = process.Detach(False)
            result["detached"] = error.Success()
            result["detach_error"] = str(error)
        for signum, handler in handlers.items():
            signal.signal(signum, signal.SIG_DFL if handler is None else handler)
        result["finished_monotonic"] = time.clock_gettime(time.CLOCK_MONOTONIC)
        save("observer.json", result)
