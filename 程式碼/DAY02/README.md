# Day02 案例程式碼 — 商品查詢缺陷

對應文章：Day 02｜ChatGPT vs Codex：對話助手與沙箱編程代理的差異

## 情境

PM 轉述「站台的查詢結果好像怪怪的」，經 ChatGPT 協助釐清後整理成
[`docs/issue-report.md`](docs/issue-report.md)，對照
[`docs/product-spec.md`](docs/product-spec.md) 規格，
定位出 `ProductSearchService` 兩個可重現的缺陷，交由 Codex 讀取三份素材後修正：

1. 關鍵字查詢大小寫敏感，導致查不到本該符合的商品。
2. 分頁邏輯先分頁、後排序，導致跨頁排序不連續。

## 專案結構

```
DAY02/
├── docs/
│   ├── issue-report.md    # 任務一：ChatGPT 協助整理的 Issue Report
│   └── product-spec.md    # 產品規格書（節錄）
├── pom.xml
└── src/
    ├── main/java/com/ithome/day02/search/
    │   ├── Product.java
    │   ├── ProductRepository.java
    │   ├── ProductSearchService.java   # 缺陷程式碼
    │   └── SortBy.java
    └── test/java/com/ithome/day02/search/
        └── ProductSearchServiceTest.java  # 重現缺陷的測試（修正前應失敗）
```

## 使用方式

```bash
mvn test
```

修正前，`search_shouldIgnoreCase_whenMatchingKeyword` 與
`search_shouldKeepSortOrderConsistent_acrossPages` 兩個測試會失敗，
即為文章中「任務二：修正可重現的缺陷，再交給 Codex」要示範的起點。
交給 Codex 時，建議一併提供 `docs/issue-report.md`、`docs/product-spec.md`
與本專案原始碼，並要求跑完 `mvn test` 確認全數通過、且未更動第三個
既有通過的測試（`search_shouldFilterByCategory`）行為。
