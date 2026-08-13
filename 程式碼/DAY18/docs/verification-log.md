# DAY17 驗證紀錄

- 驗證日期：2026-08-09
- 環境：Windows、Java 17、Maven、JUnit 5
- 工作目錄：`程式碼/DAY17/`

## 第一次執行

```text
mvn clean test
```

沙箱內執行時，Maven 需要下載 `maven-clean-plugin`，但網路權限未開放，因此建置在 JUnit 執行前停止。這次結果不能算測試失敗，也不能算驗收通過。

## 核准連線後重跑

確認下載來源為 Maven Central，僅核准本次測試所需連線後再次執行：

```text
mvn clean test
```

結果摘要：

```text
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 驗收對照

| 驗收條件 | 證據 | 結果 |
|---|---|---|
| 08:00 計算為同日 07:00 | `startsProductionOneHourBeforeDeliveryInTheSameTimezone` | 通過 |
| 保留 `Asia/Taipei` 時區 | 同一測試比對 `ZoneId` | 通過 |
| 空值輸入明確拒絕 | `rejectsMissingDeliveryTime` | 通過 |
| Maven 測試全數通過 | `mvn clean test` 輸出 | 2 項通過 |

## 人工範圍審查

- 新增 `ReportProductionWindow` 與對應測試。
- 未修改既有排程、寄信、PDF、資料庫或公開 API。
- 未實作日、週、雙週、月頻率與 Word、Excel 格式。
- 尚未驗證與既有系統整合、實際寄信及大量客戶負載；這些均不在本次任務契約範圍內。
- 本例只驗證 `Asia/Taipei`。若未來支援會切換日光節約時間的時區，須先確認「前一小時」是實際經過六十分鐘或當地鐘面時間，再補跨時區測試。
