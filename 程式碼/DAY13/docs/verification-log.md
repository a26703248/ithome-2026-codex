# DAY13 工作與驗證紀錄

## 環境

- Java：OpenLogic OpenJDK 17.0.10
- Maven：3.8.1
- JUnit：5.13.4
- Maven Surefire Plugin：3.5.3

Maven 第一次需要下載建置外掛時，沙箱阻擋外部連線。確認來源為 Maven Central 後，只核准本次建置需要的連線，再重跑相同命令。以下測試摘要皆來自成功啟動 JUnit 後的結果。

## 1. 讀取與初步假設

讀取檔案：

- `AGENTS.md`
- `pom.xml`
- `before-fix/src/main/java/com/ithome/day13/report/ReportRangeService.java`
- `before-fix/src/test/java/com/ithome/day13/report/ReportRangeServiceTest.java`

觀察結果：多日範圍透過 `ChronoUnit.DAYS.between(...) + 1` 同時計入起日與迄日。既有驗證條件使用 `!endDate.isAfter(startDate)`，會把「相等」和「早於」一起拒絕；初步假設是邊界判斷寫得過嚴。

## 2. 既有測試基線

在 `before-fix/` 執行：

```text
mvn clean test
```

摘要：

```text
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 3. 新增回歸測試後重現缺陷

在 `reproduction/` 執行：

```text
mvn -Dtest=ReportRangeServiceTest test
```

摘要：

```text
Tests run: 5, Failures: 0, Errors: 1, Skipped: 0
java.lang.IllegalArgumentException: endDate must not be before startDate
at com.ithome.day13.report.ReportRangeService.countInclusiveDays(ReportRangeService.java:14)
BUILD FAILURE
```

## 4. 最小修正

```diff
-if (!endDate.isAfter(startDate)) {
+if (endDate.isBefore(startDate)) {
```

三份 `pom.xml` 完全相同。除了新增 `sameDayRangeContainsOneDay()`，既有測試、相依套件與公開方法簽章均未修改。

## 5. 修正後完整驗證

在 DAY13 專案根目錄執行：

```text
mvn clean test
```

摘要：

```text
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 6. 未驗證與人工審查

- 未執行網頁操作、資料庫或端對端報表測試。
- 未檢查單日報表實際輸出內容，只驗證日期範圍計數。
- 人工確認主程式只改一個條件，沒有無關格式化或重構。
