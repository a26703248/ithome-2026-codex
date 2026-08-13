package com.ithome.day17.report;

import java.time.ZonedDateTime;
import java.util.Objects;

public class ReportProductionWindow {

    public ZonedDateTime productionStartsAt(ZonedDateTime deliveryAt) {
        return Objects.requireNonNull(deliveryAt, "deliveryAt").minusHours(1);
    }
}

