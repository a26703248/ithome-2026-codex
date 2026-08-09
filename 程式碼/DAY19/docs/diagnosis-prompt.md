# DAY19 Codex 診斷任務

## 輸入

- `pom.xml`
- `ReportProductionWindow.java`
- `ReportProductionWindowTest.java`
- 去識別化失敗摘要：`startsOneHourBeforeSendTimeInTheReportZone expected: <true> but was: <false>`
- 模擬條件：本機測試注入 UTC 的固定 `Clock`；業務時區為 `Asia/Taipei`

## 任務

先不要修改檔案。使用失敗時的命令重現問題，列出三個根因假設，並依驗證成本排列順序。每排除或確認一個假設，都要附上實際輸出或程式碼位置。

證據足夠後，只能修改 `ReportProductionWindow.java` 與 `ReportProductionWindowTest.java`。禁止刪除測試、放寬斷言、加入無條件重試、改變發送時間規則或順手重構其他類別。

完成後依序執行指定測試與乾淨完整測試。回報修改檔案、命令、通過數量，以及尚未驗證的真正 CI、正式排程、報表產製與郵件流程。
