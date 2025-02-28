package com.example.taskservice.model;

import java.util.List;

public class TeamMember {
    private Long id;
    private String name;
    private List<String> skills;
    private int currentLoad;

    public TeamMember() {}

    public TeamMember(Long id, String name, List<String> skills) {
        this.id = id;
        this.name = name;
        this.skills = skills;
        this.currentLoad = 0;
    }

    public void incrementLoad() {
        this.currentLoad++;
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

    public List<String> getSkills() {
        return skills;
    }

    public void setSkills(List<String> skills) {
        this.skills = skills;
    }

    public int getCurrentLoad() {
        return currentLoad;
    }

    public void setCurrentLoad(int currentLoad) {
        this.currentLoad = currentLoad;
    }
}
