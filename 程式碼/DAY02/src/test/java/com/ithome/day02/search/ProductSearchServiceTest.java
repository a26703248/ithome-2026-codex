package com.ithome.day02.search;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.Comparator;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * 這份測試對應產品規格書（docs/product-spec.md）與 issue-report.md 描述的預期行為，
 * 在 {@link ProductSearchService} 尚未修正前，兩個測試都會失敗——
 * 這正是 Day02 文章中「可重現的缺陷」，交給 Codex 讀取規格、修正程式、並讓測試轉綠的示範素材。
 */
class ProductSearchServiceTest {

    private ProductSearchService service;

    @BeforeEach
    void setUp() {
        service = new ProductSearchService(new ProductRepository());
    }

    @Test
    void search_shouldIgnoreCase_whenMatchingKeyword() {
        // 使用者以小寫「iphone」查詢，規格書要求關鍵字比對忽略大小寫，
        // 應同時找到 "iPhone 15 Pro" 與 "iphone 13"。
        List<Product> result = service.search("iphone", null, SortBy.NAME_ASC, 0, 10);

        assertEquals(2, result.size(),
                "關鍵字查詢應忽略大小寫，預期同時找到 iPhone 15 Pro 與 iphone 13");
    }

    @Test
    void search_shouldKeepSortOrderConsistent_acrossPages() {
        // 依價格由高到低排序，逐頁查詢並串接，結果應等同於「先排序、再整份切頁」。
        List<Product> expected = new ProductRepository().findAll().stream()
                .sorted(Comparator.comparing(Product::price).reversed())
                .toList();

        List<Product> page0 = service.search(null, null, SortBy.PRICE_DESC, 0, 3);
        List<Product> page1 = service.search(null, null, SortBy.PRICE_DESC, 1, 3);

        List<Product> actual = new java.util.ArrayList<>();
        actual.addAll(page0);
        actual.addAll(page1);

        assertEquals(expected.subList(0, 6).stream().map(Product::id).toList(),
                actual.stream().map(Product::id).toList(),
                "跨頁查詢的排序結果應與整體排序一致，不應該分頁後才各自排序");
    }

    @Test
    void search_shouldFilterByCategory() {
        List<Product> result = service.search(null, "耳機", SortBy.PRICE_ASC, 0, 10);

        assertEquals(2, result.size());
        assertEquals(new BigDecimal("7490"), result.get(0).price());
    }
}
