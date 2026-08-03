# 任務二驗證紀錄

> 本紀錄整理自 2026 年 8 月 3 日的實際終端輸出，供 Day02 文章與圖 4 核對；僅摘錄結果，不把工具輸出改寫成產品規格。

## 修正前

第一次在一般沙箱執行 `mvn test` 時，Maven 無法由 Maven Central 下載
`maven-resources-plugin:2.6`，回報 `Permission denied: connect`，因此尚未進入測試階段。
取得網路與 Maven 快取權限後再次執行，JUnit 5 結果如下：

```text
Tests run: 3, Failures: 2, Errors: 0, Skipped: 0
BUILD FAILURE
```

失敗測試為：

- `search_shouldIgnoreCase_whenMatchingKeyword`：預期 2 筆，實際 1 筆。
- `search_shouldKeepSortOrderConsistent_acrossPages`：預期商品 ID 為
  `[P004, P001, P003, P002, P007, P006]`，實際為
  `[P001, P003, P002, P004, P006, P005]`。

分類篩選測試 `search_shouldFilterByCategory` 通過。

## 修正範圍

`ProductSearchService` 只調整兩項查詢行為：以 `Locale.ROOT` 正規化關鍵字與商品名稱，
讓比對忽略大小寫；先排序完整結果集，再依 `page` 與 `size` 分頁。分類篩選條件未修改，
也沒有順手重構其他行為。README 與 JavaDoc 只同步更新已修正狀態。

## 修正後

一般沙箱再次因相同的 Maven 外掛下載權限而中止；取得權限後執行完整的 `mvn test`，
結果如下：

```text
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 尚未驗證與殘留風險

依 `product-spec.md` 第 5 節，本次未處理關鍵字前後空白、特殊字元比對與千筆以上資料的
查詢效能。這些項目是已知但尚待釐清的範圍，不應由本次測試結果推論為已符合需求。
