package com.example.productivityservice.service;

import org.springframework.stereotype.Service;

@Service
public class ProductivityService {
    // Dane przykładowe – w realnym systemie pobierane z bazy lub innego serwisu
    private int completedTasks = 0;
    private int totalTasks = 0;
    
    public void recordCompletedTask() {
        completedTasks++;
        totalTasks++;
    }
    
    public void recordTask() {
        totalTasks++;
    }
    
    public String generateReport() {
        double efficiency = (totalTasks > 0) ? (completedTasks * 100.0 / totalTasks) : 0;
        return "Zakończone zadania: " + completedTasks + "/" + totalTasks + 
               " (" + String.format("%.2f", efficiency) + "% efektywności)";
    }
}
