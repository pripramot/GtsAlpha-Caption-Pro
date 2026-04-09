use serde::{Deserialize, Serialize};
use tauri::command;

// ── Data models ──────────────────────────────────────────────────────────────

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct CaptionLine {
    pub start: f64,
    pub duration: f64,
    pub text: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AppConfig {
    pub output_dir: String,
    pub default_lang: String,
    pub ollama_host: String,
    pub ollama_port: u16,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            output_dir: dirs_next(),
            default_lang: "th".to_string(),
            ollama_host: "127.0.0.1".to_string(),
            ollama_port: 11434,
        }
    }
}

fn dirs_next() -> String {
    std::env::var("HOME")
        .or_else(|_| std::env::var("USERPROFILE"))
        .unwrap_or_else(|_| ".".to_string())
}

// ── Tauri commands ────────────────────────────────────────────────────────────

/// Return the application version from Cargo.toml
#[command]
pub fn get_app_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

/// Return default application configuration
#[command]
pub fn get_default_config() -> AppConfig {
    AppConfig::default()
}

/// Validate a YouTube or X/Twitter URL
#[command]
pub fn validate_url(url: String) -> Result<String, String> {
    let url = url.trim().to_string();
    if url.is_empty() {
        return Err("URL ว่างเปล่า กรุณาใส่ลิงก์".to_string());
    }
    if url.contains("youtube.com/watch")
        || url.contains("youtu.be/")
        || url.contains("twitter.com/")
        || url.contains("x.com/")
    {
        Ok(url)
    } else {
        Err("URL ไม่รองรับ รองรับเฉพาะ YouTube และ X/Twitter".to_string())
    }
}

/// Extract video ID from a YouTube URL
#[command]
pub fn extract_video_id(url: String) -> Result<String, String> {
    let url = url.trim();

    // youtu.be/<id>
    if let Some(pos) = url.find("youtu.be/") {
        let after = &url[pos + 9..];
        let id = after.split(['?', '&', '/']).next().unwrap_or("");
        if !id.is_empty() {
            return Ok(id.to_string());
        }
    }

    // youtube.com/watch?v=<id>
    if url.contains("youtube.com/watch") {
        for param in url.split('?').nth(1).unwrap_or("").split('&') {
            if let Some(v) = param.strip_prefix("v=") {
                let id = v.split('&').next().unwrap_or(v);
                if !id.is_empty() {
                    return Ok(id.to_string());
                }
            }
        }
    }

    Err("ไม่พบ Video ID ใน URL นี้".to_string())
}

/// Check if the Ollama service is reachable
#[command]
pub async fn check_ollama_status(host: String, port: u16) -> bool {
    let url = format!("http://{}:{}/api/tags", host, port);
    let client = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(3))
        .build()
        .unwrap_or_default();
    client.get(&url).send().await.map(|r| r.status().is_success()).unwrap_or(false)
}

/// List available Ollama models
#[command]
pub async fn list_ollama_models(host: String, port: u16) -> Result<Vec<String>, String> {
    let url = format!("http://{}:{}/api/tags", host, port);
    let client = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(5))
        .build()
        .map_err(|e| e.to_string())?;

    let resp = client
        .get(&url)
        .send()
        .await
        .map_err(|_| "ไม่สามารถเชื่อมต่อ Ollama ได้ กรุณาตรวจสอบว่า Ollama กำลังรันอยู่".to_string())?;

    let body: serde_json::Value = resp.json().await.map_err(|e| e.to_string())?;
    let models = body["models"]
        .as_array()
        .map(|arr| {
            arr.iter()
                .filter_map(|m| m["name"].as_str().map(str::to_string))
                .collect()
        })
        .unwrap_or_default();

    Ok(models)
}

// ── Entry point ───────────────────────────────────────────────────────────────

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_http::init())
        .invoke_handler(tauri::generate_handler![
            get_app_version,
            get_default_config,
            validate_url,
            extract_video_id,
            check_ollama_status,
            list_ollama_models,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
