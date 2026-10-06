// 插件发布链:源码资产 + 远取锁生成(10-06-plugin-src-remote-fetch 批4;design D7)。
//
// 做什么:对 11 个随包组件包逐件 `git archive HEAD plugins/<id>` 产
// dist/plugin-<id>.tar.gz(字节确定性:同 commit 重跑同 sha256),算
// sha256/size 后写 desktop/resources/plugins.lock.json(装机包随包的
// 内容寻址锁),非 --dry-run 时 `gh release upload <tag>` 传资产。
//
// 为什么必须 git archive 而非文件系统 tar:文件系统 tar 会把工作树未跟踪件
// 整体裹进——__pycache__ 之外最关键是 osint/theharvester 已 init 的 submodule
// 工作树(vendor/ 全量 GPL 源码)会越分发红线;git archive 只出 tracked 文件,
// submodule 以 gitlink 存在、内容天然不进资产。tar 成员表再过一遍双保险断言
// (vendor/、__pycache__、*.pyc 不得出现;成员前缀必须恰为 plugins/<id>/)。
//
// 用法:node scripts/release-plugins-lock.mjs <tag> [--dry-run]
//   <tag>      目标 release tag(锁内 url 与资产上传共用;动过插件源码必重跑)
//   --dry-run  只产 dist + 锁,不执行 gh 上传(本地重产锁用)
// 跨平台:纯 node 内建(zlib/crypto/child_process),发布机免 uv/免 npm install。
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { gunzipSync } from "node:zlib";
import { spawnSync } from "node:child_process";

const DESKTOP_DIR = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const REPO_ROOT = path.resolve(DESKTOP_DIR, "..");
const DIST_DIR = path.join(REPO_ROOT, "dist");
const LOCK_PATH = path.join(DESKTOP_DIR, "resources", "plugins.lock.json");

/** 随包组件包清单(与 tests/desktop/test_installer_resources.py ALL_BUNDLED_PACKAGES 同源;改件同步两处)。 */
const PACKAGES = [
  "myssia-credhunter",
  "myssia-firecrawl",
  "myssia-maigret",
  "myssia-media",
  "myssia-mediacrawler",
  "myssia-osint",
  "myssia-proxy",
  "myssia-snownlp",
  "myssia-theharvester",
  "myssia-urlwatch",
  "myssia-yake",
];

const REPO_URL = "https://github.com/xinzhuzi/myia";

/** 禁入资产红线(D7 双保险;git archive 天然排除,此为第二道)。 */
function assertMembersClean(id, names) {
  const prefix = `plugins/${id}/`;
  if (names.length === 0) throw new Error(`${id}: 资产成员表为空`);
  for (const name of names) {
    // 壳目录成员(plugins/ 与 plugins/<id>/)与 python 侧 _validated_member/剥壳语义兼容(remote.py:424-425),放行
    const isShellDir = name === "plugins/" || name === prefix;
    if (!isShellDir && !name.startsWith(prefix)) {
      throw new Error(`${id}: 成员越出唯一前缀 ${prefix}(当前 ${name})——extract_staging 剥壳语义会被破坏`);
    }
    if (name.includes("/vendor/") || name.includes("__pycache__") || name.endsWith(".pyc")) {
      throw new Error(`${id}: 红线成员入资产(${name})——vendor/分发红线与缓存件不得进资产`);
    }
  }
}

/** 极简 tar 成员扫描(仅取 name/size/typeflag;git archive 首块恒为 pax_global_header 跳过,长名走断言拒)。 */
function tarMembers(gzBuffer) {
  const tar = gunzipSync(gzBuffer);
  const names = [];
  const decoder = new TextDecoder("utf-8");
  for (let offset = 0; offset + 512 <= tar.length; ) {
    const header = tar.subarray(offset, offset + 512);
    const name = decoder.decode(header.subarray(0, 100)).replace(/\0.*$/s, "");
    if (name === "") break; // 结束块
    const sizeField = decoder.decode(header.subarray(124, 136)).replace(/\0.*$/s, "").trim();
    const size = sizeField === "" ? 0 : parseInt(sizeField, 8);
    const typeflag = String.fromCharCode(header[156]);
    if (name.length >= 100) throw new Error(`tar 长名成员未支持(${name.slice(0, 40)}…);git archive 不该产出,查树`);
    if (typeflag === "g") {
      // git archive 的 pax_global_header(仓库级元数据):跳过其数据块,不计成员
    } else if (typeflag === "0" || typeflag === "\0" || typeflag === "5") {
      names.push(name);
    } else {
      throw new Error(`tar 非常规成员类型 typeflag=${JSON.stringify(typeflag)}(name=${name});软/硬链接与 pax 扩展头不入资产`);
    }
    offset += 512 + Math.ceil(size / 512) * 512;
  }
  return names;
}

