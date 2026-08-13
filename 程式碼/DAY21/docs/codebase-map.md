# 日報服務理解地圖

| 方向 | 已確認路徑 | 證據 |
|---|---|---|
| 外部入口 | `runAt()` 僅在報表時區 08:00 繼續 | `DailyReportJob.runAt()` |
| 資料存取 | 讀取每日訂閱者與前一日數值 | `SubscriberRegistry.findDailySubscribers()`、`MetricsSource.loadPreviousDay()` |
| 核心流程 | 組合信件內文與 PDF 內容 | `DailyReportService.generateAndSend()` |
| 外部整合 | 呼叫 PDF 產生器與郵件閘道 | `PdfRenderer.render()`、`MailGateway.send()` |
| 副作用邊界 | 同一分鐘重跑會再次呼叫兩個測試替身 | `DailyReportFlowCharacterizationTest` |

## 仍待確認

- 正式排程器的呼叫頻率，以及同一分鐘是否可能重跑。
- `ZoneId`、寄送時間與訂閱條件從哪個設定來源注入。
- 正式資料庫查詢的篩選、排序、交易與重試行為。
- PDF 套件是否寫入暫存檔，以及失敗後是否留下檔案。
- 郵件閘道的重試與冪等性策略。
