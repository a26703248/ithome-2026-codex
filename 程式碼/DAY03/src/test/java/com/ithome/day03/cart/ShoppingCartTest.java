package com.ithome.day03.cart;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ShoppingCartTest {

    @Test
    void calculateTotal_withTwoItems_appliesBulkDiscount() {
        ShoppingCart cart = new ShoppingCart();
        cart.addItem(new CartItem("藍牙耳機", 800, 1));
        cart.addItem(new CartItem("保護殼", 200, 1));

        // 小計 1000，平均單品金額 500 達到門檻，套用滿額折扣 50。
        assertEquals(950, cart.calculateTotal());
    }

    @Test
    void calculateTotal_withEmptyCart_returnsZero() {
        ShoppingCart cart = new ShoppingCart();

        // 修正前：這一行會因為除以 0 丟出 ArithmeticException，測試會以 Error 結束。
        // 修正後：空購物車應直接回傳總額 0。
        assertEquals(0, cart.calculateTotal());
    }
}
