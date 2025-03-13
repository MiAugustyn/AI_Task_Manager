package com.example.aitaskmanager.controller;

import com.example.aitaskmanager.entity.Project;
import com.example.aitaskmanager.entity.Task;
import com.example.aitaskmanager.repository.ProjectRepository;
import com.example.aitaskmanager.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/tasks")
public class TaskController {

    @Autowired
    private TaskRepository taskRepository;

    @Autowired
    private ProjectRepository projectRepository;

    // Tworzenie zadania
    @PostMapping
    public ResponseEntity<Map<String, Object>> createTask(@RequestBody Map<String, Object> taskData) {
        Long projectId = Long.valueOf(taskData.get("project_id").toString());
        Optional<Project> optProject = projectRepository.findById(projectId);
        if (optProject.isEmpty()) {
            return ResponseEntity.status(404).body(Map.of("detail", "Projekt nie został znaleziony"));
        }
        Task task = new Task();
        task.setProject(optProject.get());
        task.setName(taskData.get("name").toString());
        task.setDescription((String) taskData.get("description"));
        task.setAssignedTo((String) taskData.get("assigned_to"));
        task.setStatus(taskData.getOrDefault("status", "todo").toString());
        Task saved = taskRepository.save(task);
        return ResponseEntity.ok(Map.of(
                "id", saved.getId(),
                "project_id", saved.getProject().getId(),
                "name", saved.getName(),
                "description", saved.getDescription(),
                "assigned_to", saved.getAssignedTo(),
                "status", saved.getStatus(),
                "created_at", saved.getCreatedAt()
        ));
    }

    // Pobieranie zadań z filtrowaniem i sortowaniem
    @GetMapping
    public ResponseEntity<List<Map<String, Object>>> getTasks(
            @RequestParam(required = false) String status,
            @RequestParam(required = false, defaultValue = "created_at") String sort_by,
            @RequestParam(required = false, defaultValue = "asc") String order) {
        List<Task> tasks = taskRepository.findAll();
        if (status != null) {
            tasks = tasks.stream().filter(t -> t.getStatus().equalsIgnoreCase(status)).collect(Collectors.toList());
        }
        Comparator<Task> comparator;
        if ("name".equalsIgnoreCase(sort_by)) {
            comparator = Comparator.comparing(Task::getName, String.CASE_INSENSITIVE_ORDER);
        } else {
            comparator = Comparator.comparing(Task::getCreatedAt);
        }
        if ("desc".equalsIgnoreCase(order)) {
            comparator = comparator.reversed();
        }
        tasks = tasks.stream().sorted(comparator).collect(Collectors.toList());
        List<Map<String, Object>> response = tasks.stream().map(t -> {
            Map<String, Object> map = new HashMap<>();
            map.put("id", t.getId());
            map.put("project_id", t.getProject().getId());
            map.put("name", t.getName());
            map.put("description", t.getDescription());
            map.put("assigned_to", t.getAssignedTo());
            map.put("status", t.getStatus());
            map.put("created_at", t.getCreatedAt());
            return map;
        }).collect(Collectors.toList());
        return ResponseEntity.ok(response);
    }

    // Edycja zadania – tylko dla admina
    @PreAuthorize("hasRole('ADMIN')")
    @PutMapping("/{taskId}")
    public ResponseEntity<Map<String, Object>> updateTask(@PathVariable Long taskId, @RequestBody Map<String, Object> taskData) {
        Task task = taskRepository.findById(taskId)
                .orElseThrow(() -> new RuntimeException("Zadanie nie zostało znalezione"));
        task.setName((String) taskData.getOrDefault("name", task.getName()));
        task.setDescription((String) taskData.getOrDefault("description", task.getDescription()));
        task.setAssignedTo((String) taskData.getOrDefault("assigned_to", task.getAssignedTo()));
        task.setStatus((String) taskData.getOrDefault("status", task.getStatus()));
        Task saved = taskRepository.save(task);
        return ResponseEntity.ok(Map.of(
                "id", saved.getId(),
                "project_id", saved.getProject().getId(),
                "name", saved.getName(),
                "description", saved.getDescription(),
                "assigned_to", saved.getAssignedTo(),
                "status", saved.getStatus(),
                "created_at", saved.getCreatedAt()
        ));
    }

    // Usuwanie zadania – tylko dla admina
    @PreAuthorize("hasRole('ADMIN')")
    @DeleteMapping("/{taskId}")
    public ResponseEntity<Map<String, String>> deleteTask(@PathVariable Long taskId) {
        Task task = taskRepository.findById(taskId)
                .orElseThrow(() -> new RuntimeException("Zadanie nie zostało znalezione"));
        taskRepository.delete(task);
        return ResponseEntity.ok(Map.of("detail", "Zadanie zostało usunięte"));
    }
}
