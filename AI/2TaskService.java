package com.example.taskservice.service;

import com.example.taskservice.model.Task;
import com.example.taskservice.model.TeamMember;
import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class TaskService {
    // Dla demonstracji hardcodowani członkowie zespołu
    private List<TeamMember> team = new ArrayList<>();

    public TaskService() {
        team.add(new TeamMember(1L, "Jan", Arrays.asList("Java", "Projektowanie")));
        team.add(new TeamMember(2L, "Anna", Arrays.asList("Python", "Testowanie")));
        team.add(new TeamMember(3L, "Piotr", Arrays.asList("Java", "Analiza")));
    }
    
    public Task assignTask(Task task) {
        // Prosty algorytm: wybór członka z najmniejszym obciążeniem
        TeamMember bestCandidate = team.get(0);
        for (TeamMember member : team) {
            if (member.getCurrentLoad() < bestCandidate.getCurrentLoad()) {
                bestCandidate = member;
            }
        }
        task.assignTo(bestCandidate);
        return task;
    }
    
    public List<TeamMember> getTeam() {
        return team;
    }
}
