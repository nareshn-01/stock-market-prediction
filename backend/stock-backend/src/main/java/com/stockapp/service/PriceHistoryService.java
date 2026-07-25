package com.stockapp.service;

import com.stockapp.dto.PageResponse;
import com.stockapp.dto.PriceHistoryResponse;
import com.stockapp.entity.PriceHistory;
import com.stockapp.exception.ResourceNotFoundException;
import com.stockapp.repository.PriceHistoryRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;

@Service
public class PriceHistoryService {

    private static final Logger log =
            LoggerFactory.getLogger(PriceHistoryService.class);

    private final PriceHistoryRepository repository;

    public PriceHistoryService(PriceHistoryRepository repository) {
        this.repository = repository;
    }

    public PageResponse<PriceHistoryResponse> getHistory(
            String symbol,
            int page,
            int size,
            String sort) {

        // Normalize stock symbol
        symbol = symbol.trim().toUpperCase();

        log.info("Fetching price history for stock: {}", symbol);

        String[] sortParts = sort.split(",");

        Sort.Direction direction = Sort.Direction.ASC;
        String sortBy = "timestamp";

        if (sortParts.length == 2) {
            sortBy = sortParts[0];
            direction = Sort.Direction.fromString(sortParts[1]);
        }

        Pageable pageable = PageRequest.of(
                page,
                size,
                Sort.by(direction, sortBy)
        );

        Page<PriceHistory> historyPage =
                repository.findByStock_Symbol(symbol, pageable);

        if (historyPage.isEmpty()) {

            log.warn("No price history found for stock: {}", symbol);

            throw new ResourceNotFoundException(
                    "No price history found for stock: " + symbol);
        }

        log.info("Found {} price history records for stock: {}",
                historyPage.getTotalElements(), symbol);

        return PageResponse.<PriceHistoryResponse>builder()
                .content(historyPage.getContent()
                        .stream()
                        .map(this::mapToResponse)
                        .toList())
                .page(historyPage.getNumber())
                .size(historyPage.getSize())
                .totalElements(historyPage.getTotalElements())
                .totalPages(historyPage.getTotalPages())
                .first(historyPage.isFirst())
                .last(historyPage.isLast())
                .build();
    }

    private PriceHistoryResponse mapToResponse(PriceHistory history) {

        return PriceHistoryResponse.builder()
                .timestamp(history.getTimestamp())
                .open(history.getOpen())
                .high(history.getHigh())
                .low(history.getLow())
                .close(history.getClose())
                .volume(history.getVolume())
                .build();
    }
}