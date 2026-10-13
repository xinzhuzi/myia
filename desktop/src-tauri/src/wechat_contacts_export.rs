//! 微信联系人三格式导出(task 10-14-wechat-contacts R3)。
//!
//! 联系人工作台「导出当前筛选」按钮的壳侧通道(消费方 = wechat-contacts.tsx
//! 导出行,IPC 封装 = wechat-contacts-api.ts)。与群导出(wechat_group_export)
//! 的关键分歧:**壳不收大载荷**——联系人全量(2 万行级)不进前端内存,由壳
//! spawn 安装态桥 `localdb contacts --type <t> [--keyword K] [--with-residue]
//! --limit 0 --json`(`--limit 0` = 全量导出态,桥内帽豁免,prd.md:75)取
//! 数,三格式同基础名落盘(`<base>.json/.csv/.vcf`),回执只带路径与行数
//! (内容零入日志,群导出同款隐私纪律)。
//!
//! 命令参数(wire camelCase;Rust 侧 `type` 是关键字,故参数名 `type_filter`
//! ↔ 前端 `typeFilter`,两侧文件头注互指):`{typeFilter, keyword?,
//! withResidue?, formats: ["json","csv","vcf"]}`。应答三态(群导出判例):
//! `null` = 用户取消保存对话框(静默,零写盘);对象 = `{"files": [{"name",
//! "path","rows"}], "total_rows"}`;throw = 失败(信封沿仓惯例
//! `{"code","path","message"}`,前端 asSidecarError 同形解析)。
//!
//! 三格式(R3 钉死):
//! - JSON:桥应答 `contacts.rows` 数组原形直写(pretty,零改形——evidence/
//!   类型等 provenance 不丢);
//! - CSV:表头 `username,display_name,remark,nickname,alias,type,evidence,
//!   last_contact_hint`;UTF-8 **带 BOM**(`\uFEFF`,Excel 直开中文不乱码);
//!   公式注入中和(`=`+`-`@`tab 开头前置 `'`,C1/群导出同规);evidence
//!   数组 `|` 连接;`last_contact_hint` ← 行 `description`(桥行契约无
//!   联系时间列,v1 库序不承诺时间序——description 是唯一随身提示列,如实
//!   映射不臆造);
//! - VCF(vCard 3.0,自写序列化):每联系人 `BEGIN:VCARD/VERSION:3.0`;
//!   `FN`=display_name、`N`=display_name(未知结构不臆拆,全名进家名位);
//!   `NICKNAME`=nickname(在场时);`X-WECHAT-ID`=username(扩展字段命名
//!   惯例,非许可表达);`NOTE` 收纳类型/证据(「会话痕迹」「仅残留」)/
//!   alias/description(人话标签行;群聊行另纳成员数);CRLF 行尾 +
//!   RFC 2426 折叠(75 字节,多字节字符不切半)与转义(`, ; \ 换行`)。
//!
//! 权限与隐私:导出件落盘 `0600`(chatlog-keeper private_text_writer 语义);
//! 回执只带路径与行数。
//!
//! 线程纪律:`blocking_save_file` 禁主线程(群导出判例),走
//! `tauri::async_runtime::spawn_blocking`;桥 spawn 同款(spawn_blocking 内
//! try_wait 轮询 + 超时 kill,wechat_groupinfo 孪生)。
//!
//! 红线:对微信数据只读(桥 localdb contacts = 解密副本 SQL 只读);密钥
//! 零沾(本命令不碰 keys.json);取消 = 静默返回零写盘。

use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

use serde_json::{json, Map, Value};
use tauri::AppHandle;
use tauri_plugin_dialog::DialogExt;

/// 可见五桶(wire 值 = 桥 CLI `--type` 词表;system 不出导出面)。
const TYPE_FILTERS: [&str; 5] = ["friend", "group", "official", "former", "other"];

/// 桶 wire 值 → 人话(缺省文件名与 NOTE 类型行;UI 文案判例)。
fn type_label(type_filter: &str) -> &'static str {
    match type_filter {
        "friend" => "好友",
        "group" => "群聊",
        "official" => "公众号",
        "former" => "曾经的好友",
        _ => "其他",
    }
}

/// 导出格式词表(封闭;未知格式 = invalid_params)。
const FORMATS: [&str; 3] = ["json", "csv", "vcf"];

/// 桥 bin 缺省落点(相对用户 home;wechat_groupinfo::BRIDGE_BIN_REL 同一
/// 钉死字面量,组件部署位唯一,漂移即两侧同步)。
const BRIDGE_BIN_REL: &str = ".myia/plugins/wechat-bridge/bin/wechat-bridge";

/// 桥命令帽:600s——`--with-residue` 首跑触发 message 域副本首建(sqlcipher
/// 单库上界 300s,346MB 级;Python sidecar `_QUERY_TIMEOUT_SECONDS` 同值
/// 口径),90s(群信息帽)会误杀首建。
const BRIDGE_TIMEOUT: Duration = Duration::from_secs(600);
/// try_wait 非阻塞轮询步长(wechat_groupinfo 同值孪生)。
const POLL_INTERVAL: Duration = Duration::from_millis(50);
/// 失败兜底 stderr 尾部回显长度(同孪生)。
const STDERR_TAIL_CHARS: usize = 500;

