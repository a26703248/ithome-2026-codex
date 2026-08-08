# Day 08｜用 ChatGPT 當隨身技術導師：每天九點，是哪個九點？

![Day 08 封面：每天九點，是哪個九點](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day08/day08-01-cover.png)

Day 07 整理出匯入任務查詢契約後，我接著處理需求書的「每日日報定時匯入」。需求沒有指定時間與時區，我不急著請 ChatGPT 生成 `@Scheduled`，而是先問自己：台北與東京的「每天上午九點」，下一次執行會是同一個時刻嗎？

## 先預測，再讓 ChatGPT 挑戰

OpenAI 官方的「Learn a new concept」範例強調縮小學習目標，並留下成果、限制與待解問題。我把它改成「預測表」：先填答案，再請 ChatGPT 只提反例，最後才寫 Java 驗證。

![先預測、再挑戰、最後驗證](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day08/day08-02-prediction-challenge.png)

| 我先回答的問題 | ChatGPT 負責挑戰 | 最後驗收 |
|---|---|---|
| Spring cron 有幾欄？ | 提供一個容易混用的格式 | 無效表示式測試 |
| `0 0 9 * * *` 代表什麼？ | 更換時區與基準時間 | 比對下一個 `Instant` |
| 程式會用哪個時區？ | 追問系統預設值的風險 | 檢查 `zone` 設定 |

[完整提示詞](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY08/learning-prompt.txt) 禁止 ChatGPT 在我預測前公布答案，也要求它分開框架事實、工程假設與未確認的需求。「上午九點」只是演練值，不會被回填成需求書事實。

ChatGPT 只能挑戰我的推理，不能替我宣告框架結果。如果我改了時區就跟著改答案，它要追問「哪一步換算造成差異」，而不是只回「正確」。我要留下的不是對話截圖，而是可以重算的輸入與預期輸出。

## Spring cron 比 Linux 常見格式多一欄

Spring cron 使用六個以空白分隔的欄位，順序是秒、分、時、日、月、星期。`0 0 9 * * *` 的前三欄是零秒、零分、九時，所以表示每天上午九點。若直接貼上 Linux crontab 常見的五欄 `0 9 * * *`，`CronExpression.parse` 會拋出 `IllegalArgumentException`。

我沒有只用眼睛數空白。第一項測試傳入五欄字串，確認解析器拒絕；這比把「Spring 多一個秒欄」抄進筆記更有用。未來若更換排程工具，測試也會提醒我不能直接套用同一種 cron 格式。

![Spring cron 六個欄位的順序](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day08/day08-03-cron-fields.png)

我把時間計算包成可單獨測試的 `DailyImportSchedule`，輸入 cron、時區與現在時刻，輸出下一個執行時刻：

```java
ZonedDateTime localNow = now.atZone(zone);
ZonedDateTime localNext = expression.next(localNow);
return localNext.toInstant();
```

`expression` 與 `zone` 分別由 `CronExpression.parse`、`ZoneId.of` 建立。程式先把 `Instant` 轉成排程時區下的時間，交給 Spring 計算下一次命中，再轉回絕對時刻。[完整程式與測試](https://github.com/a26703248/ithome-2026-codex/tree/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY08) 可用 `mvn clean test` 重現。

我不用 `LocalDateTime` 當斷言值，因為它只有日期與鐘點，沒有時區資訊；兩個地區都可以出現「09:00」，卻可能不是同一個時刻。轉回 `Instant` 後，測試才能不依賴執行機器的本地時區，直接比較兩個絕對時間。

## 同一個九點，不是同一個時刻

我把現在時間固定為 `2026-08-18T23:30:00Z`；尾端的 `Z` 代表協調世界時（Coordinated Universal Time，UTC）。在台北是隔天上午七點半，下一次九點對應 `01:00Z`；在東京已是上午八點半，下一次九點對應 `00:00Z`。cron 沒變，實際觸發時刻卻相差一小時。

![台北與東京的下一次九點](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day08/day08-04-timezones.png)

[排程入口](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY08/src/main/java/com/ithome/day08/tutor/DailyReportScheduler.java) 以 placeholder 宣告 cron 與 `zone` 可由外部設定，預設值只用於範例。四項 JUnit 5 測試已通過：一項拒絕五欄格式，兩項核對台北與東京的下一次時刻，一項用 Java 反射讀取註解，檢查 `@EnableScheduling`、cron 與 `zone` 字串。最後一項沒有啟動 Spring 上下文，也沒有真正等到排程觸發，這是本篇證據的邊界。

`Asia/Taipei` 這種區域型識別字比單寫 `UTC+8` 更能表達業務語意。不過時區能否由客戶設定、如何儲存，仍是待確認項目。保留 `zone` 設定位置，不代表產品決策已完成。

![ChatGPT 反例、Java 計算、JUnit 測試與官方文件](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day08/day08-05-evidence.png)

## 小結：把「我懂了」換成可重現的預測

ChatGPT 適合幫我製造反例與改變題目條件，但格式與框架行為仍以程式、測試與 Spring 官方文件為準。Day 09 會把這段排程程式交給 ChatGPT 做 Code Review 初篩，看它能不能找出時區、空值與測試邊界的問題。

## 參考資料

- [OpenAI：Learn a new concept](https://learn.chatgpt.com/use-cases/learn-a-new-concept)
- [Spring Framework：Task Execution and Scheduling](https://docs.spring.io/spring-framework/reference/integration/scheduling.html)
- [Spring Framework：CronExpression](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/scheduling/support/CronExpression.html)
- [資料工作區空間——需求書（v0．初版待釐清）](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E8%B3%87%E6%96%99%E5%B7%A5%E4%BD%9C%E5%8D%80%E9%96%93-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
