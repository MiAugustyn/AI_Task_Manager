package com.example.taskservice.model;

public class Task {
    private Long id;
    private String title;
    private String description;
    private TeamMember assignedTo;

    public Task() {}

    public Task(Long id, String title, String description) {
        this.id = id;
        this.title = title;
        this.description = description;
    }

    public void assignTo(TeamMember member) {
        this.assignedTo = member;
        member.incrementLoad();
    }

    // Gettery i settery

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public TeamMember getAssignedTo() {
        return assignedTo;
    }

    public void setAssignedTo(TeamMember assignedTo) {
        this.assignedTo = assignedTo;
    }
}
