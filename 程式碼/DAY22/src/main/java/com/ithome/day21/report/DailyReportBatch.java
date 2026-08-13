package com.ithome.day21.report;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * A reduced batch workflow used to demonstrate evidence-driven debugging.
 */
public final class DailyReportBatch {

    private final MetricsSource metricsSource;
    private final PdfRenderer pdfRenderer;
    private final MailGateway mailGateway;
    private final MonotonicClock clock;
    private final Diagnostics diagnostics;

    public DailyReportBatch(
            MetricsSource metricsSource,
            PdfRenderer pdfRenderer,
            MailGateway mailGateway,
            MonotonicClock clock,
            Diagnostics diagnostics) {
        this.metricsSource = Objects.requireNonNull(metricsSource);
        this.pdfRenderer = Objects.requireNonNull(pdfRenderer);
        this.mailGateway = Objects.requireNonNull(mailGateway);
        this.clock = Objects.requireNonNull(clock);
        this.diagnostics = Objects.requireNonNull(diagnostics);
    }

    /**
     * Reproduces the legacy coupling: one customer's email must finish before
     * the next customer's report preparation can start.
     */
    public void runLegacyForReproduction(List<Customer> customers) {
        for (Customer customer : List.copyOf(customers)) {
            PreparedReport report = prepare(customer);
            send(report);
        }
    }

    /**
     * Controlled experiment: finish report preparation before entering the
     * slow external mail boundary. This does not reduce total mail time.
     */
    public void runTwoPhaseExperiment(List<Customer> customers) {
        List<PreparedReport> preparedReports = new ArrayList<>();
        for (Customer customer : List.copyOf(customers)) {
            preparedReports.add(prepare(customer));
        }
        preparedReports.forEach(this::send);
    }

    private PreparedReport prepare(Customer customer) {
        long preparationStartedAt = clock.millis();
        diagnostics.record(customer.id(), "prepare", preparationStartedAt, 0);

        long readStartedAt = clock.millis();
        Metrics metrics = metricsSource.load(customer);
        diagnostics.record(
                customer.id(), "read", readStartedAt, clock.millis() - readStartedAt);

        long pdfStartedAt = clock.millis();
        byte[] attachment = pdfRenderer.render(customer, metrics);
        diagnostics.record(
                customer.id(), "pdf", pdfStartedAt, clock.millis() - pdfStartedAt);

        return new PreparedReport(customer, attachment);
    }

    private void send(PreparedReport report) {
        long sendStartedAt = clock.millis();
        mailGateway.send(report.customer(), report.attachment());
        diagnostics.record(
                report.customer().id(), "mail", sendStartedAt, clock.millis() - sendStartedAt);
    }

    public record Customer(String id) {
        public Customer {
            Objects.requireNonNull(id);
        }
    }

    public record Metrics(long previousDayCount, double growthRate) {
    }

    public record Timing(String customerId, String stage, long startedAtMs, long elapsedMs) {
    }

    private record PreparedReport(Customer customer, byte[] attachment) {
        private PreparedReport {
            attachment = attachment.clone();
        }
    }

    @FunctionalInterface
    public interface MetricsSource {
        Metrics load(Customer customer);
    }

    @FunctionalInterface
    public interface PdfRenderer {
        byte[] render(Customer customer, Metrics metrics);
    }

    @FunctionalInterface
    public interface MailGateway {
        void send(Customer customer, byte[] attachment);
    }

    @FunctionalInterface
    public interface MonotonicClock {
        long millis();
    }

    public static final class Diagnostics {
        private final List<Timing> timings = new ArrayList<>();

        public void record(String customerId, String stage, long startedAtMs, long elapsedMs) {
            timings.add(new Timing(customerId, stage, startedAtMs, elapsedMs));
        }

        public List<Timing> snapshot() {
            return List.copyOf(timings);
        }
    }
}
