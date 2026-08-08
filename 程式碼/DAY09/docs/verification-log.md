# DAY09 驗證紀錄

執行日期：2026-08-08

## 修正前

進入獨立的 `before-review/` 測試夾具後執行：

```shell
mvn clean test
```

結果：`Tests run: 4, Failures: 3, Errors: 0, Skipped: 0`，`BUILD FAILURE`。

夾具保留 `review-input.diff` 的 `tryStart` 與 `finish` 缺陷，另外增加一個 package-private 的 `Set<String>` 建構子，讓測試可以注入 `BarrierSet` 並固定關鍵時序。這個建構子是測試接縫，不在待審 diff 內。

三個失敗分別為：

- null 輸入實際拋出 `NullPointerException`，不符合預期的 `IllegalArgumentException`。
- 兩個並行呼叫都回傳已啟動，預期只有一個成功。
- `finish(" Workspace-42 ")` 未移除正規化後的鍵，下一次啟動仍被拒絕。

## 最小修正

- 將空值與空白檢查集中到 `normalize`。
- 直接使用 `Set.add` 的回傳值決定是否成功登記，移除 `contains`／`add` 的先檢查再執行。
- `tryStart` 與 `finish` 共用同一個 `normalize`。

再次執行：

```shell
mvn clean test
```

結果：`Tests run: 4, Failures: 0, Errors: 0, Skipped: 0`，`BUILD SUCCESS`。

## 驗證邊界

- 並行測試讓兩個呼叫都在測試用 `BarrierSet.add` 抵達 `CyclicBarrier`，再執行底層 `delegate.add`；它固定的是程式呼叫順序，不代表兩個 CPU 指令在同一瞬間執行。
- 範例只驗證單一 Java 處理程序內的互斥；多執行個體部署仍需要資料庫、分散式鎖或其他跨程序協調機制。
- 測試沒有啟動 Day 08 的 Spring 排程，也沒有連接真實工作區或匯入服務。
