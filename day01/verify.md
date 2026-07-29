# Day 01 驗證、考察與實作紀錄

本檔用來保存 Day 01 正式發布前需要核對的問題、資料來源、實作程序與驗收證據。執行結果應可由另一名讀者依相同步驟重做，而不是只保留「看起來合理」的結論。

## 一、今日要驗證的核心命題

### 命題 A：一句抱怨能否直接成為可調查的 Issue？

**操作化定義**：若接手者能從 Issue 決定至少一個可執行的技術動作，例如依步驟重現、依時間與識別碼查詢日誌，或鎖定服務與環境，則標記為 `Ready for Investigation`；若只能繼續詢問基本事實，則標記為 `Need More Information`。

**驗證材料**：

- `raw-issues.md` 的五筆原始回報。
- `issue-template.md` 的欄位。
- `converted-issues.md` 的人工整理結果。

**驗收條件**：

- [x] 每筆原始回報均完整保留。
- [x] 每筆均能指出已知訊號。
- [x] 每筆均能列出阻礙調查的主要缺口。
- [x] 每筆狀態下方均記錄判斷理由，而不是只給標籤。

### 命題 B：結構化欄位能否揭露未知，而不只是美化文字？

**驗證方法**：逐筆檢查 `Service／Module`、`Actual Result`、`Expected Result`、`Reproduction Steps`、`Environment`、`Time／Frequency`、`Error Message／Evidence`、`Impact` 及 `Missing Information`。原文或產品規格未提供的資訊必須標示為「未知」、「待確認」或「未提供」，不得留給讀者自行猜測。

**驗收條件**：

- [x] 五筆案例使用相同欄位結構。
- [x] 未知欄位及無規格依據的 Expected Result 沒有被合理化補寫。
- [x] 模糊程度沒有被虛構成數值，例如不把「有時候」改成百分比。
- [x] 「可能影響」沒有寫成「已確認影響」。

### 命題 C：人工整理結果能否作為後續 AI 實驗的對照組？

**驗證方法**：確認每筆輸出皆可用相同規則重查，並保留原始輸入、人工輸出、驗證規則、結論與限制。

**驗收條件**：

- [x] 輸入保存在 `raw-issues.md`。
- [x] 輸出保存在 `converted-issues.md`。
- [x] 模板保存在 `issue-template.md`。
- [x] 結論與限制保存在 `conclusion.md`。
- [x] 本檔記錄查核來源與驗收程序。

## 二、資料來源考察

### GitHub 問題範本（Issue Template）與問題表單（Issue Form）

**考察問題**：主流問題追蹤流程是否支援以模板引導輸入，以及用必填欄位取得結構化資料？

**查核結果**：

- GitHub Issue Template 可引導貢獻者依指定內容回報問題。
- GitHub Issue Form 以 YAML 設定格式（YAML Ain’t Markup Language，以下簡稱 YAML）定義表單，可使用文字框、下拉選單、核取方塊等元件。
- 截至 2026-07-29，Issue Forms 仍屬公開預覽（public preview）；GitHub 表單結構描述（GitHub form schema）文件顯示，公開儲存庫可透過 `validations.required` 防止支援的輸入在未填寫時送出。
- 官方範例包含目前行為（Current Behavior）、預期行為（Expected Behavior）、重現步驟（Steps To Reproduce）與環境（Environment）等概念。

**來源**：