/// vCard 物理行折叠上限(RFC 2426 §2.6:75 octets,续行以单空格起)。
const VCF_FOLD_OCTETS: usize = 75;

/// 错误信封(仓惯例 `{"code","path","message"[,"data"]}` JSON 字符串;前端
/// asSidecarError 同形解析;群导出/群信息同形孪生——私有不跨引,本地保持独立)。
fn error_value(code: &str, message: &str, data: Option<Value>) -> String {
    match data {
        Some(payload) => json!({"code": code, "path": "$", "message": message, "data": payload})
            .to_string(),
        None => json!({"code": code, "path": "$", "message": message}).to_string(),
    }
}

fn invalid_params(path: &str, message: String) -> String {
    json!({"code": "invalid_params", "path": path, "message": message}).to_string()
}

/// stderr 尾部(字符取尾防多字节截半;孪生同形)。
fn stderr_tail(stderr: &str) -> String {
    let chars: Vec<char> = stderr.chars().collect();
    let start = chars.len().saturating_sub(STDERR_TAIL_CHARS);
    chars[start..].iter().collect()
}

/// 可执行文件判定(unix 看执行位;孪生同形)。
#[cfg(unix)]
fn is_executable_file(path: &Path) -> bool {
    use std::os::unix::fs::PermissionsExt;
    path.is_file()
        && std::fs::metadata(path)
            .map(|meta| meta.permissions().mode() & 0o111 != 0)
            .unwrap_or(false)
}
#[cfg(not(unix))]
fn is_executable_file(path: &Path) -> bool {
    path.is_file()
}

/// 桥失败归一(孪生同形):stdout 单 JSON 携 `error{code,message,fix_hint}`
/// → 码名/人话原样透传(fix_hint 进 data);否则 `bridge_error` 兜底。
fn bridge_error_value(exit_code: Option<i32>, stdout: &str, stderr: &str) -> String {
    if let Ok(payload) = serde_json::from_str::<Value>(stdout.trim()) {
        if let Some(error) = payload.get("error").and_then(Value::as_object) {
            let code = error
                .get("code")
                .and_then(Value::as_str)
                .filter(|code| !code.is_empty())
                .unwrap_or("bridge_error");
            let message = error
                .get("message")
                .and_then(Value::as_str)
                .unwrap_or("桥返回失败(无说明)");
            let mut data = Map::new();
            if let Some(hint) = error.get("fix_hint").and_then(Value::as_str) {
                data.insert("fix_hint".into(), json!(hint));
            }
            return error_value(
                code,
                message,
                (!data.is_empty()).then_some(Value::Object(data)),
            );
        }
    }
    error_value(
        "bridge_error",
        &format!(
            "wechat-bridge 组件返回了无法识别的结果(exit={:?});stderr 尾部: {}",
            exit_code,
            stderr_tail(stderr).trim()
        ),
        None,
    )
}

/// 同步跑桥子进程(spawn_blocking 线程;超时 kill 兜底;孪生同形:剥
/// PYTHONPATH + MYIA_HOME 显式尊重/未设注入)。
fn run_bridge_with_deadline(
    bin: &Path,
    argv: &[String],
    myia_home_env: Option<PathBuf>,
    timeout: Duration,
) -> Result<(Option<i32>, String, String), String> {
    use std::io::Read;
    use std::process::{Command, Stdio};
    let mut command = Command::new(bin);
    command
        .args(argv)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .env_remove("PYTHONPATH");
    if let Some(root) = myia_home_env {
        command.env("MYIA_HOME", root);
    }
    let mut child = command.spawn().map_err(|e| {
        error_value(
            "spawn_failed",
            &format!("联系人导出拉起桥失败({}): {}", bin.display(), e),
            None,
        )
    })?;
    let deadline = Instant::now() + timeout;
    let mut stdout_pipe = child.stdout.take();
    let mut stderr_pipe = child.stderr.take();
    loop {
        match child.try_wait() {
            Ok(Some(status)) => {
                let mut stdout_buf = Vec::new();
                let mut stderr_buf = Vec::new();
                if let Some(mut pipe) = stdout_pipe.take() {
                    let _ = pipe.read_to_end(&mut stdout_buf);
                }
                if let Some(mut pipe) = stderr_pipe.take() {
                    let _ = pipe.read_to_end(&mut stderr_buf);
                }
                return Ok((
                    status.code(),
                    String::from_utf8_lossy(&stdout_buf).into_owned(),
                    String::from_utf8_lossy(&stderr_buf).into_owned(),
                ));
            }
            Ok(None) => {}
            Err(e) => {
                return Err(error_value(
                    "bridge_error",
                    &format!("等待桥子进程退出失败: {e}"),
                    None,
                ))
            }
        }
        if Instant::now() >= deadline {
            let _ = child.kill();
            let _ = child.wait();
            return Err(error_value(
                "bridge_timeout",
                &format!("联系人导出桥命令超过 {timeout:?} 未退出,子进程已终止"),
                None,
            ));
        }
        std::thread::sleep(POLL_INTERVAL);
    }
}

