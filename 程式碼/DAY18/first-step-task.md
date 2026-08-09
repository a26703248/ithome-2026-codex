# DAY18 第一小步任務契約

## 目標

替目前的日報產製流程建立特徵測試，鎖定既有外部行為，正式程式不得修改。

## 允許修改

- 新增 `DailyReportServiceCharacterizationTest`。
- 新增本任務的文件與驗證紀錄。

## 禁止修改

- 不修改 `src/main/` 任何檔案。
- 不抽介面、不搬檔、不重新命名、不格式化正式程式。
- 不實作新的頻率、Word、Excel 或提前一小時產製。
- 不處理 PDF 套件安全通知。

## 驗收

1. 08:00 會呼叫 PDF 元件，並將其回傳附件、前一日筆數、成長率與附件名稱交給郵件元件。
2. 07:59 不呼叫 PDF 或郵件元件。
3. `mvn -Dtest=DailyReportServiceCharacterizationTest test` 通過。
4. `mvn clean test` 通過。
5. `DailyReportService.java` 執行前後的 SHA-256 相同。

正式 PDF 檔案與郵件伺服器整合不在本次驗證範圍。

## 完成回報

- 新增檔案。
- 執行命令及結果。
- 正式程式雜湊。
- 未驗證風險與下一步前置條件。
