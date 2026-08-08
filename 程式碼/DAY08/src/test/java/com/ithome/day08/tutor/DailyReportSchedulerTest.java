package com.ithome.day08.tutor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Method;
import org.junit.jupiter.api.Test;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;

class DailyReportSchedulerTest {

    @Test
    void declaresConfigurableCronAndTimeZone() throws Exception {
        assertTrue(SchedulingConfiguration.class.isAnnotationPresent(EnableScheduling.class));
        Method method = DailyReportScheduler.class.getMethod("importDailyReport");
        Scheduled scheduled = method.getAnnotation(Scheduled.class);

        assertEquals("${daily-import.cron:0 0 9 * * *}", scheduled.cron());
        assertEquals("${daily-import.zone:Asia/Taipei}", scheduled.zone());
    }
}
