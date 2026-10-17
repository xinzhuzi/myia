//! Per-file asset grants for persisted feed images. No arbitrary file read command.
//! 双授权根(10-16-feed-wx-images Phase 2):`images/`(视觉管线持久化图)+
//! `wechat-localdb/media-cache/`(微信本地库解密图,Phase 1 产物)。
use std::io::Read;
use std::path::{Component, Path, PathBuf};
use tauri::{AppHandle, Manager};

/// 授权根相对数据根的词面路径(images/ + wechat-localdb/media-cache/)。
/// 根自身 canonicalize 后必须仍等于词面路径 —— 授权目录被符号链接指向
/// 数据根外时整根失效(沿用 images 根既有守卫)。
const AUTHORIZED_ROOTS: [&str; 2] = ["images", "wechat-localdb/media-cache"];

fn authorized_image(data_root: &Path, input: &Path) -> Result<PathBuf, String> {
    if !input.is_absolute() || input.components().any(|part| part == Component::ParentDir) {
        return Err("图片路径必须是数据根内的绝对路径".into());
    }
    let root = data_root.canonicalize().map_err(|_| "应用数据目录不可用")?;
    let file = input.canonicalize().map_err(|_| "图片已移动或不存在")?;
    if !file.is_file() {
        return Err("仅可预览应用已保存的图片".into());
    }
    let mut root_seen = false;
    let mut confined = false;
    for relative in AUTHORIZED_ROOTS {
        let expected = root.join(relative);
        if let Ok(actual) = expected.canonicalize() {
            root_seen = true;
            if actual == expected && file.starts_with(&actual) {
                confined = true;
                break;
            }
        }
    }
    if !root_seen {
        return Err("尚无已保存图片".into());
    }
    if !confined {
        return Err("仅可预览应用已保存的图片".into());
    }
    let extension = file.extension().and_then(|v| v.to_str()).unwrap_or("");
    // wxgf(微信实况容器)后缀放行但不在下方魔数白名单 → 天然拒授权,
    // UI 侧降级占位,如实呈现。
    if !matches!(extension, "png" | "jpg" | "jpeg" | "gif" | "webp" | "wxgf") {
        return Err("该文件格式不支持预览".into());
    }
    let mut head = [0; 12];
    let count = std::fs::File::open(&file)
        .and_then(|mut source| source.read(&mut head))
        .map_err(|_| "图片不可读取")?;
    let head = &head[..count];
    if !(head.starts_with(b"\x89PNG\r\n\x1a\n")
        || head.starts_with(b"\xff\xd8\xff")
        || head.starts_with(b"GIF87a")
        || head.starts_with(b"GIF89a")
        || (head.starts_with(b"RIFF") && head.get(8..12) == Some(b"WEBP")))
    {
        return Err("文件内容不是支持的图片".into());
    }
    Ok(file)
}

