# Day 20｜遺留程式碼考古：每個理解都要能回到證據

![Day 20 封面：每個理解都要能回到證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day20/day20-01-cover.png)

Day 19 用獨立縮小案例驗證新需求的 07:00 製作邊界。今天我回到尚未套用新需求的既有 08:00 路徑，追查哪段程式讀資料、呼叫可攜式文件格式（Portable Document Format，PDF）產生器，再觸發寄信。需求書已提醒產製與寄信耦合；只看 `DailyReportService` 這個名稱，很容易把猜測當答案。遺留程式碼（Legacy Code）最危險的不是看不懂，而是自以為看懂。

## 不逐檔摘要，先沿著行為走

我鎖定「每日 08:00 產生報表並寄信」這條路徑，再從入口、核心流程、資料存取、外部整合與副作用五個方向找證據，不逐一摘要無關檔案。

| 閱讀方向 | 本篇追蹤線索 | 程式證據 |
|---|---|---|
| 外部入口 | 判斷報表時區是否為 08:00 | `DailyReportJob.runAt()` |
| 核心流程 | 組合內文、附件與郵件 | `DailyReportService.generateAndSend()` |
| 資料存取 | 讀訂閱者與前一日數值 | `SubscriberRegistry`、`MetricsSource` |
| 外部整合 | 呼叫 PDF 產生器與郵件閘道 | `PdfRenderer`、`MailGateway` |
| 副作用邊界 | 兩個外部介面收到的資料 | `render()`、`send()` |

![從五個方向建立日報服務理解地圖](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day20/day20-02-five-directions.png)

## 先讓 Codex 唯讀追蹤

[OpenAI 官方文件](https://learn.chatgpt.com/use-cases/codebase-onboarding)建議先限定功能區域，再要求 Codex 說明流程、模組責任、副作用與下一批檔案。我再要求找不到證據就標成未知，不得依類別名稱推測業務行為。完整版放在[唯讀追蹤任務](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY20/docs/trace-prompt.md)。

```text
先不要修改檔案。從 DailyReportJob.runAt() 追蹤每日 08:00 的完整路徑。
每個節點列出檔案、方法、輸入、輸出、副作用與程式碼證據。
把結論分成「已由程式碼確認」與「仍待執行期確認」。
遇到排程器、環境變數、資料庫或外部服務時，不要推測。
```

這是只讀程式碼、尚未實際執行的靜態追蹤。`runAt()` 先用注入的報表時區檢查 08:00，再從 `SubscriberRegistry` 取出訂閱者，依序呼叫 `MetricsSource`、`PdfRenderer` 與 `MailGateway`。每個節點都能回到方法，但排程頻率與 `ZoneId` 的正式設定來源仍未知。

![從批次入口追到兩個外部整合呼叫](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day20/day20-03-call-path.png)

## 地圖要保留未知，不追求看起來完整

我把靜態追蹤的結論記在[理解地圖](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY20/docs/codebase-map.md)，並保留未解問題，例如排程重跑、資料庫交易、PDF 暫存檔與郵件重試。介面只標出邊界，外部系統仍待確認。

![已確認路徑與仍待正式環境確認的邊界](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day20/day20-04-certainty-boundary.png)

## 特徵測試先固定現況，也揭露風險

理解地圖仍是閱讀結論，我再用特徵測試（characterization test）固定一位測試客戶在臺北 08:00 的可觀察行為：PDF 測試替身收到標題、前一日筆數 1280 與成長率 12.5％；郵件測試替身收到附件名稱 `daily-report.pdf` 與內文。測試不連資料庫、不產生真正 PDF，也不寄信，只記錄邊界資料與呼叫次數。

```java
fixture.job.runAt(Instant.parse("2026-08-19T00:00:00Z"));

assertEquals(1, fixture.pdfRenderer.callCount);
assertEquals(1, fixture.mailGateway.callCount);
assertEquals("daily-report.pdf", fixture.mailGateway.message.attachmentName());
```

第二個測試在同一分鐘執行兩次，PDF 產生器與郵件閘道測試替身都被呼叫 2 次。測試通過不表示重複寄信正確，而是證明縮小案例沒有冪等性（idempotency，也就是重跑不會再次造成副作用）防線。完整內容可看 [DailyReportFlowCharacterizationTest.java](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY20/src/test/java/com/ithome/day20/report/DailyReportFlowCharacterizationTest.java)。

受限環境阻擋 Maven 下載外掛時，JUnit 尚未啟動；核准網路存取後重跑 `mvn clean test`，2 項測試全數通過，建置結果為 `BUILD SUCCESS`。命令與限制記在[驗證紀錄](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY20/docs/verification-log.md)。

![特徵測試固定現況並揭露重複呼叫風險](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day20/day20-05-characterization-test.png)

## 小結：先證明自己真的看懂

Codex 把搜尋範圍縮成一條行為路徑，可信度仍來自檔案、方法、測試與未解問題。綠燈只表示描述符合縮小程式。Day 21 會接上錯誤訊息與執行紀錄，追查客戶增加後偶爾延遲寄出的根因。

## 參考資料

- [OpenAI：Understand large codebases](https://learn.chatgpt.com/use-cases/codebase-onboarding)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/)
- [日報服務需求書](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E6%97%A5%E5%A0%B1%E6%9C%8D%E5%8B%99-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
