package com.example.projectservice.controller;

import com.example.projectservice.model.Project;
import com.example.projectservice.model.Task;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/projects")
public class ProjectController {
    // Prosty "repozytorium" w pamięci
    private Map<Long, Project> projectRepo = new HashMap<>();
    private Long projectIdCounter = 1L;

    @PostMapping
    public ResponseEntity<Project> createProject(@RequestBody Project project) {
        project.setId(projectIdCounter++);
        projectRepo.put(project.getId(), project);
        return ResponseEntity.ok(project);
    }

    @PostMapping("/{projectId}/tasks")
    public ResponseEntity<Project> addTaskToProject(@PathVariable Long projectId, @RequestBody Task task) {
        Project project = projectRepo.get(projectId);
        if (project == null) {
            return ResponseEntity.notFound().build();
        }
        project.addTask(task);
        return ResponseEntity.ok(project);
    }

    @GetMapping("/{projectId}")
    public ResponseEntity<Project> getProject(@PathVariable Long projectId) {
        Project project = projectRepo.get(projectId);
        if (project == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(project);
    }
}
