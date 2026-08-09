package com.ithome.day18.report;

import java.time.ZonedDateTime;
import java.util.Objects;

/**
 * Legacy sample: scheduling, report composition, PDF rendering, and email delivery
 * are intentionally coordinated in one method so the refactoring seam is visible.
 */
public class DailyReportService {

    private final MetricsSource metricsSource;
    private final PdfRenderer pdfRenderer;
    private final MailGateway mailGateway;

    public DailyReportService(
            MetricsSource metricsSource,
            PdfRenderer pdfRenderer,
            MailGateway mailGateway) {
        this.metricsSource = Objects.requireNonNull(metricsSource);
        this.pdfRenderer = Objects.requireNonNull(pdfRenderer);
        this.mailGateway = Objects.requireNonNull(mailGateway);
    }

    public boolean runIfScheduled(ZonedDateTime now, Customer customer) {
        Objects.requireNonNull(now, "now");
        Objects.requireNonNull(customer, "customer");

        if (now.getHour() != 8 || now.getMinute() != 0) {
            return false;
        }

        Metrics metrics = metricsSource.loadPreviousDay(customer.id());
        String body = "前一日筆數：" + metrics.previousDayCount()
                + "\n成長率：" + metrics.growthRatePercent() + "%";
        byte[] attachment = pdfRenderer.render("每日報表\n" + body);

        mailGateway.send(new MailMessage(
                customer.email(),
                "每日報表",
                body,
                "daily-report.pdf",
                attachment));
        return true;
    }

    public record Customer(String id, String email) {
    }

    public record Metrics(long previousDayCount, double growthRatePercent) {
    }

    public record MailMessage(
            String to,
            String subject,
            String body,
            String attachmentName,
            byte[] attachment) {
    }

    @FunctionalInterface
    public interface MetricsSource {
        Metrics loadPreviousDay(String customerId);
    }

    @FunctionalInterface
    public interface PdfRenderer {
        byte[] render(String content);
    }

    @FunctionalInterface
    public interface MailGateway {
        void send(MailMessage message);
    }
}
