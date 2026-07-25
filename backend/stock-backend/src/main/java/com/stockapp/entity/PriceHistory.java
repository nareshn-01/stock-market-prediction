package com.stockapp.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "price_history")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PriceHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "stock_id", nullable = false)
    private Stock stock;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal open;

    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal high;

    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal low;

    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal close;

    @Column(nullable = false)
    private Long volume;

    @Column(nullable = false)
    private String interval;
}