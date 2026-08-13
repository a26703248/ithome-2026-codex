# DAY18 大型重構任務拆解範例

這個 Java 17／Maven 範例保留一個刻意集中協調多段流程的 `DailyReportService`，示範大型重構的第一小步：只新增特徵測試，不修改正式程式。

## 目錄

- `task-map.md`：四個可驗證步驟與相依順序。
- `first-step-task.md`：交給 Codex 的第一小步任務契約。
- `src/main/`：時間判斷、內容組合、PDF 與郵件元件協調集中在同一方法的既有範例。
- `src/test/`：記錄 08:00 與 07:59 兩條呼叫路徑的 JUnit 5 特徵測試。
- `docs/verification-log.md`：測試、雜湊與範圍審查紀錄。

## 執行

```text
mvn -Dtest=DailyReportServiceCharacterizationTest test
mvn clean test
```