function run(cmd, args, opts = {}) {
  const result = spawnSync(cmd, args, { cwd: REPO_ROOT, encoding: "utf-8", ...opts });
  if (result.error) throw new Error(`无法执行 ${cmd}: ${result.error.message}`);
  if (result.status !== 0) {
    throw new Error(`${cmd} ${args.join(" ")} 退出码 ${result.status}\n${(result.stderr || "").slice(-800)}`);
  }
  return result;
}

const argv = process.argv.slice(2);
const dryRun = argv.includes("--dry-run");
const tag = argv.find((a) => !a.startsWith("--"));
if (!tag) {
  console.error("用法: node scripts/release-plugins-lock.mjs <tag> [--dry-run]");
  process.exit(2);
}
if (!/^v\d/.test(tag)) {
  console.error(`tag 形态应为 v*(当前 ${tag});锁 url 与 release 资产同 tag 语义`);
  process.exit(2);
}

mkdirSync(DIST_DIR, { recursive: true });
for (const stale of readdirSync(DIST_DIR)) {
  if (stale.startsWith("plugin-") && stale.endsWith(".tar.gz")) {
    rmSync(path.join(DIST_DIR, stale));
  }
}

const assets = {};
for (const id of PACKAGES) {
  const outPath = path.join(DIST_DIR, `plugin-${id}.tar.gz`);
  // vendor 子树整体排除:osint/theharvester 的 vendor/{Photon,theHarvester} 是 gitlink
  // submodule(git archive 本就不出其内容,只残留空目录壳),exclude 连壳也剥——
  // 资产零 vendor 面,红线断言保持绝对(任何 vendor 成员=红)。
  run("git", [
    "archive",
    "--format=tar.gz",
    "-o",
    outPath,
    "HEAD",
    `plugins/${id}`,
    `:(exclude)plugins/${id}/vendor`,
  ]);
  assertMembersClean(id, tarMembers(readFileSync(outPath)));
  const sha256 = createHash("sha256").update(readFileSync(outPath)).digest("hex");
  const size = statSync(outPath).size;
  const yaml = readFileSync(path.join(REPO_ROOT, "plugins", id, "plugin.yaml"), "utf-8");
  const versionMatch = /^version:\s*(\S+)\s*$/m.exec(yaml);
  if (!versionMatch) throw new Error(`${id}: plugin.yaml 无 version 字段(锁 version 供装机预显)`);
  assets[id] = {
    url: `${REPO_URL}/releases/download/${tag}/plugin-${id}.tar.gz`,
    sha256,
    size,
    version: versionMatch[1],
  };
  console.log(`${id}  ${size}B  ${sha256.slice(0, 12)}…`);
}

const lock = {
  manifest_version: 1,
  repo: REPO_URL,
  tag,
  generated_at: new Date().toISOString(),
  assets,
};
writeFileSync(LOCK_PATH, `${JSON.stringify(lock, null, 2)}\n`);
console.log(`锁已写 ${path.relative(REPO_ROOT, LOCK_PATH)}(tag=${tag},${PACKAGES.length} 件)`);

if (dryRun) {
  console.log("--dry-run:跳过 gh release upload(dist/ 与锁已就绪)");
} else {
  run("gh", ["release", "upload", tag, ...PACKAGES.map((id) => path.join("dist", `plugin-${id}.tar.gz`)), "--clobber"]);
  console.log(`资产已传 release ${tag}(--clobber 覆盖语义)`);
}
