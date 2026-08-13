package com.ithome.day22.report;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** A reduced batch workflow used to keep documentation claims reproducible. */
public final class ReportBatch {

    private final ReportPreparer reportPreparer;
    private final MailGateway mailGateway;

    public ReportBatch(ReportPreparer reportPreparer, MailGateway mailGateway) {
        this.reportPreparer = Objects.requireNonNull(reportPreparer);
        this.mailGateway = Objects.requireNonNull(mailGateway);
    }

    public void runTwoPhaseExperiment(List<Customer> customers) {
        List<PreparedReport> preparedReports = new ArrayList<>();

        // 先完成所有報表準備，再呼叫郵件服務，避免慢速回應推遲下一份報表。
        // 這項實驗沒有縮短郵件總耗時。
        for (Customer customer : List.copyOf(customers)) {
            preparedReports.add(reportPreparer.prepare(customer));
        }

        preparedReports.forEach(mailGateway::send);
    }

    public record Customer(String id) {
        public Customer {
            Objects.requireNonNull(id);
        }
    }

    public record PreparedReport(Customer customer, byte[] attachment) {
        public PreparedReport {
            Objects.requireNonNull(customer);
            attachment = attachment.clone();
        }
    }

    @FunctionalInterface
    public interface ReportPreparer {
        PreparedReport prepare(Customer customer);
    }

    @FunctionalInterface
    public interface MailGateway {
        void send(PreparedReport report);
    }
}
