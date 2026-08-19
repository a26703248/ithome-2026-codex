# Day 22 文件證據範例

這個 Java 17／Maven 縮小專案延續 Day 21 的兩階段實驗，用來示範如何從程式、測試與執行結果更新文件。它不是正式日報服務，也不會連接排程器、資料庫、PDF 元件或郵件服務。

## 可以重現的行為

- 批次會先完成所有測試客戶的報表準備，再進入寄信階段。
- 測試替身可證明慢速郵件回應不會延後第二份報表的準備時間。
- 兩階段實驗沒有縮短郵件總耗時，也沒有實作佇列、重試或冪等性。

## 前置條件

- Java Development Kit（JDK）17。
- Apache Maven；本篇驗證環境為 3.8.1。

## 執行測試

在本目錄執行：

```shell
mvn clean test
```

驗證成功時應包含以下摘要：

```text
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

完整的實測命令、版本與結果見 [`docs/verification-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY23/docs/verification-log.md)。

## 尚未確認，不應自行補寫

這份公開縮小專案沒有正式服務的啟動參數、設定檔位置、環境變數、部署流程及實際排程設定。需求書雖記錄既有系統每天 08:00 產生報表，但本專案沒有相應的執行期設定證據，因此不提供正式啟動或部署指令。

文件內容與證據的對應關係見 [`docs/source-map.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY23/docs/source-map.md)。
