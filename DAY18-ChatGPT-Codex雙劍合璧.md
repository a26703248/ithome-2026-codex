# Day 18｜ChatGPT＋Codex 雙劍合璧：用任務契約接好規劃與執行

![Day 18 封面：從規劃走到可驗收的執行](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day18/day18-01-cover.png)

Day 17 我先誠實列出這套日報服務的現況與新需求之間的落差。把 Day 16 的交付方式套進來準備動手時，第一個碰到的還是規格落差：業務列了四種頻率，以及 PDF、Word、Excel 三種檔案格式，程式端卻有六項問題沒定案。Codex 若只看到功能清單，可能直接改動耦合的舊流程。此時缺的不是更多提示詞，而是哪些決策成立、何處必須停手。

## 交接物不是聊天紀錄，而是任務契約

依 OpenAI 官方文件建議：重要任務不只要說明結果，還要補上會影響判斷的專案資訊，並明訂產物與停手範圍；進入程式庫後，也要指出程式位置與完成檢查。我把這些內容整理成「任務契約」，讓它能脫離原本對話獨立閱讀。

| 角色 | 這次負責什麼 | 本次不授權它決定什麼 |
|---|---|---|
| ChatGPT | 整理需求、找缺口、比較切法 | 不能替業務決定未定規則 |
| 我 | 確認範圍、風險與驗收條件 | 不能把不確定性藏進提示詞 |
| Codex | 讀專案、修改、測試、回報 | 不能自行擴張需求 |

![ChatGPT、作者與 Codex 的接力流程](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day18/day18-02-handoff-flow.png)

## 先讓 ChatGPT 把資訊缺口攤開

我先附上[日報服務需求書](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E6%A1%88%E4%BE%8B/%E6%97%A5%E5%A0%B1%E6%9C%8D%E5%8B%99-%E9%9C%80%E6%B1%82%E6%9B%B8.md)，請 ChatGPT 區分「已知事實、推測、待確認問題」，再找出能獨立驗收的最小切片。這一步沒有請它寫程式：

```text
閱讀需求書後，先整理已知事實、技術推測與待確認問題。
不要替未決問題補答案，也不要開始實作。
只切出一個不改變既有寄信與 PDF 邏輯、可用單元測試驗收的任務，
最後依目標、背景、允許修改、禁止修改、驗收、測試、未知事項輸出。
```

![原始需求拆成事實、推測與待確認問題](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day18/day18-03-requirement-gaps.png)

我沒有按功能名稱直接切工作，而是先比較相依性，最後只留下以含時區時間為輸入與輸出的運算。它不用載入舊 PDF 套件，也不會啟動寄信流程；其他需求等規則確認後再另開任務。完整提問保存在 [planning-prompt.txt](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY18/planning-prompt.txt)。

## 把決定寫成可執行的任務契約

我確認後的契約只允許新增時間計算類別與測試：輸入含時區的指定發送時間，回傳提前一小時的製作開始時間。既有排程、寄信、PDF、資料庫與 API 一律不能修改。Word、Excel、多頻率與逾時的規則仍待確認，對應功能則列為本輪禁止實作。

```text
目標：新增可獨立測試的「製作開始時間」計算。
允許修改：新增 ReportProductionWindow 與對應測試。
禁止修改：既有排程、寄信、PDF、資料庫與公開 API。
驗收：08:00（Asia/Taipei）輸入必須得到同日 07:00，並保留時區。
必跑測試：mvn clean test
回報：檔案、命令、結果、未驗證風險。
```

![任務契約把範圍、驗收與未知事項寫清楚](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day18/day18-04-task-contract.png)

全文見 [task-contract.md](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY18/task-contract.md)。契約的重點不是格式漂亮，而是讓「沒做什麼」跟「做了什麼」同樣清楚。

## Codex 執行，再由我對照證據

依核准後的契約，本次範例新增 `ReportProductionWindow`，核心邏輯只有一件事：

```java
public ZonedDateTime productionStartsAt(ZonedDateTime deliveryAt) {
    return Objects.requireNonNull(deliveryAt, "deliveryAt").minusHours(1);
}
```

`ZonedDateTime` 保留日期、時間與時區；`minusHours(1)` 沿時間軸回推。若支援日光節約時間，須先確認「一小時」指六十分鐘或鐘面時間。

我檢查程式差異（diff），確認沒有修改禁止範圍；再執行 `mvn clean test`，兩項 JUnit 5 測試通過，分別驗證提前一小時與空值拒絕。這只證明時間計算符合契約，不代表週報、格式輸出或實際寄信已完成。

![規劃、修改、測試與殘留風險的對映](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day18/day18-05-verification-map.png)

實際命令見 [DAY18 驗證紀錄](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY18/docs/verification-log.md)。本次沒有替六項未決問題實作答案；單次案例也不足以宣稱固定效率提升。

## 小結：先核准契約，再讓工具接力

這次我把流程停在兩個人工關卡：執行前核准範圍，執行後核對證據。ChatGPT 整理結果通過前一關，才成為 Codex 任務；完成摘要通過後一關，才算交付。Day 19 會把同一套做法用在日報服務的耦合重構，逐步保留測試與回復空間。

## 參考資料

- [OpenAI：Prompting](https://learn.chatgpt.com/docs/prompting)
