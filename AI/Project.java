package com.example.projectservice.model;

import java.util.ArrayList;
import java.util.List;

public class Project {
    private Long id;
    private String name;
    private List<Task> tasks = new ArrayList<>();

    public Project() {}

    public Project(Long id, String name) {
        this.id = id;
        this.name = name;
    }

    // Gettery i settery

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<Task> getTasks() {
        return tasks;
    }

    public void addTask(Task task) {
        tasks.add(task);
    }
}
