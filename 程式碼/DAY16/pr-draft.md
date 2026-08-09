# 修正同日起訖的報表日期範圍

## 原始問題

`ReportRangeService.countInclusiveDays()` 把起日等於迄日判定為非法範圍，導致單日報表無法進入後續產製流程。

## 修改內容

- 將非法範圍判斷收斂為「迄日早於起日」。
- 新增同日起訖應回傳 1 的回歸測試。
- 不修改公開方法簽章、既有斷言、建置設定或相依套件。

## 驗證證據

```text
命令：mvn clean test
結果：Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
結束碼：0
```

提交前另執行 `git diff --cached --check`，並人工確認 staged diff 只有主程式與對應測試。

## 風險與未完成事項

- 尚未執行網頁、資料庫與端對端測試。
- 尚未確認單日報表的實際輸出內容。
- PR 合併前仍需由維護者檢查需求邊界與測試覆蓋。

