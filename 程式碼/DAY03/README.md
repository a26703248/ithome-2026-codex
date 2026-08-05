# Day03 案例程式碼 — 購物車總額計算缺陷

對應文章：Day 03｜打造你的 AI 開發環境總覽（「用一個小任務驗證環境真的可用」）

## 情境

一個刻意保留缺陷的最小 Java／Maven 專案：購物車在有商品時能正確計算總額並套用
滿額折扣，但空購物車呼叫 `calculateTotal()` 會因為除以 0 丟出
`ArithmeticException`。任務與驗收條件見 [`docs/task-brief.md`](docs/task-brief.md)。

這個案例的目的不是示範複雜的修復，而是讓讀者（或作者本人）走完一輪
「提出任務 → Codex 讀取並修改 → 跑測試 → 看差異 → 人工審查」的最短回饋迴圈，
藉此確認手上的 ChatGPT／Codex 環境真的可用，而不是只是安裝完成。

## 專案結構

```
DAY03/
├── docs/
│   ├── task-brief.md         # 任務描述與驗收條件
│   └── verification-log.md   # 驗證紀錄範本（待作者填入實際輸出）
├── pom.xml
└── src/
    ├── main/java/com/ithome/day03/cart/
    │   ├── CartItem.java
    │   └── ShoppingCart.java        # 含缺陷：空購物車計算總額會丟出例外
    └── test/java/com/ithome/day03/cart/
        └── ShoppingCartTest.java    # 修正前，空購物車測試應以 Error 結束
```

## 使用方式

```bash
mvn test
```

修正前，`calculateTotal_withEmptyCart_returnsZero` 應該失敗（Error，而非單純斷言不符）；
`calculateTotal_withTwoItems_appliesBulkDiscount` 應該通過。修正
`ShoppingCart.calculateTotal()` 讓空清單時直接回傳 0 之後，兩個測試都應該通過。

實際指令與輸出請記錄在 [`docs/verification-log.md`](docs/verification-log.md)，
不要用臆測的畫面或文字取代。
