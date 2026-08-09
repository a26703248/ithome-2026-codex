# Day 23 驗證紀錄

驗證日期：2026-08-09

## 驗證環境

- OpenJDK 17.0.10。
- Apache Maven 3.8.1。
- Windows 11。
- Spring Boot 4.1.0。
- Apache PDFBox 2.0.23。

這是公開縮小案例的實測環境，不代表正式日報服務的版本、相依或部署設定。

## 測試命令

```shell
mvn clean test
```

第一次執行被受限環境阻擋 Maven Central 連線，尚未進入編譯。核准連線後，建置依序發現 `@WebMvcTest` 缺少啟動設定、`@Validated` 無法代理 `final` 控制器，以及路徑驗證例外未固定轉成 400。其後把已停止開源支援的 Spring Boot 3.3.5 升至 4.1.0，舊版測試註解套件再次造成編譯失敗；改用 Boot 4.1 的 Web MVC 測試模組與 Spring Framework `@MockitoBean` 後，以相同命令重跑：

```text
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

六項測試涵蓋缺少身分物件、授權政策拒絕、錯誤客戶代號、未知格式、已授權請求獲得受理，以及 PDF 輸出檔頭。

## 相依版本與通知範圍

```shell
mvn dependency:tree "-Dincludes=org.apache.pdfbox:pdfbox"
```

結果固定為：

```text
org.apache.pdfbox:pdfbox:jar:2.0.23:compile
```

另以相依清單與詳細相依樹確認 `commons-logging` 1.3.6 仍由 Spring Core 7.0.8 帶入，有效範圍為 `compile`；PDFBox 的排除設定不代表整棵相依樹已移除該套件。本篇不把它誤記為已完成排除。

Apache PDFBox 官方安全頁指出，2.0.23 受 CVE-2021-31811 與 CVE-2021-31812 影響，觸發條件是載入特製 PDF；2.0.24 修正。縮小專案的 `PdfReportRenderer` 只建立新的 `PDDocument` 並輸出，搜尋 `PDDocument.load` 與 `Loader.loadPDF` 均無結果。這只能支持「目前縮小路徑未找到可達呼叫」，不能證明正式系統不受影響，也不能取代升級評估。

## 已修正與仍未知

- 修正：身分與客戶授權分開、輸入格式與長度受到限制、路徑驗證的 400 回應不附詳細內容、日誌不再記錄完整收件信箱。
- 已知但未在本文處理：PDFBox 2.0.23 升級與相容性測試應另開工作。
- 未知：正式系統的完整呼叫路徑與相依清單，以及 API 閘道、限流、佇列、跨節點冪等性、祕密管理與監控設定。
