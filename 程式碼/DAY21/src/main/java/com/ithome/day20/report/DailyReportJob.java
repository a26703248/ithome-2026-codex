package com.ithome.day20.report;

import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.Objects;

/**
 * Legacy batch entry invoked by an external scheduler.
 */
public final class DailyReportJob {

    private final ZoneId reportZone;
    private final SubscriberRegistry subscriberRegistry;
    private final DailyReportService reportService;

    public DailyReportJob(
            ZoneId reportZone,
            SubscriberRegistry subscriberRegistry,
            DailyReportService reportService) {
        this.reportZone = Objects.requireNonNull(reportZone);
        this.subscriberRegistry = Objects.requireNonNull(subscriberRegistry);
        this.reportService = Objects.requireNonNull(reportService);
    }

    public int runAt(Instant now) {
        ZonedDateTime reportTime = Objects.requireNonNull(now).atZone(reportZone);
        if (reportTime.getHour() != 8 || reportTime.getMinute() != 0) {
            return 0;
        }

        List<DailyReportService.Customer> customers =
                subscriberRegistry.findDailySubscribers();
        customers.forEach(reportService::generateAndSend);
        return customers.size();
    }

    @FunctionalInterface
    public interface SubscriberRegistry {
        List<DailyReportService.Customer> findDailySubscribers();
    }
}