- [About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [Syntax for GitHub's form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)

**查閱日期**：2026-07-29。

### Jira Cloud 的描述、環境與證據

**考察問題**：環境與附件是否只是本文自行創造的欄位，還是既有工具確實支援的問題資訊？

**查核結果**：

- Jira Cloud 的工作項目描述可容納文字、程式片段、圖片與檔案。
- Jira Cloud 有環境（Environment）系統欄位，可記錄建立問題時的環境資訊。
- Jira 表單支援描述（Description）、附件（Attachment）與優先級（Priority）等系統欄位；欄位是否顯示，會受空間（space）、工作類型（work type）與管理員配置影響。因此本文模板是本系列的基準，不宣稱為 Jira 唯一標準。

**來源**：

- [Add files, images, and other content to describe a work item](https://support.atlassian.com/jira-software-cloud/docs/add-files-images-and-other-content-to-describe-an-issue/)
- [Add or remove fields from your form](https://support.atlassian.com/jira-software-cloud/docs/add-or-remove-fields-from-your-form/)
- [Working with the environment system field](https://support.atlassian.com/jira/kb/working-with-the-environment-system-field/)

**查閱日期**：2026-07-29。

### 發布前仍須人工確認的時效性項目

- [x] 2026-07-29 已重新開啟上述官方連結，確認頁面可存取。
- [x] 已依 2026-07-29 的 GitHub 與 Jira 產品術語更新文章用詞。
- [x] 已確認文章把欄位定義為本系列人工基準，沒有誤寫成所有團隊都必須採用的規範。

## 三、實作內容

### 實作 1：建立人工 Issue 欄位基準

**輸入**：`raw-issues.md` 的五句回報。

**處理規則**：

1. 只擷取原文直接支持的功能、行為、症狀與頻率。
2. 可以調整語序，但不得增加部署環境、裝置、錯誤碼、根因或影響人數。
3. 原文缺少的欄位填「未知」或「未提供」。
4. 推測只能改寫成待確認問題。
5. 每筆結果必須判斷 `Need More Information` 或 `Ready for Investigation`。

**輸出**：`issue-template.md`。

### 實作 2：人工轉換五筆案例

逐筆套用模板，並把結果寫入 `converted-issues.md`。轉換後依下列四類規則人工審查關鍵主張：

| 標記 | 判斷問題 | 可否進入事實欄位 |
| --- | --- | --- |
| 原始事實 | 能否在原始回報中直接找到依據？ | 可以 |
| 保守整理 | 是否只改變表達，沒有增加可驗證主張？ | 可以 |
| 未知 | 原始回報是否完全沒有提供？ | 以「未知／未提供」記錄 |
| 待確認推測 | 是否只是合理可能性？ | 不可以；改放追問或調查假設 |

關鍵主張的追溯紀錄如下：

| 案例 | 整理後主張 | 來源或判定依據 | 分類 |
| --- | --- | --- | --- |
| 001 | 涉及登入功能 | 「登入功能怪怪的」 | 原始事實 |
| 001 | 失敗具有間歇性 | 「有時候會失敗」 | 原始事實 |
| 001 | Expected Result 待確認 | 原文與現有產品規格均未提供 | 未知 |
| 002 | 涉及網站頁面的點擊操作 | 「網站頁面點擊怪怪的」 | 原始事實 |
| 003 | 使用者感受到近期變慢 | 「最近系統變得很慢」 | 保守整理 |
| 004 | 有使用者表示未收到通知信 | 「使用者說沒有收到通知信」 | 保守整理 |
| 005 | 訂單查詢無法完成 | 「訂單功能無法查詢」 | 保守整理 |

### 實作 3：執行反向追溯

對 `converted-issues.md` 每一個肯定句提問：

> 這個資訊能否追溯到原始回報或產品規格？若只是由欄位定義或功能常識推得，是否已標為「未知／待確認」？

若答案為否，執行下列其中一項：

1. 刪除該主張。
2. 改成「未知」。
3. 改成 `Missing Information` 中的問句。
4. 若屬可能影響，明確加上「可能」並指出範圍未知。

### 實作 4：建立後續責任界線與 AI 比較介面

Day 02 先使用本基準界定 AI 與人工的欄位責任；Day 03 起才以相同輸入比較模型多次輸出。後續 AI 輸出至少要能對照下列項目：

| 比較項目 | 後續檢查方式 |
| --- | --- |
| 欄位完整性 | 是否產生模板要求的全部欄位 |
| 事實忠實度 | 是否增加原文沒有的具體事實 |
| 未知處理 | 是否明確標記未知，或用流暢文字掩蓋缺口 |
| 追問品質 | 問題是否具體、可回答且有助縮小調查範圍 |
| 狀態判斷 | 是否有足夠資訊支持分流結果 |
| 輸出穩定性 | 相同輸入多次執行時，核心欄位是否一致 |

本日不對 AI 表現下結論；這張表只建立未來實驗的比較介面。

## 四、逐筆驗收表

| 編號 | 保留原文 | 未虛構環境／錯誤 | 未把模糊頻率數值化 | 具體追問 | 狀態有理由 | 主要證據 |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | 通過 | 通過 | 通過 | 通過 | 通過 | `raw-issues.md` 第 1 筆；`converted-issues.md` Issue 001 |
| 002 | 通過 | 通過 | 不適用 | 通過 | 通過 | `raw-issues.md` 第 2 筆；`converted-issues.md` Issue 002 |
| 003 | 通過 | 通過 | 不適用 | 通過 | 通過 | `raw-issues.md` 第 3 筆；`converted-issues.md` Issue 003 |
| 004 | 通過 | 通過 | 不適用 | 通過 | 通過 | `raw-issues.md` 第 4 筆；`converted-issues.md` Issue 004 |
| 005 | 通過 | 通過 | 不適用 | 通過 | 通過 | `raw-issues.md` 第 5 筆；`converted-issues.md` Issue 005 |

## 五、文章與素材發布檢查

- [x] `note.md` 從 `# Day 01：標題` 開始，沒有 YAML frontmatter。
- [x] 標題層級依 `#`、`##`、`###` 排列，沒有跳級。
- [x] 專有名詞第一次出現時提供中文全名、英文全名與縮寫。
- [x] 五張圖片皆為 16:9 橫向 PNG。
- [x] 五張圖片放在 `圖檔/Day01/`，命名為 `Day01-序號-英文簡述.png`。
- [x] 文章中的圖片使用 GitHub raw 絕對網址、獨立成行，並提供繁體中文 alt 文字。
- [x] 文章包含輸入、輸出、驗證與結論四類證據。
- [x] 文章說明本次沒有使用 AI，未虛構模型、Prompt 或實驗結果。
- [ ] 正式發布前確認 GitHub 儲存庫為公開，並測試五張 raw 圖片網址。

## 六、目前限制與下一輪待辦

- 本次樣本只有五筆，且由作者刻意撰寫，代表性有限。
- 尚未邀請第二名工程師獨立套用模板，無法評估人工判讀一致性。
- 尚未向真實回報者追問，無法測量補件成功率與溝通往返次數。
- 尚未定義分類、優先級與人工責任邊界；此項留待 Day 02。
- 尚未測試模型多次輸出的穩定性；此項留待 Day 03。
- 尚未建立 Issue 品質評分量表；此項留待 Day 04。

正式發表前若要提高證據強度，建議補做下列驗證：

1. 邀請另一名工程師只閱讀 `raw-issues.md` 與 `issue-template.md`，獨立整理五筆案例。
2. 比較兩人的已知／未知判斷與追問順序。
3. 記錄不一致欄位，修訂模板定義。
4. 將修訂日期、判斷理由與差異保存在本檔。
