package com.ithome.day23.report;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;

/** Reduced PDF generation path. It does not accept or parse an existing PDF. */
public final class PdfReportRenderer {

    public byte[] renderBlankReport() throws IOException {
        try (PDDocument document = new PDDocument();
                ByteArrayOutputStream output = new ByteArrayOutputStream()) {
            document.addPage(new PDPage());
            document.save(output);
            return output.toByteArray();
        }
    }
}
