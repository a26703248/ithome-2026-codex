# Day 24｜安全與程式碼品質把關：測試通過，只證明你測過的那一部分

![Day 24 封面：安全檢查從清單、證據、判讀走到決策](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day24/day24-01-cover.png)

Day 23 留下一筆 PDF 套件通知。需求書還要新增 Word 與 Excel；縮小案例只把 `WORD`、`EXCEL` 列入格式清單，沒有實作兩種產出。現有測試通過，仍沒回答：請求者能否操作別的客戶？信箱會不會進入日誌？套件警示能否被觸發？

## 我把檢查拆成六層

我沒有用「掃描通過」結案，而是從需求與權限、程式行為、相依套件、資料與祕密、執行環境、維運與監控逐層提問。每格要附測試、命令、設定或官方通知；沒有證據就寫「待確認」。

![需求權限、程式行為、相依、資料祕密、執行環境與維運監控六層檢查](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day24/day24-02-six-layers.png)

[開放全球應用程式安全專案（Open Worldwide Application Security Project，OWASP）Top 10: 2025 的軟體供應鏈失效項目](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/)也涵蓋版本追蹤、可信來源、持續掃描與更新流程。本段由我依案例改寫，來源為 OWASP Top 10 Team；該頁採[姓名標示 3.0 未本地化（CC BY 3.0）](https://creativecommons.org/licenses/by/3.0/)授權。

## 先驗證身分，再驗證能否操作這位客戶

人工智慧（Artificial Intelligence，AI）修改草稿取得 `Principal` 後，就把路徑中的 `customerId` 交給服務。縮小專案未接入 Spring Security，只能確認請求帶有身分物件，不能驗證登入流程或客戶權限。修正版改由 `ReportAccessPolicy` 判斷。格式使用列舉，代表只能從固定清單選擇；客戶代號、檔名與信箱也限制格式及長度。`customerId` 路徑參數格式不符時只回傳 400，不附細節。

```java
if (principal == null) {
    return ResponseEntity.status(401).build();
}
if (!accessPolicy.canCreate(principal.getName(), customerId)) {
    return ResponseEntity.status(403).build();
}
```

在縮小端點裡，401 表示沒有 `Principal`；403 表示已有身分物件，但授權政策拒絕操作。這只驗證控制器分支，不能取代正式驗證中介軟體的整合測試。

縮小案例的[修改前方法片段](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY24/docs/ReportController-before.java.txt)與[修正版控制器](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY24/src/main/java/com/ithome/day23/report/ReportController.java)都保留在專案裡。

![Java 修改前後：將身分識別、客戶授權、輸入限制與日誌資料分開檢查](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day24/day24-03-code-review.png)

## 套件版本命中，不等於攻擊路徑成立

列出 Maven 相依與版本的 `mvn dependency:tree` 確認專案使用 Apache PDFBox 2.0.23。[Apache 官方安全頁](https://pdfbox.apache.org/security.html)指出，該版載入特製 PDF 時受 Common Vulnerabilities and Exposures（CVE）編號 CVE-2021-31811、CVE-2021-31812 影響，2.0.24 已修正。我的 `PdfReportRenderer` 只建立新文件；搜尋兩個載入方法都沒有結果。

![PDFBox 通知從版本、觸發條件、縮小呼叫路徑到正式系統未知範圍的判讀](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day24/day24-04-evidence-matrix.png)

我沒有把警示寫成「正式系統存在可利用漏洞」，也沒有直接關掉。縮小案例未找到載入路徑只是目前的反證；正式程式與完整相依仍未知，升級及相容性測試另開工作。

## Codex 初篩後，我再用清單找漏網之魚

參考 [OpenAI 官方安全變更審查案例](https://learn.chatgpt.com/use-cases/scan-code-changes-for-security)後，我在[審查提示](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY24/docs/review-prompt.md)鎖定修改前控制器與工作樹，要求 Codex 為每個發現附上程式位置、觸發條件、既有證據與缺少的驗證；第一輪只產生報告，不修改程式。

在我的初篩紀錄裡，Codex 先列出跨客戶授權缺口；套件警示加上呼叫路徑後，才沒有把「命中版本」寫成「已能攻擊」。人工六層複核又找到完整信箱進入日誌，修正版只記請求代號、客戶代號與格式；缺少的正式限流與佇列設定則列為未知。

![Codex 初篩、套件通知加呼叫路徑與人工六層複核的發現比較](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day24/day24-05-review-comparison.png)

最後執行 `mvn clean test`：6 項測試、0 項失敗、0 項錯誤，結果為 `BUILD SUCCESS`。範圍涵蓋身分、授權、客戶代號、格式、受理流程與 PDF 檔頭；[驗證紀錄](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY24/docs/verification-log.md)也整理未成功嘗試的原因。

## 小結：生成程式碼也要走完品質護欄

這次留下的不是掃描綠燈，而是一條能回到程式、命令與設定的判斷鏈。只有版本警示、沒有呼叫路徑，不能升級成事故，也不能直接關單。Day 25 會換到產品經理、品質保證、設計與維運視角，延續這套協作方式。

## 參考資料

- [OpenAI：Scan code changes for security](https://learn.chatgpt.com/use-cases/scan-code-changes-for-security)
- [Apache PDFBox：Security](https://pdfbox.apache.org/security.html)
- [OWASP Top 10:2025：A03 Software Supply Chain Failures](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/)
- [日報服務需求書](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E6%A1%88%E4%BE%8B/%E6%97%A5%E5%A0%B1%E6%9C%8D%E5%8B%99-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
