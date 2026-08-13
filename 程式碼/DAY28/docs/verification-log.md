# Day 27 驗證紀錄

草擬日期：2026-08-10

## 環境（待作者本機執行後補齊）

- 建議：Windows 11、OpenJDK 17、Apache Maven 3.8 以上、JUnit Jupiter 5.13.4（比照 Day
  24～26 的既有環境）。
- 本次草擬環境只安裝 OpenJDK 11 的 JRE（缺 `javac`），也沒有 Maven，且沙盒對外網路
  受限、無法下載 Maven 或 JUnit 相依套件，因此只能以人工方式覆核程式邏輯與測試設計，
  尚未實際編譯或執行 `mvn clean test`。這一點與 Day 24／25 已附上真實建置輸出不同，
  作者發布前必須在本機重新執行並貼上實際結果，不可只沿用本文件的預期說明。

## 待執行指令

```shell
cd 程式碼/DAY27
mvn clean test
```

## 測試設計與預期結果（人工覆核，非實際執行輸出）

`OcrPreprocessorTest` 共 8 項測試：

1. `highConfidenceTextIsAccepted`：信心分數 0.95，預期 `ACCEPT`。
2. `exactAcceptThresholdIsAccepted`：信心分數剛好等於 0.90，預期仍為 `ACCEPT`（邊界案例）。
3. `midConfidenceGoesToManualReview`：信心分數 0.80，預期 `MANUAL_REVIEW`。
4. `exactManualReviewThresholdGoesToManualReview`：信心分數剛好等於 0.70，預期
   `MANUAL_REVIEW`，不是 `RETRY`（邊界案例，是策略 A 第一次生成時漏掉的部分）。
5. `lowConfidenceWithRetriesLeftIsRetried`：信心分數 0.50、重試次數 0，預期 `RETRY`。
6. `lowConfidenceRetryBudgetExhaustedIsRejected`：信心分數 0.50、重試次數已達上限 2，
   預期 `REJECT`。
7. `blankTextIsRejectedRegardlessOfConfidence`：文字為空白字串、信心分數 0.99，預期
   `REJECT`。
8. `nullTextIsRejected`：文字為 `null`、信心分數 0.99，預期 `REJECT`。

預期結果為 `Tests run: 8, Failures: 0, Errors: 0, Skipped: 0`，但這是依程式邏輯推演的
預期值，不是實際建置輸出；作者需在本機執行後，把真實的 `BUILD SUCCESS` 或失敗訊息
貼回本文件與 `README.md`。

## 證據邊界

即使本機執行通過，結果也只涵蓋 `OcrPreprocessor` 的記憶體內單元測試：信心分數分流
判斷本身。未驗證真正的 OCR 引擎輸出格式、重試佇列、檔案儲存、AI 草稿生成呼叫，或
`docs/cost-log.md` 中的分鐘數（那是撰寫過程的人工計時記錄，不是自動化量測）。方案
費用、API 計價與 token 用量仍待作者於發布日依當下最新資料查證。
