# DAY18 驗證紀錄

- 驗證日期：2026-08-09
- 環境：Windows 11、OpenLogic JDK 17.0.10、Maven 3.8.1、JUnit 5.13.4
- 工作目錄：`程式碼/DAY18/`

## 第一小步範圍

- 正式程式保留時間判斷、報表內容組合、PDF 與郵件元件協調集中在同一方法的現況。
- 本輪只新增 `DailyReportServiceCharacterizationTest` 與說明文件。
- 未實作日、週、雙週、月頻率，未新增 Word、Excel，也未處理 PDF 套件安全通知。

## 測試執行

第一次執行時，Maven 在受限環境解析建置相依項目時遭到阻擋，因此在 JUnit 啟動前停止。確認來源為 Maven Central 並核准本次連線後，局部測試通過。補上明確呼叫次數斷言後於 2026-08-09 10:12:20 重跑，摘要如下：

```text
mvn -Dtest=DailyReportServiceCharacterizationTest test
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

接著於 2026-08-09 10:12:32 執行完整測試：

```text
mvn clean test
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 驗收對照

| 驗收條件 | 證據 | 結果 |
|---|---|---|
| 08:00 各呼叫 PDF 與郵件元件一次，並交付附件 | `passesCurrentDailyAttachmentToMailGatewayAtEightOClock` 的 `callCount` 與內容斷言 | 通過 |
| 郵件元件收到前一日筆數、成長率與附件名稱 | 同一測試逐項比對 | 通過 |
| 07:59 不呼叫 PDF 或郵件元件 | `doesNotCallPdfOrMailGatewayBeforeEightOClock` 的零次呼叫斷言 | 通過 |
| 正式程式未變更 | 執行前後 SHA-256 均為 `9B432193F90DA8428E7137C5DE5B2133B0F4525D108310E5E39AAFF9F604E6CB` | 通過 |

## 尚未證明

- 特徵測試只記錄這個縮小案例的現況，不代表正式環境的排程、PDF 套件或郵件伺服器已完成整合驗證。
- 測試通過不代表既有行為一定符合新需求；它只提供後續純重構的比較基準。
- 負載增加後的延遲寄出問題尚未定位，留待 Day 19 的測試與持續整合流程處理。
