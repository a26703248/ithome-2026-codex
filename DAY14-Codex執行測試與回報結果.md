# Day 14｜Codex 執行測試與回報結果：別只看綠燈

![Day 14 封面：從完成摘要回到可驗證證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day14/day14-01-cover.png)

Day 13 修完同日起訖的日期錯誤後，畫面出現 `BUILD SUCCESS`。但它沒有回答在哪裡執行、跑了哪些測試、是否有所略過，也沒有證明網頁上的報表能產出。這次我重讀工作紀錄，確認 Codex 的完成摘要能否指回證據。

## 我把驗證拆成四層

我會依序檢查重現、局部、完整與人工四層證據；綠色訊息只代表某次命令成功結束。

| 證據層次 | 要回答的問題 | 本案例做法 |
|---|---|---|
| 重現測試 | 原始缺陷真的存在嗎？ | 在 `程式碼/DAY13/reproduction/` 執行指定測試，得到 1 項錯誤 |
| 局部測試 | 直接修改的行為正確嗎？ | 修正後只跑 `ReportRangeServiceTest`，5 項通過 |
| 完整測試 | 既有單元測試有回歸嗎？ | 在 `程式碼/DAY13/` 執行 `mvn clean test` |
| 人工檢查 | 測試沒寫到的邊界有守住嗎？ | 核對程式碼差異（diff）、公開方法與未驗證項目 |

![四層驗證證據：從重現到人工檢查](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day14/day14-02-four-layers.png)

若新增的測試從未在舊程式上失敗，我無法確認它真的抓到客服回報的日期邊界。

## 我先讀命令，再讀結果

我先記錄工作目錄、完整命令與程序結束碼（exit code）。舊程式加入回歸測試後，實際紀錄是：

```text
工作目錄：程式碼/DAY13/reproduction
命令：mvn -Dtest=ReportRangeServiceTest test
結束碼：1
Tests run: 5, Failures: 0, Errors: 1, Skipped: 0
BUILD FAILURE
```

Maven Surefire Plugin（Maven 測試外掛）已將測試交給 JUnit Platform 執行，錯誤落在 `sameDayRangeContainsOneDay()`，才算重現缺陷。摘要中的 `Failures` 是斷言不符，`Errors` 是測試因例外中止，`Skipped` 則是未執行。修正後在 `程式碼/DAY13/` 跑指定類別與完整測試，結束碼均為 0，五項測試全數通過。

![從命令、測試執行鏈到結果摘要逐段判讀](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day14/day14-03-read-output.png)

重跑時受限環境無法連到 Maven Central，訊息是 `Permission denied: connect`。輸出停在從 Maven Central 下載建置外掛，JUnit 尚未啟動，應回報為「環境阻擋」。確認目的地後，我只開放本次建置需要的連線，再重跑同一命令。

## 測試通過後，我仍要看 diff

這次 diff 只有兩處：日期條件由 `!isAfter` 改成 `isBefore`，並新增 `sameDayRangeContainsOneDay()` 回歸測試，斷言同日起訖應回傳 1。`pom.xml`、既有測試及公開方法簽章都沒變，可排除刪除測試、放寬斷言或升級相依套件等假修正。

![diff 人工審查：程式條件、測試斷言與未變更邊界](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day14/day14-04-diff-review.png)

Codex 的審查畫面反映 Git 儲存庫目前的差異，不一定只有 Codex 寫入的內容。因此我先確認檔案清單與比較範圍；測試能證明被斷言的行為，不能替我審查需求範圍。

## 技術子任務完成，原始問題仍是部分完成

| 驗收條件 | 證據 | 狀態 | 後續行動 |
|---|---|---|---|
| 同日起訖回傳 1 | 回歸測試先錯 1 項，修正後通過 | 完成 | 保留測試避免復發 |
| 公開方法簽章與建置設定不變 | 原始碼 diff、`pom.xml` 相同 | 完成 | 進入程式碼審查 |
| 使用者可產出單日報表 | 尚未執行網頁、資料庫與端對端測試 | 未驗證 | 在測試環境跑完整報表流程 |

![驗收條件必須逐項對上證據與狀態](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day14/day14-05-acceptance.png)

若範圍是修正 `countInclusiveDays()`，技術子任務已完成；若範圍仍是「單日報表會失敗」，目前只能判定部分完成。只要回報實際命令、測試數量、程式差異、未驗證項目與下一步，審查者就不用猜「完成」涵蓋到哪裡。

## 小結：驗收要回到工作紀錄

我不會把 Codex 的最後一句當成驗收結果，而會回查命令、測試範圍、結束碼與程式差異。綠燈只涵蓋已執行且被寫成檢查的行為。Day 15 會接著處理：為了取得這些證據，檔案、指令、網路與憑證權限應開放到什麼程度。

## 參考資料

- [OpenAI：Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenAI：Integrated terminal](https://learn.chatgpt.com/docs/integrated-terminal)
- [OpenAI：Code review](https://learn.chatgpt.com/docs/code-review)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/)
- [Apache Maven：Maven Surefire Plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)
