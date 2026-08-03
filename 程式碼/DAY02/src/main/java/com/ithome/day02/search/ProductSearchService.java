package com.ithome.day02.search;

import java.util.Comparator;
import java.util.List;
import java.util.Locale;

/**
 * 商品查詢服務。
 *
 * <p>依據 Day02 案例規格提供下列查詢行為：
 * <ol>
 *   <li>關鍵字比對忽略大小寫。</li>
 *   <li>先排序整體結果集，再依頁碼與每頁筆數切出資料。</li>
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
        String normalizedKeyword = keyword == null ? null : keyword.toLowerCase(Locale.ROOT);

        List<Product> filtered = repository.findAll().stream()
                .filter(p -> normalizedKeyword == null
                        || normalizedKeyword.isBlank()
                        || p.name().toLowerCase(Locale.ROOT).contains(normalizedKeyword))
                .filter(p -> category == null || category.isBlank() || category.equals(p.category()))
                .toList();

        List<Product> sorted = sort(filtered, sortBy);

        return sorted.stream()
                .skip((long) page * size)
                .limit(size)
                .toList();
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
