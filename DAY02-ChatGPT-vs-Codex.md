# Day 02｜ChatGPT vs Codex：對話助手與沙箱編程代理的差異

![Day 02 封面：同一項任務，依工作階段選擇工具](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day02/day02-01-cover.png)

Day 01 用「功能好像怪怪的」帶出開發上的問題，今天我把這個案例繼續拆開。若立刻調整程式，可能會需要花時間確認問題甚至改錯，但若只請 ChatGPT 提供修正碼，還要整合與驗證。兩種做法對應工作階段：前者需要釐清未知，後者需要在專案中完成已知任務。

## 先建立兩種工作心智模型

ChatGPT 是以對話為核心的通用助手，適合追問、整理、比較與產出內容；依方案與設定，也能搜尋網路與分析檔案。Codex 則是代理，可以在授權的本機或雲端環境中瀏覽程式庫、修改檔案、執行命令與測試，再回報差異與結果。這類環境可用沙箱限制檔案、命令與網路權限，讓任務隔離執行。

![ChatGPT 與 Codex 的工作心智模型比較](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day02/day02-02-mental-model.png)

| 比較維度 | ChatGPT      | Codex |
|---|--------------|---|
| 主要互動 | 整理想法、問題探討    | 以任務驅動專案操作 |
| 上下文 | 對話、上傳檔案、可用工具 | 指定專案、檔案與執行環境 |
| 主要產出 | 分析、草稿、規格與建議  | 程式碼差異、命令與測試結果 |
| 驗證方式 | 核對來源、需求與推論   | 檢查差異、測試與執行紀錄 |
| 常見風險 | 補出不存在的前提     | 依錯誤邊界完成看似正確、實際偏題的修改 |

隨著時間的演進功能會持續改變，所以以上是我目前整理個人工作流程和習慣上比較出來的，若有個人觀點皆以自己的習慣為主。

## 案例一：模糊需求先交給 ChatGPT 釐清

我先提供原始回報與「重新操作一次無法重現」的背景，請 ChatGPT 不要猜根因，只列出產品經理（Product Manager，PM）、工程師與品質保證（Quality Assurance，QA）需要補齊的問題：使用者角色、環境、關鍵字、篩選與排序條件、操作步驟、預期結果、實際結果、例外情境及驗收方式。

![從模糊回報整理成可驗證的 Issue Report](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day02/day02-03-requirement-clarification.png)

我刪除了「一定是後端查詢錯誤」與「無法重現就代表問題不存在」等假設，最後整理成問題報告（Issue Report）：小寫關鍵字漏掉含大寫字母的商品，以及價格排序跨頁不連續。ChatGPT 補的是提問框架，不是商業規則；報告仍須由相關人員確認。

## 案例二：可重現的缺陷再交給 Codex

接著，我讓 Codex 讀取問題報告、產品規格、Java 查詢服務與 JUnit 5 測試。第一次在沙箱執行 Maven 測試命令 `mvn test` 時，Maven 因網路權限無法下載外掛。我確認下載範圍並核准必要的網路與 Maven 快取權限後，再請 Codex 執行；三項測試出現兩項失敗。Codex 只調整兩項查詢行為：以 `Locale.ROOT` 採用不受使用者語系影響的大小寫轉換規則，以及先排序完整結果再分頁。

![Codex 從重現失敗到測試通過的驗證流程](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day02/day02-04-codex-verification.png)

重跑後三項測試全部通過，既有分類篩選測試也通過。不過，前後空白、特殊字元與大量資料效能尚未驗證，不能因畫面顯示成功就推論所有需求都已完成。

## 選擇工具：當前資訊是否足夠明確

![選擇工具：看下一步需要什麼證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day02/day02-05-decision-tree.png)

需要補問題、比較方案、整理規格時，我先用 ChatGPT；已有明確邊界，且下一步要讀檔、修改、執行與測試時，我改用 Codex。像補驗收條件適合前者，修正可重現缺陷、增加 JUnit 5 測試或調整跨模組相依關係則適合後者。複雜任務通常不是二選一，而是先對話釐清，再讓代理執行。

## 小結：工具協助執行，責任仍由人承擔

我曾在需求盲區尚未確認前就開始修改，最後因返工拖延交付。今天的判斷原則是：**用 ChatGPT 在未知中補齊問題，用 Codex 在已知邊界內完成實作；兩者都必須由人檢查證據並承擔決策。**

Day 03 將進一步比較 ChatGPT 應用程式／網頁版、OpenAI 應用程式介面（Application Programming Interface，API），以及 Codex 的命令列介面（Command-Line Interface，CLI）、整合開發環境（Integrated Development Environment，IDE）擴充套件與雲端任務，組成人工智慧（Artificial Intelligence，AI）開發環境。

## 參考資料

- [OpenAI Help Center：ChatGPT Capabilities Overview](https://help.openai.com/en/articles/9260256-chatgpt-capabilities-overview)
- [OpenAI Help Center：Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- [OpenAI：Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenAI：Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)
- [OpenAI：Codex sandboxing](https://learn.chatgpt.com/docs/sandboxing)
- [Day 02 Java 案例與驗證紀錄](./%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY02/docs/task2-verification.md)
