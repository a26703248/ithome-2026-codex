# Day 22 Codex 文件更新任務

```text
目標：更新 README，讓第一次接觸此縮小專案的 Java 工程師能重現已驗證行為。

請讀取：
- pom.xml
- src/main/java/com/ithome/day22/report/ReportBatch.java
- src/test/java/com/ithome/day22/report/ReportBatchDocumentationTest.java
- README-before.md
- ../DAY21/docs/verification-log.md

可信來源順序：可重現測試與命令輸出 > 目前程式與建置設定 > 需求書 > 舊 README。

輸出限制：
1. 只修改 README.md 與必要的程式註解，不改正式行為與測試。
2. 不得由類別名稱推測正式排程、環境變數、部署方式或業務規則。
3. 找不到證據時標成「待確認」，並指出需要哪個角色或來源。
4. 註解只說明程式本身看不出的設計理由與限制，不逐行翻譯。
5. 不得寫入金鑰、內部網址、客戶資料或正式環境路徑。

完成後執行 mvn clean test，逐條核對 README 中的命令、版本、路徑與行為，
並回報已驗證內容、未知邊界與實際命令結果。
```
