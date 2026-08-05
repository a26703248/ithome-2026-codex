package com.ithome.day03.cart;

import java.util.ArrayList;
import java.util.List;

/**
 * 購物車。
 *
 * <p><b>已知缺陷（刻意保留，作為 Day03 驗證環境用的任務）：</b>
 * {@link #calculateTotal()} 在購物車是空的時候，會因為除以 0 丟出
 * {@link ArithmeticException}，而不是回傳總額 0。
 * 這個缺陷應交給 Codex 修正，並用 {@code mvn test} 驗證。</p>
 */
public class ShoppingCart {

    /** 平均單品金額達到此門檻，套用滿額折扣。 */
    private static final int BULK_DISCOUNT_THRESHOLD = 500;

    /** 滿額折扣金額。 */
    private static final int BULK_DISCOUNT_AMOUNT = 50;

    private final List<CartItem> items = new ArrayList<>();

    public void addItem(CartItem item) {
        items.add(item);
    }

    public int itemCount() {
        return items.size();
    }

    /**
     * 計算購物車總額：先加總每項商品小計，
     * 再依「平均單品金額」判斷是否套用滿額折扣。
     */
    public int calculateTotal() {
        int subtotal = 0;
        for (CartItem item : items) {
            subtotal += item.totalPrice();
        }

        // 缺陷：items 為空時 items.size() 為 0，這一行會丟出 ArithmeticException。
        int averageItemPrice = subtotal / items.size();
        int discount = averageItemPrice >= BULK_DISCOUNT_THRESHOLD ? BULK_DISCOUNT_AMOUNT : 0;

        return subtotal - discount;
    }
}
