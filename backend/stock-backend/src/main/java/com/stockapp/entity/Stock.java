package com.stockapp.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "stocks")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Stock {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 20)
    private String symbol;

    @Column(nullable = false, length = 10)
    private String exchange;

    @Column(name = "company_name", nullable = false, length = 150)
    private String companyName;

    @Column(length = 100)
    private String sector;

    @Column(length = 20)
    private String isin;
}