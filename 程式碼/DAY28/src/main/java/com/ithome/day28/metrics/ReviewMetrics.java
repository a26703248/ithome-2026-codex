package com.ithome.day28.metrics;

/**
 * {@link ReviewMetricsCalculator} 的彙總結果。所有欄位皆為對一批
 * {@link ReviewRecord} 取平均或比例，樣本數（sampleSize）必須跟著結果
 * 一起呈現，避免只看單一數字就下結論。
 */
public final class ReviewMetrics {

    private final int sampleSize;
    private final double avgDraftToFinalMinutes;
    private final double avgReviewMinutes;
    private final double majorRevisionOrRejectRate;
    private final double completionRate;
    private final double avgCitationErrorCount;

    public ReviewMetrics(int sampleSize, double avgDraftToFinalMinutes, double avgReviewMinutes,
                          double majorRevisionOrRejectRate, double completionRate,
                          double avgCitationErrorCount) {
        this.sampleSize = sampleSize;
        this.avgDraftToFinalMinutes = avgDraftToFinalMinutes;
        this.avgReviewMinutes = avgReviewMinutes;
        this.majorRevisionOrRejectRate = majorRevisionOrRejectRate;
        this.completionRate = completionRate;
        this.avgCitationErrorCount = avgCitationErrorCount;
    }

    public int sampleSize() {
        return sampleSize;
    }

    public double avgDraftToFinalMinutes() {
        return avgDraftToFinalMinutes;
    }

    public double avgReviewMinutes() {
        return avgReviewMinutes;
    }

    /** 「大幅修改」或「否決」佔全部樣本的比例，對應需求書第七節的問題。 */
    public double majorRevisionOrRejectRate() {
        return majorRevisionOrRejectRate;
    }

    /** 未被否決、有進入定稿流程的比例；否決視為未完成任務。 */
    public double completionRate() {
        return completionRate;
    }

    public double avgCitationErrorCount() {
        return avgCitationErrorCount;
    }
}
