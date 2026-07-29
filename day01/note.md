# Day 01：一句「登入怪怪的」，為什麼還不是可處理的 Issue？

> 📝 *本系列為 iThome 鐵人賽學習筆記，屬個人教學與非商業用途；文中法規與標準內容均以自己的話轉述並註明出處，非逐字引用。*

軟體團隊收到的問題，往往不是從規格完整的表單開始，而是從客服轉述、通訊軟體訊息，甚至一句「登入怪怪的，有時候會失敗」開始。這句話可能指向嚴重的服務異常，也可能只是單一帳號、特定登入方式或短暫網路問題。然而，在補齊必要資訊以前，工程師很難穩定重現，也難以確認最有效的調查入口。

本系列將逐步建立「AI 輔助問題追蹤與開發助手」。不過，在要求人工智慧（Artificial Intelligence，以下簡稱 AI）整理問題之前，必須先定義人類認可的結果。Day 01 因此不呼叫 ChatGPT，也不要求模型猜測答案，而是先建立一套人工整理基準：哪些欄位構成可處理的問題追蹤項目（Issue）、已知資訊如何放入欄位、未知資訊如何誠實保留，以及下一輪應追問什麼。

![工程師面對模糊登入回報與空白問題單](../%E5%9C%96%E6%AA%94/Day01/Day01-01-vague-login-report.png)

## 一句抱怨提供了訊號，卻還沒有提供調查入口

先看今天的第一筆原始回報：

> 登入功能怪怪的，有時候會失敗。

這句話不是「毫無資訊」。它至少提供了兩個可保留的訊號：

- 涉及的功能可能是「登入」。
- 問題不是每次發生，而是具有間歇性。

真正的困難在於，它沒有回答工程師展開調查時立即需要的問題：

- 使用者採用帳號密碼、單一登入（Single Sign-On，SSO），還是第三方登入？
- 「失敗」是畫面沒有反應、回到登入頁、顯示錯誤，還是收到伺服器錯誤？
- 問題發生在正式、測試或開發環境？
- 哪一個時間點、帳號、裝置與瀏覽器曾經發生？
- 能否重現？若可以，操作順序為何？
- 有沒有截圖、錯誤訊息、日誌或請求識別碼（Request ID）？
- 影響一名使用者、特定群組，還是所有人？

因此，「有問題」與「可以開始處理」是兩個不同狀態。本文所稱的「可處理」，不是指 Issue 一建立就足以確認根因，而是指接手者至少能採取明確的下一步：重現、查詢證據、縮小範圍，或向正確的人追問。若連下一步都無法決定，這張 Issue 的狀態應是「需要補充資訊」，而不是假裝已經進入修復。

## 結構化欄位的目的，是減少來回猜測

問題追蹤工具沒有唯一、放諸四海皆準的欄位組合。不同產品、團隊與風險等級，都會影響表單設計。不過，主流工具都支援用模板或表單提高輸入的一致性。GitHub 官方文件說明，問題範本（Issue Template）可引導回報者提供指定內容，問題表單（Issue Form）則能進一步使用結構化欄位；截至 2026 年 7 月 29 日，Issue Forms 仍屬公開預覽（public preview），而 `validations.required` 必填設定只適用於公開儲存庫。Jira Cloud 提供描述（Description）、環境（Environment）等內建欄位及附件能力；優先級（Priority）等欄位是否顯示，會受空間（space）、工作類型（work type）與管理員配置影響。

這些功能解決的是「如何收集」，但欄位本身仍須由團隊定義。針對本系列的錯誤回報，Day 01 採用下列人工基準：

