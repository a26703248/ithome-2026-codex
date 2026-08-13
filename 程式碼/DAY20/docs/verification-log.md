# DAY19 驗證紀錄

- 驗證日期：2026-08-09
- 環境：Windows 11、OpenLogic JDK 17.0.10、Maven 3.8.1、JUnit 5.13.4
- 工作目錄：`程式碼/DAY19/`

## 失敗重現

失敗版本收到 `reportZone` 後沒有使用它，直接以 `Clock` 的 UTC 時區取得本地時間。固定瞬間 `2026-08-18T23:00:00Z` 在 `Asia/Taipei` 是次日 07:00，應符合 08:00 發送前一小時的條件；失敗版本卻拿 23:00 比較。

```text
mvn -Dtest=ReportProductionWindowTest test
Tests run: 3, Failures: 1, Errors: 0, Skipped: 0
ReportProductionWindowTest.startsOneHourBeforeSendTimeInTheReportZone
expected: <true> but was: <false>
BUILD FAILURE
```

## 最小修正

在取得 `Clock` 時間後使用 `withZoneSameInstant(reportZone)`，保留同一瞬間並轉成訂閱設定的業務時區。沒有刪除測試、放寬斷言或加入重試。

## 修正後驗證

```text
mvn -Dtest=ReportProductionWindowTest test
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS

mvn clean test
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 尚未證明

- 縮小案例沒有接上正式排程器，未驗證多節點或重複觸發。
- 縮小案例沒有接上真正的 CI；UTC 條件來自測試注入的固定 `Clock`。
- 固定時鐘測試沒有涵蓋報表產製超過一小時時的處理規則。
- 沒有連接 PDF 產生器、郵件伺服器或客戶設定資料庫。
