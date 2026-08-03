# Day02 案例程式碼 — 商品查詢缺陷

對應文章：Day 02｜ChatGPT vs Codex：對話助手與沙箱編程代理的差異

## 情境

PM 轉述「站台的查詢結果好像怪怪的」，經 ChatGPT 協助釐清後整理成
[`docs/issue-report.md`](docs/issue-report.md)，對照
[`docs/product-spec.md`](docs/product-spec.md) 規格，
定位出 `ProductSearchService` 兩個可重現的缺陷，並交由 Codex 讀取三份素材後修正：

1. 關鍵字查詢大小寫敏感，導致查不到本該符合的商品。
2. 分頁邏輯先分頁、後排序，導致跨頁排序不連續。

## 專案結構

```
DAY02/
├── docs/
│   ├── issue-report.md    # 任務一：ChatGPT 協助整理的 Issue Report
│   ├── product-spec.md    # 產品規格書（節錄）
│   └── task2-verification.md  # 任務二：實際測試與修正範圍紀錄
├── pom.xml
└── src/
    ├── main/java/com/ithome/day02/search/
    │   ├── Product.java
    │   ├── ProductRepository.java
    │   ├── ProductSearchService.java   # 已修正的查詢服務
    │   └── SortBy.java
    └── test/java/com/ithome/day02/search/
        └── ProductSearchServiceTest.java  # 重現缺陷的測試（修正前應失敗）
```

## 使用方式

```bash
mvn test
```

目前三個測試均應通過。修正前，
`search_shouldIgnoreCase_whenMatchingKeyword` 與
`search_shouldKeepSortOrderConsistent_acrossPages` 會失敗，這是文章中
「任務二：修正可重現的缺陷，再交給 Codex」所示範的起點。Codex 讀取
`docs/issue-report.md`、`docs/product-spec.md` 與專案原始碼後，只調整關鍵字比對
及排序／分頁順序，未更動第三個既有通過的分類篩選行為。