/// 桥上下文前置(home/bin 探测 + MYIA_HOME 注入决策;孪生同形,
/// component_missing 同 B5 口径)。
fn resolve_bridge_context(app: &AppHandle) -> Result<(PathBuf, Option<PathBuf>), String> {
    use tauri::Manager;
    let home = app
        .path()
        .home_dir()
        .map_err(|e| error_value("internal_error", &format!("用户 home 目录不可解析: {e}"), None))?;
    let bin = home.join(BRIDGE_BIN_REL);
    if !(bin.is_file() && is_executable_file(&bin)) {
        return Err(error_value(
            "component_missing",
            &format!("微信本机桥组件未安装或不可执行: {}", bin.display()),
            None,
        ));
    }
    let myia_home_env = if std::env::var_os("MYIA_HOME").is_some() {
        None
    } else {
        Some(crate::data_root(app).map_err(|e| {
            error_value("internal_error", &format!("数据根不可解析: {e}"), None)
        })?)
    };
    Ok((bin, myia_home_env))
}

/// 桥 stdout → 成功载荷(exit 0 且无 `error` 键;孪生同判据)。
fn bridge_success_payload(
    exit_code: Option<i32>,
    stdout: &str,
    stderr: &str,
) -> Result<Value, String> {
    let payload: Value = serde_json::from_str(stdout.trim())
        .map_err(|_| bridge_error_value(exit_code, stdout, stderr))?;
    let success = exit_code.unwrap_or(-1) == 0
        && payload.is_object()
        && payload.get("error").map(Value::is_null).unwrap_or(true);
    if success {
        Ok(payload)
    } else {
        Err(bridge_error_value(exit_code, stdout, stderr))
    }
}

/// 桥 argv 组装(纯函数;`--limit 0` = 全量导出态,prd.md:75——三态语义
/// 见桥 contacts_query.normalize_cli_limit,壳侧只发 0 不发页大小)。
fn build_bridge_argv(
    type_filter: &str,
    keyword: Option<&str>,
    with_residue: bool,
) -> Vec<String> {
    let mut argv = vec![
        "localdb".into(),
        "contacts".into(),
        "--type".into(),
        type_filter.into(),
        "--limit".into(),
        "0".into(),
    ];
    if let Some(keyword) = keyword {
        argv.push("--keyword".into());
        argv.push(keyword.into());
    }
    if with_residue {
        argv.push("--with-residue".into());
    }
    argv.push("--json".into());
    argv
}

/// 桥应答 → `contacts.rows` 数组(缺对象/非数组 = 形状漂移结构化报)。
fn contacts_rows(payload: &Value) -> Result<Vec<Value>, String> {
    match payload
        .get("contacts")
        .and_then(|inner| inner.get("rows"))
        .and_then(Value::as_array)
    {
        Some(rows) => Ok(rows.clone()),
        None => Err(error_value(
            "bridge_error",
            "contacts 应答缺 contacts.rows 数组(桥侧形状漂移)",
            None,
        )),
    }
}

/// 文件名净化(群导出同款:路径分隔符/冒号/控制符替 `_`,其余保真)。
fn sanitize_file_name(raw: &str) -> String {
    raw.chars()
        .map(|c| match c {
            '/' | '\\' | ':' => '_',
            c if (c as u32) < 0x20 => '_',
            c => c,
        })
        .collect()
}

/// 缺省基础名(保存对话框):`联系人-<桶人话>-<YYYY-MM-DD>`(扩展名由
/// 所选格式补,对话框 filter 只提示 JSON——三件成套是本命令语义)。
fn default_base_name(type_filter: &str) -> String {
    let date = chrono::Local::now().format("%Y-%m-%d").to_string();
    format!("联系人-{}-{}", type_label(type_filter), date)
}

// ---------------------------------------------------------------------------
// CSV(UTF-8 BOM + 公式注入中和 + RFC 4180;群导出 csv_field 同规孪生)
// ---------------------------------------------------------------------------

/// CSV 表头(R3 钉死八列)。
const CONTACTS_CSV_HEADER: &str =
    "username,display_name,remark,nickname,alias,type,evidence,last_contact_hint";

/// CSV 单元格:公式注入中和先于引号判定(`=` `+` `-` `@` `\t` 开头前置
/// `'`;昵称/备注攻击者可控,OWASP CSV Injection 同款中和)。
fn csv_field(field: &str) -> String {
    let neutralized = match field.chars().next() {
        Some('=' | '+' | '-' | '@' | '\t') => format!("'{field}"),
        _ => field.to_string(),
    };
    if neutralized.contains(',')
        || neutralized.contains('"')
        || neutralized.contains('\n')
        || neutralized.contains('\r')
    {
        format!("\"{}\"", neutralized.replace('"', "\"\""))
    } else {
        neutralized
    }
}

/// 行字段抽取(username 缺行跳过不判错——单行漂移不拦整表)。
struct ContactRecord {
    username: String,
    display_name: String,
    remark: String,
    nickname: String,
    alias: String,
    type_label: String,
    evidence: Vec<String>,
    description: Option<String>,
    member_count: Option<i64>,
}

fn str_field(record: &Map<String, Value>, key: &str) -> String {
    record.get(key).and_then(Value::as_str).unwrap_or("").to_string()
}

