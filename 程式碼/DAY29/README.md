# Day 28 複核指標量測工具

本專案示範「AI 輔助生成系統」需求書第七節提出、尚待回答的量測問題：系統
導入後如何量測是否真的縮短撰寫時間，以及草稿被大幅修改或否決的比例。
`ReviewMetricsCalculator` 把一批複核紀錄彙總成平均生成到定稿時間、平均複核
時間、大幅修改或否決比例、任務完成率、平均引用錯誤數，是 Day 28 文章「分析」
表格數字的計算依據，不含資料庫存取、報表輸出或真正的複核介面。

## 已實作的規則

- `ReviewMetricsCalculator.calculate()` 接受一批同批次（例如同一 cohort）的
  `ReviewRecord`，回傳 `ReviewMetrics`。
- 傳入 `null` 丟出 `NullPointerException`；傳入空清單丟出
  `IllegalArgumentException`，不會除以零算出誤導性的平均值。
- 「大幅修改或否決比例」把 `MAJOR_REVISION` 與 `REJECTED` 都算進分子。
- 「任務完成率」只把 `REJECTED` 視為未完成，`MAJOR_REVISION` 仍算完成
  （因為最終仍有定稿），這點與「大幅修改或否決比例」的定義不同，兩者要
  分開看，不能只看其中一個就下結論。

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

本次草擬是在沒有 Maven／完整 JDK（僅有 JRE，缺 `javac`）的環境完成，尚未
實際執行上述指令，詳見 [`docs/verification-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY29/docs/verification-log.md)。
作者發布前務必在本機重新執行並更新結果。

## 相關文件

- [`docs/baseline-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY29/docs/baseline-log.md)：撰寫本工具的配對前後測
  計時紀錄，以及套用本工具計算出的基準線／AI 協作批次比較數字，是文章兩個
  表格的原始資料。
- [`docs/verification-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY29/docs/verification-log.md)：測試設計與待補的
  實際執行結果。
