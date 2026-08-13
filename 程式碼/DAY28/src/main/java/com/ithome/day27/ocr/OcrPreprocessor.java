package com.ithome.day27.ocr;

/**
 * 「AI 輔助生成系統」ETL 前處理流程中，OCR 辨識完成後的分流判斷。
 * 只處理判斷邏輯本身，不含實際 OCR 引擎呼叫、佇列或重試排程。
 *
 * 門檻值為本次案例示範設定，不是公司已核定的正式標準；正式門檻仍待
 * 需求書第七節提出的「不同文件品質是否有不同標準」跨部門確認。
 */
public final class OcrPreprocessor {

    /** 信心分數達到此門檻（含）以上，直接接受並進入草稿生成。 */
    public static final double ACCEPT_THRESHOLD = 0.90;

    /** 信心分數達到此門檻（含）以上、未達 ACCEPT_THRESHOLD，交由人工複核。 */
    public static final double MANUAL_REVIEW_THRESHOLD = 0.70;

    /** 低於 MANUAL_REVIEW_THRESHOLD 時，最多允許重試的次數。 */
    public static final int MAX_RETRY = 2;

    /**
     * 依辨識文字與信心分數決定下一步。
     *
     * @param extractedText   OCR 辨識出的文字，可能為 {@code null} 或空白
     * @param confidenceScore OCR 引擎回報的信心分數，介於 0.0～1.0
     * @param retryCount      這份掃描檔目前已經重試的次數
     */
    public OcrOutcome evaluate(String extractedText, double confidenceScore, int retryCount) {
        if (extractedText == null || extractedText.isBlank()) {
            return OcrOutcome.REJECT;
        }
        if (confidenceScore >= ACCEPT_THRESHOLD) {
            return OcrOutcome.ACCEPT;
        }
        if (confidenceScore >= MANUAL_REVIEW_THRESHOLD) {
            return OcrOutcome.MANUAL_REVIEW;
        }
        if (retryCount < MAX_RETRY) {
            return OcrOutcome.RETRY;
        }
        return OcrOutcome.REJECT;
    }
}