| 欄位 | 欄位回答的問題 | 本系列的填寫原則 |
| --- | --- | --- |
| Service／Module | 哪個服務、功能或模組受到影響？ | 只填原始回報可支持的範圍；無法確認時填「未知」 |
| Title | 接手者如何快速辨識問題？ | 使用「功能＋可觀察症狀」；不寫未證實的根因 |
| Summary | 發生了什麼、目前知道多少？ | 簡潔重述已知內容，並明示資訊限制 |
| Actual Result | 實際觀察到什麼？ | 記錄可觀察結果，不把推測當結果 |
| Expected Result | 正常情況應該如何？ | 依回報者陳述或產品規格填寫；無依據時填「未知／待確認」 |
| Reproduction Steps | 如何再次觸發問題？ | 不知道就填「未知」，不可自行補步驟 |
| Environment | 問題在哪裡發生？ | 可包含部署環境、作業系統、裝置、瀏覽器及版本 |
| Time／Frequency | 何時發生、多久發生一次？ | 保留原始語意；「有時候」不能擴寫成百分比 |
| Error Message | 系統提供了什麼錯誤？ | 逐字保存錯誤碼或訊息；沒有資料就填「未提供」 |
| Evidence | 有哪些可核對的材料？ | 截圖、錄影、日誌、追蹤識別碼或監控圖表 |
| Impact | 誰受到影響、工作中斷到何種程度？ | 已知影響與可能影響分開寫 |
| Missing Information | 還缺少哪些調查條件？ | 轉成具體、可回答的追問 |
| Triage Status | 下一步應進入哪個狀態？ | Day 01 使用 `Need More Information` 或 `Ready for Investigation` |

這份表不是要求回報者第一次就填滿所有欄位。它的價值在於讓「空白」也能被看見。若沒有明確欄位，缺少的環境、時間與證據很容易埋在一段自然語言裡；一旦拆成欄位，接手者就能判斷哪些資料已確認，哪些仍待追查。

![模糊回報經過整理後形成有欄位也有缺口的 Issue](../%E5%9C%96%E6%AA%94/Day01/Day01-02-complaint-to-issue.png)

## 最重要的規則：未知就是未知

把句子改寫得流暢，不代表可以增加原文沒有的事實。假設原始輸入只有：

```text
登入功能怪怪的，有時候會失敗。
```

下列描述看似專業，實際上混入了三項沒有來源的資訊。超文字傳輸協定（Hypertext Transfer Protocol，以下簡稱 HTTP）的 500 狀態碼表示伺服器錯誤類型，但原始回報並未提供這項證據：

```text
使用者在 Production 使用 Chrome 登入時發生 HTTP 500。
```

原文沒有指出正式環境、Chrome 或 HTTP 500 狀態碼。若將這些猜測寫入 Issue，後續工程師可能直接查詢錯誤的環境與日誌，反而延長處理時間。Day 01 採用四種記錄方式區分資料性質：

| 資料性質 | 定義 | 登入案例 |
| --- | --- | --- |
| 原始事實 | 回報者明確提供的內容 | 登入、偶爾失敗 |
| 保守整理 | 不增加新事實的改寫 | 「登入功能偶發失敗」 |
| 未知 | 原文沒有提供，無法判定 | 環境、登入方式、錯誤訊息 |
| 待確認推測 | 有助調查但尚未證實的可能性 | 是否只有 SSO 發生、是否集中於特定版本 |

「待確認推測」可以放進調查假設或追問清單，卻不能偽裝成 Actual Result。這條界線也是後續設計提示詞（Prompt）、結構化輸出與自動驗證的基礎：模型若把合理猜測寫成確定事實，格式再漂亮也不合格。

![已知事實與未經證實推測之間的界線](../%E5%9C%96%E6%AA%94/Day01/Day01-03-facts-vs-assumptions.png)

## 先用人工完成一次，建立後續比較基準

本次實作選用五句刻意保留模糊性的回報：

1. 登入功能怪怪的，有時候會失敗。
2. 網站頁面點擊怪怪的。
3. 最近系統變得很慢。
4. 使用者說沒有收到通知信。
5. 訂單功能無法查詢。

處理流程固定為四步：

1. 圈出原文直接支持的名詞、行為與症狀。
2. 將已知內容放入對應欄位，不補充原文沒有的環境或錯誤。
3. 將空缺改寫成具體問題。
4. 判斷目前可否開始調查；若不行，標記 `Need More Information`。

以登入案例為例，人工拆解結果如下：

