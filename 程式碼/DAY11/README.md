# DAY10 Codex 代理迴圈案例

本案例以 `CsvBatchPlanner` 多算空批次的邊界錯誤，示範 Codex 如何從定位問題走到提出交付證據。

- `before-fix/`：保留修正前版本，五項測試中兩項失敗。
- 專案根目錄：保留最小修正後版本，五項測試全部通過。
- `task-prompt.txt`：交給 Codex 的任務、限制與驗收條件。
- `docs/verification-log.md`：修正前後的命令、結果與差異證據。

## 重現

修正前：

```shell
cd before-fix
mvn clean test
```

修正後：

```shell
mvn clean test
```
