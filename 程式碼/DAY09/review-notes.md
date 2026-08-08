# ChatGPT 初篩演練的人工複核筆記

這份檔案不是可直接合併的審查結論，也不代表某次真實的 ChatGPT 對話。表格故意安排找到、誤報與漏報，用來保存文章示範的複核流程與證據種類；實際重跑 `review-prompt.txt` 時，結果可能不同。

| 演練項目 | 分類 | 人工複核 | 證據／處理 |
|---|---|---|---|
| `workspaceId.isBlank()` 在 null 輸入會先拋出 `NullPointerException` | 確定問題 | 接受 | JUnit 5 以 null 重現；修正後統一拋 `IllegalArgumentException` |
| `contains` 與 `add` 分開執行，兩個排程可能都回傳 `true` | 確定問題 | 接受，但不採用「同步整個方法」的過度修正 | 以 `CyclicBarrier` 讓兩個呼叫在測試用 `BarrierSet.add` 會合；改用單次 `Set.add` 的回傳值判斷 |
| `ConcurrentHashMap.newKeySet()` 本身不是執行緒安全 | 誤報 | 否決 | Oracle Java 17 API 說明其由 `ConcurrentHashMap` 支援；問題是複合的先檢查再執行，不是容器本身 |
| `finish` 未使用與 `tryStart` 相同的正規化規則 | 漏報 | 人工補上 | JUnit 5 以 `" Workspace-42 "` 重現；抽出單一 `normalize` 方法 |
