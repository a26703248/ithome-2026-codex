package com.ithome.day20.report;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

import com.ithome.day20.report.DailyReportService.Customer;
import com.ithome.day20.report.DailyReportService.MailMessage;
import com.ithome.day20.report.DailyReportService.Metrics;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.ZoneId;
import java.util.List;
import org.junit.jupiter.api.Test;

class DailyReportFlowCharacterizationTest {

    private static final Customer CUSTOMER =
            new Customer("customer-001", "ops@example.com");
    private static final Instant TAIPEI_EIGHT =
            Instant.parse("2026-08-19T00:00:00Z");

    @Test
    void sendsCurrentPdfAndMailAtEightOClock() {
        FlowFixture fixture = new FlowFixture();

        int delivered = fixture.job.runAt(TAIPEI_EIGHT);

        assertEquals(1, delivered);
        assertEquals(1, fixture.subscriberRegistry.callCount);
        assertEquals(1, fixture.metricsSource.callCount);
        assertEquals("customer-001", fixture.metricsSource.customerId);
        assertEquals(1, fixture.pdfRenderer.callCount);
        assertEquals(
                "每日報表\n前一日筆數：1280\n成長率：12.5%",
                fixture.pdfRenderer.content);
        assertEquals(1, fixture.mailGateway.callCount);
        assertEquals("ops@example.com", fixture.mailGateway.message.to());
        assertEquals("daily-report.pdf", fixture.mailGateway.message.attachmentName());
        assertEquals(
                "前一日筆數：1280\n成長率：12.5%",
                fixture.mailGateway.message.body());
        assertSame(fixture.pdfRenderer.result, fixture.mailGateway.message.attachment());
    }

    @Test
    void repeatsCurrentSideEffectsWhenTheSameMinuteRunsTwice() {
        FlowFixture fixture = new FlowFixture();

        fixture.job.runAt(TAIPEI_EIGHT);
        fixture.job.runAt(TAIPEI_EIGHT);

        assertEquals(2, fixture.subscriberRegistry.callCount);
        assertEquals(2, fixture.metricsSource.callCount);
        assertEquals(2, fixture.pdfRenderer.callCount);
        assertEquals(2, fixture.mailGateway.callCount);
    }

    private static final class FlowFixture {
        private final CapturingSubscriberRegistry subscriberRegistry =
                new CapturingSubscriberRegistry();
        private final CapturingMetricsSource metricsSource =
                new CapturingMetricsSource();
        private final CapturingPdfRenderer pdfRenderer =
                new CapturingPdfRenderer();
        private final CapturingMailGateway mailGateway =
                new CapturingMailGateway();
        private final DailyReportJob job = new DailyReportJob(
                ZoneId.of("Asia/Taipei"),
                subscriberRegistry,
                new DailyReportService(metricsSource, pdfRenderer, mailGateway));
    }

    private static final class CapturingSubscriberRegistry
            implements DailyReportJob.SubscriberRegistry {
        private int callCount;

        @Override
        public List<Customer> findDailySubscribers() {
            callCount++;
            return List.of(CUSTOMER);
        }
    }

    private static final class CapturingMetricsSource
            implements DailyReportService.MetricsSource {
        private int callCount;
        private String customerId;

        @Override
        public Metrics loadPreviousDay(String customerId) {
            callCount++;
            this.customerId = customerId;
            return new Metrics(1280, 12.5);
        }
    }

    private static final class CapturingPdfRenderer
            implements DailyReportService.PdfRenderer {
        private int callCount;
        private String content;
        private final byte[] result = "pdf-bytes".getBytes(StandardCharsets.UTF_8);

        @Override
        public byte[] render(String content) {
            callCount++;
            this.content = content;
            return result;
        }
    }

    private static final class CapturingMailGateway
            implements DailyReportService.MailGateway {
        private int callCount;
        private MailMessage message;

        @Override
        public void send(MailMessage message) {
            callCount++;
            this.message = message;
        }
    }
}
