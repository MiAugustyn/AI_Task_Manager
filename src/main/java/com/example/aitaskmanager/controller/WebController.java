package com.example.aitaskmanager.controller;

import com.example.aitaskmanager.entity.Project;
import com.example.aitaskmanager.entity.Task;
import com.example.aitaskmanager.repository.ProjectRepository;
import com.example.aitaskmanager.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import java.util.List;

@Controller
public class WebController {

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private TaskRepository taskRepository;

    // Strona główna – wyświetla listę projektów i zadań
    @GetMapping("/")
    public String index(Model model) {
        List<Project> projects = projectRepository.findAll();
        List<Task> tasks = taskRepository.findAll();
        model.addAttribute("projects", projects);
        model.addAttribute("tasks", tasks);
        return "index";
    }

    // Formularz dodawania projektu
    @PostMapping("/add_project")
    public String addProject(@RequestParam("name") String name,
                             @RequestParam(value = "description", required = false) String description) {
        Project project = new Project();
        project.setName(name);
        project.setDescription(description);
        projectRepository.save(project);
        return "redirect:/";
    }

    // Formularz dodawania zadania
    @PostMapping("/add_task")
    public String addTask(@RequestParam("project_id") Long projectId,
                          @RequestParam("name") String name,
                          @RequestParam(value = "description", required = false) String description,
                          @RequestParam(value = "assigned_to", required = false) String assignedTo,
                          @RequestParam(value = "status", defaultValue = "todo") String status) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Projekt nie został znaleziony"));
        Task task = new Task();
        task.setProject(project);
        task.setName(name);
        task.setDescription(description);
        task.setAssignedTo(assignedTo);
        task.setStatus(status);
        taskRepository.save(task);
        return "redirect:/";
    }

    // Widok analizy produktywności
    @GetMapping("/view_analysis")
    public String viewAnalysis(@RequestParam(name = "project_id", required = false) Long projectId,
                               Model model) {
        List<Task> tasks;
        if (projectId != null) {
            tasks = taskRepository.findByProjectId(projectId);
        } else {
            tasks = taskRepository.findAll();
        }
        String analysisText;
        if (tasks.isEmpty()) {
            analysisText = "Brak zadań do analizy.";
        } else {
            int totalTasks = tasks.size();
            long doneTasks = tasks.stream().filter(t -> "done".equalsIgnoreCase(t.getStatus())).count();
            double productivityRatio = totalTasks > 0 ? (double) doneTasks / totalTasks : 0;
            String suggestion = productivityRatio < 0.5
                    ? "Niska produktywność. Zalecamy przydzielenie dodatkowych zasobów."
                    : "Produktywność na dobrym poziomie.";
            analysisText = "Liczba zadań: " + totalTasks + "<br>" +
                    "Zakończonych zadań: " + doneTasks + "<br>" +
                    "Wskaźnik produktywności: " + String.format("%.2f", productivityRatio) + "<br>" +
                    "Sugestia: " + suggestion;
        }
        model.addAttribute("analysis_text", analysisText);
        return "analysis";
    }
}
