package com.ithome.day23.report;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.security.Principal;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ReportController.class)
class ReportControllerSecurityTest {

    private static final Principal ALICE = () -> "alice";

    @Autowired private MockMvc mvc;

    @MockitoBean private ReportController.ReportAccessPolicy accessPolicy;

    @MockitoBean private ReportController.ReportService reportService;

    @Test
    void rejectsUnauthenticatedRequest() throws Exception {
        mvc.perform(validRequest(null)).andExpect(status().isUnauthorized());

        verify(reportService, never()).create(anyString(), any(), anyString());
    }

    @Test
    void authenticatedUserStillNeedsCustomerAuthorization() throws Exception {
        when(accessPolicy.canCreate("alice", "cust-002")).thenReturn(false);

        mvc.perform(validRequest(ALICE)).andExpect(status().isForbidden());

        verify(reportService, never()).create(anyString(), any(), anyString());
    }

    @Test
    void rejectsMalformedCustomerId() throws Exception {
        mvc.perform(post("/customers/not-a-customer/reports")
                        .principal(ALICE)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(validBody()))
                .andExpect(status().isBadRequest())
                .andExpect(content().string(""));
    }

    @Test
    void rejectsUnsupportedFormat() throws Exception {
        mvc.perform(post("/customers/cust-001/reports")
                        .principal(ALICE)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"format":"HTML","fileStem":"daily","recipientEmail":"ops@example.test"}
                                """))
                .andExpect(status().isBadRequest());
    }

    @Test
    void authorizedRequestIsAccepted() throws Exception {
        when(accessPolicy.canCreate("alice", "cust-001")).thenReturn(true);

        mvc.perform(validRequest(ALICE))
                .andExpect(status().isAccepted())
                .andExpect(jsonPath("$.requestId").isNotEmpty());

        verify(reportService).create(anyString(), any(), anyString());
    }

    private static org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder validRequest(
            Principal principal) {
        var request = post("/customers/cust-001/reports")
                .contentType(MediaType.APPLICATION_JSON)
                .content(validBody());
        return principal == null ? request : request.principal(principal);
    }

    private static String validBody() {
        return """
                {"format":"PDF","fileStem":"daily","recipientEmail":"ops@example.test"}
                """;
    }
}
