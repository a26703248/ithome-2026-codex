package com.ithome.day02.search;

import java.math.BigDecimal;

/**
 * 商品資料模型。
 *
 * @param id       商品編號
 * @param name     商品名稱（可能混合大小寫，例如 "iPhone 15 Pro" / "iphone 13"）
 * @param category 商品分類，例如「手機」「筆電」
 * @param price    商品售價
 * @param stock    庫存數量
 */
public record Product(String id, String name, String category, BigDecimal price, int stock) {
}
