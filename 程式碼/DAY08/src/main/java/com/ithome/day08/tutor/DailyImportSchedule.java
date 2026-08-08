package com.ithome.day08.tutor;

import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Objects;
import org.springframework.scheduling.support.CronExpression;

public final class DailyImportSchedule {

    private final CronExpression expression;
    private final ZoneId zone;

    public DailyImportSchedule(String cron, String zone) {
        this.expression = CronExpression.parse(cron);
        this.zone = ZoneId.of(zone);
    }

    public Instant nextAfter(Instant now) {
        ZonedDateTime localNow = now.atZone(zone);
        ZonedDateTime localNext = expression.next(localNow);
        return Objects.requireNonNull(localNext, "cron has no next execution").toInstant();
    }
}
