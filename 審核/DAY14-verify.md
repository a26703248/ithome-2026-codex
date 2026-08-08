# DAY14 發布前驗證

## 文章與圖片

- [x] 以中文字與全形標點計算為 1,090 字，落在 900～1,100 字目標範圍。
- [x] 延續 DAY13 的 `ReportRangeService` 日期邊界案例，並銜接 DAY15 權限與安全邊界。
- [x] 文章含 5 張圖片，皆為 1600 × 900（16:9）。
- [x] 5 張圖片均使用 `raw.githubusercontent.com` 網址，且每張獨立成行。
- [x] 圖片已逐張檢查，沒有文字溢出、裁切或失真。
- [x] 首次出現使用「程式碼差異（diff）」「程序結束碼（exit code）」與「Maven Surefire Plugin（Maven 測試外掛）」。

## 程式與測試證據

- [x] `程式碼/DAY13/before-fix/` 執行 `mvn clean test`：結束碼 0，4 項測試通過。
- [x] `程式碼/DAY13/reproduction/` 執行 `mvn -Dtest=ReportRangeServiceTest test`：結束碼 1，5 項測試中 1 項錯誤，0 項略過。
- [x] 重現錯誤為 `IllegalArgumentException`，堆疊指向 `ReportRangeService.java:14`。
- [x] `程式碼/DAY13/` 執行指定測試類別：結束碼 0，5 項測試通過。
- [x] `程式碼/DAY13/` 執行 `mvn clean test`：結束碼 0，5 項測試通過，失敗、錯誤、略過均為 0。
- [x] 受限環境的 `Permission denied: connect` 發生於 Maven 外掛下載階段，JUnit 尚未啟動，文章已正確分類為環境阻擋。
- [x] 三份 `pom.xml` 相同；程式差異只有一行日期條件與一項新增回歸測試，公開方法簽章及既有四項測試未變。

## 三角色審查

- [x] 著作權審查：未使用 ISO／CNS、法律或 CC 授權素材；官方文件僅作事實參考，圖片為本專案自行產生。
- [x] 著作權審查：已改掉與草稿「AI 建議」相同的小結標題，沒有直接沿用草稿建議文字。
- [x] 事實審查：已將「無回歸」改為「未發現回歸」，並將套件來源精確寫為 Maven Central。
- [x] 事實審查：Codex 整合終端與審查窗格敘述已依 2026-08-08 官方文件核對。
- [x] 編輯審查：已補上 `Failures`、`Errors`、`Skipped` 與結束碼說明。
- [x] 編輯審查：圖片已把 Surefire 改列為測試執行鏈，並統一「公開方法簽章」用語與完整工作目錄。

## 作者發布前確認

- [ ] 發布當日重新開啟 OpenAI、JUnit 與 Maven 參考連結，確認介面名稱與官方文件仍有效。
- [ ] 作者確認第一人稱敘述符合實際操作與個人判斷，並完成自己的改寫或補充後再發布。
- [ ] 若當日修改文章，同步更新圖片、測試數據與本驗證清單。
