package com.ithome.day21.report;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.ithome.day21.report.DailyReportBatch.Customer;
import com.ithome.day21.report.DailyReportBatch.Diagnostics;
import com.ithome.day21.report.DailyReportBatch.Timing;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class DailyReportBatchDebugTest {

    private static final List<Customer> CUSTOMERS =
            List.of(new Customer("customer-001"), new Customer("customer-002"));

    @Test
    void slowMailDelaysTheNextPreparationInTheLegacyFlow() {
        Fixture fixture = new Fixture(900);

        fixture.batch.runLegacyForReproduction(CUSTOMERS);

        assertEquals(0, fixture.startedAt("customer-001", "prepare"));
        assertEquals(950, fixture.startedAt("customer-002", "prepare"));
        assertEquals(900, fixture.elapsed("customer-001", "mail"));
    }

    @Test
    void replacingMailWithAFastStubRemovesMostOfTheObservedDelay() {
        Fixture fixture = new Fixture(0);

        fixture.batch.runLegacyForReproduction(CUSTOMERS);

        assertEquals(50, fixture.startedAt("customer-002", "prepare"));
        assertEquals(10, fixture.elapsed("customer-001", "read"));
        assertEquals(40, fixture.elapsed("customer-001", "pdf"));
    }

    @Test
    void twoPhaseExperimentPreparesEveryReportBeforeEnteringTheMailBoundary() {
        Fixture fixture = new Fixture(900);

        fixture.batch.runTwoPhaseExperiment(CUSTOMERS);

        assertEquals(50, fixture.startedAt("customer-002", "prepare"));
        assertEquals(
                List.of("prepare:customer-001", "prepare:customer-002", "mail:customer-001", "mail:customer-002"),
                fixture.boundaryEvents);
    }

    private static final class Fixture {
        private final FakeClock clock = new FakeClock();
        private final Diagnostics diagnostics = new Diagnostics();
        private final List<String> boundaryEvents = new ArrayList<>();
        private final DailyReportBatch batch;

        private Fixture(long mailLatencyMs) {
            batch = new DailyReportBatch(
                    customer -> {
                        boundaryEvents.add("prepare:" + customer.id());
                        clock.advance(10);
                        return new DailyReportBatch.Metrics(1280, 12.5);
                    },
                    (customer, metrics) -> {
                        clock.advance(40);
                        return new byte[] {1, 2, 3};
                    },
                    (customer, attachment) -> {
                        boundaryEvents.add("mail:" + customer.id());
                        clock.advance(mailLatencyMs);
                    },
                    clock::millis,
                    diagnostics);
        }

        private long startedAt(String customerId, String stage) {
            return timing(customerId, stage).startedAtMs();
        }

        private long elapsed(String customerId, String stage) {
            return timing(customerId, stage).elapsedMs();
        }

        private Timing timing(String customerId, String stage) {
            return diagnostics.snapshot().stream()
                    .filter(timing -> timing.customerId().equals(customerId))
                    .filter(timing -> timing.stage().equals(stage))
                    .findFirst()
                    .orElseThrow();
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
