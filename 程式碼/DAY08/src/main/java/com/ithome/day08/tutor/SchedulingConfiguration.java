package com.ithome.day08.tutor;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

@Configuration(proxyBeanMethods = false)
@EnableScheduling
public class SchedulingConfiguration {

    @Bean
    DailyReportScheduler dailyReportScheduler(DailyReportImporter importer) {
        return new DailyReportScheduler(importer);
    }
}
