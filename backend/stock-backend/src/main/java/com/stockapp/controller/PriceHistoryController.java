package com.stockapp.controller;

import com.stockapp.dto.PageResponse;
import com.stockapp.dto.PriceHistoryResponse;
import com.stockapp.service.PriceHistoryService;
import io.swagger.v3.oas.annotations.Parameter;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Pattern;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/stocks")
@Validated
public class PriceHistoryController {

    private final PriceHistoryService service;

    public PriceHistoryController(PriceHistoryService service) {
        this.service = service;
    }

    @GetMapping("/{symbol}/history")
    public PageResponse<PriceHistoryResponse> getHistory(

            @Parameter(description = "Stock symbol (e.g. RELIANCE, TCS, INFY)")
            @PathVariable
            @Pattern(
                    regexp = "^[a-zA-Z0-9]+$",
                    message = "Stock symbol must contain only letters and numbers"
            )
            String symbol,

            @Parameter(description = "Page number (0-based)")
            @RequestParam(defaultValue = "0")
            @Min(value = 0, message = "Page number cannot be negative")
            int page,

            @Parameter(description = "Number of records per page")
            @RequestParam(defaultValue = "20")
            @Min(value = 1, message = "Page size must be greater than zero")
            int size,

            @Parameter(description = "Sort format: field,direction (e.g. timestamp,desc)")
            @RequestParam(defaultValue = "timestamp,desc")
            String sort) {

        return service.getHistory(symbol, page, size, sort);
    }
}