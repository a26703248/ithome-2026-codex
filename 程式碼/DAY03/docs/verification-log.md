# Day03 驗證紀錄

> 本紀錄對應 [`task-brief.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY03/docs/task-brief.md) 的實際操作結果。
> 文章與圖 5 只採用以下已確認資訊；發布當日仍須重新查證產品介面與版本。

## 操作日期與環境

- 日期：2026-08-05
- 作業系統：Windows 11
- JDK：OpenJDK 17.0.10
- Maven：3.8.1
- JUnit：5.10.2（由 `pom.xml` 確認）
- Git：2.36.1.windows.1
- 使用的 Codex 入口：Codex App

## 修正前：執行 `mvn test`

```text
[ERROR] Tests run: 2, Failures: 0, Errors: 1, Skipped: 0
[ERROR] ShoppingCartTest.calculateTotal_withEmptyCart_returnsZero:25
        ArithmeticException: / by zero
[INFO] BUILD FAILURE
```

## 修正範圍

Codex 只修改 `ShoppingCart.java` 的 `calculateTotal()`，在計算平均單品金額前加入：

```java
if (items.isEmpty()) {
    return 0;
}
```

測試檔與既有滿額折扣邏輯均未修改。

## 修正後：執行 `mvn test`

```text
[INFO] Running com.ithome.day03.cart.ShoppingCartTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

## 人工審查結論

- 改動是否僅限驗收條件範圍：是，僅增加空清單提前回傳。
- 是否夾帶無關格式化／重構：由 Codex 變更檢視畫面確認沒有。
- 是否可以安心提交：測試與修改範圍已通過本次技術驗證；正式提交前仍須完成 `AGENTS.md` 規定的三角色審查。

## 遇到的問題與處理方式

在受限環境重新執行 `mvn test` 時，Maven 起初無法連線下載
`maven-resources-plugin`，因此尚未進入 JUnit 測試。確認下載來源為 Maven Central 後，
核准本次 `mvn test` 所需的網路存取，再次執行後兩項測試全部通過。
