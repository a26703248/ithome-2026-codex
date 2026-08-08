# DAY09：ChatGPT Code Review 初篩

本範例延續 Day 08 的每日匯入排程，將同一工作區的重疊執行保護縮成一個可測試的 `DailyImportGate`。

## 檔案

- `review-input.diff`：刻意保留 null、先檢查再執行及正規化不一致問題的待審 diff。
- `review-prompt.txt`：要求 ChatGPT 把觀察整理成可由另一位審查者重做的驗證卡。
- `review-notes.md`：將初篩項目轉為人工複核與證據紀錄。
- `before-review/`：可獨立執行的修正前測試夾具，預期出現三項失敗。
- `src/main`：複核後的最小修正版。
- `src/test`：null、並行、正規化與重複啟動的 JUnit 5 測試。

## 執行

```shell
mvn clean test
```

若要重現修正前紅燈：

```shell
cd before-review
mvn clean test
```

這個指令預期以三項測試失敗結束；回到上層執行測試，才是修正版的綠燈結果。
