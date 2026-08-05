package com.ithome.day03.cart;

/**
 * 購物車內的單一品項：商品名稱、單價與數量。
 */
public class CartItem {

    private final String name;
    private final int unitPrice;
    private final int quantity;

    public CartItem(String name, int unitPrice, int quantity) {
        this.name = name;
        this.unitPrice = unitPrice;
        this.quantity = quantity;
    }

    public String getName() {
        return name;
    }

    public int getUnitPrice() {
        return unitPrice;
    }

    public int getQuantity() {
        return quantity;
    }

    /** 這一項品項的小計（單價 × 數量）。 */
    public int totalPrice() {
        return unitPrice * quantity;
    }
}
