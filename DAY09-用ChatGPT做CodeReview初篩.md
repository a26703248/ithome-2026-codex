# Day 09｜用 ChatGPT 做程式碼審查（Code Review）初篩：找到問題，不等於可以合併

![Day 09 封面：先找疑點，再決定能不能合併](./%E5%9C%96%E6%AA%94/Day09/day09-01-cover.png)

Day 08 已用測試保護「每天九點」的時區計算。這次我往排程外移一層，審查新增的匯入閘門。我讀這小段 Java 程式差異（diff）時，視線先停在 `strip` 與 `toLowerCase`；把集合操作排成時序後，才發現互斥判斷被拆成兩步。ChatGPT 可以擴大搜尋面，回覆仍不是合併依據。

## 我把審查責任拆成三層

OpenAI 目前把理解程式碼庫、執行測試與審查變更列為 Codex 工作；本篇的模擬初篩只處理已提供的需求與 diff，不直接操作專案。三層分工如下：

| 審查層次 | 我交給它的工作 | 為何不能單獨作為合併依據 |
|---|---|---|
| ChatGPT 初篩 | 找空值、並行衝突與測試缺口 | 不知道未提供的程式與業務脈絡 |
| 編譯與 JUnit 5 | 重現輸入、時序與實際結果 | 通過只代表已寫下的條件成立 |
| 人工程式碼審查 | 對照需求、否決誤報、決定是否擋下 | 合併責任仍由團隊承擔 |

![Code Review 的初篩、證據與決策三層責任](./%E5%9C%96%E6%AA%94/Day09/day09-02-three-layers.png)

我只問每一點能否轉成失敗斷言；無法重現的先留問題單，不要求作者改碼。以上層次並無誰先誰後，而是涵蓋範圍不同，所以可依照個人習慣調整。

## 先給規則，再貼最小 diff

[完整提示詞](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY09/review-prompt.txt) 先交代兩條本文演練假設：同一個 `workspaceId` 同時間只能有一批匯入，前後空白與英文大小寫不影響識別。兩者尚未寫入 v0 需求，正式開發前仍須確認。模擬輸入只包含 [待審 diff](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY09/review-input.diff)，不要求重寫整個類別。

```java
if (runningWorkspaces.contains(key)) {
    return false;
}
runningWorkspaces.add(key);
return true;
```

因未保存作者本人的 ChatGPT 原始對話，以下標為模擬初篩：null（空值）會在 `isBlank()` 變成 `NullPointerException`，兩個執行緒也可能同時通過 `contains`。方向合理，證據仍是空的。

![去識別化 Java diff 的三個失敗條件](./%E5%9C%96%E6%AA%94/Day09/day09-03-diff-findings.png)

## 把兩項建議寫成紅燈測試

我補了四項 JUnit 5 測試。[修正前測試](./%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY09/before-review) 只多一個讓測試能換入自訂集合的建構子，業務方法仍與待審 diff 相同。`CyclicBarrier` 會在測試用的 `BarrierSet.add` 攔住兩個呼叫，等到齊再放行到實際集合。修正前結果是 `Tests run: 4, Failures: 3`：null 例外錯誤、兩次啟動都回傳成功，還有模擬初篩刻意漏掉的第三項——`tryStart` 存入正規化鍵，`finish` 卻用原字串移除，工作完成後仍無法再次啟動。

最小修正沒有替整個方法加鎖，而是使用 `ConcurrentHashMap.newKeySet()` 所提供集合的單次 `add` 完成「檢查並登記」，再用回傳值判斷是否啟動；開始與完成也共用同一個 `normalize`：

```java
public boolean tryStart(String workspaceId) {
    return runningWorkspaces.add(normalize(workspaceId));
}

public void finish(String workspaceId) {
    runningWorkspaces.remove(normalize(workspaceId));
}
```

重跑 `mvn clean test` 後，四項測試全部通過。[完整程式、測試與驗證紀錄](./%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY09) 也保留了修正前後的結果。

![JUnit 5 測試從三項失敗到四項通過](./%E5%9C%96%E6%AA%94/Day09/day09-04-red-green.png)

## 模擬初篩也要放入誤報與漏報

演練另外放入一項誤報：把 `ConcurrentHashMap.newKeySet()` 本身列成執行緒安全疑點。我查 Java 17 的API文件後否決這項疑慮：容器操作安全，錯在檢查與登記被拆成兩個呼叫。`finish` 的鍵值不一致則留給人工補上。下表的 Java 開發套件（Java Development Kit，JDK）文件就是判斷來源。

| 問題 | 模擬初篩 | 測試／文件 | 最終結論 |
|---|---|---|---|
| null 例外型別 | 找到 | JUnit 5 紅燈 | 修正 |
| `contains`＋`add` | 找到 | 並行測試紅燈 | 改用單次 `add` |
| `newKeySet` 不安全 | 誤報 | JDK 文件 | 否決 |
| `finish` 鍵不一致 | 漏報 | 人工補測試 | 修正 |

![ChatGPT、自動化證據與人工審查的結果比較](./%E5%9C%96%E6%AA%94/Day09/day09-05-comparison.png)

匯入閘門只保護一份 Java 服務；多份同時執行仍需資料庫等共用機制。原始碼也只能放進核准工作區。表格故意保留誤報與漏報，用來示範複核流程，不代表某次真實的 ChatGPT 對話。

## 小結：建議要走到證據，才能進入決策

這份模擬初篩先攤開可能的失敗條件，JUnit 5 與官方文件留下可重現證據，人工審查再補上遺漏脈絡。從 Day 05 到今天，同一份需求已由問題清單走到能執行的驗證。接下來 Day 10 會先講一個故事，定調接下來人類與 Codex 該怎麼合作，再實際讓 Codex 進入工作目錄，觀察代理如何完成一輪任務。

## 參考資料

- [OpenAI：ChatGPT 與 Codex 使用情境](https://learn.chatgpt.com/)
- [Oracle Java 17：ConcurrentHashMap](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)
- [Oracle Java 17：Set.add 與 KeySetView.add](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.KeySetView.html)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/index.html)
- [Apache Maven Surefire Plugin 3.5.3](https://maven.apache.org/surefire-archives/surefire-3.5.3/maven-surefire-plugin/plugin-info.html)
- [資料工作區空間——需求書（v0．初版待釐清）](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/%E8%B3%87%E6%96%99%E5%B7%A5%E4%BD%9C%E5%8D%80%E7%A9%BA%E9%96%93-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
