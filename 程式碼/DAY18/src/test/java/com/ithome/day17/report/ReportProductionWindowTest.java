package com.ithome.day17.report;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.ZoneId;
import java.time.ZonedDateTime;
import org.junit.jupiter.api.Test;

class ReportProductionWindowTest {

    private final ReportProductionWindow window = new ReportProductionWindow();

    @Test
    void startsProductionOneHourBeforeDeliveryInTheSameTimezone() {
        ZonedDateTime deliveryAt = ZonedDateTime.of(
                2026, 8, 17, 8, 0, 0, 0, ZoneId.of("Asia/Taipei"));

        ZonedDateTime actual = window.productionStartsAt(deliveryAt);

        assertEquals(deliveryAt.minusHours(1), actual);
        assertEquals(deliveryAt.getZone(), actual.getZone());
    }

    @Test
    void rejectsMissingDeliveryTime() {
        assertThrows(NullPointerException.class, () -> window.productionStartsAt(null));
    }
}

