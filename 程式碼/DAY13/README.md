# DAY13 第一個 Codex 任務實戰

這個 Java 17／Maven 範例記錄一張資訊不足的 issue，如何補上確切輸入、修改範圍與測試命令，再交給 Codex 修正。

## 目錄

- `issue.md`：原始問題單。
- `task-prompt.txt`：補齊重現步驟與邊界後的任務說明。
- `before-fix/`：尚未加入回歸測試的原始版本。
- `reproduction/`：已加入單日範圍回歸測試、但尚未修正主程式的版本。
- `src/`：完成最小修正並保留回歸測試的版本。
- `docs/verification-log.md`：實際命令、測試摘要與人工審查紀錄。

## 執行

```text
mvn clean test
```
