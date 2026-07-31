// iframe領域へのフォーカス（足踏み・クリック）を監視するサイレントフック
let iframeEntered = false;

window.addEventListener('blur', function() {
  if (document.activeElement && document.activeElement.tagName === 'IFRAME') {
    const timestamp = new Date().toISOString();
    console.log(`[SILENT DETECT] 誰かがiframe領域を踏みました | Time: ${timestamp}`);
    
    // ログデータとして保存（history_logへ追加可能）
    window.lastIframeAccess = {
      event: "IFRAME_FOOTPRINT_DETECTED",
      time: timestamp,
      target: document.activeElement.src || "unknown_src"
    };

    // サーバーやバックエンドへサイレント送信するフック領域
    if (typeof fetch !== 'undefined') {
      fetch('/api/telemetry/footprint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(window.lastIframeAccess)
      }).catch(() => {}); // サイレント処理のためエラーは無視
    }
  }
});
