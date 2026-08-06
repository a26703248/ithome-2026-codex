# DAY07 三角色審查與發布前驗證

審查對象：`DAY07-用ChatGPT生成API規格與文件.md`

審查日期：2026-08-06

## 審查結論

| 審查角色 | 初審主要疑慮 | 處理結果 | 複核 |
|---|---|---|---|
| 著作權合規 | 初版沿用草稿「AI 建議」的 `500／422` 情境、POST 端點與 curl＋Java 組合 | 從 Day 05 已有的 `jobId` 重新推導 `GET /imports/{jobId}`；提示詞改用 `DECISIONS`／`DOCUMENT_TEMPLATE`；重做文章、程式與圖片 | 通過，草稿 AI 建議近似沿用估為 0% |
| 事實正確性 | 初版契約與控制器不完整對齊；新版白名單曾缺 OpenAPI 文件模板來源 | 移除舊版；補 `DOCUMENT_TEMPLATE`，刪除無來源的 operationId、summary、examples、`additionalProperties`；統一 200／404、UUID 與四個狀態 | 靜態內容通過；`mvn clean test` 待重跑 |
| 讀者清晰度與規範 | 初版 curl 無法直接重現、程式片段跳步、圖片路徑不一致；新版曾缺 UUID 全名與圖文狀態邊界 | 移除 curl；補完整程式與測試連結、名詞解釋、執行入口；五張圖全部重生並核對文字 | 編輯與發布格式通過；測試結果待補 |

## 著作權與引用檢查

- 本篇未使用 ISO／CNS、法律條文或 OWASP 授權內容，不需讀取或比對 `條文/` 正本。
- 新版開場的 `jobId`、`PENDING` 與查詢需求可回溯至 Day 05 成稿；`GET /imports/{jobId}`、200／404、四狀態與白名單提示詞是重新設計的素材。
- 已移除 DAY07 草稿「AI 建議」中的 500／422、POST 工作區端點、欄位錯誤與 curl＋Java 組合；複核估算近似沿用為 0%。
- OpenAPI、HTTP、Spring 與 OpenAI 官方文件只做短小的功能性轉述，沒有逐段翻譯或大量引用。
- 五張圖片由 `圖檔/Day07/generate_day07_images.py` 從空白畫布產生，只使用幾何圖形、文字與系統字型，未嵌入外部照片、圖示、商標或字型檔。

## 靜態事實與程式核對

- Day 05 已建立非同步匯入任務、`jobId` 與初始狀態 `PENDING`；本文清楚把查詢路徑、404 與其餘三個狀態標成工程示範，不冒充 v0 需求事實。
- OpenAPI、Spring Web 控制器與 Java 用戶端皆使用 `GET /imports/{jobId}`。
- `ImportJobView` 在 OpenAPI 與 Java 都只有 `jobId`、`status`；狀態均為 `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`。
- 404 回應在 OpenAPI 與 Java 都使用 `code`、`message`，且只有 `code` 固定為 `IMPORT_NOT_AVAILABLE`。
- `DECISIONS` 管理業務契約；`DOCUMENT_TEMPLATE` 提供 OpenAPI 的標題、版本、兩個 response description 與 schema 名稱。現有規格沒有無來源的業務限制。
- 契約測試靜態檢查 GET 路徑、200／404 的精確集合、UUID format 與四個 enum；控制器測試兩項，Java 用戶端測試一項，共四項。

## 測試狀態：待作者重跑

- 重做 GET 版本後嘗試執行 Maven，但 Codex 桌面環境因命令核准額度用完而拒絕啟動程序；這不是測試失敗，也不能算測試通過。
- 舊 POST 版本曾有六項測試通過，但該程式與契約已丟棄，結果不得當成新版證據。
- 發布前需在 `程式碼/DAY07/` 執行：

```shell
mvn clean test
```

- 只有看到 `Tests run: 4, Failures: 0, Errors: 0, Skipped: 0` 與 `BUILD SUCCESS`，才能把文章中的「尚待重新執行」更新為實際通過結果。

## 格式與產物檢查

- 全文排除圖片行約 1,001 個漢字，符合 900～1,100 字目標，也超過 300 字下限。
- 標題層級為一個 `#` 主標題，後續使用 `##`，沒有跳級。
- 五張圖片皆為 1280 × 720 px、16:9；文章使用 `raw.githubusercontent.com` 網址，且每張圖片獨立成行。
- API、OpenAPI Specification、HTTP、UUID 與 SDK 均在首次出現時補全名或中文說明。
- 範例統一使用 Java 17、Spring Web、Maven、JUnit 5 與 Java `HttpClient`，沒有混入其他程式語言。

## 作者發布前確認

- [ ] 在 `程式碼/DAY07/` 執行 `mvn clean test`，保存四項測試與 `BUILD SUCCESS` 紀錄。
- [ ] 若測試通過，把正文「尚待重新執行」改成實際結果；若失敗，先修正契約、程式或測試再發布。
- [ ] 親自在 ChatGPT 重跑 `contract-prompt.txt`，確認輸出沒有增加 DECISIONS 與 DOCUMENT_TEMPLATE 以外的業務內容。
- [ ] 圖片推送到 GitHub 後，確認五個 raw 網址能在 iThome 編輯器載入。
- [ ] 再次確認身分驗證、輪詢間隔、完成資料位置與失敗原因仍標為本文範圍外，沒有被讀者誤認為正式決策。
- [ ] 文章上線當日重新打開 OpenAPI、RFC、Spring、OpenAI 與 GitHub 連結。
- [ ] 發布後若需修改，於發布當日完成。
