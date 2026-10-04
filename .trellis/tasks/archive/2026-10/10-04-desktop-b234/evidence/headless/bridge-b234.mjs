// bridge-b234.mjs — 10-04-desktop-b234 无头冒烟桥(法 = 10-03-detail-images
// evidence/app-headless/bridge-di.mjs 先例拷贝改造):
//   sidecar = 真 spawn 当前源码 desktop/entry.py serve(desktop/.venv-build python),
//   协议同构:stdin 一行 {"id","method","params"} → stdout 一行 {"id","result"|"error"}。
// 差异:MYIA_HOME 指向夹具根 /tmp/myia-b234-e2e/home(db/plugins 全隔离,serve
// 上下文缺省 db 即夹具库——比先例的 shim 注入 params.db 更贴真壳数据通路),
// 并显式清掉 MYIA_PLUGIN_DIR(市场安装根尊重该 env,防串真机)。
import { createServer } from "node:http";
import { spawn } from "node:child_process";

const REPO = "/Users/zhengbingjin/Project/Github/MYIA";
const PY = `${REPO}/desktop/.venv-build/bin/python`;
const PORT = Number(process.argv[2] || 0) || 54119;

const child = spawn(PY, [`${REPO}/desktop/entry.py`, "serve"], {
  cwd: REPO,
  stdio: ["pipe", "pipe", "pipe"],
  env: {
    ...process.env,
    MYIA_HOME: "/tmp/myia-b234-e2e/home",
    MYIA_PLUGIN_DIR: "",
  },
});

let buffer = "";
const pending = new Map();
let nextId = 1;

child.stdout.setEncoding("utf8");
child.stdout.on("data", (chunk) => {
  buffer += chunk;
  let idx;
  while ((idx = buffer.indexOf("\n")) >= 0) {
    const line = buffer.slice(0, idx).trim();
    buffer = buffer.slice(idx + 1);
    if (!line) continue;
    let msg;
    try {
      msg = JSON.parse(line);
    } catch {
      continue;
    }
    if (msg && msg.id !== undefined && pending.has(msg.id)) {
      const waiter = pending.get(msg.id);
      pending.delete(msg.id);
      waiter(msg);
    }
  }
});
child.stderr.setEncoding("utf8");
child.stderr.on("data", (c) => process.stderr.write(`[sidecar] ${c}`));
child.on("exit", (code, signal) => {
  console.error(`[bridge] sidecar exited code=${code} signal=${signal}`);
  for (const waiter of pending.values()) waiter({ error: { code: "sidecar_not_running", path: "$", message: `sidecar 进程未运行 (exit ${code}/${signal})` } });
  pending.clear();
  sidecarAlive = false;
});

let sidecarAlive = true;

function rpc(method, params) {
  return new Promise((resolve) => {
    if (!sidecarAlive || child.stdin.destroyed) {
      resolve({ error: { code: "sidecar_not_running", path: "$", message: "sidecar 进程未运行" } });
      return;
    }
    const id = nextId++;
    const timer = setTimeout(() => {
      if (pending.has(id)) {
        pending.delete(id);
        resolve({ error: { code: "sidecar_timeout", path: "$", message: "sidecar 应答超时(120s)" } });
      }
    }, 120_000);
    pending.set(id, (msg) => {
      clearTimeout(timer);
      resolve(msg);
    });
    child.stdin.write(JSON.stringify({ id, method, params: params ?? {} }) + "\n");
  });
}

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "POST, GET, OPTIONS",
  "access-control-allow-headers": "content-type",
};

const server = createServer((req, res) => {
  if (req.method === "OPTIONS") {
    res.writeHead(204, CORS);
    res.end();
    return;
  }
  if (req.method === "POST" && req.url === "/rpc") {
    let body = "";
    req.setEncoding("utf8");
    req.on("data", (c) => (body += c));
    req.on("end", async () => {
      let payload;
      try {
        payload = JSON.parse(body || "{}");
      } catch {
        res.writeHead(400, CORS);
        res.end(JSON.stringify({ error: { code: "bad_request", path: "$", message: "invalid json" } }));
        return;
      }
      const msg = await rpc(payload.method, payload.params);
      res.writeHead(200, { ...CORS, "content-type": "application/json" });
      res.end(JSON.stringify(msg));
    });
    return;
  }
  res.writeHead(404, CORS);
  res.end("{}");
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`bridge on http://127.0.0.1:${PORT}`);
});

const shutdown = () => {
  try { child.stdin.end(); child.kill(); } catch {}
  server.close();
  process.exit(0);
};
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
