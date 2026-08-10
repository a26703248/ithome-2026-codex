package com.ithome.day27.ocr;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * 這份測試檔本身就是 Day 27 文章比較「一次生成」與「拆小步驟」兩種策略的對象。
 * 邊界案例（第 3、4 項）是策略 A 第一次生成時漏掉、覆核後才補上的部分。
 */
class OcrPreprocessorTest {

    private final OcrPreprocessor preprocessor = new OcrPreprocessor();

    @Test
    void highConfidenceTextIsAccepted() {
        assertEquals(OcrOutcome.ACCEPT, preprocessor.evaluate("採購單內容", 0.95, 0));
    }

    @Test
    void exactAcceptThresholdIsAccepted() {
        // 邊界案例：信心分數剛好等於門檻值，仍應視為接受，不是進入複核。
        assertEquals(OcrOutcome.ACCEPT, preprocessor.evaluate("採購單內容", 0.90, 0));
    }

    @Test
    void midConfidenceGoesToManualReview() {
        assertEquals(OcrOutcome.MANUAL_REVIEW, preprocessor.evaluate("採購單內容", 0.80, 0));
    }

    @Test
    void exactManualReviewThresholdGoesToManualReview() {
        // 邊界案例：信心分數剛好等於複核門檻，應進複核，不是被視為可重試。
        assertEquals(OcrOutcome.MANUAL_REVIEW, preprocessor.evaluate("採購單內容", 0.70, 0));
    }

    @Test
    void lowConfidenceWithRetriesLeftIsRetried() {
        assertEquals(OcrOutcome.RETRY, preprocessor.evaluate("模糊掃描內容", 0.50, 0));
    }

    @Test
    void lowConfidenceRetryBudgetExhaustedIsRejected() {
        assertEquals(OcrOutcome.REJECT, preprocessor.evaluate("模糊掃描內容", 0.50, 2));
    }

    @Test
    void blankTextIsRejectedRegardlessOfConfidence() {
        assertEquals(OcrOutcome.REJECT, preprocessor.evaluate("   ", 0.99, 0));
    }

    @Test
    void nullTextIsRejected() {
        assertEquals(OcrOutcome.REJECT, preprocessor.evaluate(null, 0.99, 0));
    }
}
