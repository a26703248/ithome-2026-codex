# DAY17 ChatGPT＋Codex 任務契約範例

這個 Java 17／Maven 範例示範如何把日報服務的模糊新增需求，收斂成一個可交給 Codex 執行與驗收的小任務。

## 目錄

- `planning-prompt.txt`：請 ChatGPT 整理缺口與任務契約草案的提示詞。
- `task-contract.md`：經人工確認後交給 Codex 的任務契約。
- `src/`：時間計算元件與 JUnit 5 測試。
- `docs/verification-log.md`：實際測試與範圍審查紀錄。

## 執行

```text
mvn clean test
```

