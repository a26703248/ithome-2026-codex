# Day 19｜自動化測試維運：先證明根因，再處理紅燈

![Day 19 封面：先證明根因，再處理紅燈](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-01-cover.png)

Day 18 的 08:00 與 07:59 測試鎖住舊發送規則；今天驗證「發送前一小時開始製作」，邊界因此移到 07:00。我尚未接上真正的持續整合（Continuous Integration，CI），而是在本機注入世界協調時間（Coordinated Universal Time，UTC）的固定時鐘模擬執行器。結果 `startsOneHourBeforeSendTimeInTheReportZone` 出現 `expected: <true> but was: <false>`。

## 紅燈先分流，不先改斷言

我把 log 切成三段看：Maven 是否完成解析與編譯、Maven Surefire 測試外掛是否真的啟動 JUnit、哪個案例在哪種環境失敗。這次前兩段都正常，差異集中在 UTC 與臺北時間。若此時直接把 `assertTrue` 改掉，07:00 沒有開始製作報表的錯誤也會一起被放過。

| 類型 | 我會找的證據 | 可接受處理 |
|---|---|---|
| 產品缺陷 | 固定輸入仍穩定失敗 | 最小修改並補回歸測試 |
| 測試缺陷 | 斷言與需求或公開介面不符 | 修正測試意圖 |
| 環境差異 | Java 開發工具包（Java Development Kit，JDK）、時區或設定不同 | 固定並記錄環境 |
| 相依問題 | 測試啟動前解析失敗 | 核對來源、版本與權限 |
| 偶發失敗 | 相同條件下結果不一致 | 找共享狀態、時間或競態 |

![持續整合紅燈的五類分流與禁止捷徑](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-02-failure-classification.png)

## 先讓 Codex 診斷，暫時不給修正權

我把去除帳號、路徑與憑證的失敗摘要、`pom.xml`、正式程式與測試交給 Codex，並把順序寫清楚：

```text
先不要改檔。重現指定測試，列出三個根因假設與驗證順序。
證據足夠後，只能修改 ReportProductionWindow 與對應測試。
禁止刪除測試、放寬斷言、無條件重試或順手重構。
最後執行局部測試、完整測試，回報命令與殘留風險。
```

這個邊界讓 Codex 先比對時間值。失敗版本雖然收到了 `reportZone`，卻只呼叫 `ZonedDateTime.now(clock)`；測試注入 UTC 的固定 `Clock` 時，程式直接拿 23:00 與預期的臺北 07:00 比較。根因是產品程式忽略訂閱時區，誤用注入時鐘的 UTC 本地時間，不是 JUnit 5 判錯。

排除順序留在[診斷任務](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY19/docs/diagnosis-prompt.md)：Surefire 報告已有測試名稱與堆疊，表示建置與 JUnit 都已啟動；固定瞬間排除等待造成的不穩；逐項比對 `Clock` 時區、訂閱時區與預期時間後，才定位到未使用的參數。

![從失敗訊息、假設到最小重現的診斷順序](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-03-diagnosis-sequence.png)

## 回歸測試固定瞬間，也明確指定業務時區

我用 `Clock.fixed()` 在本機固定 UTC 瞬間，再明確傳入業務時區 `Asia/Taipei`：

```java
Clock ciClock = Clock.fixed(
        Instant.parse("2026-08-18T23:00:00Z"), ZoneOffset.UTC);
ReportProductionWindow window = new ReportProductionWindow(ciClock);

assertTrue(window.shouldStart(
        LocalTime.of(8, 0), ZoneId.of("Asia/Taipei")));
```

我用同一個測試類別放入三個固定瞬間：23:00Z 轉成臺北 07:00 時必須啟動；22:59Z 與 23:01Z 轉成 06:59 與 07:01 時都必須保持關閉。`withZoneSameInstant(reportZone)` 加入前，第一條斷言固定出現 `false`；加入後三條一起通過。前後各一分鐘的測試也能攔住「07 點整個小時都啟動」的錯誤實作。完整內容可看 [ReportProductionWindowTest.java](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY19/src/test/java/com/ithome/day19/report/ReportProductionWindowTest.java)。

![時區缺陷修正前後與三條邊界測試](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-04-timezone-regression.png)

## 綠燈要附上可重跑的證據

修正前，指定類別是 3 項測試、1 項失敗；修正後重跑指定類別與 `mvn clean test`，兩次都是 3 項通過、`BUILD SUCCESS`。這只證明注入 UTC 時鐘、以臺北為業務時區的縮小案例正確，尚未證明真正的 CI、正式排程器、產製耗時與郵件送達。命令與限制記在[驗證紀錄](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY19/docs/verification-log.md)。日後若使用 CI log，我會先移除儲存庫名稱、內部路徑、Token 與服務網址。

![修正前失敗、局部測試與乾淨建置三段證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-05-ci-verification.png)

## 小結：先證明根因，再讓測試變綠

這次我要求 Codex 交出的不是一句「已修好」，而是失敗命令、時間換算、程式差異與重跑結果。這些資料讓我能逐項判斷是否放行，也留下日後再次失敗時的比較基準。Day 20 會帶著這份基準進入陌生的遺留程式碼（Legacy Code），從可觀察行為畫出程式路徑。

## 參考資料

- [OpenAI：Prompting](https://learn.chatgpt.com/docs/prompting)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/)
- [Oracle Java 17：Clock](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Clock.html)
- [Oracle Java 17：ZonedDateTime](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/ZonedDateTime.html)
- [日報服務需求書](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E6%97%A5%E5%A0%B1%E6%9C%8D%E5%8B%99-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
