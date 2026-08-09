# Day 20 驗證紀錄

驗證日期：2026-08-09

## 測試命令

```shell
mvn clean test
```

第一次執行時，Maven 需要從 Maven Central 下載 `maven-clean-plugin`，但受限環境拒絕網路連線，因此建置停在相依解析階段，JUnit 尚未啟動。確認來源後核准這次連線，再以相同命令執行。

## 成功結果

```text
Running com.ithome.day20.report.DailyReportFlowCharacterizationTest
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 已驗證範圍

- 臺北時間 08:00 會讀取一位訂閱者與前一日數值，接著各呼叫一次 PDF 產生器與郵件閘道測試替身。
- 縮小案例交給郵件閘道的附件名稱為 `daily-report.pdf`，內文包含前一日筆數 1280 與成長率 12.5％。
- 同一分鐘呼叫兩次時，兩個測試替身各被呼叫兩次，縮小案例沒有冪等防線。

## 尚未驗證

- 正式排程器、依賴注入與環境變數來源。
- 正式資料庫、PDF 套件、檔案系統與郵件服務。
- 交易、重試、併發與真正的郵件送達結果。
