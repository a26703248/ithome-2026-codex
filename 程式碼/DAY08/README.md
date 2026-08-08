# Day 08 可執行範例

這個專案用 Spring `CronExpression` 與 Java 時間 API 驗證：cron 格式、時區與基準時間如何共同決定下一次執行時刻。

```shell
mvn clean test
```

驗收範圍：

- Spring cron 需要六個欄位，五欄 Linux crontab 格式會被拒絕。
- 同一個每日上午九點 cron，在 `Asia/Taipei` 與 `Asia/Tokyo` 對應不同 `Instant`。
- `@Scheduled` 的 cron 與 `zone` 使用可外部設定的 placeholder。

限制：反射測試只核對註解字串，沒有啟動 Spring 上下文，也沒有等待真實排程觸發。
