# Day 26 存取治理最小案例

本專案示範開發團隊自己使用 Codex 存取「AI 輔助生成系統」不同分級資料時，一段最小的
存取治理程式契約。它只驗證角色是否核准存取，以及稽核紀錄是否留存，不包含畫面、正式檔案
系統、單一登入或正式稽核儲存。

## 已實作的規則

- 資料分級分為公開、內部、限閱三級（示範順序，非公司已核定的正式分級）。
- 每個分級只有對應角色可以存取；角色不符會被拒絕。
- 使用目的欄位不可空白，否則直接拒絕。
- 不論核准或拒絕，都會新增一筆稽核紀錄，包含時間、角色、分級與用途。

## 執行測試

使用 Java Development Kit 17 與 Apache Maven，在本目錄執行：

```shell
mvn clean test
```

預期結果應包含：

```text
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

本次草擬是在沒有 Maven／JDK 編譯工具的環境完成，尚未實際執行上述指令，詳見
[`docs/verification-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY27/docs/verification-log.md)。作者發布前務必在本機重新執行並更新結果。

## 相關文件

- [`docs/governance-inventory.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY27/docs/governance-inventory.md)：使用案例盤點、六個治理面向與待角色確認清單。
- [`docs/verification-log.md`](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY27/docs/verification-log.md)：測試設計與待補的實際執行結果。
