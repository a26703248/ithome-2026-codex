# Day 10｜Codex 是什麼？從回答走到可驗證的修改

![Day 10 封面：從回答走到可驗證的修改](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day10/day10-01-cover.png)

Day 09 已把匯入閘門的三個問題寫成紅燈測試。這次我換一個更小的缺陷：資料工作區每 500 筆切成一個批次，`CsvBatchPlanner` 卻會替 1,000 筆資料排出第三個空批次。我只把問題、限制與專案交給 Codex，刻意不提示錯在哪一行，觀察它能不能把修正做完並留下證據。

Day 02 的工具定位到這裡要落地了。我不靠介面名稱判斷代理，而是看它能否在約定範圍內持續取得新結果，再依結果修改專案。今天的觀察對象不是回答寫得像不像，而是最後能不能交出檔案、命令與測試紀錄。

## 我用四個檢查點看代理工作

OpenAI 官方文件目前將檢查檔案、修改程式與執行本機工具列為 Codex 命令列工作。我把「取得新結果，再調整下一個動作」的循環稱為代理迴圈（agent loop）。我用四個檢查點讀它的工作紀錄：

| 檢查點 | 我期待 Codex 做什麼 | 我留下什麼證據 |
|---|---|---|
| 定位 | 讀任務、規則、測試與相關原始碼 | 讀取範圍、問題重現方式 |
| 動作 | 選擇最小修改並執行必要命令 | 改過的檔案、命令紀錄 |
| 驗證 | 分辨工具失敗與測試失敗，再檢查程式碼差異（diff） | 退出碼、測試摘要、實際差異 |
| 交付 | 說明成果，也列出尚未覆蓋的風險 | 可重現步驟、未解事項 |

![Codex 的四個代理工作檢查點](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day10/day10-02-agent-loop.png)

任何一格出現新線索，都可能回到前面重新定位。卡在權限、相依套件或需求矛盾時，停下並說清楚阻礙，也比假裝修好更有用。

## 面對一個動作，我先問兩個問題

第一題是「這個命令現在碰得到什麼？」檔案、指令與網路能走到哪裡，由沙箱（sandbox）這層執行限制決定。第二題是「若要跨出去，誰來開門？」核准策略決定 Codex 何時必須停下請求核准；請求可以交給使用者，也可以依組織設定由其他審查機制處理。

![工作範圍與越界核准的兩個問題](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day10/day10-03-boundary.png)

我這次只開放專案工作區寫入，外部網路則保留核准。這些限制能縮小影響面，不能判斷需求是否正確；測試設計、機密資料與正式環境仍要由人把關。

## 實測：整批資料多出一個空批次

任務規則是「每批最多 500 筆；剛好整除時不能新增空批次，0 筆應為 0 批」。提示詞限制只能修改 `CsvBatchPlanner.java`，不得變更測試與 `pom.xml`，完成後要執行 `mvn clean test` 並說明剩餘風險。

準備 DAY10 的 Maven 環境時，第一次執行先出現 `Permission denied: connect`，當時 Maven 要從 Maven Central 下載建置外掛 `maven-clean-plugin`，Java 測試框架 JUnit 5 根本還沒開始。我確認來源後，只核准這次建置需要的連線。環境就緒後再對修正前快照執行同一命令，結果才顯示 `Tests run: 5, Failures: 2`：0 筆被算成 1 批，1,000 筆被算成 3 批。

![從環境阻礙到定位批次計算錯誤](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day10/day10-04-work-log.png)

原始程式不論有沒有餘數都加一。Codex 保留既有參數檢查，只改計數方式：

```diff
-        return rowCount / batchSize + 1;
+        int fullBatches = rowCount / batchSize;
+        return rowCount % batchSize == 0 ? fullBatches : fullBatches + 1;
```

重跑同一命令後，0、200、1,000、1,001 筆與不合法批次大小五項測試全部通過。我再檢查 diff，確認測試與建置設定沒有被改寫。完整的[任務提示詞](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY10/task-prompt.txt)、[程式碼與修正前版本](https://github.com/a26703248/ithome-2026-codex/tree/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY10)及[驗證紀錄](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY10/docs/verification-log.md)都可重現。

![修改、測試與人工審查三份交付證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day10/day10-05-evidence.png)

## 小結：我只收證據，不收一句「好了」

Codex 把找檔、改碼、跑工具與整理結果接成一條工作脈絡。它跑得越順，我越會追問三件事：改動是否符合需求、邊界案例是否真的被測到、沒有驗證的部分是否攤在回報裡。任何一題答不出來，我就把任務退回定位階段。Day 11 會接著比較命令列介面、整合開發環境擴充功能與 Codex cloud，選出適合自己的工作入口。

## 參考資料

- [OpenAI：Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenAI：Codex 沙箱](https://learn.chatgpt.com/docs/sandboxing)
- [OpenAI：代理核准與安全](https://learn.chatgpt.com/docs/agent-approvals-security)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/index.html)
- [Apache Maven Surefire Plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)
