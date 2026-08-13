# Day 20 遺留程式碼理解範例

這個 Java 17／Maven 範例把日報服務縮成一條可追蹤的批次路徑：

1. `DailyReportJob.runAt()` 以注入的報表時區判斷是否為 08:00。
2. `SubscriberRegistry` 讀取每日報表訂閱者。
3. `DailyReportService.generateAndSend()` 讀取數值，再呼叫 PDF 產生器與郵件閘道。

範例刻意保留一個遺留系統風險：同一分鐘重跑會再次呼叫兩個外部邊界。測試替身只能證明呼叫次數，無法證明正式資料庫、PDF 套件與郵件服務的執行期行為。

執行測試：

```shell
mvn clean test
```
