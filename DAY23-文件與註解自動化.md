# Day 23｜文件與註解自動化：生成文字很快，建立可信文件靠證據

![Day 23 封面：從來源、草稿、驗證到維護責任](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day23/day23-01-cover.png)

Day 22 的縮小實驗確認：先準備所有報表，再寄信，能避免慢速回應拖延下一份報表，但總耗時不變。實驗沒有郵件佇列、失敗重試與避免重複寄信的冪等性；正式系統有沒有，仍待確認。若只把前半句交給 Codex，專案說明檔（README）容易留下過度承諾。文件可信度得由證據決定。

## 先讓過時文件失敗一次

我先在公開縮小專案執行舊版留下的啟動指令。為了保留失敗現場，[`README-before.md`](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY23/README-before.md) 沒有先被修掉，其中仍要求執行：

```shell
java -jar target/daily-report.jar --config config/prod.yml
```

實際執行立即得到 `Error: Unable to access jarfile target/daily-report.jar`。專案裡既沒有這個 Java Archive（JAR）檔，也沒有 `config/prod.yml`；我不能因為指令失效，就請 Codex 猜一個新版正式啟動方式。新版 README 只保留能在公開專案重現的測試命令，正式啟動、環境變數與部署流程一律標成待確認。

## 文件來源比生成順序更重要

我先建立[文件來源對映](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY23/docs/source-map.md)，再開始改字。測試與命令輸出優先於程式名稱，現行設定優先於舊 README。需求書只定義每日報表的既有數值；週、雙週、月的計算區間則在表格標成「待產品決策」。

| 文件內容 | 可信來源 | 驗證方式 | 維護責任 |
|---|---|---|---|
| Java 17 編譯目標 | Maven 建置設定檔 `pom.xml` | `mvn clean test` | 修改建置設定者 |
| 兩階段處理順序 | 程式與 JUnit 測試 | 核對事件序列 | 日報服務維護者 |
| 正式啟動與部署 | 公開專案沒有來源 | 查正式部署設定 | 平台維運者 |
| 週、雙週、月的計算區間，以及是否沿用每日欄位 | 需求書尚未定義 | 產品決策 | 產品負責人 |

![文件內容、可信來源、驗證方式與狀態的對映](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day23/day23-02-source-map.png)

來源對映完成後，我才移除無法重現的啟動指令，留下已驗證命令與待確認事項。

![README 修改前後：移除無證據的啟動指令，保留可重現測試](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day23/day23-03-readme-before-after.png)

## 給 Codex 的不是一句「補文件」

[OpenAI 官方提示文件](https://learn.chatgpt.com/docs/prompting)建議，較大或重要的工作要說清楚成果、材料、形式與限制；Codex 任務還需相關程式、重現方式與驗證方法。我的[文件更新任務](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY23/docs/documentation-prompt.md)限定：讀者為接手專案的 Java 工程師；只改 README 與必要註解；不推測正式排程、環境變數或業務規則；缺少證據就標成待確認；最後逐條執行文件命令。

更新後我執行 `mvn clean test`，2 項測試、0 項失敗、0 項錯誤，結果為 `BUILD SUCCESS`。第一次建置被受限環境擋在 Maven Central 套件庫，JUnit 尚未開始；核准連線後才成功。失敗階段與重跑結果都保留在[驗證紀錄](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY23/docs/verification-log.md)，避免只留下綠燈截圖。

![過時指令失敗與新版測試成功的實際驗證](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day23/day23-04-command-verification.png)

## 我刪掉哪一種註解？

`// 把報表加入清單` 只重複 `preparedReports.add(...)`。我刪掉它，改記錄這次迴圈為何放在寄信之前，以及這項安排沒有解決什麼：

```java
// 先完成所有報表準備，再呼叫郵件服務，避免慢速回應推遲下一份報表。
// 這項實驗沒有縮短郵件總耗時。
for (Customer customer : List.copyOf(customers)) {
    preparedReports.add(reportPreparer.prepare(customer));
}
```

這兩句不是歷史猜測。測試證明第二份報表在 50 毫秒開始準備，但兩次 900 毫秒的寄信等待仍讓總時間到 1900 毫秒。完整程式放在 [`ReportBatch.java`](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY23/src/main/java/com/ithome/day22/report/ReportBatch.java)。註解說明為什麼，測試負責防止說明悄悄失真。

![冗餘註解與有效註解的比較](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day23/day23-05-comment-comparison.png)

Codex 草擬後，我仍逐條執行命令，將缺少來源的欄位交給產品或平台維運者。能交接的不是更長的 README，而是成功與失敗紀錄、來源對映及待確認清單。

## 小結：讓文件成為可重現的入口

Day 23 最後留下三樣東西：能重跑的 `mvn clean test`、保留失敗階段的驗證紀錄，以及明確負責人的未決事項。Day 24 會用同樣做法追查需求書裡的套件安全性通知，驗證人工智慧生成程式碼是否越過安全與品質門檻。

## 參考資料

- [OpenAI：Prompting](https://learn.chatgpt.com/docs/prompting)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/)
- [日報服務需求書](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E6%97%A5%E5%A0%B1%E6%9C%8D%E5%8B%99-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
