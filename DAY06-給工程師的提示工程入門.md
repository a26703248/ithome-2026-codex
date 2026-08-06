# Day 06｜給工程師的提示工程（Prompt Engineering）入門：把提示詞當成工作說明

![Day 06 封面：把提示詞當成可驗收的工作說明](./%E5%9C%96%E6%AA%94/Day06/day06-01-cover.png)

Day 05 我請 ChatGPT 比較架構時，沒有只丟一句「請給我最佳架構」。這句話沒說機器限制、資料來源、比較維度與完成條件。提示詞不是讓模型變聰明的咒語，而是一份工作說明；資訊缺口越多，回應越容易偏離現場。

## 我用六個欄位檢查提示詞

OpenAI 對 ChatGPT 的提示建議，是把要求寫得清楚、具體，提供足夠背景，並依第一輪回應反覆調整。我把這些原則整理成自己的六欄檢查表。這不是每次必填的官方格式；高風險開發任務若漏掉一欄，我就要說明原因。

| 組成 | 本次欄位正規化案例 |
|---|---|
| 任務 | 將兩種來源轉成同一個 `WorkspaceDocument` |
| 背景 | Day 04 的示範欄位名稱不同，初版（v0）需求尚未定義對齊規則 |
| 輸入 | 兩個 Java 紀錄類別（record）、欄位型別及允許的空值 |
| 限制 | Java 17、不加第三方套件、不改公開介面 |
| 輸出 | `DataNormalizer`、JUnit 5 測試與假設清單 |
| 驗收 | 用 Maven 執行 `mvn test`，核對欄位、預設值及來源標籤後續變更不影響輸出 |

![六個提示詞組成：任務、背景、輸入、限制、輸出與驗收](./%E5%9C%96%E6%AA%94/Day06/day06-02-six-parts.png)

## 同一個任務，我改了三版

第一版只有一句：「請用 Java 幫我把兩種資料格式對齊。」如果 ChatGPT 不先追問就直接產生程式，只能自行假設欄位、空值與目標模型；即使程式能編譯，也無法證明符合需求。

第二版補上 `title`、`description`、`tags` 與兩組時間欄位，並要求未知處標成「待確認」。這版已縮小可回答範圍，但「時間缺值怎麼辦」仍沒有團隊決定。

第三版才把本篇示範規則寫死：字串缺值轉空字串、標籤缺值轉空清單、時間缺值轉 `Instant.EPOCH`（Unix 紀元起點）。這是可替換的測試規則，不是 v0 需求事實。完整版本放在 [Day 06 可驗證版提示詞](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY06/prompt-v3-verifiable.txt)。

```text
先列出仍缺少的決策；若已能實作，再輸出最小差異。
不得新增依賴或更動公開介面。
完成後回報測試命令、結果與尚未驗證的假設。
```

![三版提示詞從模糊指令演進到可驗收工作說明](./%E5%9C%96%E6%AA%94/Day06/day06-03-prompt-evolution.png)

| 版本 | 還要人工補什麼 | 可驗證程度 |
|---|---|---|
| 簡略版 | 全部欄位與行為 | 低，只能檢查語法 |
| 補背景版 | 空值及時間語意 | 中，可檢查欄位 |
| 可驗證版 | 業務是否接受示範規則 | 高，可執行測試 |

我不把這張表當成模型成功率；它只記錄同一任務還有多少決策藏在回應裡。提示詞變長不是目的，讓未知資訊浮出來才是。

## 程式可以生成，驗收要自己跑

依第三版示範規則完成的核心轉換很短。實作將缺少的時間轉成 `Instant.EPOCH`，測試再固定這項預期：

```java
return new WorkspaceDocument(
        stringOrEmpty(title),
        stringOrEmpty(description),
        tags == null ? List.of() : List.copyOf(tags),
        createdAt == null ? Instant.EPOCH : createdAt,
        updatedAt == null ? Instant.EPOCH : updatedAt);
```

`List.copyOf` 會複製成不可修改的清單；來源清單後續增刪不影響輸出，內含 `null` 則會被拒絕。後者也是本篇示範規則，不是 v0 決策。

六個 JUnit 5 測試涵蓋兩種來源、空值、清單複製、標籤內 `null` 與 `null` 來源。執行 `mvn test` 後六項全數通過；這只能證明程式符合本篇規則，不能替業務決定預設值是否合適。

![回應品質不看篇幅，要看假設是否可見、結果是否可測](./%E5%9C%96%E6%AA%94/Day06/day06-04-quality-check.png)

## 模板依風險增減

查一個編譯錯誤，我通常貼錯誤訊息、相關程式與期望行為就開始；涉及資料轉換、公開介面或安全邊界，我才展開六欄。欄位版本改變時，提示詞也要一起更新。密碼、金鑰、客戶資料與未授權程式碼則不會因為模板需要輸入就放進去。

![可複用提示詞卡片：先交代工作，再要求證據](./%E5%9C%96%E6%AA%94/Day06/day06-05-reusable-card.png)

## 小結：讓未知有明確的退回條件

這次真正改善的不是提示詞看起來有多完整，而是規則、未知與退回條件都留在檯面上。Day 07 我會把檢查焦點移到 HTTP 介面，逐項核對請求、回應與錯誤案例是否一致。

## 參考資料

- [OpenAI：Prompt engineering best practices for ChatGPT](https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt)
- [OpenAI：How do I create a good prompt for an AI model?](https://help.openai.com/en/articles/4936848-how-do-i-create-a-good-prompt-for-an-ai-model-like-gpt4)
- [JUnit 5 User Guide](https://docs.junit.org/5.10.2/user-guide/)
- [Java 17：List](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/List.html)
- [Java 17：Instant.EPOCH](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Instant.html#EPOCH)
- [資料工作區空間——需求書（v0．初版待釐清）](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E8%B3%87%E6%96%99%E5%B7%A5%E4%BD%9C%E5%8D%80%E7%A9%BA%E9%96%93-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
