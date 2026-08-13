package com.ithome.day23.report;

import static java.nio.charset.StandardCharsets.US_ASCII;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import org.junit.jupiter.api.Test;

class PdfReportRendererTest {

    @Test
    void createsPdfWithoutLoadingExternalPdfInput() throws Exception {
        byte[] result = new PdfReportRenderer().renderBlankReport();

        assertTrue(result.length > 100);
        assertEquals("%PDF", new String(Arrays.copyOf(result, 4), US_ASCII));
    }
}
