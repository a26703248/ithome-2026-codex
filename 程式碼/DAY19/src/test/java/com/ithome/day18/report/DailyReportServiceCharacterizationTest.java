package com.ithome.day18.report;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ithome.day18.report.DailyReportService.Customer;
import com.ithome.day18.report.DailyReportService.MailMessage;
import com.ithome.day18.report.DailyReportService.Metrics;
import java.nio.charset.StandardCharsets;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import org.junit.jupiter.api.Test;

class DailyReportServiceCharacterizationTest {

    private static final ZoneId TAIPEI = ZoneId.of("Asia/Taipei");
    private static final Customer CUSTOMER = new Customer("customer-001", "ops@example.com");

    @Test
    void passesCurrentDailyAttachmentToMailGatewayAtEightOClock() {
        CapturingPdfRenderer pdfRenderer = new CapturingPdfRenderer();
        CapturingMailGateway mailGateway = new CapturingMailGateway();
        DailyReportService service = new DailyReportService(
                ignored -> new Metrics(1280, 12.5),
                pdfRenderer,
                mailGateway);

        boolean triggered = service.runIfScheduled(
                ZonedDateTime.of(2026, 8, 18, 8, 0, 0, 0, TAIPEI),
                CUSTOMER);

        assertTrue(triggered);
        assertEquals(1, pdfRenderer.callCount);
        assertEquals(1, mailGateway.callCount);
        assertEquals("每日報表\n前一日筆數：1280\n成長率：12.5%", pdfRenderer.content);
        assertEquals("ops@example.com", mailGateway.message.to());
        assertEquals("每日報表", mailGateway.message.subject());
        assertEquals("前一日筆數：1280\n成長率：12.5%", mailGateway.message.body());
        assertEquals("daily-report.pdf", mailGateway.message.attachmentName());
        assertEquals("pdf-bytes", new String(
                mailGateway.message.attachment(), StandardCharsets.UTF_8));
    }

    @Test
    void doesNotCallPdfOrMailGatewayBeforeEightOClock() {
        CapturingPdfRenderer pdfRenderer = new CapturingPdfRenderer();
        CapturingMailGateway mailGateway = new CapturingMailGateway();
        DailyReportService service = new DailyReportService(
                ignored -> new Metrics(1280, 12.5),
                pdfRenderer,
                mailGateway);

        boolean triggered = service.runIfScheduled(
                ZonedDateTime.of(2026, 8, 18, 7, 59, 0, 0, TAIPEI),
                CUSTOMER);

        assertFalse(triggered);
        assertEquals(0, pdfRenderer.callCount);
        assertEquals(0, mailGateway.callCount);
        assertNull(pdfRenderer.content);
        assertNull(mailGateway.message);
    }

    private static final class CapturingPdfRenderer implements DailyReportService.PdfRenderer {
        private int callCount;
        private String content;

        @Override
        public byte[] render(String content) {
            callCount++;
            this.content = content;
            return "pdf-bytes".getBytes(StandardCharsets.UTF_8);
        }
    }

    private static final class CapturingMailGateway implements DailyReportService.MailGateway {
        private int callCount;
        private MailMessage message;

        @Override
        public void send(MailMessage message) {
            callCount++;
            this.message = message;
        }
    }
}
