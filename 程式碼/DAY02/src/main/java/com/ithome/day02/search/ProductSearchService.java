package com.ithome.day02.search;

import java.util.Comparator;
import java.util.List;

/**
 * 商品查詢服務。
 *
 * <p><b>本類別刻意保留 Day02 文章情境要修的缺陷，請勿在教學以外的地方直接使用：</b>
 * <ol>
 *   <li>關鍵字比對使用大小寫敏感的 {@code String#contains}，導致使用者用小寫關鍵字
 *       （例如 "iphone"）搜尋時，找不到名稱含大寫字母的商品（例如 "iPhone 15 Pro"）。</li>
 *   <li>分頁邏輯先分頁、後排序（{@code skip/limit} 在 {@code sort} 之前執行），
 *       導致跨頁的排序結果不連續，同一份查詢條件換頁後順序是錯的。</li>
 * </ol>
 * 對應產品規格書（docs/product-spec.md）第 2 節「關鍵字需忽略大小寫」與
 * 第 3 節「排序需在整體結果集上進行，分頁不得影響排序」。
 */
public class ProductSearchService {

    private final ProductRepository repository;

    public ProductSearchService(ProductRepository repository) {
        this.repository = repository;
    }

    /**
     * 查詢商品。
     *
     * @param keyword  關鍵字，可為 null 或空字串表示不篩選
     * @param category 分類，可為 null 或空字串表示不篩選
     * @param sortBy   排序方式
     * @param page     頁碼，從 0 開始
     * @param size     每頁筆數
     * @return 該頁的商品清單
     */
    public List<Product> search(String keyword, String category, SortBy sortBy, int page, int size) {
        List<Product> filtered = repository.findAll().stream()
                // BUG 1：關鍵字比對大小寫敏感，未依規格書要求忽略大小寫。
                .filter(p -> keyword == null || keyword.isBlank() || p.name().contains(keyword))
                .filter(p -> category == null || category.isBlank() || category.equals(p.category()))
                .toList();

        // BUG 2：應該先排序、再分頁；這裡先分頁、後排序，導致跨頁排序錯亂。
        List<Product> paged = filtered.stream()
                .skip((long) page * size)
                .limit(size)
                .toList();

        return sort(paged, sortBy);
    }

    private List<Product> sort(List<Product> products, SortBy sortBy) {
        Comparator<Product> comparator = switch (sortBy) {
            case PRICE_ASC -> Comparator.comparing(Product::price);
            case PRICE_DESC -> Comparator.comparing(Product::price).reversed();
            case NAME_ASC -> Comparator.comparing(Product::name, String.CASE_INSENSITIVE_ORDER);
        };
        return products.stream().sorted(comparator).toList();
    }
}