| 判讀項目 | 結果 | 理由 |
| --- | --- | --- |
| Service／Module | 登入功能 | 原文直接指出 |
| Title | 登入功能偶發失敗 | 僅整理「登入」與「有時候會失敗」 |
| Actual Result | 登入有時失敗，失敗畫面未知 | 保留頻率語意，不虛構錯誤 |
| Expected Result | 未知；待回報者或產品規格確認 | 功能常識不能取代已確認需求 |
| Reproduction Steps | 未知 | 原文沒有操作步驟 |
| Environment | 未知 | 原文沒有部署環境、裝置或瀏覽器 |
| Time／Frequency | 時間未知；頻率僅知「有時候」 | 不把模糊頻率換算成數字 |
| Error Message／Evidence | 未提供 | 原文沒有錯誤碼、截圖或日誌 |
| Impact | 至少有使用者可能無法登入；範圍未知 | 區分可推得的直接影響與未知規模 |
| Triage Status | `Need More Information` | 缺少重現、環境、時間及證據 |

整理後的 Issue 不是把空格全部填滿，而是把「知道什麼」與「還要問什麼」寫清楚：

```markdown
# Issue 001：登入功能偶發失敗

## Summary

使用者回報登入功能有時無法完成。目前尚未確認登入方式、
發生環境、錯誤訊息、發生時間與影響範圍。

## Actual Result

登入有時失敗；具體失敗畫面未知。

## Expected Result

未知；須由回報者陳述或產品規格確認登入成功時的既定行為。

## Reproduction Steps

未知。

## Environment

未知。

## Time／Frequency

- 發生時間：未知。
- 發生頻率：原始回報僅描述為「有時候」。

## Error Message／Evidence

未提供。

## Missing Information

1. 使用哪一種登入方式？
2. 問題發生在哪個環境、裝置與瀏覽器？
3. 失敗時的畫面、錯誤訊息或錯誤碼為何？
4. 最近一次發生的時間與時區為何？
5. 能否重現？操作步驟為何？
6. 哪些帳號受到影響？
7. 是否有截圖、日誌或 Request ID？

## Triage Status

Need More Information
```

