package com.ithome.day23.report;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.security.Principal;
import java.util.Objects;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/customers/{customerId}/reports")
public class ReportController {

    private static final Logger LOG = LoggerFactory.getLogger(ReportController.class);

    private final ReportAccessPolicy accessPolicy;
    private final ReportService reportService;

    public ReportController(ReportAccessPolicy accessPolicy, ReportService reportService) {
        this.accessPolicy = Objects.requireNonNull(accessPolicy);
        this.reportService = Objects.requireNonNull(reportService);
    }

    @PostMapping
    public ResponseEntity<ReportAccepted> create(
            @PathVariable @Pattern(regexp = "cust-[0-9]{3}") String customerId,
            @Valid @RequestBody CreateReportRequest request,
            Principal principal) {
        if (principal == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        if (!accessPolicy.canCreate(principal.getName(), customerId)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }

        String requestId = UUID.randomUUID().toString();
        reportService.create(customerId, request, requestId);
        LOG.info(
                "report request accepted requestId={} customerId={} format={}",
                requestId,
                customerId,
                request.format());
        return ResponseEntity.accepted().body(new ReportAccepted(requestId));
    }

    public record CreateReportRequest(
            @NotNull ReportFormat format,
            @NotBlank @Size(max = 80) @Pattern(regexp = "[A-Za-z0-9_-]+") String fileStem,
            @NotBlank @Email @Size(max = 254) String recipientEmail) {}

    public record ReportAccepted(String requestId) {}

    public enum ReportFormat {
        PDF,
        WORD,
        EXCEL
    }

    @FunctionalInterface
    public interface ReportAccessPolicy {
        boolean canCreate(String actorId, String customerId);
    }

    @FunctionalInterface
    public interface ReportService {
        void create(String customerId, CreateReportRequest request, String requestId);
    }
}
