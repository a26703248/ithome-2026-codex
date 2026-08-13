package com.ithome.day19.report;

import java.time.Clock;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.temporal.ChronoUnit;
import java.util.Objects;

public final class ReportProductionWindow {

    private final Clock clock;

    public ReportProductionWindow(Clock clock) {
        this.clock = Objects.requireNonNull(clock, "clock");
    }

    public boolean shouldStart(LocalTime sendTime, ZoneId reportZone) {
        Objects.requireNonNull(sendTime, "sendTime");
        Objects.requireNonNull(reportZone, "reportZone");

        LocalTime currentMinute = ZonedDateTime.now(clock)
                .withZoneSameInstant(reportZone)
                .toLocalTime()
                .truncatedTo(ChronoUnit.MINUTES);
        LocalTime productionTime = sendTime.minusHours(1);
        return currentMinute.equals(productionTime);
    }
}
