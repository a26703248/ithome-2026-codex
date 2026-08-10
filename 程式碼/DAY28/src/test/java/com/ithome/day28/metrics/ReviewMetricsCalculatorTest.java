package com.ithome.day28.metrics;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * 本測試檔本身就是 Day 28 文章「配對前後測」比較的對象：同一份規格分別以
 * 人工撰寫（基準線）與 Codex 協作（AI 協作）各實作一次，見
 * docs/baseline-log.md 的計時紀錄。最後一項測試使用的 16 筆樣本資料，
 * 就是文章「分析」表格數字的原始來源。
 */
class ReviewMetricsCalculatorTest {

    private final ReviewMetricsCalculator calculator = new ReviewMetricsCalculator();

    @Test
    void nullRecordsThrowsException() {
        assertThrows(NullPointerException.class, () -> calculator.calculate(null));
    }

    @Test
    void emptyRecordsThrowsException() {
        // 沒有樣本時直接丟例外，不要算出一個看似正常、其實沒有意義的平均值。
        assertThrows(IllegalArgumentException.class, () -> calculator.calculate(List.of()));
    }

    @Test
    void singleRecordAveragesEqualItsOwnValues() {
        ReviewRecord record = new ReviewRecord("d-01", ReviewCohort.BASELINE, 100, 20,
                ReviewOutcome.ACCEPTED, 0);
        ReviewMetrics metrics = calculator.calculate(List.of(record));

        assertEquals(1, metrics.sampleSize());
        assertEquals(100.0, metrics.avgDraftToFinalMinutes(), 0.001);
        assertEquals(20.0, metrics.avgReviewMinutes(), 0.001);
        assertEquals(0.0, metrics.majorRevisionOrRejectRate(), 0.001);
        assertEquals(1.0, metrics.completionRate(), 0.001);
    }

