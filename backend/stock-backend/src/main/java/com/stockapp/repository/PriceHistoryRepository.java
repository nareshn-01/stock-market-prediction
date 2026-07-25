package com.stockapp.repository;

import com.stockapp.entity.PriceHistory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PriceHistoryRepository extends JpaRepository<PriceHistory, Long> {

    Page<PriceHistory> findByStock_Symbol(String symbol, Pageable pageable);

}