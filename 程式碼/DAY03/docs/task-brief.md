# Day03 驗證任務：修正購物車空清單計算總額的例外

> 用途：這是 Day03「用一個小任務驗證環境真的可用」的任務說明，
> 供作者實際操作 ChatGPT／Codex 一輪，並把過程記錄進
> [`verification-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY03/docs/verification-log.md)，而不是直接當發布內容照抄。

## 任務描述

`ShoppingCart.calculateTotal()`（`src/main/java/com/ithome/day03/cart/ShoppingCart.java`）
在購物車有商品時運作正常，但購物車是空的時候呼叫它會丟出
`ArithmeticException: / by zero`，而不是回傳總額 0。

對應測試 `ShoppingCartTest.calculateTotal_withEmptyCart_returnsZero()`
（`src/test/java/com/ithome/day03/cart/ShoppingCartTest.java`）
在修正前應該會以 Error（非單純斷言失敗）結束。

## 驗收條件

- 空購物車呼叫 `calculateTotal()` 回傳 `0`，不再丟出例外。
- 既有測試 `calculateTotal_withTwoItems_appliesBulkDiscount()` 維持通過，
  滿額折扣邏輯不能被順手改掉。
- 修改範圍只涉及 `ShoppingCart.calculateTotal()` 的空清單判斷，
  不夾帶無關的格式化、重構或新增功能。
- `mvn test` 全部通過。

## 建議操作步驟

1. 對 ChatGPT 說明上述缺陷與期望行為，確認要修的是「空清單時的除法」，
   不是滿額折扣門檻本身。
2. 用選定的 Codex 入口（CLI／IDE 擴充功能／cloud）指向本專案，
   請它只針對 `calculateTotal()` 做最小修改。
3. 執行 `mvn test`，確認兩個測試都通過。
4. 用 `git diff` 或編輯器內建比對工具，人工檢查改動範圍是否符合驗收條件。
5. 把實際操作入口、指令、測試輸出與人工審查結論記錄進
   [`verification-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY03/docs/verification-log.md)。

## 安全與資料範圍

本任務不含真實客戶資料、金鑰或內部路徑，商品名稱與金額皆為示範用途，
可以放心整份交給 ChatGPT／Codex 處理。
