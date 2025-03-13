package com.example.aitaskmanager.controller;

import com.example.aitaskmanager.entity.Project;
import com.example.aitaskmanager.repository.ProjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/projects")
public class ProjectController {

    @Autowired
    private ProjectRepository projectRepository;

    // Tworzenie projektu – dostępne dla zalogowanych użytkowników
    @PostMapping
    public ResponseEntity<Map<String, Object>> createProject(@RequestBody Map<String, String> projectData) {
        Project project = new Project();
        project.setName(projectData.get("name"));
        project.setDescription(projectData.get("description"));
        Project saved = projectRepository.save(project);
        return ResponseEntity.ok(Map.of(
                "id", saved.getId(),
                "name", saved.getName(),
                "description", saved.getDescription(),
                "created_at", saved.getCreatedAt()
        ));
    }

    // Pobieranie projektów
    @GetMapping
    public ResponseEntity<List<Project>> getProjects() {
        return ResponseEntity.ok(projectRepository.findAll());
    }

    // Edycja projektu – tylko dla admina
    @PreAuthorize("hasRole('ADMIN')")
    @PutMapping("/{projectId}")
    public ResponseEntity<Map<String, Object>> updateProject(@PathVariable Long projectId, @RequestBody Map<String, String> projectData) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new RuntimeException("Projekt nie został znaleziony"));
        project.setName(projectData.getOrDefault("name", project.getName()));
        project.setDescription(projectData.getOrDefault("description", project.getDescription()));
        Project saved = projectRepository.save(project);
        return ResponseEntity.ok(Map.of(
                "id", saved.getId(),
                "name", saved.getName(),
                "description", saved.getDescription(),
                "created_at", saved.getCreatedAt()
        ));
    }

    // Usuwanie projektu – tylko dla admina
    @PreAuthorize("hasRole('ADMIN')")
    @DeleteMapping("/{projectId}")
    public ResponseEntity<Map<String, String>> deleteProject(@PathVariable Long projectId) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new RuntimeException("Projekt nie został znaleziony"));
        projectRepository.delete(project);
        return ResponseEntity.ok(Map.of("detail", "Projekt został usunięty"));
    }
}