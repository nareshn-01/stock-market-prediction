package com.stockapp.dto;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StockResponse {

    private Long id;

    private String symbol;

    private String exchange;

    private String companyName;

    private String sector;
}