fn parse_record(row: &Value) -> Option<ContactRecord> {
    let record = row.as_object()?;
    let username = record.get("username").and_then(Value::as_str)?.to_string();
    let display_name = {
        let display = str_field(record, "display_name");
        if display.trim().is_empty() {
            username.clone() // 真名零虚构:回落寻址键
        } else {
            display
        }
    };
    let evidence = record
        .get("evidence")
        .and_then(Value::as_array)
        .map(|items| {
            items
                .iter()
                .filter_map(Value::as_str)
                .map(str::to_string)
                .collect()
        })
        .unwrap_or_default();
    Some(ContactRecord {
        username,
        display_name,
        remark: str_field(record, "remark"),
        nickname: str_field(record, "nickname"),
        alias: str_field(record, "alias"),
        type_label: str_field(record, "type"),
        evidence,
        description: record
            .get("description")
            .and_then(Value::as_str)
            .filter(|text| !text.trim().is_empty())
            .map(str::to_string),
        member_count: record.get("member_count").and_then(Value::as_i64),
    })
}

fn parse_records(rows: &[Value]) -> Vec<ContactRecord> {
    rows.iter().filter_map(parse_record).collect()
}

/// 联系人表 CSV 文本:BOM + 头行 + 数据行(CRLF;evidence `|` 连接;
/// last_contact_hint ← description)。
fn build_contacts_csv(records: &[ContactRecord]) -> String {
    let mut csv = String::from("\u{feff}");
    csv.push_str(CONTACTS_CSV_HEADER);
    csv.push_str("\r\n");
    for record in records {
        let evidence_joined = record.evidence.join("|");
        let cells = [
            record.username.as_str(),
            record.display_name.as_str(),
            record.remark.as_str(),
            record.nickname.as_str(),
            record.alias.as_str(),
            record.type_label.as_str(),
            evidence_joined.as_str(),
            record.description.as_deref().unwrap_or(""),
        ];
        let escaped: Vec<String> = cells.iter().map(|cell| csv_field(cell)).collect();
        csv.push_str(&escaped.join(","));
        csv.push_str("\r\n");
    }
    csv
}

// ---------------------------------------------------------------------------
// VCF(vCard 3.0 自写序列化:CRLF + RFC 2426 折叠/转义)
// ---------------------------------------------------------------------------

/// vCard 文本转义(RFC 2426 §4:`\` `,` `;` 换行;换行 → 字面 `\n`)。
fn vcf_escape(text: &str) -> String {
    let mut out = String::with_capacity(text.len());
    for ch in text.chars() {
        match ch {
            '\\' => out.push_str("\\\\"),
            ',' => out.push_str("\\,"),
            ';' => out.push_str("\\;"),
            '\n' => out.push_str("\\n"),
            '\r' => {}
            _ => out.push(ch),
        }
    }
    out
}

/// 单逻辑行 → 物理行折叠(≤75 octets,续行单空格起;多字节字符不切半——
/// 按字节推进,边界落在字符中间时回退到 char boundary)。
fn vcf_fold_line(line: &str) -> String {
    let bytes = line.as_bytes();
    if bytes.len() <= VCF_FOLD_OCTETS {
        return format!("{line}\r\n");
    }
    let mut out = String::new();
    let mut start = 0usize;
    let mut budget = VCF_FOLD_OCTETS;
    let mut first = true;
    while start < bytes.len() {
        let mut end = (start + budget).min(bytes.len());
        // 续行预算少 1(行首折叠空格占位)
        while end < bytes.len() && !line.is_char_boundary(end) {
            end -= 1;
        }
        let chunk = &line[start..end];
        if first {
            out.push_str(chunk);
            first = false;
        } else {
            out.push_str("\r\n ");
            out.push_str(chunk);
        }
        start = end;
        budget = VCF_FOLD_OCTETS - 1;
        // 极端:0 预算护(不可达,75>1;防死循环兜底)
        if budget == 0 {
            break;
        }
    }
    out.push_str("\r\n");
    out
}

/// evidence wire 值 → 人话(R3:「会话痕迹」「仅残留」;identity_fields →
/// 「身份字段残留」——附加证据位)。
fn evidence_label(evidence: &[String]) -> &'static str {
    if evidence.iter().any(|item| item == "msg_residue") {
        "会话痕迹"
    } else if evidence.iter().any(|item| item == "identity_fields") {
        "身份字段残留"
    } else {
        "仅残留"
    }
}

