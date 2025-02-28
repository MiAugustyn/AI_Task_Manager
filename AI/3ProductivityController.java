package com.example.productivityservice.controller;

import com.example.productivityservice.service.ProductivityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/productivity")
public class ProductivityController {
    
    @Autowired
    private ProductivityService productivityService;
    
    @GetMapping("/report")
    public ResponseEntity<String> generateReport() {
        String report = productivityService.generateReport();
        return ResponseEntity.ok(report);
    }
}
