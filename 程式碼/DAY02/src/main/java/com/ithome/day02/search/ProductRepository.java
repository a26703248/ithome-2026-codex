package com.ithome.day02.search;

import java.math.BigDecimal;
import java.util.List;

/**
 * 商品查詢案例用的記憶體資料來源。
 *
 * <p>資料刻意混合大小寫命名（"iPhone 15 Pro" / "iphone 13"），
 * 用來重現 Day02 文章情境中「查詢結果好像怪怪的」缺陷。
 */
public class ProductRepository {

    private static final List<Product> PRODUCTS = List.of(
            new Product("P001", "iPhone 15 Pro", "手機", new BigDecimal("39900"), 12),
            new Product("P002", "iphone 13", "手機", new BigDecimal("21900"), 30),
            new Product("P003", "MacBook Air M3", "筆電", new BigDecimal("37900"), 8),
            new Product("P004", "MacBook Pro 14", "筆電", new BigDecimal("62900"), 5),
            new Product("P005", "AirPods Pro 2", "耳機", new BigDecimal("7490"), 50),
            new Product("P006", "AirPods Max", "耳機", new BigDecimal("16900"), 3),
            new Product("P007", "iPad Air", "平板", new BigDecimal("20900"), 20),
            new Product("P008", "iPad mini", "平板", new BigDecimal("15900"), 15)
    );

    public List<Product> findAll() {
        return PRODUCTS;
    }
}
