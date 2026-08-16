# Repository instructions

## Scope
- 本規範適用於此目錄下的所有檔案。

## Project
- 使用 Java 17 與 Maven。
- 正式程式碼位於 src/main/java；測試程式碼位於 src/test/java。

## Change boundaries
- 修 bug 時，除非任務明確允許，否則不要修改測試檔案或 pom.xml。
- 新增相依套件、刪除檔案，或變更公開 API 之前，請先詢問。

## Verification
- 修改 Java 程式碼後，執行 mvn clean test。
- 若指令無法執行，請回報確切的錯誤訊息，不要宣稱測試已通過。

## Completion report
- 列出已變更的檔案、執行過的指令、測試結果，以及尚存的風險。