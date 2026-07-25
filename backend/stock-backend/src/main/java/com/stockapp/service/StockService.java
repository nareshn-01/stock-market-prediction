package com.stockapp.service;

import com.stockapp.dto.StockResponse;
import com.stockapp.entity.Stock;
import com.stockapp.repository.StockRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StockService {

    private static final Logger log =
            LoggerFactory.getLogger(StockService.class);

    private final StockRepository stockRepository;

    public StockService(StockRepository stockRepository) {
        this.stockRepository = stockRepository;
    }

    public List<StockResponse> getAllStocks() {

        log.info("Fetching all stocks");

        List<StockResponse> stocks = stockRepository.findAll()
                .stream()
                .map(this::mapToResponse)
                .toList();

        log.info("Found {} stocks", stocks.size());

        return stocks;
    }

    private StockResponse mapToResponse(Stock stock) {
        return StockResponse.builder()
                .id(stock.getId())
                .symbol(stock.getSymbol())
                .exchange(stock.getExchange())
                .companyName(stock.getCompanyName())
                .sector(stock.getSector())
                .build();
    }
}