/// 单联系人 → vCard 3.0 文本(FN/N/NICKNAME/X-WECHAT-ID/NOTE;群聊行
/// member_count 入 NOTE)。
fn build_vcard(record: &ContactRecord) -> String {
    let mut card = String::new();
    card.push_str(&vcf_fold_line("BEGIN:VCARD"));
    card.push_str(&vcf_fold_line("VERSION:3.0"));
    card.push_str(&vcf_fold_line(&format!("FN:{}", vcf_escape(&record.display_name))));
    // N 结构位:未知结构不臆拆,全名进家名位(四空组件补齐)
    card.push_str(&vcf_fold_line(&format!(
        "N:{};;;;",
        vcf_escape(&record.display_name)
    )));
    if !record.nickname.trim().is_empty() {
        card.push_str(&vcf_fold_line(&format!(
            "NICKNAME:{}",
            vcf_escape(&record.nickname)
        )));
    }
    card.push_str(&vcf_fold_line(&format!(
        "X-WECHAT-ID:{}",
        vcf_escape(&record.username)
    )));
    // NOTE 收纳:类型/证据/别名/描述(+群成员数)——人话标签行,行间以
    // 字面 \n 转义(vCard 文本换行形态)
    let type_text = if record.type_label.trim().is_empty() {
        "其他".to_string()
    } else {
        type_label(&record.type_label).to_string()
    };
    let mut note = format!("类型:{type_text}\n证据:{}", evidence_label(&record.evidence));
    if !record.alias.trim().is_empty() {
        note.push_str("\n别名:");
        note.push_str(&record.alias);
    }
    if let Some(description) = &record.description {
        note.push_str("\n描述:");
        note.push_str(description);
    }
    if let Some(member_count) = record.member_count {
        note.push_str(&format!("\n群成员数:{member_count}"));
    }
    card.push_str(&vcf_fold_line(&format!("NOTE:{}", vcf_escape(&note))));
    card.push_str(&vcf_fold_line("END:VCARD"));
    card
}

/// 联系人集 → VCF 全文(每联系人一卡片)。
fn build_contacts_vcf(records: &[ContactRecord]) -> String {
    let mut vcf = String::new();
    for record in records {
        vcf.push_str(&build_vcard(record));
    }
    vcf
}

// ---------------------------------------------------------------------------
// 落盘(0600)+ 回执
// ---------------------------------------------------------------------------

/// 单导出件(回执行;name = 文件名,path = 绝对路径,rows = 数据行数)。
#[derive(Debug)]
struct ExportedFile {
    name: String,
    path: String,
    rows: usize,
}

/// 写文件并收紧权限 0600(chatlog-keeper private_text_writer 语义;unix
/// set_permissions,非 unix 家族照写不设位——平台差异如实)。
fn write_private_file(path: &Path, body: &str) -> Result<(), String> {
    std::fs::write(path, body).map_err(|err| {
        error_value(
            "export_failed",
            &format!("导出件写入失败({}): {err}", path.display()),
            None,
        )
    })?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let _ = std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o600));
    }
    Ok(())
}

/// 保存对话框所选路径 → 三格式基础名(`<所选>.json/.csv/.vcf`;所选路径
/// 的末段扩展名剥掉作基础名——对话框 filter 提示 JSON,用户带不带扩展名
/// 都归一到基础名形态)。
fn base_from_picked(picked: &Path) -> PathBuf {
    picked.with_extension("")
}

/// 对话框结果 + 桥 rows → 三件落盘(纯接缝,cargo 测试直驱)。
///
/// `None`(用户取消)= `Ok(None)` 静默零写盘;`Some(path)` = 按 formats
/// 子集落盘(顺序 = 调用方给定;JSON 行数 = rows 原长,CSV/VCF 行数 =
/// 可解析行数——username 缺行跳过不拦整表)。已落盘件不因后续件失败回滚
/// (对用户数据零删除纪律,失败如实上屏哪件没成)。
fn finish_contacts_export(
    picked: Option<PathBuf>,
    rows: &[Value],
    formats: &[String],
) -> Result<Option<(Vec<ExportedFile>, usize)>, String> {
    let Some(picked) = picked else {
        return Ok(None);
    };
    let base = base_from_picked(&picked);
    let records = parse_records(rows);
    let mut files: Vec<ExportedFile> = Vec::new();
    for format in formats {
        let path = base.with_extension(format);
        let body = match format.as_str() {
            "json" => {
                let mut body = serde_json::to_string_pretty(&Value::Array(rows.to_vec()))
                    .map_err(|err| {
                        error_value(
                            "export_failed",
                            &format!("联系人 JSON 序列化失败: {err}"),
                            None,
                        )
                    })?;
                body.push('\n');
                body
            }
            "csv" => build_contacts_csv(&records),
            "vcf" => build_contacts_vcf(&records),
            other => {
                return Err(invalid_params(
                    "$.formats",
                    format!("未知导出格式 {other:?}(合法:json/csv/vcf)"),
                ))
            }
        };
        write_private_file(&path, &body)?;
        files.push(ExportedFile {
            name: path
                .file_name()
                .map(|name| name.to_string_lossy().into_owned())
                .unwrap_or_default(),
            path: path.display().to_string(),
            rows: if format == "json" {
                rows.len()
            } else {
                records.len()
            },
        });
    }
    Ok(Some((files, rows.len())))
}

fn export_receipt(files: Vec<ExportedFile>, total_rows: usize) -> Value {
    json!({
        "files": files
            .into_iter()
            .map(|file| json!({"name": file.name, "path": file.path, "rows": file.rows}))
            .collect::<Vec<Value>>(),
        "total_rows": total_rows,
    })
}

