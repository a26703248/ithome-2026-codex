# Day 07｜用 ChatGPT 生成 API 規格與文件：讓 jobId 有下一步

![Day 07 封面：拿到 jobId，還不算流程完成](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day07/day07-01-cover.png)

Day 06 的匯入端點會建立非同步任務，回傳 `jobId`（任務識別碼）與 `PENDING`。我繼續往前端流程走，才發現後半段還是空白：要去哪裡查任務？除了等待，還有哪些結果？如果每個人各自補答案，前端可能沿著錯誤路徑進行固定間隔重複查詢（輪詢），後端增加狀態時也沒人知道。今天我先收窄範圍，只替「查詢一筆匯入任務」建立可核對的應用程式介面（Application Programming Interface，API）契約。

## 從既有 jobId 寫出決策白名單

OpenAPI 規格（OpenAPI Specification）用與程式語言無關的格式描述超文字傳輸協定（Hypertext Transfer Protocol，HTTP）介面。原始需求沒有定義查詢路徑與任務狀態，所以我把下表標成本文的工程示範，不回填成 v0（初版）需求事實。

| 決策 | 設定值                                                       |
|---|-----------------------------------------------------------|
| 方法與路徑 | `GET /imports/{jobId}`                                    |
| 路徑參數 | `jobId` 必填，格式為通用唯一識別碼（Universally Unique Identifier，UUID） |
| 找到任務 | `200`，回傳 `jobId`、`status`                                 |
| 狀態集合 | `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`                  |
| 無法取得 | `404`，回傳 `code` 與 `message`；代碼固定為 `IMPORT_NOT_AVAILABLE`  |
| 身分驗證 | 不在本文示範範圍，正式介面不可直接省略                                       |
| 規格版本 | OpenAPI `3.1.0`                                           |

這個範圍刻意很小。Day 06 已建立 `jobId` 與初始狀態，本文只補可追蹤的下一步；進度百分比、完成資料位置、失敗原因與輪詢間隔都沒有可靠決策，先不塞進契約。

![從 Day 06 的 jobId 接續查詢契約](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day07/day07-02-contract-flow.png)

## 提示詞改用白名單，不讓模型補缺口

延續一貫做法，我把限制寫得更像機器可檢查的規則。[完整提示詞](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY07/contract-prompt.txt) 用 `DECISIONS` 約束業務契約；OpenAPI 必填的標題與版本，以及本文採用的描述文字，則取自 `DOCUMENT_TEMPLATE`：

```text
不得擴充 HTTP 回應碼、狀態或資料欄位。
若任一項衝突，僅輸出 STOP_REVIEW 與衝突項目，不要產生規格。
生成後逐一列出業務內容與文件文字的來源鍵。
```

產生 [OpenAPI YAML](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY07/openapi.yaml) 後，我逐項回看白名單，尤其注意 `jobId` 的 UUID 格式、`200`／`404` 回應，以及 `status` 的四個列舉值（enum）。

![查詢契約的五個決策位置](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day07/day07-03-openapi-focus.png)

```yaml
/imports/{jobId}:
  get:
    responses:
      '200':
        description: The job state is available.
status:
  type: string
  enum: [PENDING, RUNNING, SUCCEEDED, FAILED]
```

這裡的 `200` 只代表查詢成功；回應中的 `status: FAILED` 仍表示匯入失敗。`404` 則固定回傳 `IMPORT_NOT_AVAILABLE`，程式依代碼分流，訊息文字留給人閱讀。把 HTTP 結果與任務結果分開，前端才不會看到綠色狀態碼就誤判工作完成。

## 用測試比對規格與 Spring Web

我沒有只檢查 YAML 能不能開啟。契約測試會確認方法是 `GET`、路徑參數採 UUID、回應集合恰好是 `200` 與 `404`，狀態集合也必須與決策表完全相同。Controller 則把查詢結果分成兩條明確路徑：

```java
Optional<ImportJobView> job = importJobs.find(jobId);
if (job.isPresent()) {
    return ResponseEntity.ok(job.get());
}
return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(new ApiError("IMPORT_NOT_AVAILABLE", "import job is not available"));
```

[ImportStatusController.java](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY07/src/main/java/com/ithome/day07/imports/ImportStatusController.java) 的 Java `ImportStatus` 也只有四個值。規格若新增 `CANCELLED`，Java 與測試必須一起修改，否則解析成功仍不代表契約一致。[範例 README](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY07/README.md) 的執行入口是 `mvn clean test`。本文重做後的四項測試尚待重新執行，因此這裡只記錄驗收範圍，不把它寫成通過結果。

![OpenAPI、Controller 與 JUnit 5 的逐項對映](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day07/day07-04-cross-check.png)

## Java 呼叫範例也只做一件事

[WorkspaceImportClient.java](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY07/src/main/java/com/ithome/day07/imports/WorkspaceImportClient.java) 使用 Java 17 內建的 `HttpClient` 送出 `GET`，不額外引入軟體開發套件（Software Development Kit，SDK）：

```java
var result = client.find(baseUri, jobId);
```

[對應測試](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY07/src/test/java/com/ithome/day07/imports/ClientExampleTest.java) 會建立 `client`、`baseUri` 與 `jobId`，啟動只在本機運作的測試伺服器，確認用戶端能讀到 `RUNNING`。它只驗證請求方法與回應讀取，不代表真實服務的權限、逾時與輪詢策略已完成。前端仍要依狀態決定下一步：等待中的任務繼續查詢，成功或失敗則停止，不能把收到 `200` 直接解讀成匯入成功。

![四種任務狀態對應前端下一步](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day07/day07-05-response-examples.png)

## 小結：契約讓非同步流程接得起來

這次我從 Day 06 已有的 `jobId` 出發，限定 ChatGPT 只能整理決策白名單，再用 OpenAPI、控制器與測試建立對映；Day 08 會沿用這種「先劃範圍、再找證據」的做法，練習學習陌生的排程技術。

## 參考資料

- [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0.html)
- [RFC 9110：HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [Spring Framework：Annotated Controllers](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/)
- [OpenAI：Prompt engineering best practices for ChatGPT](https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt)
- [資料工作區空間——需求書（v0．初版待釐清）](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E6%A1%88%E4%BE%8B/%E8%B3%87%E6%96%99%E5%B7%A5%E4%BD%9C%E5%8D%80%E7%A9%BA%E9%96%93-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
