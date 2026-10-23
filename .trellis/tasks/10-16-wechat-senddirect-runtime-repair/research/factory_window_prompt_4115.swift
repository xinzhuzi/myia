// Local, passive window status only. No WeChat APIs, input synthesis or debugger.
import AppKit
import Darwin

func monotonicNow() -> Double {
    var value = timespec()
    clock_gettime(CLOCK_MONOTONIC, &value)
    return Double(value.tv_sec) + Double(value.tv_nsec) / 1_000_000_000
}

func phase(now: Double, deadline: Double, ready: Bool, ended: Bool) -> String {
    if ended || now >= deadline { return "ended" }
    return ready ? "ready" : "waiting"
}

if CommandLine.arguments == [CommandLine.arguments[0], "--self-test"] {
    precondition(phase(now: 1, deadline: 2, ready: false, ended: false) == "waiting")
    precondition(phase(now: 1, deadline: 2, ready: true, ended: false) == "ready")
    precondition(phase(now: 2, deadline: 2, ready: true, ended: false) == "ended")
    precondition(phase(now: 1, deadline: 2, ready: true, ended: true) == "ended")
    print("prompt phase checks passed")
    exit(0)
}

guard CommandLine.arguments.count == 4,
      let deadline = Double(CommandLine.arguments[2]),
      ["fixture", "live"].contains(CommandLine.arguments[3]) else { exit(64) }
let folder = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let fixture = CommandLine.arguments[3] == "fixture"
let app = NSApplication.shared
app.setActivationPolicy(.accessory)
let previousFront = NSWorkspace.shared.frontmostApplication?.processIdentifier
final class PassivePanel: NSPanel {
    override var canBecomeKey: Bool { false }
    override var canBecomeMain: Bool { false }
}
guard let screen = NSScreen.main else { exit(69) }
let frame = screen.visibleFrame
let panel = PassivePanel(contentRect: NSRect(x: frame.midX - 310, y: frame.maxY - 134,
                                             width: 620, height: 110),
                         styleMask: [.borderless, .nonactivatingPanel],
                         backing: .buffered, defer: false)
panel.level = .statusBar
panel.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .ignoresCycle]
panel.ignoresMouseEvents = true
panel.hidesOnDeactivate = false
panel.isOpaque = false
panel.backgroundColor = .clear
panel.hasShadow = true
let view = NSView(frame: NSRect(x: 0, y: 0, width: 620, height: 110))
view.wantsLayer = true
view.layer?.cornerRadius = 14
let title = NSTextField(labelWithString: fixture ? "提示界面自检 · 请勿发送" : "正在连接 · 请先不要发送")
title.frame = NSRect(x: 24, y: 59, width: 576, height: 30)
title.font = .systemFont(ofSize: 23, weight: .semibold)
title.textColor = .white
let detail = NSTextField(labelWithString: fixture ? "自有夹具验证，不操作微信" : "就绪后此处会直接提示，无需等待对话回复")
detail.frame = NSRect(x: 24, y: 24, width: 576, height: 25)
detail.font = .systemFont(ofSize: 15)
detail.textColor = NSColor.white.withAlphaComponent(0.9)
view.addSubview(title)
view.addSubview(detail)
panel.contentView = view
view.layer?.backgroundColor = NSColor.systemIndigo.cgColor
panel.orderFrontRegardless()

func save(_ name: String, _ value: [String: Any]) {
    guard let data = try? JSONSerialization.data(withJSONObject: value, options: [.sortedKeys]) else { exit(70) }
    do { try data.write(to: folder.appendingPathComponent(name), options: .atomic) }
    catch { exit(74) }
}

guard panel.isVisible, !panel.isKeyWindow, !panel.isMainWindow else { exit(70) }
save("prompt-visible.json", ["visible": panel.isVisible, "pid": ProcessInfo.processInfo.processIdentifier,
                            "nonactivating": !panel.isKeyWindow && !panel.isMainWindow,
                            "focus_preserved": previousFront == NSWorkspace.shared.frontmostApplication?.processIdentifier,
                            "fixture": fixture, "started_monotonic": monotonicNow()])
var seen = Set<String>()
var endedAt: Double?
let timer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { _ in
    let now = monotonicNow()
    let readyPath = folder.appendingPathComponent("ready.json")
    let ended = ["supervisor.json", "prompt-stop.json"].contains { FileManager.default.fileExists(atPath: folder.appendingPathComponent($0).path) }
    var current = phase(now: now, deadline: deadline, ready: false, ended: ended)
    var remaining = deadline - now
    if let data = try? Data(contentsOf: readyPath),
       let ready = (try? JSONSerialization.jsonObject(with: data)) as? [String: Any],
       ready["ready"] as? Bool == true, let observeDeadline = ready["deadline"] as? Double {
        remaining = min(deadline, observeDeadline) - now
        current = phase(now: now, deadline: min(deadline, observeDeadline), ready: true, ended: ended)
    }
    if !seen.contains(current) {
        seen.insert(current)
        save("prompt-" + current + ".json", ["phase": current, "monotonic": now,
                                              "fixture": fixture, "visible": panel.isVisible])
    }
    if current == "ready" {
        if !fixture { title.stringValue = "可以发送 · 现在手动发送一次" }
        detail.stringValue = fixture ? "自有夹具已就绪；请勿发送微信消息" : "文件传输助手：今天真是个好日子（剩余 \(max(0, Int(remaining))) 秒）"
        view.layer?.backgroundColor = NSColor.systemGreen.withAlphaComponent(0.95).cgColor
    } else if current == "ended" {
        if !fixture { title.stringValue = "本次窗口已结束 · 请勿发送" }
        detail.stringValue = fixture ? "界面自检结束，无微信操作" : "不补发、不重挂；等待对话中的核验结果"
        view.layer?.backgroundColor = NSColor.darkGray.cgColor
        if endedAt == nil { endedAt = now }
        if (ended || now >= deadline) && now - (endedAt ?? now) >= 0.35 { app.terminate(nil) }
    }
}
RunLoop.main.add(timer, forMode: .common)
app.run()
