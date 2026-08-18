# Day 19｜大型重構任務拆解：讓每次改動都能停、能測、能退

![Day 19 封面：讓每次改動都能停、能測、能退](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-01-cover.png)

Day 18 新增了可獨立測試的 `ReportProductionWindow`，依任務契約還沒有接回舊服務。我回到縮小案例查看 `DailyReportService.runIfScheduled()`：它先判斷時間，再讀取數值、組合內文，把內容交給 PDF 元件，最後將附件交給郵件元件。五個動作集中在同一個方法。若我只說「幫我重構」，Codex 可能一併調整呼叫順序與 Word、Excel 格式；就算編譯通過，也看不出原有流程是否被改動。

![日報服務單一方法集中協調四段流程](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-02-coupling-scope.png)

## 先寫下 T1 的停手條件

我沒有先估要拆幾個類別，而是替 T1 設三道停手線：`src/main` 的 256 位元安全雜湊演算法（Secure Hash Algorithm 256-bit，SHA-256）值不能改、08:00 與 07:59 都要留下測試、局部與完整測試都要通過。我把現況寫成特徵測試（characterization test）：08:00 會呼叫 PDF 元件，並把附件與內文交給郵件元件；07:59 不會呼叫這兩個元件。它記錄的是目前觀察，不代表舊流程符合新需求。

| 檢查點 | 證據 | 何時停手 |
|---|---|---|
| 正式程式 | `DailyReportService.java` 的 SHA-256 | 雜湊不同就先查範圍 |
| 08:00 路徑 | 測試替身收到附件、內文與檔名 | 任一欄位不符就停止 |
| 07:59 路徑 | PDF、郵件測試替身皆為空 | 出現呼叫就停止 |
| 建置結果 | 局部、完整測試各自通過 | 任一命令失敗就不進 T2 |

## 先畫任務地圖，再交付第一步

任務順序沿著 `runIfScheduled()` 的控制流程安排：T1 留下現況證據，T2 移出時間判斷，T3 分開內文組合與傳送協調，T4 再建立通用格式路由並接回既有 PDF。新增格式與套件安全通知不塞進這條路線。T2、T3 都要改同一個方法，我因此排成前後關係，不同時交給兩個任務。以 T2 為例，T1 全過、時間判斷有獨立測試且公開介面不變，才准許進入 T3。

![從特徵測試到格式介面的重構任務地圖](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-03-task-map.png)

完整依賴、修改範圍與驗收條件放在 [task-map.md](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY19/task-map.md)。我只把 [T1 任務契約](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY19/first-step-task.md)交給 Codex，並把禁止事項直接寫進任務：

```text
只新增 DailyReportServiceCharacterizationTest 與驗證紀錄。
禁止修改 src/main，不搬檔、不改名、不實作新頻率與新格式。
驗收：執行局部與完整測試，回報檔案、結果、雜湊與殘留風險。
```

![第一小步只允許新增特徵測試與驗證紀錄](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-04-first-step-diff.png)

## Codex 完成後，我核對的不只有綠燈

縮小後的 Java 範例用 JUnit 5 鎖定兩條路徑。我用 `CapturingPdfRenderer` 與 `CapturingMailGateway` 當測試替身（test double）；它們不產生有效 PDF，也不連郵件伺服器，只記住呼叫次數與程式交出的內容。呼叫 `runIfScheduled(...)` 後，`triggered` 記錄流程是否啟動，斷言再核對呼叫次數、附件名稱與信件內文：

```java
assertTrue(triggered);
assertEquals(1, pdfRenderer.callCount);
assertEquals(1, mailGateway.callCount);
assertEquals("daily-report.pdf", mailGateway.message.attachmentName());
assertEquals("前一日筆數：1280\n成長率：12.5%", mailGateway.message.body());
```

完整測試在 [DailyReportServiceCharacterizationTest.java](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY19/src/test/java/com/ithome/day18/report/DailyReportServiceCharacterizationTest.java)。

第一次執行時，Maven 在受限環境解析建置相依項目時遭到阻擋，JUnit 尚未開始；我確認來源後才核准連線。接著先執行 `mvn -Dtest=DailyReportServiceCharacterizationTest test`，再執行 `mvn clean test`，兩次都是兩項通過並出現 `BUILD SUCCESS`。我再用 SHA-256 比對正式程式，執行前後雜湊值相同。這些證據只涵蓋縮小案例，尚未驗證正式 PDF、郵件伺服器或延遲寄出問題。完整命令與限制記在[驗證紀錄](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY19/docs/verification-log.md)。

![從行為基準、測試到正式程式雜湊的驗證節點](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day19/day19-05-verification-nodes.png)

## 小結：完成節點比待辦數量重要

我原本想讓 T2、T3 同時進行，實際對照檔案後才發現兩者都改 `runIfScheduled()`，於是改成循序；反過來，若每次只改一個變數名稱，交接成本又會超過得到的保護。我的切點以兩件事為準：失敗時能指出哪一段，完成時能拿出證據。Day 20 會沿用這份基準，處理延遲寄出疑點需要的測試與持續整合流程。

## 參考資料

- [OpenAI：Prompting](https://learn.chatgpt.com/docs/prompting)
- [OpenAI：Sandbox](https://learn.chatgpt.com/docs/sandboxing)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/)
- [日報服務需求書](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E6%97%A5%E5%A0%B1%E6%9C%8D%E5%8B%99-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
