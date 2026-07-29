# Day 02 驗證、考察與實作紀錄

本檔保存 Day 02 的研究來源、責任矩陣設計、案例測試、驗收結果與發布前待辦，並以問題追蹤項目（Issue）及人工智慧（Artificial Intelligence，以下簡稱 AI）協作為範圍。目標是讓第三人能重做欄位分類，而不是只接受「AI 輔助、人工負責」的抽象結論。

## 一、今日要驗證的核心命題

### 命題 A：責任邊界能否套用一致規則，而不是依直覺分類？

**驗證方法**：對每個 Issue 欄位依序回答三個問題：

1. 內容能否追溯到原始回報、產品規格或系統紀錄？
2. 錯誤通過後的後果是否容易發現與復原？
3. 是否需要正式權限、資源承諾或跨團隊情境？

**驗收條件**：

- [x] `responsibility-matrix.md` 承接 Day 01 的 13 個模板欄位，再加入分類、優先級與負責人，共 16 個欄位，且均有主要層級。
- [x] 每個欄位均記錄 AI 可做工作、限制、責任角色與採用前證據。
- [x] 同一判斷規則能套用到標題、分類、優先級與派工等不同欄位。

### 命題 B：AI 產生的合理內容是否仍可能越過責任邊界？

**驗證方法**：以 Day 01 登入回報建立八個候選輸出，檢查合理性是否被誤當成事實或授權。

**驗收條件**：

- [x] 標題與摘要只使用原始回報可支持的內容。
- [x] Category 保留為建議，沒有升格為已確認根因。
- [x] 預期結果（Expected Result）在缺乏規格時標示未知。
- [x] 優先級（Priority）在缺乏影響與服務等級時不得直接採用。
- [x] 分流狀態（Triage Status）與負責人（Assignee）在未授權前不得觸發工作流程。

### 命題 C：「人工覆核」是否具有可執行條件？

**驗證方法**：檢查覆核設計是否同時具備來源、產出性質、責任角色與操作紀錄。

**驗收條件**：

- [x] 審查者能看到原始來源，而不只看到 AI 摘要。
- [x] 欄位能區分原始輸入、AI 草稿、AI 建議與人工決定。
- [x] L3 欄位指定具名角色類型，不只寫「人工」。
- [x] 接受、修改、拒絕與覆寫都有預定稽核紀錄。

## 二、官方資料來源考察

本節查核美國國家標準與技術研究院（National Institute of Standards and Technology，以下簡稱 NIST）《人工智慧風險管理框架》（Artificial Intelligence Risk Management Framework，以下簡稱 AI RMF）及其配套資料。

### NIST AI RMF 1.0 的角色與監督原則

**考察問題**：把人與 AI 的角色、責任及監督方式明確化，是否有可靠風險管理來源支持？

**查核結果**：

- NIST AI RMF 1.0 的 Govern 2.1 描述的治理結果包括讓組織內與 AI 風險相關的角色、責任與溝通路徑清楚且有紀錄。
- Govern 3.2 描述政策與程序應能區分人與 AI 配置中的角色、責任及監督。
- Appendix C 說明 AI RMF 提供機會區分使用、互動與管理 AI 系統時的各種人類角色與責任。
- AI RMF 是自願採用的跨領域風險管理資源，不是 Issue 欄位標準。
- 截至 2026-07-29，NIST AIRC 頁面標示 AI RMF 1.0 正在修訂。

**來源**：

