package com.ithome.day24.review;

import org.junit.jupiter.api.Test;

import java.util.List;

import static com.ithome.day24.review.ReviewWorkflow.Decision.ACCEPTED;
import static com.ithome.day24.review.ReviewWorkflow.Decision.MODIFIED;
import static com.ithome.day24.review.ReviewWorkflow.Decision.REJECTED;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ReviewWorkflowTest {

    @Test
    void acceptedDraftKeepsOriginalVersion() {
        ReviewWorkflow workflow = new ReviewWorkflow("AI 草稿");

        workflow.submit(ACCEPTED, null, "內容已核對", "reviewer-01");

        assertEquals(1, workflow.versions().size());
        assertEquals(ACCEPTED, workflow.events().get(0).decision());
    }

    @Test
    void modifiedDraftAppendsVersionInsteadOfOverwritingOriginal() {
        ReviewWorkflow workflow = new ReviewWorkflow("原始草稿");

        workflow.submit(MODIFIED, "人工修改稿", "修正引用來源", "reviewer-02");

        assertEquals(List.of("原始草稿", "人工修改稿"),
                workflow.versions().stream().map(ReviewWorkflow.DraftVersion::content).toList());
    }

    @Test
    void everyDecisionRequiresReason() {
        for (ReviewWorkflow.Decision decision : ReviewWorkflow.Decision.values()) {
            ReviewWorkflow workflow = new ReviewWorkflow("待複核草稿");
            String revisedContent = decision == MODIFIED ? "人工修改稿" : null;

            assertThrows(IllegalArgumentException.class,
                    () -> workflow.submit(decision, revisedContent, " ", "reviewer-03"));
        }
    }

    @Test
    void rejectedDraftKeepsOriginalAndRecordsDecision() {
        ReviewWorkflow workflow = new ReviewWorkflow("需保留的原稿");

        workflow.submit(REJECTED, null, "引用來源無法核對", "reviewer-04");

        assertEquals("需保留的原稿", workflow.versions().get(0).content());
        assertEquals("引用來源無法核對", workflow.events().get(0).reason());
    }
}
