# Day 25｜不只是工程師：先把跨角色交接變成可驗證的工作

![Day 25 封面：人工智慧加速的是交接，不是取代角色](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day25/day25-01-cover.png)

Day 24 檢查權限、相依套件與測試；換到「AI輔助生成系統」，我先看交付紀錄。Java 程式已能拒絕未填複核原因的提交、保留原稿；敏感內容遮蔽、畫面失敗狀態、正式授權與監控仍列為待確認。`BUILD SUCCESS` 沒有消掉這些空格，所以本篇從「下一位拿到什麼證據」開始。

## 我的分界：要不要碰專案

我以產出是否碰專案分工具：ChatGPT 整理來源；要讀寫檔案、執行命令或留下可重跑結果，才交給 Codex。產品經理也能請 Codex 查限制，工程師也會用 ChatGPT 整理訪談。OpenAI 官方分別提供需求文件、介面原型與品質保證（Quality Assurance，QA）案例，我只在指定審查者與證據後採用其中做法。

![跨角色工具責任矩陣](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day25/day25-02-role-matrix.png)

| 角色 | ChatGPT 協助 | Codex 協助 | 人工責任 |
|---|---|---|---|
| 產品經理（Product Manager，PM） | 整理決議與空白 | 查既有實作限制 | 範圍、優先順序 |
| 法遵／資安 | 規則轉成問題 | 找權限與日誌證據 | 分級與例外 |
| 設計 | 整理狀態與文案 | 產生介面原型 | 可用性與一致性 |
| QA | 擴充測試案例 | 實作並執行測試 | 測試範圍與風險 |
| 工程／維運 | 整理方案與手冊 | 修改、測試、查設定 | 差異、部署與復原 |

## 用 ChatGPT 把空白攤開

桌上演練時，我刻意把起始交辦縮成「請做複核介面」。我把需求書裡待確認的去識別化規則交給 ChatGPT，限制它只能使用提供的內容：

```text
請整理成：已確認、待確認、驗收條件、負責人。
缺少依據就標示「待確認」，不要自行決定門檻或責任歸屬。
每項驗收條件都要能由畫面、測試、日誌或設定驗證。
```

我把「不含自動發布」列為已確認，並將複核原因必填、保留版本納入最小驗收。我再從設計角度補列載入、儲存失敗與唯讀，從 QA 角度補列空白原因與版本衝突；這些不是跨部門簽認結果。

![模糊交辦經 ChatGPT 整理成已確認、待確認、驗收條件與負責人](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day25/day25-03-handoff-before-after.png)

## 規格確認後，才讓 Codex 實作契約

確認後，我把條件、可改目錄與測試要求交給 Codex。[Java 最小案例](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY25/src/main/java/com/ithome/day24/review/ReviewWorkflow.java)只驗證複核決策，不含資料庫或正式授權。複核原因不可空白；每次決策新增事件，不覆蓋原稿。

```java
String normalizedReason = reason == null ? "" : reason.strip();
if (normalizedReason.isBlank()) {
    throw new IllegalArgumentException("複核原因不可空白");
}
events.add(new ReviewEvent(decision, normalizedReason, reviewer));
```

![從 PM 決議到 Codex 實作、QA 驗收與維運接手的跨角色流程](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day25/day25-04-handoff-flow.png)

我執行 `mvn clean test`，[4 項測試全部通過](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY25/docs/verification-log.md)：採用、修改後保留版本、複核原因必填，以及否決後保留原稿。結果只涵蓋程式契約；畫面、正式授權、資料留存與版本衝突仍待真實環境驗證。

## 上線判斷還要回到各角色

[交付包](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY25/docs/handoff-record.md)把未完成項目連到建議責任角色與所需證據。法遵／資安要核定遮蔽與留存規則，QA 要決定風險覆蓋，維運要檢查權限、監控與復原步驟。共用欄位是否真的縮短等待時間，仍要放進真實流程量測。

![需求、介面、程式、測試與部署證據串成可追溯交付鏈](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day25/day25-05-evidence-chain.png)

## 小結：讓下一位重跑我的判斷

我用一個問題檢查交付：接手者能否分辨既定需求、演練假設與待確認項目，並重跑同一組測試？只有答案還不夠，來源與驗證方法也要留下。Day 26 會處理下一題：這套做法怎樣離開個人聊天紀錄，變成團隊能測試與維護的提示詞（Prompt）資產。

## 參考資料

- [OpenAI：ChatGPT 與 Codex 使用案例總覽](https://learn.chatgpt.com/use-cases)
- [OpenAI：Draft PRDs from internal context](https://learn.chatgpt.com/use-cases/draft-prds-from-sources)
- [OpenAI：Turn user stories into UI mocks](https://learn.chatgpt.com/use-cases/user-stories-to-ui-mocks)
- [OpenAI：QA your app with Computer Use](https://learn.chatgpt.com/use-cases/qa-your-app-with-computer-use)
- [AI 輔助生成系統需求書](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/AI%E8%BC%94%E5%8A%A9%E7%94%9F%E6%88%90%E7%B3%BB%E7%B5%B1-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
