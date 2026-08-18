# Day 22｜AI 輔助 Debug 實戰：合理解釋不是根因

![Day 22 封面：合理解釋不是根因，實驗才是證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day22/day22-01-cover.png)

Day 21 已確認日報服務會逐位讀資料、產生 PDF，再呼叫郵件閘道。需求書另有一條未查明的舊問題：客戶增加後，曾有報表接近發送時間才開始，導致部分信件延遲。我第一個直覺是資料量拖慢計算；但直覺只能當假設，不能直接寫進根因欄。為了示範方法，我先建立一個縮小假設：同步寄信會不會擋住後面客戶的報表？

## 先把症狀寫成可觀察的數字

我用兩位測試客戶重現這個假設，替每一段加入開始時間與耗時，再把 `Diagnostics.snapshot()` 整理成以下摘要。紀錄只留下測試代號、階段與毫秒數，不含收件人、附件內容、Token、內部網址或完整路徑。

```text
customer-001 prepare startedAt=0ms
customer-001 read=10ms pdf=40ms mail=900ms
customer-002 prepare startedAt=950ms
```

這段摘要只證明合成案例的第二份報表晚了 950 毫秒開始，尚未說明正式事故的原因。同樣症狀可能來自資料讀取、PDF 元件或郵件服務，先選一個最順眼的解釋，後面的修改就容易只是在配合答案。

![延遲症狀與三個待驗證根因假設](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day22/day22-02-symptom-vs-root-cause.png)

我把除錯表固定成四欄：症狀、能被實驗推翻的假設、最小實驗、結果。資料變慢就固定輸入，比較讀取時間；PDF 退化就換成測試替身，也就是用可控制行為取代外部元件的物件；郵件阻塞則只調整郵件替身的回應時間。一次改一個條件，結果才知道支持哪個假設。

## 讓 Codex 排假設，不准先改程式

[OpenAI 官方文件](https://learn.chatgpt.com/docs/prompting)建議 Codex 除錯任務要交代可重現行為、相關程式、限制與驗證方式。我把任務寫成：「先重現後面客戶較晚開始的現象，分段記錄 `read`、`pdf`、`mail`；每次只替換一個測試替身；證據足夠前不要修改正式流程。」完整內容放在[除錯任務](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY22/docs/debug-prompt.md)。

交付資料包時，我只放能重現問題的程式、測試與去識別化紀錄。正式日誌留在原管控範圍，不把整包客戶資料與憑證貼進對話。

![把三個合理解釋改寫成能被實驗推翻的假設](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day22/day22-03-hypothesis-table.png)

測試時鐘只會向前增加，且可由測試控制，不用 `sleep()` 等真實時間。讀資料固定為 10 毫秒、PDF 固定為 40 毫秒、郵件固定為 900 毫秒時，第二份在 950 毫秒開始；只把郵件等待改成 0，觀察值就變成 50 毫秒。資料與 PDF 假設在這個縮小案例不獲支持，證據指向同步等待郵件回應阻塞了下一份報表。

![只改郵件等待時間的最小實驗與結果](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day22/day22-04-minimal-experiment.png)

## 兩階段實驗只隔離準備與寄信

我沒有把實驗直接當成上線修正，而是先把流程切成兩階段：所有報表準備完成後，才進入寄信階段。

```java
List<PreparedReport> preparedReports = new ArrayList<>();
for (Customer customer : customers) {
    preparedReports.add(prepare(customer));
}
preparedReports.forEach(this::send);
```

保留 900 毫秒郵件等待後，第二份仍在 50 毫秒開始；但舊流程與兩階段流程的第二封信都在 1900 毫秒完成。這證明準備與寄信互相阻塞，沒有證明信件延遲已解決。`mvn clean test` 的 3 項測試全部通過，結果為 `BUILD SUCCESS`；程式與數字記在[回歸測試](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY22/src/test/java/com/ithome/day21/report/DailyReportBatchDebugTest.java)及[驗證紀錄](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY22/docs/verification-log.md)。

![兩階段實驗先準備全部報表，三項回歸測試通過](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day22/day22-05-fix-and-regression.png)

若要真正處理信件延遲，下一步還要設計有容量上限的郵件佇列與工作者，驗證佇列塞滿時如何限流、失敗後如何重試，以及重跑同一任務會不會重複寄信。上線前也要用正式監控確認延遲分布；臨時診斷、除錯旗標和測試資料則要移除。

## 小結：用實驗淘汰假設

ChatGPT 與 Codex 可以加速展開假設、搜尋呼叫點與執行實驗，但根因仍要由可重現結果支持。Day 23 會把這次確認的流程、驗證命令與未知邊界補回過時的專案文件，避免下一位維運者重新猜一次。

## 參考資料

- [OpenAI：Prompting](https://learn.chatgpt.com/docs/prompting)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/)
- [日報服務需求書](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E6%97%A5%E5%A0%B1%E6%9C%8D%E5%8B%99-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
