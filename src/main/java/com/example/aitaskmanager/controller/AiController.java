package com.example.aitaskmanager.controller;

import com.example.aitaskmanager.entity.Task;
import com.example.aitaskmanager.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/ai_suggestions")
public class AiController {

    @Autowired
    private TaskRepository taskRepository;

    @GetMapping
    public ResponseEntity<Map<String, Object>> aiSuggestions() {
        List<Task> tasks = taskRepository.findAll();
        if (tasks.isEmpty()) {
            return ResponseEntity.ok(Map.of("suggestion", "Brak zadań do analizy. Dodaj nowe zadania, aby otrzymać sugestie."));
        }
        int totalTasks = tasks.size();
        long doneTasks = tasks.stream().filter(t -> "done".equalsIgnoreCase(t.getStatus())).count();
        double productivityRatio = totalTasks > 0 ? (double) doneTasks / totalTasks : 0;
        String suggestion = productivityRatio < 0.5
                ? "AI: Produktywność niska. Zalecamy przeanalizowanie przydziału zadań i wsparcie zespołu."
                : "AI: Produktywność na dobrym poziomie. Kontynuuj obecne strategie!";
        return ResponseEntity.ok(Map.of(
                "total_tasks", totalTasks,
                "completed_tasks", doneTasks,
                "productivity_ratio", productivityRatio,
                "suggestion", suggestion
        ));
    }
}
