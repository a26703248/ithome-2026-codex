package com.ithome.day13.report;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.LocalDate;
import org.junit.jupiter.api.Test;

class ReportRangeServiceTest {

    private final ReportRangeService reportRangeService = new ReportRangeService();

    @Test
    void threeDayRangeIncludesBothEndpoints() {
        assertEquals(
                3,
                reportRangeService.countInclusiveDays(
                        LocalDate.of(2026, 8, 19), LocalDate.of(2026, 8, 21)));
    }

    @Test
    void endBeforeStartIsRejected() {
        assertThrows(
                IllegalArgumentException.class,
                () -> reportRangeService.countInclusiveDays(
                        LocalDate.of(2026, 8, 20), LocalDate.of(2026, 8, 19)));
    }

    @Test
    void nullStartIsRejected() {
        assertThrows(
                NullPointerException.class,
                () -> reportRangeService.countInclusiveDays(null, LocalDate.of(2026, 8, 19)));
    }

    @Test
    void nullEndIsRejected() {
        assertThrows(
                NullPointerException.class,
                () -> reportRangeService.countInclusiveDays(LocalDate.of(2026, 8, 19), null));
    }
}
