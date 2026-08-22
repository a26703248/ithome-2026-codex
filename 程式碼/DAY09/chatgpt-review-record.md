# Day 09｜ChatGPT 初篩補作模擬對話稿

> 補作日期：2026-08-22
>
> 紀錄性質：原始撰稿對話未保存。本稿由本次編修依 `review-prompt.txt` 與 `review-input.diff` 重新建立，用來公開初篩的輸入、模擬輸出與追問過程；它不是原始對話的逐字復原，也不是 ChatGPT 產品介面的匯出紀錄。

## 第一輪：找出可以驗證的疑點

### 我送出的內容

```text
你是 Java 程式碼審查者。請只審查下方 diff，不要重寫整個類別。

背景：
- 每日匯入排程可能由兩個執行緒幾乎同時觸發。
- 同一個 workspaceId 同一時間只能有一批匯入。
- workspaceId 前後空白與英文大小寫不影響識別。
- 無效 workspaceId 應得到 IllegalArgumentException，不應洩漏其他例外。
- Java 17；runningWorkspaces 由 ConcurrentHashMap.newKeySet() 建立。

請依正確性、並行安全、測試缺口與可維護性檢查，將每項觀察寫成一張「驗證卡」：
- 判定：BLOCK 或 VERIFY。
- 程式依據：指出 diff 中相關敘述。
- 反例：給一組輸入，或列出兩個執行緒的交錯順序。
- 可執行確認：說明要加哪個測試、跑哪個工具或查哪份 API 文件。
- 修改範圍：只描述最小變更位置，不提供整個類別的重寫版。

無法提出反例的觀察一律標成 VERIFY。不要替人工審查者下合併結論。

待審查 diff：

diff --git a/DailyImportGate.java b/DailyImportGate.java
new file mode 100644
--- /dev/null
+++ b/DailyImportGate.java
@@ -0,0 +1,27 @@
+package com.ithome.day09.review;
+
+import java.util.Locale;
+import java.util.Set;
+import java.util.concurrent.ConcurrentHashMap;
+
+public final class DailyImportGate {
+
+    private final Set<String> runningWorkspaces =
+            ConcurrentHashMap.newKeySet();
+
+    public boolean tryStart(String workspaceId) {
+        if (workspaceId.isBlank()) {
+            throw new IllegalArgumentException("workspaceId must not be blank");
+        }
+        String key = workspaceId.strip().toLowerCase(Locale.ROOT);
+        if (runningWorkspaces.contains(key)) {
+            return false;
+        }
+        runningWorkspaces.add(key);
+        return true;
+    }
+
+    public void finish(String workspaceId) {
+        runningWorkspaces.remove(workspaceId);
+    }
+}
```

### 補作模擬回覆

#### 驗證卡一：null 輸入洩漏非預期例外

- 判定：`BLOCK`
- 程式依據：`tryStart` 先呼叫 `workspaceId.isBlank()`，沒有先判斷 null。
- 反例：呼叫 `tryStart(null)` 時，程式會在 `isBlank()` 拋出 `NullPointerException`，不符合無效輸入應回報 `IllegalArgumentException` 的規則。
- 可執行確認：新增 JUnit 5 測試，以 `assertThrows(IllegalArgumentException.class, () -> gate.tryStart(null))` 驗證例外型別；在修正前執行測試應失敗。
- 修改範圍：只調整 `tryStart` 的輸入驗證，先處理 null，再檢查空白。

#### 驗證卡二：檢查與登記不是單一操作

- 判定：`BLOCK`
- 程式依據：`runningWorkspaces.contains(key)` 與 `runningWorkspaces.add(key)` 分成兩次呼叫。
- 反例：執行緒 A 與 B 都對同一個 key 呼叫 `contains`，兩者都取得 `false`；A 的 `add` 回傳 `true`，B 的 `add` 回傳 `false`，但原方法忽略 `add` 的回傳值，兩個 `tryStart` 最後都直接回傳 `true`。結果是兩個排程都認為自己已取得啟動權。
- 可執行確認：新增兩個執行緒同時呼叫 `tryStart("workspace-42")` 的 JUnit 5 測試，斷言兩個回傳值中只能有一個是 `true`。測試須控制關鍵時序，避免只靠重複執行碰運氣。
- 修改範圍：只調整 `tryStart` 的檢查與登記方式，讓一次集合操作的回傳值決定是否啟動。

#### 驗證卡三：先確認集合保證

- 判定：`VERIFY`
- 程式依據：欄位型別只有 `Set<String>`，實作由 `ConcurrentHashMap.newKeySet()` 建立；目前 diff 沒有說明依賴的執行緒安全保證。
- 反例：沒有足夠依據證明集合的單次操作不安全，因此不能直接判定缺陷。
- 可執行確認：查閱 Java 17 的 `ConcurrentHashMap.newKeySet()`、`KeySetView` 與 `Set.add` API 文件，確認單次 `add` 的並行語意及回傳值。
- 修改範圍：確認文件前不改欄位；若保證成立，只需處理驗證卡二的複合操作。

以上是待驗證清單，不是合併結論。`finish` 的輸入處理與正規化規則也應加入測試矩陣，但僅憑目前列出的反例，尚未完成可重現確認。

## 第二輪：把兩個阻擋項目改成測試規格

### 我追問

```text
先不要提供修正版程式。請把兩個 BLOCK 各改寫成一項 JUnit 5 測試規格，列出測試名稱、安排、動作、斷言，以及測試可能產生假陰性的地方。
```

### 補作模擬回覆

#### 測試一：null 應視為無效輸入

- 測試名稱：`rejectsNullWorkspaceIdAsInvalidInput`
- 安排：建立新的 `DailyImportGate`。
- 動作：呼叫 `tryStart(null)`。
- 斷言：應拋出 `IllegalArgumentException`。
- 假陰性風險：若只斷言「有拋出例外」，`NullPointerException` 也會通過；必須指定例外型別。

#### 測試二：相同工作區只能有一次啟動成功

- 測試名稱：`onlyOneConcurrentAttemptStartsTheSameWorkspace`
- 安排：建立兩個執行緒，讓兩者對同一個 `workspaceId` 呼叫 `tryStart`。
- 動作：在兩個呼叫都完成後收集布林回傳值。
- 斷言：恰好一個回傳值是 `true`，另一個是 `false`。
- 假陰性風險：若直接提交兩個工作而不控制時序，第一個執行緒可能在第二個開始前完成 `add`，缺陷版也會偶然通過。測試需要屏障或可注入的集合，把兩個呼叫固定在檢查完成、登記尚未完成的區間。

## 人工複核註記

- null 與 `contains`／`add` 兩項已轉成修正前會失敗的 JUnit 5 測試。
- Java 17 API 文件證實 `ConcurrentHashMap.newKeySet()` 提供可安全並行使用的集合；第三張卡經查證後排除，不是容器缺陷。
- 補作回覆只提醒 `finish` 應進入測試矩陣，沒有指出它以未正規化字串移除鍵的具體反例；此漏報由人工審查補上。
- 完整測試、修正與執行結果見 `README.md` 與 `docs/verification-log.md`。
