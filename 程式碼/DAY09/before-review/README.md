# 修正前可重現測試夾具

這個獨立 Maven 專案保留 `review-input.diff` 的三個業務方法缺陷。為了讓並行時序可以穩定重現，類別額外加入一個 package-private 的 `Set<String>` 建構子；這個測試接縫不在原始 diff 中，也不改變 `tryStart` 與 `finish` 的缺陷行為。

執行：

```shell
mvn clean test
```

預期結果：`Tests run: 4, Failures: 3, Errors: 0, Skipped: 0`，建置失敗。這裡的失敗是刻意保留的紅燈基準，不是可部署版本。
