# Day 13｜第一個 Codex 任務實戰：從 issue 到可驗證修正

![Day 13 封面：從 issue 到可驗證修正](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day13/day13-01-cover.png)

Day 12 把專案規則寫進 `AGENTS.md`，今天我將它放進一個 Java 17／Maven 報表專案。客服原始回報只有：「日期起點和終點選同一天時，報表會失敗，請協助修正。」沒有確切日期、錯誤訊息與正常結果，光靠這句話，我還寫不出會失敗的測試，也無法判斷修補有沒有超出範圍。

![原始 issue 與五個待補欄位](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day13/day13-02-issue-gaps.png)

## 我把缺口補成能重跑的修正說明

我先在原始版本執行 `mvn clean test`，四項既有測試全數通過，表示測試還沒涵蓋客服操作。接著補上這次要交給 Codex 的確切條件：

| 項目    | 本次內容 |
|-------|---|
| 呼叫    | `countInclusiveDays(2026-08-19, 2026-08-19)` |
| 現況    | 拋出 `IllegalArgumentException` |
| 正常結果  | 同日起訖算一天，回傳 `1` |
| 可改檔案  | `ReportRangeService.java` 與新增的一項測試 |
| 不可改內容 | `pom.xml`、既有測試、相依套件、公開方法簽章 |
| 通過方式  | 指定測試先出現失敗，修正後再跑全部測試 |

公開方法簽章指方法名稱、參數與回傳型別。這次要保留 `countInclusiveDays(LocalDate, LocalDate)`，避免呼叫端跟著改。

![把問題單補成能重跑的修正說明](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day13/day13-03-task-contract.png)

工作紀錄先讀了 `AGENTS.md`、`pom.xml`、`ReportRangeService.java` 與現有測試。多日範圍本來就會加一，把起日與迄日都算進去；初步假設因此落在前面的日期檢查，而不是天數計算公式。

## 先跑指定測試類別，再跑完整測試

我讓 Codex 新增 `sameDayRangeContainsOneDay()`。這是一項 JUnit 5 測試；JUnit 5 是 Java 的單元測試框架，而回歸測試會在同一錯誤再次出現時把它抓出來。執行 `mvn -Dtest=ReportRangeServiceTest test` 時，`-Dtest` 只選指定測試類別，結果為 `Tests run: 5, Errors: 1`。

堆疊落在 `ReportRangeService.java:14`。原本的 `!endDate.isAfter(startDate)` 把「相等」也判成錯誤，與錯誤訊息所寫的「迄日不得早於起日」不一致。修正只換掉條件：

```diff
-if (!endDate.isAfter(startDate)) {
+if (endDate.isBefore(startDate)) {
```

![從基線、重現到最小修正與完整測試](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day13/day13-04-work-log.png)

最後執行 `mvn clean test`；`clean` 先移除舊建置產物，`test` 再跑這個範例專案的全部單元測試。五項測試的失敗與錯誤都是 0。我人工檢查程式碼差異（diff），確認既有測試、`pom.xml` 與公開方法都沒變。

## 我用五個問題讀完成回報

| 審查問題 | 這次答案 |
|---|---|
| 哪裡判錯？ | 日期相等被誤判成迄日較早 |
| 改了哪裡？ | 一個條件判斷與一項新測試 |
| 跑了什麼？ | 指定測試先錯 1 項；完整測試 5 項通過 |
| 哪些沒跑？ | 網頁操作、資料庫與端對端報表 |
| 還要確認什麼？ | 單日報表的實際輸出內容 |

![審查完成回報的五個問題](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day13/day13-05-completion-report.png)

這次沒有另外做純人工修正的計時對照，因此我只能證明流程留下了可核對的檔案、命令與結果，不能宣稱省下幾分鐘。若要比較效率，我會替人工與 Codex 分別記錄整理問題、定位、修改、測試及審查時間，並使用相同環境與通過條件。

完整的[原始 issue](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY13/issue.md)、[任務提示詞](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY13/task-prompt.txt)、[三階段程式碼](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY13/README.md)與[工作及驗證紀錄](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY13/docs/verification-log.md)都能重新檢查。

## 小結：先準備紅燈與邊界

這次我先提供會失敗的日期、不可變更的介面與兩階段測試，再讓 Codex 動手。Codex 協助讀檔、試驗與整理，人仍要決定什麼行為才正確。Day 14 會接著逐段閱讀工作紀錄、diff 與測試輸出，確認完成訊息究竟有多少證據。

## 參考資料

- [OpenAI：Prompting](https://learn.chatgpt.com/docs/prompting)
- [OpenAI：Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/)
- [Apache Maven：Maven Surefire Plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)