    @Test
    void multipleRecordsAverageDraftToFinalAndReviewMinutes() {
        List<ReviewRecord> records = List.of(
                new ReviewRecord("d-01", ReviewCohort.BASELINE, 100, 20, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("d-02", ReviewCohort.BASELINE, 120, 30, ReviewOutcome.ACCEPTED, 0)
        );
        ReviewMetrics metrics = calculator.calculate(records);

        assertEquals(110.0, metrics.avgDraftToFinalMinutes(), 0.001);
        assertEquals(25.0, metrics.avgReviewMinutes(), 0.001);
    }

    @Test
    void majorRevisionOrRejectRateCountsBothCategories() {
        List<ReviewRecord> records = List.of(
                new ReviewRecord("d-01", ReviewCohort.AI_ASSISTED, 60, 20, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("d-02", ReviewCohort.AI_ASSISTED, 60, 20, ReviewOutcome.MAJOR_REVISION, 1),
                new ReviewRecord("d-03", ReviewCohort.AI_ASSISTED, 60, 20, ReviewOutcome.REJECTED, 1),
                new ReviewRecord("d-04", ReviewCohort.AI_ASSISTED, 60, 20, ReviewOutcome.ACCEPTED, 0)
        );
        ReviewMetrics metrics = calculator.calculate(records);

        // 大幅修改與否決都算「需要額外人工介入」，兩者合計 2/4。
        assertEquals(0.5, metrics.majorRevisionOrRejectRate(), 0.001);
    }

    @Test
    void completionRateExcludesOnlyRejected() {
        List<ReviewRecord> records = List.of(
                new ReviewRecord("d-01", ReviewCohort.BASELINE, 60, 20, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("d-02", ReviewCohort.BASELINE, 60, 20, ReviewOutcome.MAJOR_REVISION, 0),
                new ReviewRecord("d-03", ReviewCohort.BASELINE, 60, 20, ReviewOutcome.REJECTED, 0)
        );
        ReviewMetrics metrics = calculator.calculate(records);

        // 大幅修改後仍有定稿，只有否決才算沒完成：2/3。
        assertEquals(2.0 / 3.0, metrics.completionRate(), 0.001);
    }

    @Test
    void avgCitationErrorCountAcrossRecords() {
        List<ReviewRecord> records = List.of(
                new ReviewRecord("d-01", ReviewCohort.AI_ASSISTED, 60, 20, ReviewOutcome.ACCEPTED, 2),
                new ReviewRecord("d-02", ReviewCohort.AI_ASSISTED, 60, 20, ReviewOutcome.ACCEPTED, 0)
        );
        ReviewMetrics metrics = calculator.calculate(records);

        assertEquals(1.0, metrics.avgCitationErrorCount(), 0.001);
    }

    @Test
    void baselineAndAiAssistedCohortsProduceDifferentMetrics() {
        // 與 docs/baseline-log.md 的「批次二：AI 輔助生成系統」16 筆樣本一致，
        // 是文章「分析」表格數字的原始來源，非自動化系統量測。
        List<ReviewRecord> baseline = List.of(
                new ReviewRecord("baseline-01", ReviewCohort.BASELINE, 108, 18, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("baseline-02", ReviewCohort.BASELINE, 95, 20, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("baseline-03", ReviewCohort.BASELINE, 120, 25, ReviewOutcome.MAJOR_REVISION, 1),
                new ReviewRecord("baseline-04", ReviewCohort.BASELINE, 88, 16, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("baseline-05", ReviewCohort.BASELINE, 102, 22, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("baseline-06", ReviewCohort.BASELINE, 130, 28, ReviewOutcome.REJECTED, 1),
                new ReviewRecord("baseline-07", ReviewCohort.BASELINE, 90, 19, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("baseline-08", ReviewCohort.BASELINE, 99, 21, ReviewOutcome.ACCEPTED, 0)
        );
        List<ReviewRecord> aiAssisted = List.of(
                new ReviewRecord("ai-01", ReviewCohort.AI_ASSISTED, 58, 24, ReviewOutcome.ACCEPTED, 1),
                new ReviewRecord("ai-02", ReviewCohort.AI_ASSISTED, 65, 31, ReviewOutcome.MAJOR_REVISION, 2),
                new ReviewRecord("ai-03", ReviewCohort.AI_ASSISTED, 52, 22, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("ai-04", ReviewCohort.AI_ASSISTED, 70, 35, ReviewOutcome.MAJOR_REVISION, 1),
                new ReviewRecord("ai-05", ReviewCohort.AI_ASSISTED, 60, 28, ReviewOutcome.ACCEPTED, 1),
                new ReviewRecord("ai-06", ReviewCohort.AI_ASSISTED, 55, 26, ReviewOutcome.ACCEPTED, 0),
                new ReviewRecord("ai-07", ReviewCohort.AI_ASSISTED, 74, 33, ReviewOutcome.REJECTED, 2),
                new ReviewRecord("ai-08", ReviewCohort.AI_ASSISTED, 62, 29, ReviewOutcome.ACCEPTED, 1)
        );

        ReviewMetrics baselineMetrics = calculator.calculate(baseline);
        ReviewMetrics aiMetrics = calculator.calculate(aiAssisted);

        assertEquals(104.0, baselineMetrics.avgDraftToFinalMinutes(), 0.01);
        assertEquals(21.125, baselineMetrics.avgReviewMinutes(), 0.01);
        assertEquals(0.25, baselineMetrics.majorRevisionOrRejectRate(), 0.01);
        assertEquals(0.875, baselineMetrics.completionRate(), 0.01);
        assertEquals(0.25, baselineMetrics.avgCitationErrorCount(), 0.01);

        assertEquals(62.0, aiMetrics.avgDraftToFinalMinutes(), 0.01);
        assertEquals(28.5, aiMetrics.avgReviewMinutes(), 0.01);
        assertEquals(0.375, aiMetrics.majorRevisionOrRejectRate(), 0.01);
        assertEquals(0.875, aiMetrics.completionRate(), 0.01);
        assertEquals(1.0, aiMetrics.avgCitationErrorCount(), 0.01);
    }
}
