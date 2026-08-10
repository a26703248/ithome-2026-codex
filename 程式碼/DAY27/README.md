# Day 27 OCR 前處理分流與成本紀錄

本專案示範「AI 輔助生成系統」ETL 前處理流程中，OCR 辨識完成後依信心分數分流的
最小邏輯，並附上撰寫測試當下實際記錄的計時資料，作為 Day 27 文章「總成本」表格與
「兩種任務策略」比較的依據。程式本身只驗證分流判斷，不含真正的 OCR 引擎、佇列或
檔案系統。

## 已實作的規則

- 信心分數達到 0.90（含）以上直接接受（`ACCEPT`）。
- 信心分數在 0.70（含）～0.90 之間交由人工複核（`MANUAL_REVIEW`）。
- 信心分數低於 0.70 且重試次數未達上限，退回重新辨識（`RETRY`）。
- 信心分數低於 0.70 且重試次數已達上限，或辨識文字為空白／`null`，直接退回（`REJECT`）。
- 門檻值為本次案例示範設定，不是公司已核定的正式標準。

## 執行測試

使用 Java Development Kit 17 與 Apache Maven，在本目錄執行：

```shell
mvn clean test
```

預期結果應包含：

```text
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

本次草擬是在沒有 Maven／完整 JDK（僅有 JRE，缺 `javac`）的環境完成，尚未實際執行
上述指令，詳見 [`docs/verification-log.md`](docs/verification-log.md)。作者發布前務必在
本機重新執行並更新結果。

## 相關文件

- [`docs/cost-log.md`](docs/cost-log.md)：撰寫本測試檔過程中，兩種任務策略的實際計時
  紀錄，是文章成本表格的原始資料。
- [`docs/verification-log.md`](docs/verification-log.md)：測試設計與待補的實際執行結果。
