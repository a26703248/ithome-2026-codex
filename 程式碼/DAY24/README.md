# Day 24 跨角色交接最小案例

本專案示範「複核與修改介面」背後的一小段 Java 契約。它只驗證複核決策與版本保留，不包含畫面、資料庫、正式驗證授權、稽核儲存或部署設定。

## 已實作的規則

- 複核決策包含採用、修改與否決。
- 修改會新增草稿版本，不覆蓋原始內容。
- 每種決策都必須填寫複核原因，並留下複核事件。
- 程式不提供自動發布或自動核准功能。

## 執行測試

使用 Java Development Kit 17 與 Apache Maven，在本目錄執行：

```shell
mvn clean test
```

成功結果應包含：

```text
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

完整實測結果見 [`docs/verification-log.md`](docs/verification-log.md)。
