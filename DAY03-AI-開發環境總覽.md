# Day 03｜打造你的 AI 開發環境總覽

![Day 03 封面：讓上下文留在工作現場](./%E5%9C%96%E6%AA%94/Day03/day03-01-cover.png)

Day 02 談完 ChatGPT 與 Codex 的分工後，但「選對工具」只解決一半問題，操作介面選錯一樣會卡手。今天的案例是要修正 Java 購物車缺陷時，我先用 ChatGPT 確認預期行為，再到 Codex 開啟專案，最後用 Maven 跑測試。如果每一步都靠複製貼上銜接，不只會中斷心流，還得重複送出相同上下文，所以今天我們要來探討甚麼工具能讓我們的心流不會被中斷。

## ChatGPT App、Web 與 API，我怎麼選？

三種app操作方式功能上面相不同情境，所以並沒有誰比較厲害的狀況。ChatGPT App與Web功能上一模一樣，而近期 ChatGPT App 也整合進 Codex中可以方便使用者在一個App中切換操作;OpenAI API 主要為程式觸發且較為複雜，這一系列文章中不會使用到，所以這邊不過多描述若想了解可閱讀OpenAI官方文件。

![ChatGPT App、Web 與 API 的操作介面比較](./%E5%9C%96%E6%AA%94/Day03/day03-02-chatgpt-surfaces.png)

| 操作介面         | 我會在什麼時候用 | 需要先注意什麼 |
|-------------|---|---|
| ChatGPT App | 任務會用到本機檔案或桌面工具 | 只開放工作需要的資料與權限 |
| ChatGPT Web | 臨時討論、研究或整理上傳檔案 | 先確認方案與工作區允許的功能 |
| OpenAI API  | 需要批次、自動觸發或整合進系統 | 金鑰、成本、錯誤處理都要自己管理 |

## Codex 的差別，在於離程式碼多近

命令列介面（Command-Line Interface，CLI）適合直接在終端機操作本機專案；Codex cloud 則在設定好的雲端環境執行背景或平行任務。現在桌面 App 也能使用 Codex，我這次就是從 Codex App 進行修改與審查。

| 操作介面 | 適合的工作節奏 | 我會檢查的結果 |
|---|---|---|
| Codex App | 同時管理專案、對話與較長任務 | 執行紀錄、產物與檔案差異 |
| Codex CLI | 終端機內連續讀檔、修改和測試 | 實際命令及完整輸出 |
| Codex cloud | 將可重建的工作交給遠端繼續執行 | 環境設定、摘要、差異與測試 |

介面可以依習慣切換，驗收標準不能跟著放寬。至少要看清楚改了哪些檔案、執行了哪些命令，以及測試到底有沒有開始。

## 我的最小可用環境

![Day 03 最小可用開發環境](./%E5%9C%96%E6%AA%94/Day03/day03-04-minimum-environment.png)

以上是我的程式測試執行版本，不代表大家都得裝同一套版本；只要專案可以重現問題、執行測試、查看差異並在需要時還原，就足以開始練習。產品介面與方案則要在發布當日再確認一次。

## 實測：空購物車為什麼會除以零？

Day03 專案的 `ShoppingCart.calculateTotal()` 會先加總金額，再用商品數量計算平均值。購物車是空的時候，原始程式仍然執行除法，因此修正前跑 `mvn test`，兩項測試中有一項出現 `ArithmeticException`。我限定 Codex 只能修改總額計算方法，不能更動測試與既有折扣邏輯。

實際加入的程式只有空清單判斷：

```java
if (items.isEmpty()) {
    return 0;
}
```

重跑時還碰到另一個狀況：Maven 因網路權限無法下載外掛。這時候 JUnit 其實還沒執行，不能看到紅字就認定修正失敗。我確認下載來源後，只核准這次測試需要的連線；再次執行，兩項測試全部通過。接著檢查 Codex 的變更畫面，確認沒有順手改測試，也沒有夾帶無關重構。

![從失敗測試、最小修改到兩項測試通過](./%E5%9C%96%E6%AA%94/Day03/day03-05-environment-verification.png)

完整輸出放在 [Day 03 驗證紀錄](./%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY03/docs/verification-log.md)。這次需求、修改和驗證能留在同一條工作脈絡裡；不過上下文越完整，也越要控制機密資料、檔案範圍與網路權限。

## 小結：先讓一條流程跑得順

我會先選一個能完成「交代任務、修改、測試、看差異」的操作介面，再依工作需求補上其他工具。全部都裝不等於效率更高，能留下可核對的證據才重要。Day 04 會先用一個開場故事帶出這次需求有多模糊，Day 05 接著使用這套環境，把它整理成可以確認與驗收的技術規格。

## 參考資料

- [OpenAI：ChatGPT desktop app](https://learn.chatgpt.com/docs/app)
- [OpenAI：ChatGPT on the web](https://learn.chatgpt.com/docs/web)
- [OpenAI：Developer quickstart](https://developers.openai.com/api/docs/quickstart)
- [OpenAI：Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenAI：Codex cloud](https://learn.chatgpt.com/docs/cloud)
- [OpenAI Help Center：ChatGPT 與 API 的帳務管理](https://help.openai.com/en/articles/9039756)