- [AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- [Appendix C: AI Risk Management and Human-AI Interaction](https://airc.nist.gov/airmf-resources/airmf/appendices/app-c-ai-risk-management-and-human-ai-interaction/)

**版本資訊**：AI RMF 1.0 於 2023-01-26 正式發布。查閱日期：2026-07-29。

### 生成式人工智慧（Generative Artificial Intelligence，以下簡稱生成式 AI）的錯誤內容風險

**考察問題**：為何流暢文字仍須保留來源與人工確認？

**查核結果**：

- NIST AI 600-1 將生成式 AI 自信呈現錯誤、虛假、偏離輸入或前後矛盾內容的現象稱為虛構（confabulation）風險。
- 本文以「虛構／錯誤內容」說明這類風險，不把特定模型輸出預設為正確。
- 此風險支持來源追溯與未知標記，但不代表每一個生成結果都錯誤。

**來源**：

- [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [NIST AI 600-1 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

**版本資訊**：NIST AI 600-1，2024-07-26 發布；NIST 頁面於 2026-04-08 更新。查閱日期：2026-07-29。

### NIST AI RMF 實務手冊（Playbook）中的人工監督紀錄

**考察問題**：人工覆核除了按鈕以外，還應保留什麼？

**查核結果**：

- NIST AI RMF Playbook 是框架的配套落地建議。
- Playbook 建議記錄指定角色對 AI 輸出的監督程度。
- Playbook 也建議追蹤使用者覆寫、回報錯誤、申訴或裁決等下游行動。
- Playbook 是彈性建議，不是必須逐項完成的檢查表。

**來源**：

- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/)
- [NIST AI RMF Playbook — Measure](https://airc.nist.gov/airmf-resources/playbook/measure/)

**查閱日期**：2026-07-29。

### 發布前時效性確認

- [x] 2026-07-29 已開啟上述 NIST 官方頁面。
- [x] 已註明 AI RMF 1.0 正在修訂，未把它描述為最新定稿且永不變動。
- [x] 已區分 NIST 原則與本專案自行設計的四層矩陣。
- [x] 未將自願風險管理資源描述成法律義務。

## 三、實作內容

### 實作 1：定義四層責任模型

| 層級 | 實作意義 | 必要資料 |
| --- | --- | --- |
| L0 | 原始證據獨立保存 | 原文、檔案、時間、來源與版本 |
| L1 | AI 只整理有來源的內容 | 來源連結、草稿標記、審查狀態 |
| L2 | AI 候選值不直接生效 | 建議標記、理由、候選選項 |
| L3 | 具權限角色作成決定 | 決定者、依據、時間、接受或覆寫紀錄 |

輸出：`responsibility-matrix.md`。

### 實作 2：為每個欄位指定責任

逐一處理 Day 01 的 13 個模板欄位，再加入分類、優先級與負責人，共 16 個欄位。每一欄填寫：

1. 主要責任層級。
2. AI 可執行工作。
3. 禁止或限制。
4. 最終責任角色。
5. 採用前證據。

完成標準不是每列都有文字，而是另一名讀者能依三個判斷問題理解為何分到該層。

### 實作 3：執行登入案例邊界測試

輸入：

```text
登入功能怪怪的，有時候會失敗。
```

測試項目：

- Title 與 Summary 是否只保守整理原文。
- Category 是否保持候選身分。
- 預期結果是否避免用常識創造規格。
- 優先級是否等待影響與服務等級證據。
- 缺少資訊是否具體且不要求不必要敏感資訊。
- 分流狀態與負責人是否等待授權。

輸出：`boundary-tests.md`。

### 實作 4：設計最低稽核紀錄

後續資料結構至少需要保存：

| 記錄項目 | 用途 |
| --- | --- |
| `fieldName` | 哪一個欄位被產生或修改 |
| `sourceRefs` | 內容依據哪些原始回報、規格或證據 |
| `contentType` | 原始輸入、AI 草稿、AI 建議或人工決定 |
| `generatedValue` | AI 產生的候選值 |
| `finalValue` | 覆核後採用的值 |
| `reviewerRole` | 哪一類被授權角色進行覆核 |
| `reviewAction` | 接受、修改、拒絕或覆寫 |
| `reviewReason` | 作成動作的理由 |
| `timestamp` | 產生與覆核時間 |

Day 02 只定義資料需求，不提前實作 Day 09 的 JavaScript 物件表示法（JavaScript Object Notation，JSON）或 Day 26 的表述性狀態轉移應用程式介面（Representational State Transfer Application Programming Interface，REST API）。

## 四、逐項驗收表

| 驗收項目 | 證據位置 | 結果 |
| --- | --- | --- |
| 16 個欄位均有責任層級 | `responsibility-matrix.md`「欄位矩陣」 | 通過 |
| L0 原始資料不被 AI 覆寫 | 矩陣「原始回報」「錯誤訊息／證據」 | 通過 |
| L1 草稿可以追溯來源 | `boundary-tests.md` B01、B02 | 通過 |
| L2 建議未偽裝成已確認值 | B03、B06、B07 | 通過 |
| L3 決策有具名角色 | B04、B05、B08 | 通過 |
| 預期結果未用常識補寫 | B04 | 通過 |
| 優先級未在資訊不足時定案 | B05 | 通過 |
| 人工覆核包含來源與稽核紀錄 | 本檔命題 C、實作 4 | 通過 |
| Day 02 未虛構模型測試結果 | `conclusion.md`「限制」 | 通過 |

## 五、文章與素材發布檢查

- [x] `note.md` 從 `# Day 02：標題` 開始，沒有 YAML frontmatter。
- [x] 固定定位聲明位於標題正下方。
- [x] 標題層級使用 `#`、`##`、`###`，沒有跳級。
- [x] 專有名詞首次出現時提供中文全名、英文全名與縮寫。
- [x] 文章包含輸入、輸出、驗證與結論四類證據。
- [x] 五張圖片皆為 16:9 橫向 PNG。
- [x] 圖片放在 `圖檔/Day02/`，檔名使用 `Day02-序號-英文簡述.png`。
- [x] 圖片以 GitHub raw 絕對網址獨立成行，並提供繁體中文 alt。
- [x] 文章明示本日沒有執行模型穩定性實驗。
- [ ] 正式發布前確認 GitHub 儲存庫為公開，並測試五張 raw 圖片網址。

## 六、限制與後續待辦

- 本次是責任政策與紙上案例測試，尚未蒐集模型實際輸出。
- 四層矩陣尚未經另一個真實團隊試用，角色名稱可能需要調整。
- 尚未測量覆核接受率、修改率、拒絕率與處理時間。
- 尚未驗證審查者能否穩定判斷 L1、L2 與 L3。
- 尚未把責任層級寫成 Java 類型、資料庫欄位或工作流程權限。

Day 03 實作前應：

1. 固定相同原始輸入與提示詞。
2. 保存模型、參數、時間與完整輸出。
3. 對同一輸入執行多次。
4. 依本日矩陣標示差異發生在 L1、L2 或 L3。
5. 不用單次成功案例代表模型穩定性。