完整五筆人工整理結果保存在專案儲存庫的 [`day01/converted-issues.md`](https://github.com/a26703248/ithome-2026-codex/blob/main/day01/converted-issues.md)。這些結果不是「標準答案」，而是後續實驗的比較基準。Day 02 先使用這份基準界定 AI 與人工的欄位責任；Day 03 才以相同輸入比較模型多次輸出，檢查模型是否遺漏欄位、增加不存在的事實，或提出無法回答的追問。

## 五筆回報揭露了相同的資訊缺口

五句原始回報涉及不同功能，但都不足以直接進入修復。人工整理後的共同結果如下：

| 編號 | 原始回報中的可用訊號 | 主要缺口 | 初步狀態 |
| --- | --- | --- | --- |
| 001 | 登入、間歇性失敗 | 登入方式、環境、時間、錯誤、證據、影響範圍 | `Need More Information` |
| 002 | 網站頁面、點擊後異常 | 頁面網址、元件、實際結果、期望結果、環境、重現步驟 | `Need More Information` |
| 003 | 系統、近期變慢 | 操作項目、反應時間、比較基準、時間範圍、環境、影響人數 | `Need More Information` |
| 004 | 通知信、未收到 | 觸發事件、收件人網域、發送時間、郵件狀態、垃圾郵件匣、追蹤資料 | `Need More Information` |
| 005 | 訂單查詢、無法完成 | 查詢條件、畫面結果、權限、環境、時間、錯誤與證據 | `Need More Information` |

這個結果不能推導出「所有模糊回報都無法調查」。例如，若監控系統同時告警，值班工程師仍可能從告警時間與服務名稱開始查詢；高風險事件也可能先止血再補資料。本文的結論僅限於本次五筆輸入：單看這些句子，沒有足夠證據決定技術調查入口。

![從重現、環境、頻率、日誌與影響建立調查流程](../%E5%9C%96%E6%AA%94/Day01/Day01-04-investigation-workflow.png)

## 「需要補充資訊」仍然是一個可執行結果

`Need More Information` 並不表示把 Issue 退回後不再處理。有效的分流至少要完成三件事：

1. 保留原始回報，避免改寫後失去來源。
2. 列出少量但高資訊量的追問，讓回報者知道如何補充。
3. 指定補件後的下一個狀態與負責角色。

追問也應有順序。對登入失敗而言，「最近一次發生時間、登入方式、錯誤畫面或 Request ID」通常比「還有其他資訊嗎」更容易取得，也更能縮小搜尋範圍。若一次丟出十多個模糊問題，回報者仍可能不知道如何回答。

此外，Issue 欄位不應混淆三種不同決策：

- **是否可開始調查**：取決於是否有明確下一步。
- **是否嚴重**：取決於影響範圍、持續時間、替代方案與業務風險。
- **是否優先處理**：還涉及團隊資源、服務等級與其他工作。

原始回報若缺乏影響資料，便不能只因「登入」兩字就自動判定最高優先級。優先級與責任邊界會在 Day 02 進一步處理。

## 可重用的人工 Issue 模板

本次實作整理出下列模板，後續無論由人填寫或由 AI 協助產生，都必須遵守相同欄位語意：

```markdown
# [Issue 編號]：[功能／模組]＋[可觀察症狀]

## Original Report

[完整保留原始回報]

## Summary

[只使用已知資訊摘要問題，並說明主要限制]

## Service／Module

[已知名稱；否則填「未知」]

## Actual Result

[實際觀察；未知部分明確標示]

## Expected Result

[依回報者陳述或產品規格填寫；沒有依據時填「未知／待確認」]

## Reproduction Steps

[步驟；否則填「未知」]

## Environment

[部署環境、裝置、作業系統、瀏覽器、版本；否則填「未知」]

## Time／Frequency

[最近發生時間、時區、頻率；不得自行換算]

## Error Message／Evidence

[錯誤碼、原文訊息、截圖、日誌、Request ID；否則填「未提供」]

## Impact

[已確認影響與未知範圍分開記錄]

## Missing Information

1. [最優先追問]
2. [次要追問]

## Triage Status

[Need More Information／Ready for Investigation]
```

模板的可重用版本另存於專案儲存庫的 [`day01/issue-template.md`](https://github.com/a26703248/ithome-2026-codex/blob/main/day01/issue-template.md)。此時仍未使用 AI；這是刻意的實驗設計。沒有人工基準，就無法判斷後續自動化究竟提高品質，還是只提高文字產量。

![從人工基準、結構化資料到受控 AI 協作的演進路線](../%E5%9C%96%E6%AA%94/Day01/Day01-05-human-baseline-roadmap.png)

## 今日結論：先定義可接受的輸出，再談自動化

Day 01 得到四項基礎結論：

1. 模糊回報仍包含可保存的訊號，但不一定足以提供技術調查入口。
2. 結構化欄位的價值不只是填資料，也包括揭露未知與安排追問。
3. 保守整理可以改寫語句，卻不能把合理推測升格為事實。
4. `Need More Information` 是有效的分流結果，前提是同時提供具體追問與後續流程。

今天完成的人工欄位、五筆案例與模板，將成為後續實驗的對照組。Day 02 將處理更棘手的責任問題：標題、摘要、分類、影響與優先級之中，哪些可以交給 AI 建議，哪些必須保留給人決定？

## 參考資料

- GitHub Docs，〈[About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)〉，查閱日期：2026-07-29。
- GitHub Docs，〈[Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)〉，查閱日期：2026-07-29。
- GitHub Docs，〈[Syntax for GitHub's form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)〉，查閱日期：2026-07-29。
- Atlassian Support，〈[Add files, images, and other content to describe a work item](https://support.atlassian.com/jira-software-cloud/docs/add-files-images-and-other-content-to-describe-an-issue/)〉，查閱日期：2026-07-29。
- Atlassian Support，〈[Add or remove fields from your form](https://support.atlassian.com/jira-software-cloud/docs/add-or-remove-fields-from-your-form/)〉，查閱日期：2026-07-29。
- Atlassian Support，〈[Working with the environment system field](https://support.atlassian.com/jira/kb/working-with-the-environment-system-field/)〉，查閱日期：2026-07-29。
