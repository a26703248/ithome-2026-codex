# Day 07 可驗證範例

本目錄保存文章使用的 OpenAPI 契約、Spring Web 控制器與 JUnit 5 測試。案例從 Day 05 已建立的 `jobId` 與 `PENDING` 往下推進，示範前端如何查詢匯入任務；路徑、狀態集合與錯誤格式仍是本篇工程決策，不代表 `案例/資料工作區空間-需求書.md` 已確認。

執行：

```shell
mvn clean test
```

測試會檢查：

- Swagger Parser 能解析 `openapi.yaml`，且路徑、UUID 參數、回應與狀態集合符合決策清單。
- 控制器的 `200` 與 `404` 行為符合契約。
- Java `HttpClient` 範例能向本機測試伺服器送出查詢並讀到 `RUNNING`。

`圖檔/Day07/` 的五張 PNG 由 `generate_day07_images.py` 從空白畫布產生，只使用幾何圖形、文字與系統字型，沒有嵌入外部照片、圖示或字型檔。
