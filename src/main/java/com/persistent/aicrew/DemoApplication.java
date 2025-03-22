package com.persistent.aicrew;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication(scanBasePackages = { "com.persistent.aicrew.service",
"com.persistent.aicrew.repository" })
@ComponentScan(basePackages="com.persistent.aicrew.controller")

@ComponentScan({ "org.slf4j.Logger" })
@EnableCaching
@EnableScheduling
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

}
