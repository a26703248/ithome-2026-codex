# Day 06｜AI 輔助系統設計：讓 ChatGPT 攤開選項，不替團隊拍板

![Day 06 封面：先比較代價，再決定架構](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day06/day06-01-cover.png)

Day 05 第二輪加入兩個會影響架構的示範條件：每日約 `1 TB`，資料來源速率約 `12 MB/s`。若兩者都以十進位計算，而且 `12 MB/s` 是可持續的端到端有效速率，光是傳輸就超過 23 小時。這時若把整批工作綁在同步的超文字傳輸協定（Hypertext Transfer Protocol，HTTP）請求裡，逾時、重送與部分失敗都會變得難處理；但因此立刻拆成多個服務，也可能只是增加維運負擔。

## 先給限制，再請 ChatGPT 提方案

我把 Day 05 的需求書、示範條件與未知資訊放在同一個 ChatGPT 專案裡。ChatGPT 專案能集中對話、檔案與專案指示，不過「放進專案」不代表內容已經正確，我仍要分開文件事實、示範輸入與工程推論。

![先把設計限制與未知資訊放進同一張圖](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day06/day06-02-constraints.png)

我沒有用「請給我最佳架構」這樣直接得到答案的提示詞，而是要求它用相同維度比較三個候選方案。完整提示詞放在 [Day 06 架構比較提示詞](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY06/architecture-prompt.txt)，核心限制如下：

```text
提出三個可逐步演進的候選架構，不要替團隊選定答案。
每個方案都要說明元件責任、資料流、失敗復原、資料一致性、
部署影響、監控需求與尚待確認事項。
區分文件事實、示範條件與工程推論；無法估算就直接寫明。
```

這種寫法也符合 OpenAI 對提示詞的建議：先給清楚且具體的背景，再根據第一輪輸出逐步補條件。我的第二輪追問不是「哪個最好」，而是「哪項證據會讓方案升級或淘汰」。

## 用同一把尺比較三個方案

先補兩個名詞：模組化單體是「內部分模組、整體仍單一部署」；訊息代理則是在元件間暫存並轉交訊息的基礎設施。

![三個候選架構的責任邊界](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day06/day06-03-options.png)

| 方案 | 優點 | 主要代價 | 適用證據 |
|---|---|---|---|
| 同步單體 | 元件少，容易先做 | 長時間請求與重送難控制 | 實測確認批次小、處理時間短 |
| 模組化單體＋非同步任務 | 匯入與編輯流程分開，仍維持單一部署 | 要管理任務狀態、重送與待處理任務 | 匯入耗時，但尚無獨立擴充證據 |
| 獨立匯入服務＋訊息代理 | 可獨立擴充，並縮小部分故障影響 | 多出部署、監控與跨服務一致性成本 | 壓測或事故證明單一部署已成瓶頸 |

需求書沒有部署環境、事故率與團隊技能資料，所以維運成本目前無法量化。我寧可保留空白，也不把生成的數字當成證據。

## 我先選可演進的最小邊界

第一版我選「模組化單體＋非同步任務」做驗證：匯入應用程式介面（Application Programming Interface，API）只建立任務並回傳識別碼，背景工作元件（Worker）讀取任務、轉換來源欄位，再寫入工作區。排程與手動匯入走同一條流程；訊息代理與獨立服務先不加入，但保留日後拆分的介面。

![第一版資料流：API 建立任務，背景工作元件執行匯入](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day06/day06-04-selected-flow.png)

Spring Boot 控制器先回傳 `202 Accepted`，表示伺服器已接受請求，但處理尚未完成，也不保證最後成功：

```java
@PostMapping("/imports")
ResponseEntity<ImportJobView> submit(@RequestBody ImportCommand command) {
    UUID jobId = importJobs.enqueue(command);
    return ResponseEntity.accepted().body(new ImportJobView(jobId, "PENDING"));
}
```

這段程式只確立邊界，還不是完整解法。前端取得 `jobId` 後，還要用查詢 API 取得任務結果。任務表要保存狀態與錯誤原因；同一批資料重送時要有「冪等鍵」，也就是避免重複寫入的識別值；待處理任務清單（工作佇列）也要有容量上限與告警。Spring Boot 雖可設定非同步執行器與排程器，我仍要依壓測結果設定資源。

## 決策後，先寫失敗條件

![架構決策紀錄：現在採用、暫緩項目與驗證門檻](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day06/day06-05-decision-record.png)

我會用接近 `12 MB/s` 的來源流量做壓測，觀察工作區編輯延遲、任務積壓與資料庫寫入；再刻意中斷處理，確認重啟後不會漏資料或重複寫入；最後用兩個租戶，也就是兩個客戶的獨立資料範圍，驗證資料隔離。若背景工作元件長期追不上來源、拖慢前台，或匯入故障持續影響前台，才有證據把它拆成獨立服務。

## 小結：設計由證據推進

這次留下的不是 ChatGPT 對方案的排名，而是可核對的比較欄位與重評門檻。Day 07 會把這份架構落成可驗證的 API 規格與文件。

## 參考資料

- [OpenAI：Prompt engineering best practices for ChatGPT](https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt)
- [OpenAI：Projects in ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt)
- [Spring Boot：Task Execution and Scheduling](https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html)
- [NIST：SI prefixes](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes)
- [資料工作區空間——需求書（v0．初版待釐清）](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E8%B3%87%E6%96%99%E5%B7%A5%E4%BD%9C%E5%8D%80%E7%A9%BA%E9%96%93-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