/// 联系人三格式导出(R3;工作台「导出当前筛选」唯一通道):保存对话框定
/// 基础名 → spawn 安装态桥全量查询(`--limit 0`)→ 三格式同基础名落盘
/// (0600)。应答 `null` = 用户取消(前端静默);对象 = 回执;throw = 失败
/// (桥错误族 20/21/22 原样透传,前端结构化直显)。
#[tauri::command]
pub async fn wechat_contacts_export(
    app: AppHandle,
    type_filter: String,
    keyword: Option<String>,
    with_residue: Option<bool>,
    formats: Vec<String>,
) -> Result<Option<Value>, String> {
    let type_filter = type_filter.trim().to_string();
    if !TYPE_FILTERS.contains(&type_filter.as_str()) {
        return Err(invalid_params(
            "$.typeFilter",
            format!(
                "typeFilter 须为 {} 之一,当前为 {type_filter:?}",
                TYPE_FILTERS.join("/")
            ),
        ));
    }
    if formats.is_empty() {
        return Err(invalid_params("$.formats", "formats 不能为空(json/csv/vcf 至少选一)".into()));
    }
    for format in &formats {
        if !FORMATS.contains(&format.as_str()) {
            return Err(invalid_params(
                "$.formats",
                format!("未知导出格式 {format:?}(合法:json/csv/vcf)"),
            ));
        }
    }
    let keyword = keyword
        .map(|value| value.trim().to_string())
        .filter(|value| !value.is_empty());
    let with_residue = with_residue.unwrap_or(false);

    let (bin, myia_home_env) = resolve_bridge_context(&app)?;

    // ① 保存对话框(spawn_blocking 线程;取消 = None 静默零写盘)
    let default_file_name = format!("{}.json", default_base_name(&type_filter));
    let dialog_app = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        dialog_app
            .dialog()
            .file()
            .set_file_name(&default_file_name)
            .add_filter("JSON", &["json"])
            .blocking_save_file()
            .map(|file| file.into_path())
    });
    let picked = joined
        .await
        .map_err(|err| error_value("internal_error", &format!("导出保存对话框线程失败: {err}"), None))?;
    let picked = match picked {
        None => None,
        Some(Ok(path)) => Some(path),
        Some(Err(err)) => {
            return Err(error_value("export_failed", &format!("保存路径不可用: {err}"), None))
        }
    };
    let Some(picked) = picked else {
        log::info!("联系人导出:用户取消保存对话框(type={type_filter}),静默返回零写盘");
        return Ok(None);
    };

    // ② 桥全量查询(--limit 0 = 全量导出态;residue 首跑可能触发 message
    // 域副本首建,600s 帽承接,「考古中…」态由前端如实呈现)
    let argv = build_bridge_argv(&type_filter, keyword.as_deref(), with_residue);
    let bridge_bin = bin.clone();
    let bridge_home = myia_home_env.clone();
    let bridge_argv = argv.clone();
    let joined =
        tauri::async_runtime::spawn_blocking(move || {
            run_bridge_with_deadline(&bridge_bin, &bridge_argv, bridge_home, BRIDGE_TIMEOUT)
        });
    let (exit_code, stdout, stderr) = match joined.await {
        Ok(Ok(outcome)) => outcome,
        Ok(Err(error)) => return Err(error),
        Err(err) => {
            return Err(error_value(
                "internal_error",
                &format!("联系人导出桥命令线程失败: {err}"),
                None,
            ))
        }
    };
    let payload = bridge_success_payload(exit_code, &stdout, &stderr)?;
    let rows = contacts_rows(&payload)?;

    // ③ 三格式落盘 + 回执(内容零入日志)
    let (files, total_rows) =
        finish_contacts_export(Some(picked), &rows, &formats)?.expect("Some 路径必返回 Some");
    log::info!(
        "联系人导出:{} 件落盘 type={} rows={} keyword={:?} residue={}",
        files.len(),
        type_filter,
        total_rows,
        keyword,
        with_residue
    );
    Ok(Some(export_receipt(files, total_rows)))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::tempdir;

    /// 契约夹具(桥 contacts.rows 行形状;全合成)。
    fn rows_fixture() -> Vec<Value> {
        vec![
            json!({
                "username": "wxid_friend_a",
                "display_name": "好友A",
                "remark": "备注A",
                "nickname": "好友A",
                "alias": "alias_a",
                "type": "friend",
                "local_type": 1,
                "evidence": [],
                "description": "同事"
            }),
            json!({
                "username": "wxid_former_b",
                "display_name": "旧友B",
                "remark": "",
                "nickname": "旧友B",
                "alias": "alias_b",
                "type": "former",
                "local_type": 3,
                "evidence": ["msg_residue", "identity_fields"],
                "description": null
            }),
            json!({
                "username": "44782403251@chatroom",
                "display_name": "合成群A",
                "remark": "",
                "nickname": "合成群A",
                "alias": "",
                "type": "group",
                "local_type": 2,
                "evidence": [],
                "description": null,
                "member_count": 3
            }),
            json!({
                "username": "wxid_former_c",
                "display_name": "旧友C",
                "remark": "",
                "nickname": "旧友C",
                "alias": "",
                "type": "former",
                "local_type": 3,
                "evidence": [],
                "description": null
            }),
        ]
    }

    /// 三件成套:JSON 可解析回 rows 原形;CSV 头行 + 数据行 + BOM;
    /// VCF 卡片数 = 行数。
    #[test]
    fn export_writes_three_formats_same_base() {
        let dir = tempdir().unwrap();
        let rows = rows_fixture();
        let (files, total) = finish_contacts_export(
            Some(dir.path().join("联系人-好友-2026-10-14.json")),
            &rows,
            &["json".to_string(), "csv".to_string(), "vcf".to_string()],
        )
        .unwrap()
        .unwrap();
        assert_eq!(total, 4);
        assert_eq!(files.len(), 3);
        assert_eq!(files[0].name, "联系人-好友-2026-10-14.json");
        assert_eq!(files[1].name, "联系人-好友-2026-10-14.csv");
        assert_eq!(files[2].name, "联系人-好友-2026-10-14.vcf");
        // JSON 原形直写(pretty 再解析回等值)
        let written: Value = serde_json::from_str(
            &fs::read_to_string(dir.path().join("联系人-好友-2026-10-14.json")).unwrap(),
        )
        .unwrap();
        assert_eq!(written, Value::Array(rows.clone()));
        // CSV:头行 + 4 数据行;BOM 专项测试另断言
        let csv = fs::read_to_string(dir.path().join("联系人-好友-2026-10-14.csv")).unwrap();
        let lines: Vec<&str> = csv.lines().collect();
        assert_eq!(lines.len(), 5);
        assert_eq!(lines[0], format!("\u{feff}{CONTACTS_CSV_HEADER}"));
        assert!(lines[1].starts_with("wxid_friend_a,好友A,备注A,好友A,alias_a,friend,,同事"));
        assert!(lines[2].contains("msg_residue|identity_fields"));
        // VCF:4 卡片
        let vcf = fs::read_to_string(dir.path().join("联系人-好友-2026-10-14.vcf")).unwrap();
        assert_eq!(vcf.matches("BEGIN:VCARD").count(), 4);
        assert_eq!(vcf.matches("END:VCARD").count(), 4);
    }

    /// 对话框取消(seam None)= 静默返回,零写盘。
    #[test]
    fn dialog_cancel_returns_silently_without_writes() {
        let dir = tempdir().unwrap();
        let outcome = finish_contacts_export(None, &rows_fixture(), &["json".to_string()]).unwrap();
        assert!(outcome.is_none());
        assert_eq!(fs::read_dir(dir.path()).unwrap().count(), 0, "取消零写盘");
    }

    /// CSV BOM:首三字节 EF BB BF(Excel 直开中文不乱码)。
    #[test]
    fn csv_carries_utf8_bom() {
        let csv = build_contacts_csv(&parse_records(&rows_fixture()));
        let bytes = csv.as_bytes();
        assert_eq!(&bytes[..3], &[0xEF, 0xBB, 0xBF]);
    }

    /// 公式注入中和(群导出同规):`=+-@`/tab 开头前置 `'`;普通单元格零改形。
    #[test]
    fn csv_neutralizes_formula_prefix_cells() {
        assert_eq!(csv_field("=HYPERLINK(\"http://x\")"), "\"'=HYPERLINK(\"\"http://x\"\")\"");
        assert_eq!(csv_field("+1+1"), "'+1+1");
        assert_eq!(csv_field("-x"), "'-x");
        assert_eq!(csv_field("@import"), "'@import");
        assert_eq!(csv_field("\t跳格开头"), "'\t跳格开头");
        assert_eq!(csv_field("好友A"), "好友A");
        assert_eq!(csv_field(""), "");
        // 攻击载荷整链落盘:公式原样不得出现在行首
        let rows = vec![json!({
            "username": "wxid_evil", "display_name": "=cmd|' /C calc'!A0",
            "remark": "", "nickname": "", "alias": "", "type": "friend",
            "evidence": [], "description": null
        })];
        let csv = build_contacts_csv(&parse_records(&rows));
        assert!(csv.contains("'=cmd|"), "{csv}");
        assert!(!csv.contains("\r\n=cmd|"), "{csv}");
    }

    /// VCF 内容:FN/N/NICKNAME/X-WECHAT-ID/NOTE 在场;evidence 人话
    /// (会话痕迹/仅残留);群行成员数入 NOTE;CRLF 行尾。
    #[test]
    fn vcf_fields_and_note_semantics() {
        let records = parse_records(&rows_fixture());
        let vcf = build_contacts_vcf(&records);
        assert!(vcf.contains("FN:好友A\r\n"));
        assert!(vcf.contains("N:好友A;;;;\r\n"));
        assert!(vcf.contains("NICKNAME:好友A\r\n"));
        assert!(vcf.contains("X-WECHAT-ID:wxid_friend_a\r\n"));
        // NOTE:类型/证据/别名/描述人话标签(换行 = 字面 \n 转义)
        assert!(vcf.contains("NOTE:类型:好友\\n证据:仅残留\\n别名:alias_a\\n描述:同事\r\n"));
        assert!(vcf.contains("证据:会话痕迹"));
        // 群行:成员数入 NOTE
        assert!(vcf.contains("群成员数:3"));
        // display_name 空白回落 username(真名零虚构)
        let rows = vec![json!({
            "username": "wxid_bare", "display_name": "", "remark": "", "nickname": "",
            "alias": "", "type": "friend", "evidence": [], "description": null
        })];
        let vcf = build_contacts_vcf(&parse_records(&rows));
        assert!(vcf.contains("FN:wxid_bare"));
        // nickname 缺席(空)不产 NICKNAME 行
        assert!(!vcf.contains("NICKNAME"));
    }

    /// VCF 转义:逗号/分号/反斜杠/换行昵称夹具(RFC 2426)。
    #[test]
    fn vcf_escapes_special_characters() {
        let rows = vec![json!({
            "username": "wxid_special", "display_name": "名,字;半\\角",
            "remark": "", "nickname": "两\n行", "alias": "", "type": "friend",
            "evidence": [], "description": "描;述,值"
        })];
        let vcf = build_contacts_vcf(&parse_records(&rows));
        assert!(vcf.contains("FN:名\\,字\\;半\\\\角\r\n"));
        assert!(vcf.contains("NICKNAME:两\\n行\r\n"));
        // description「描;述,值」→ NOTE 内转义为「描\;述\,值」
        assert!(vcf.contains("描述:描\\;述\\,值"));
    }

    /// VCF 折叠:长 NOTE 超 75 octets 折为多物理行(续行单空格起),
    /// 拼回(去 CRLF+空格)无损;多字节字符不切半(拼回合法 UTF-8)。
    #[test]
    fn vcf_folds_long_lines_at_75_octets() {
        let long_description = "很长的描述行".repeat(40); // 5 chars × 40 × 3 bytes = 600 字节
        let rows = vec![json!({
            "username": "wxid_long", "display_name": "长描述联系人",
            "remark": "", "nickname": "", "alias": "", "type": "friend",
            "evidence": [], "description": long_description
        })];
        let vcf = build_contacts_vcf(&parse_records(&rows));
        for physical in vcf.split("\r\n") {
            assert!(
                physical.len() <= VCF_FOLD_OCTETS,
                "物理行超 75 octets: {physical}"
            );
        }
        // 拼回无损:去续行空格前缀,描述原文完整在场
        let unfolded = vcf.replace("\r\n ", "");
        assert!(unfolded.contains(&format!("描述:{long_description}")));
        // 字符串整体仍是合法 UTF-8(未切半;from_utf8 直验)
        assert!(std::str::from_utf8(vcf.as_bytes()).is_ok());
    }

    /// 导出件权限 0600(unix)。
    #[test]
    fn exported_files_are_private_0600() {
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            let dir = tempdir().unwrap();
            let (files, _) = finish_contacts_export(
                Some(dir.path().join("contacts.json")),
                &rows_fixture(),
                &["json".to_string(), "csv".to_string(), "vcf".to_string()],
            )
            .unwrap()
            .unwrap();
            for file in files {
                let mode = fs::metadata(&file.path).unwrap().permissions().mode();
                assert_eq!(mode & 0o777, 0o600, "{} 应为 0600", file.path);
            }
        }
    }

    /// 基础名推导:带/不带扩展名的所选路径都归一到基础名(三件同基名)。
    #[test]
    fn base_from_picked_strips_extension() {
        assert_eq!(
            base_from_picked(Path::new("/tmp/联系人-好友-2026-10-14.json")),
            Path::new("/tmp/联系人-好友-2026-10-14")
        );
        assert_eq!(
            base_from_picked(Path::new("/tmp/联系人-好友")),
            Path::new("/tmp/联系人-好友")
        );
    }

    /// 桥 argv 组装:`--limit 0` 全量 + keyword/residue 旗标按需。
    #[test]
    fn bridge_argv_full_export_semantics() {
        let argv = build_bridge_argv("former", Some("张"), true);
        assert_eq!(
            argv,
            vec![
                "localdb", "contacts", "--type", "former", "--limit", "0",
                "--keyword", "张", "--with-residue", "--json"
            ]
        );
        let argv = build_bridge_argv("friend", None, false);
        assert!(!argv.contains(&"--with-residue".to_string()));
        assert!(!argv.contains(&"--keyword".to_string()));
        assert!(argv.contains(&"0".to_string()), "--limit 0 全量导出态必在");
    }

    /// 桥应答守门:缺 contacts.rows = 形状漂移结构化报;错误族透传。
    #[test]
    fn bridge_payload_gates_rows() {
        let rows = contacts_rows(&json!({"contacts": {"rows": [{"username": "x"}]}})).unwrap();
        assert_eq!(rows.len(), 1);
        assert!(contacts_rows(&json!({"contacts": {}})).is_err());
        assert!(contacts_rows(&json!({})).is_err());
        let named = bridge_success_payload(
            Some(21),
            "{\"error\": {\"code\": \"key_unavailable\", \"message\": \"密钥缺位\", \"fix_hint\": \"先取钥\"}}",
            "",
        )
        .unwrap_err();
        assert!(named.contains("\"code\":\"key_unavailable\""), "{named}");
    }

    /// 未知格式拒(invalid_params);零写盘前拒。
    #[test]
    fn unknown_format_rejected() {
        let dir = tempdir().unwrap();
        let err = finish_contacts_export(
            Some(dir.path().join("x.json")),
            &rows_fixture(),
            &["pdf".to_string()],
        )
        .unwrap_err();
        assert!(err.contains("invalid_params"), "{err}");
        assert_eq!(fs::read_dir(dir.path()).unwrap().count(), 0);
    }
}
