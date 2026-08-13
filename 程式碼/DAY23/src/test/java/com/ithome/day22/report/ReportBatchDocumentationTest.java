package com.ithome.day22.report;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.ithome.day22.report.ReportBatch.Customer;
import com.ithome.day22.report.ReportBatch.PreparedReport;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ReportBatchDocumentationTest {

    private static final List<Customer> CUSTOMERS =
            List.of(new Customer("customer-001"), new Customer("customer-002"));

    @Test
    void preparesEveryReportBeforeEnteringTheMailBoundary() {
        Fixture fixture = new Fixture(900);

        fixture.batch.runTwoPhaseExperiment(CUSTOMERS);

        assertEquals(
                List.of(
                        "prepare:customer-001",
                        "prepare:customer-002",
                        "mail:customer-001",
                        "mail:customer-002"),
                fixture.events);
    }

    @Test
    void slowMailDoesNotPostponePreparationButStillConsumesDeliveryTime() {
        Fixture fixture = new Fixture(900);

        fixture.batch.runTwoPhaseExperiment(CUSTOMERS);

        assertEquals(50, fixture.preparationStartedAt.get("customer-002"));
        assertEquals(1900, fixture.clock.millis());
    }

    private static final class Fixture {
        private final FakeClock clock = new FakeClock();
        private final List<String> events = new ArrayList<>();
        private final Map<String, Long> preparationStartedAt = new LinkedHashMap<>();
        private final ReportBatch batch;

        private Fixture(long mailLatencyMs) {
            batch = new ReportBatch(
                    customer -> {
                        events.add("prepare:" + customer.id());
                        preparationStartedAt.put(customer.id(), clock.millis());
                        clock.advance(50);
                        return new PreparedReport(customer, new byte[] {1, 2, 3});
                    },
                    report -> {
                        events.add("mail:" + report.customer().id());
                        clock.advance(mailLatencyMs);
                    });
        }
    }

    private static final class FakeClock {
        private long nowMs;

        private long millis() {
            return nowMs;
        }

        private void advance(long milliseconds) {
            nowMs += milliseconds;
        }
    }
}
