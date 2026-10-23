// 打包前源码树清理(10-05-desktop-managed-py-env 第 7 步;第 1 步遗留裁量)。
//
// 为什么需要:tauri.conf.json 的 resources map 形目录映射(../../src/myssia →
// myssia-src/myssia 等)在 tauri-utils 里是 Walk 递归 + 结构保真,**没有排除语义**
// (第 1 步质检实读 tauri-utils 2.10.1 resources.rs 核实),gitignored 的
// __pycache__/(实测 src/myssia 下 12 个目录)与 macOS 的 .DS_Store 会被原样
// 打进安装包;10-11-wechat-ui-bridge D5 随包组件源码树 plugins/wechat-bridge
// 起同病加新——本机 pip 源码冒烟遗留的 build/ 与 *.egg-info/ 同样原样进包
// (2026-10-12 装机打包实测)。CI 干净检出台面天然没有;本机开发构建由本脚本在
// beforeBuildCommand 链(vite 构建之前)兜底清理。幂等:目录不存在即静默通过;
// 删除的只是可再生垃圾(pyc 按 mtime+size 校验,删掉后 Python 首次 import 自行
// 重建,无正确性影响;build//egg-info 由 pip 重装再生成)。
//
// 用法:node scripts/clean-pycache.mjs [目录 ...]
//   缺省 = 随包源码树(相对本文件定位:../src/myssia、../myssia_desktop_entry、
//   ../plugins/wechat-bridge 三棵);
//   显式传参 = 测试用(相对当前工作目录或绝对路径均可)。
// 跨平台:纯 node:fs 零依赖(macOS/Linux/Windows runner 行为一致;不用 `find`,
// Windows 上该名解析到 System32 文本搜索工具)。
import { existsSync, readdirSync, rmSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const DESKTOP_DIR = path.dirname(path.dirname(fileURLToPath(import.meta.url)));

/** 随包源码树(tauri.conf.json resources 映射的目录源,第 1 步 PYENV_RESOURCE_MAP;
 * 10-11-wechat-ui-bridge D5 起含随包组件源码树 plugins/wechat-bridge →
 * components/wechat-bridge;10-24-huawei-ai-news-absorb Step 6.3 起含
 * myssia-classifier/myssia_classifier → myssia-src/myssia_classifier 源码随包
 * (classifier 0.0.7 随包,PYTHONPATH 影子优先于 site-packages PyPI 钉版)。 */
const DEFAULT_ROOTS = [
  path.resolve(DESKTOP_DIR, "../src/myssia"),
  path.resolve(DESKTOP_DIR, "../myssia-classifier/myssia_classifier"),
  path.resolve(DESKTOP_DIR, "myssia_desktop_entry"),
  path.resolve(DESKTOP_DIR, "../plugins/wechat-bridge"),
];

/** 不进包的再生物:Python 字节码缓存 + macOS Finder 元数据 + pip 源码装工件
 * (setuptools 的 build/ 与 *.egg-info/;D5 注册表随包源码目录在本机 pip 冒烟
 * 后会遗留这两类目录,resources 无排除语义会被原样打进安装包)。 */
const JUNK_NAMES = new Set(["__pycache__", ".DS_Store", "build"]);
/** pip 源码装元数据目录后缀(egg-info 名字带工程名,按后缀识别)。 */
const JUNK_SUFFIXES = [".egg-info"];

/** 递归清理一棵树;返回删除的条目数(目录/文件各计 1)。 */
function cleanTree(dir) {
  if (!existsSync(dir)) return 0;
  let removed = 0;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    const isJunk =
      JUNK_NAMES.has(entry.name) ||
      JUNK_SUFFIXES.some((suffix) => entry.name.endsWith(suffix));
    if (isJunk) {
      rmSync(full, { recursive: true, force: true });
      removed += 1;
    } else if (entry.isDirectory()) {
      removed += cleanTree(full);
    }
  }
  return removed;
}

const roots =
  process.argv.length > 2
    ? process.argv.slice(2).map((arg) => path.resolve(process.cwd(), arg))
    : DEFAULT_ROOTS;
let total = 0;
for (const root of roots) total += cleanTree(root);
const display = roots.map((root) => path.relative(process.cwd(), root) || ".").join(", ");
console.log(`clean-pycache: ${total} 个垃圾条目(__pycache__/.DS_Store/build/egg-info)已清理: ${display}`);
