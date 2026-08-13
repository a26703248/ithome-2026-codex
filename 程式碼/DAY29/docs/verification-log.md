# Day 28 驗證紀錄

草擬日期：2026-08-10

## 環境（待作者本機執行後補齊）

- 建議：Windows 11、OpenJDK 17、Apache Maven 3.8 以上、JUnit Jupiter 5.13.4（比照
  Day 24～27 的既有環境）。
- 本次草擬環境只安裝 OpenJDK 11 的 JRE（缺 `javac`），也沒有 Maven，且沙盒對外
  網路受限、無法下載 Maven 或 JUnit 相依套件，因此只能以人工方式覆核程式邏輯、
  測試設計與 `docs/baseline-log.md` 的手算彙總數字，尚未實際編譯或執行
  `mvn clean test`。這一點與 Day 24／25 已附上真實建置輸出不同，作者發布前必須
  在本機重新執行並貼上實際結果，不可只沿用本文件的預期說明。

## 待執行指令

```shell
cd 程式碼/DAY28
mvn clean test
```

## 測試設計與預期結果（人工覆核，非實際執行輸出）

`ReviewMetricsCalculatorTest` 共 8 項測試：

1. `nullRecordsThrowsException`：`records` 傳入 `null`，預期丟出
   `NullPointerException`。
2. `emptyRecordsThrowsException`：`records` 為空清單，預期丟出
   `IllegalArgumentException`，而不是算出無意義的平均值或除以零。
3. `singleRecordAveragesEqualItsOwnValues`：單筆紀錄時，各項平均值應等於該筆
   紀錄本身的數值。
4. `multipleRecordsAverageDraftToFinalAndReviewMinutes`：兩筆紀錄
   （100/20、120/30 分鐘），預期平均為 110.0／25.0 分鐘。
5. `majorRevisionOrRejectRateCountsBothCategories`：4 筆中 1 筆
   `MAJOR_REVISION`、1 筆 `REJECTED`，預期比例為 0.5（兩者合計 2/4）。
6. `completionRateExcludesOnlyRejected`：3 筆中 1 筆 `MAJOR_REVISION`、1 筆
   `REJECTED`，預期完成率為 2/3（大幅修改仍算完成，只有否決不算）。
7. `avgCitationErrorCountAcrossRecords`：2 筆引用錯誤數分別為 2、0，預期平均
   為 1.0。
8. `baselineAndAiAssistedCohortsProduceDifferentMetrics`：套用
   `docs/baseline-log.md` 的 16 筆樣本資料（基準線／AI 協作各 8 筆），預期
   彙總結果與該文件第三節表格一致（例如基準線平均生成到定稿時間 104.0
   分鐘、AI 協作 62.0 分鐘）。此項數字已用獨立計算（手算加總後除以樣本數）
   覆核過一次，與程式邏輯結果相符，但仍未經 JUnit 實際執行確認。

預期結果為 `Tests run: 8, Failures: 0, Errors: 0, Skipped: 0`，但這是依程式
邏輯推演與手算覆核的預期值，不是實際建置輸出；作者需在本機執行後，把真實的
`BUILD SUCCESS` 或失敗訊息貼回本文件與 `README.md`。

## 證據邊界

即使本機執行通過，結果也只涵蓋 `ReviewMetricsCalculator` 的記憶體內單元測試：
聚合邏輯本身。未驗證真正的複核介面、資料庫寫入，或 `docs/baseline-log.md`
中生成到定稿時間、複核時間、引用錯誤數等欄位是否貼近實際系統運作情形——
這批資料是本次桌上演練依需求書情境設計的示範數字，不是正式系統上線後蒐集
的統計結果，不能直接當成客戶導入成效的證明。
