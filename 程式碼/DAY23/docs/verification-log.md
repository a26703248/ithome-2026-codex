# Day 22 驗證紀錄

驗證日期：2026-08-09

## 驗證環境

- OpenJDK 17.0.10。
- Apache Maven 3.8.1。
- Windows 11。

這是本篇縮小案例的實測環境，不代表正式日報服務的執行環境。

## 過時指令

執行 `README-before.md` 留下的舊指令：

```shell
java -jar target/daily-report.jar --config config/prod.yml
```

結果：

```text
Error: Unable to access jarfile target/daily-report.jar
```

縮小專案沒有該 JAR、設定檔或正式啟動方式的證據，因此新版 README 移除這項指令並標為待確認，不另外猜一條看似合理的替代命令。

## 測試命令

```shell
mvn clean test
```

受限環境第一次阻擋 Maven 連到 Maven Central，建置停在外掛解析階段，JUnit 尚未執行。確認來源後核准連線，再以相同命令重跑。

成功結果：

```text
Running com.ithome.day22.report.ReportBatchDocumentationTest
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## 已驗證範圍

- `pom.xml` 的 Java 編譯目標為 17。
- 批次會先準備兩份測試報表，再進入兩次郵件呼叫。
- 郵件測試替身每次等待 900 毫秒時，第二份仍在 50 毫秒開始準備，但總時間仍為 1900 毫秒。

## 尚未驗證

- 正式日報服務的啟動參數、設定檔位置、環境變數與部署流程。
- 正式排程器、資料庫、PDF 元件與郵件服務。
- 佇列容量、重試、冪等性、交易與多執行個體行為。
