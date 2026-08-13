package com.ithome.day27.ocr;

/**
 * OCR／ETL 前處理後，一份掃描檔應該被如何處理。
 * 對應需求書第七節尚待確認的問題：「OCR 辨識準確率的可接受門檻是多少？」
 */
public enum OcrOutcome {
    /** 信心分數達到門檻，直接進入 AI 草稿生成流程。 */
    ACCEPT,
    /** 信心分數落在灰色地帶，交由複核人員判斷是否可用。 */
    MANUAL_REVIEW,
    /** 信心分數過低，但重試次數尚未用盡，交回 OCR 重新辨識。 */
    RETRY,
    /** 內容為空，或信心分數過低且重試次數已用盡，直接退回上傳者。 */
    REJECT
}
