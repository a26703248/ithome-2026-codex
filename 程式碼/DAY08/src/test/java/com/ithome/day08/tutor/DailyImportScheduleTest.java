package com.ithome.day08.tutor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.Instant;
import org.junit.jupiter.api.Test;

class DailyImportScheduleTest {

    private static final Instant NOW = Instant.parse("2026-08-18T23:30:00Z");

    @Test
    void rejectsFiveFieldUnixCronExpression() {
        assertThrows(
                IllegalArgumentException.class,
                () -> new DailyImportSchedule("0 9 * * *", "Asia/Taipei"));
    }

    @Test
    void calculatesNextTaipeiNineAmAsUtcInstant() {
        DailyImportSchedule schedule =
                new DailyImportSchedule("0 0 9 * * *", "Asia/Taipei");

        assertEquals(Instant.parse("2026-08-19T01:00:00Z"), schedule.nextAfter(NOW));
    }

    @Test
    void sameNineAmCronProducesDifferentInstantInTokyo() {
        DailyImportSchedule schedule =
                new DailyImportSchedule("0 0 9 * * *", "Asia/Tokyo");

        assertEquals(Instant.parse("2026-08-19T00:00:00Z"), schedule.nextAfter(NOW));
    }
}
