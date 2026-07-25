package com.stockapp.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI stockMarketAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Indian Stock Market Analysis API")
                        .description("REST APIs for Indian Stock Market Analysis and Prediction")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("Naresh N")));
    }
}