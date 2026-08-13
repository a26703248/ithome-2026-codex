package com.ithome.day19.report;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import org.junit.jupiter.api.Test;

class ReportProductionWindowTest {

    private static final ZoneId TAIPEI = ZoneId.of("Asia/Taipei");
    private static final LocalTime SEND_TIME = LocalTime.of(8, 0);

    @Test
    void startsOneHourBeforeSendTimeInTheReportZone() {
        Clock ciClock = Clock.fixed(
                Instant.parse("2026-08-18T23:00:00Z"),
                ZoneOffset.UTC);
        ReportProductionWindow window = new ReportProductionWindow(ciClock);

        assertTrue(window.shouldStart(SEND_TIME, TAIPEI));
    }

    @Test
    void doesNotStartOneMinuteBeforeTheProductionWindow() {
        Clock ciClock = Clock.fixed(
                Instant.parse("2026-08-18T22:59:00Z"),
                ZoneOffset.UTC);
        ReportProductionWindow window = new ReportProductionWindow(ciClock);

        assertFalse(window.shouldStart(SEND_TIME, TAIPEI));
    }

    @Test
    void doesNotStartOneMinuteAfterTheProductionWindow() {
        Clock ciClock = Clock.fixed(
                Instant.parse("2026-08-18T23:01:00Z"),
                ZoneOffset.UTC);
        ReportProductionWindow window = new ReportProductionWindow(ciClock);

        assertFalse(window.shouldStart(SEND_TIME, TAIPEI));
    }
}
