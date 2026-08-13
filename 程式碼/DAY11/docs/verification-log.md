# DAY10 驗證紀錄

## 任務限制

- 每批最多匯入 500 筆，不能為整除資料多建立空批次。
- 0 筆資料應回傳 0 批。
- 只能修改 `CsvBatchPlanner.java`，不修改測試與建置設定。
- 完成後執行 `mvn clean test`，再檢查差異。

## 修正前

執行位置：`程式碼/DAY10/before-fix/`

```shell
mvn clean test
```

準備 DAY10 Maven 環境時，第一次執行先因沙箱阻擋 `maven-clean-plugin:2.5` 下載而失敗，JUnit 5 尚未開始。確認下載來源為 Maven Central 後核准此次連線。外掛與相依套件就緒後，再對修正前快照執行同一命令，得到真正的測試結果：

```text
Tests run: 5, Failures: 2, Errors: 0, Skipped: 0
CsvBatchPlannerTest.returnsZeroForNoRows expected: <0> but was: <1>
CsvBatchPlannerTest.returnsTwoForExactMultiple expected: <2> but was: <3>
BUILD FAILURE
```

## 最小修改

```diff
-        return rowCount / batchSize + 1;
+        int fullBatches = rowCount / batchSize;
+        return rowCount % batchSize == 0 ? fullBatches : fullBatches + 1;
```

## 修正後

執行位置：`程式碼/DAY10/`

```shell
mvn clean test
```

實際結果：

```text
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 人工檢查

- 已確認修正前後的測試與建置設定內容相同，主程式只調整批次計數。
- 已確認 0、200、1,000、1,001 筆與不合法批次大小五個案例全部通過。
- 尚未驗證非常大的 `rowCount` 對實際匯入佇列與記憶體的影響。