#[tauri::command]
pub async fn feed_image_path(app: AppHandle, path: String) -> Result<String, String> {
    let root = crate::data_root(&app).map_err(|_| "应用数据目录不可用")?;
    let file =
        tauri::async_runtime::spawn_blocking(move || authorized_image(&root, Path::new(&path)))
            .await
            .map_err(|_| "图片路径校验失败")??;
    let path = file.to_str().ok_or("图片路径编码不可用")?.to_owned();
    // allow_file uses escaped glob patterns; special directory names cannot widen scope.
    app.asset_protocol_scope()
        .allow_file(&file)
        .map_err(|_| "图片授权失败")?;
    Ok(path)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    fn fixture() -> (tempfile::TempDir, PathBuf) {
        let dir = tempfile::tempdir().unwrap();
        let images = dir.path().join("images");
        fs::create_dir(&images).unwrap();
        let path = images.join("image.png");
        fs::write(&path, b"\x89PNG\r\n\x1a\nfixture").unwrap();
        (dir, path)
    }

    #[test]
    fn permits_only_existing_images_under_current_root() {
        let (root, image) = fixture();
        assert_eq!(
            authorized_image(root.path(), &image).unwrap(),
            image.canonicalize().unwrap()
        );
        assert!(authorized_image(root.path(), &root.path().join("images/missing.png")).is_err());
        assert!(authorized_image(root.path(), Path::new("images/image.png")).is_err());
        assert!(
            authorized_image(root.path(), &root.path().join("images/../images/image.png")).is_err()
        );
        assert!(authorized_image(root.path(), &root.path().join("images")).is_err());
    }

    #[test]
    fn rejects_outside_paths_unsupported_suffix_and_disguised_text() {
        let (root, _) = fixture();
        let outside = root.path().join("secret.png");
        fs::write(&outside, b"\x89PNG\r\n\x1a\nsecret").unwrap();
        assert!(authorized_image(root.path(), &outside).is_err());
        let text = root.path().join("images/text.png");
        fs::write(&text, b"private text").unwrap();
        assert!(authorized_image(root.path(), &text).is_err());
        let svg = root.path().join("images/image.svg");
        fs::write(&svg, b"<svg/>").unwrap();
        assert!(authorized_image(root.path(), &svg).is_err());
    }

    fn media_fixture() -> (tempfile::TempDir, PathBuf) {
        let dir = tempfile::tempdir().unwrap();
        let media = dir.path().join("wechat-localdb").join("media-cache");
        fs::create_dir_all(&media).unwrap();
        let path = media.join("decrypted.jpg");
        fs::write(&path, b"\xff\xd8\xff\xe0media fixture").unwrap();
        (dir, path)
    }

    #[test]
    fn permits_wechat_media_cache_images_and_rejects_wxgf_payloads() {
        let (root, image) = media_fixture();
        assert_eq!(
            authorized_image(root.path(), &image).unwrap(),
            image.canonicalize().unwrap()
        );
        // wxgf 实况容器:后缀放行、魔数不在白名单 → 拒授权(UI 降级占位)
        let live = image.parent().unwrap().join("moment.wxgf");
        fs::write(&live, b"wxgf-live-photo-bytes").unwrap();
        assert!(authorized_image(root.path(), &live).is_err());
        // png 解密产物同门放行(魔数核对)
        let png = image.parent().unwrap().join("photo.png");
        fs::write(&png, b"\x89PNG\r\n\x1a\nmedia fixture").unwrap();
        assert!(authorized_image(root.path(), &png).is_ok());
    }

    #[test]
    fn rejects_wechat_paths_outside_media_cache_root() {
        let (root, image) = media_fixture();
        // 同在 wechat-localdb/ 下但不在 media-cache/ 内(如桥自身库件)
        let sibling = image.parent().unwrap().parent().unwrap().join("session.db.jpg");
        fs::write(&sibling, b"\xff\xd8\xff\xe0sibling").unwrap();
        assert!(authorized_image(root.path(), &sibling).is_err());
        // 数据根外任意合法图片(另一临时根)
        let elsewhere = tempfile::tempdir().unwrap();
        let external = elsewhere.path().join("external.jpg");
        fs::write(&external, b"\xff\xd8\xff\xe0external").unwrap();
        assert!(authorized_image(root.path(), &external).is_err());
    }

    #[cfg(unix)]
    #[test]
    fn rejects_file_and_images_root_symlink_escape() {
        use std::os::unix::fs::symlink;
        let (root, image) = fixture();
        let other = tempfile::tempdir().unwrap();
        let link = root.path().join("images/escape.png");
        let external = other.path().join("external.png");
        fs::copy(&image, &external).unwrap();
        symlink(&external, &link).unwrap();
        assert!(authorized_image(root.path(), &link).is_err());
        let alternate = tempfile::tempdir().unwrap();
        symlink(image.parent().unwrap(), alternate.path().join("images")).unwrap();
        assert!(authorized_image(alternate.path(), &image).is_err());
        // media-cache 根符号链接逃逸同门:根指向数据根外 → 该根失效
        let media = tempfile::tempdir().unwrap();
        fs::create_dir_all(media.path().join("wechat-localdb")).unwrap();
        let outside_media = other.path().join("real-media");
        fs::create_dir(&outside_media).unwrap();
        fs::write(
            outside_media.join("stolen.jpg"),
            b"\xff\xd8\xff\xe0stolen media",
        )
        .unwrap();
        symlink(&outside_media, media.path().join("wechat-localdb/media-cache")).unwrap();
        assert!(
            authorized_image(media.path(), &outside_media.join("stolen.jpg")).is_err()
        );
    }
}
