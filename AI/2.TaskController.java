package com.example.taskservice.controller;

import com.example.taskservice.model.Task;
import com.example.taskservice.model.TeamMember;
import com.example.taskservice.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/tasks")
public class TaskController {
    
    @Autowired
    private TaskService taskService;
    
    @PostMapping("/assign")
    public ResponseEntity<Task> assignTask(@RequestBody Task task) {
        Task assignedTask = taskService.assignTask(task);
        return ResponseEntity.ok(assignedTask);
    }
    
    // Endpoint dodatkowy do pobrania członków zespołu (przykładowo)
    @GetMapping("/team")
    public ResponseEntity<List<TeamMember>> getTeam() {
        return ResponseEntity.ok(taskService.getTeam());
    }
}
