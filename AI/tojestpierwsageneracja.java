import java.util.*;

// Główna klasa uruchamiająca system
public class AITaskManager {
    public static void main(String[] args) {
        // Inicjalizacja zespołu
        List<TeamMember> team = new ArrayList<>();
        team.add(new TeamMember("Jan", Arrays.asList("Java", "Projektowanie")));
        team.add(new TeamMember("Anna", Arrays.asList("Python", "Testowanie")));
        team.add(new TeamMember("Piotr", Arrays.asList("Java", "Analiza")));
        
        // Inicjalizacja projektu
        Project projekt = new Project("Projekt AI Task Manager");
        
        // Dodawanie zadań do projektu
        projekt.addTask(new Task("Moduł zarządzania projektami", 
                "Stworzenie funkcji do tworzenia i śledzenia projektów", 5));
        projekt.addTask(new Task("Moduł przydzielania zadań", 
                "Implementacja algorytmu przydzielania zadań do członków zespołu", 3));
        projekt.addTask(new Task("Moduł analizy produktywności", 
                "Stworzenie raportów i dashboardów", 4));
        
        // Przydzielanie zadań przy użyciu prostej logiki AI (symulacja)
        TaskAssigner.assignTasks(projekt.getTasks(), team);
        
        // Wyświetlanie przydzielonych zadań
        System.out.println("Przydzielone zadania:");
        for (Task t : projekt.getTasks()) {
            System.out.println(t);
        }
        
        // Symulacja ukończenia zadań i analizy produktywności
        ProductivityAnalyzer analyzer = new ProductivityAnalyzer();
        // Zakładamy, że dwa pierwsze zadania zostały ukończone
        analyzer.recordCompletedTask(projekt.getTasks().get(0));
        analyzer.recordCompletedTask(projekt.getTasks().get(1));
        // Trzecie zadanie jest w toku – tylko rejestrujemy zadanie w systemie
        analyzer.recordTask(projekt.getTasks().get(2));
        
        System.out.println("\nRaport produktywności:");
        System.out.println(analyzer.generateReport());
    }
}

// Klasa reprezentująca członka zespołu
class TeamMember {
    private String name;
    private List<String> skills;
    private int currentLoad; // Liczba aktualnie przypisanych zadań
    
    public TeamMember(String name, List<String> skills) {
        this.name = name;
        this.skills = skills;
        this.currentLoad = 0;
    }
    
    public String getName() {
        return name;
    }
    
    public List<String> getSkills() {
        return skills;
    }
    
    public int getCurrentLoad() {
        return currentLoad;
    }
    
    public void incrementLoad() {
        currentLoad++;
    }
    
    @Override
    public String toString() {
        return name;
    }
}

// Klasa reprezentująca zadanie
class Task {
    private String title;
    private String description;
    private int estimatedHours;
    private TeamMember assignedTo;
    private boolean completed;
    
    public Task(String title, String description, int estimatedHours) {
        this.title = title;
        this.description = description;
        this.estimatedHours = estimatedHours;
        this.assignedTo = null;
        this.completed = false;
    }
    
    public String getTitle() {
        return title;
    }
    
    public int getEstimatedHours() {
        return estimatedHours;
    }
    
    public TeamMember getAssignedTo() {
        return assignedTo;
    }
    
    // Przypisanie zadania do członka zespołu
    public void assignTo(TeamMember member) {
        this.assignedTo = member;
        member.incrementLoad();
    }
    
    // Oznaczenie zadania jako ukończonego
    public void markCompleted() {
        this.completed = true;
    }
    
    public boolean isCompleted() {
        return completed;
    }
    
    @Override
    public String toString() {
        String assignment = (assignedTo != null) ? assignedTo.getName() : "Brak przypisania";
        return "Zadanie: " + title + " | Przypisane do: " + assignment;
    }
}

// Klasa reprezentująca projekt
class Project {
    private String name;
    private List<Task> tasks;
    
    public Project(String name) {
        this.name = name;
        this.tasks = new ArrayList<>();
    }
    
    // Dodanie zadania do projektu
    public void addTask(Task task) {
        tasks.add(task);
    }
    
    public List<Task> getTasks() {
        return tasks;
    }
    
    public String getName() {
        return name;
    }
}

// Klasa implementująca algorytm przydzielania zadań (symulacja AI)
class TaskAssigner {
    // Prosty algorytm przydziela zadania członkowi z najmniejszym obciążeniem
    public static void assignTasks(List<Task> tasks, List<TeamMember> team) {
        for (Task task : tasks) {
            TeamMember bestCandidate = null;
            int minLoad = Integer.MAX_VALUE;
            for (TeamMember member : team) {
                if (member.getCurrentLoad() < minLoad) {
                    minLoad = member.getCurrentLoad();
                    bestCandidate = member;
                }
            }
            if (bestCandidate != null) {
                task.assignTo(bestCandidate);
            }
        }
    }
}

// Klasa analizująca produktywność zespołu
class ProductivityAnalyzer {
    private int completedTasks;
    private int totalTasks;
    
    public ProductivityAnalyzer() {
        this.completedTasks = 0;
        this.totalTasks = 0;
    }
    
    // Rejestracja ukończonego zadania
    public void recordCompletedTask(Task task) {
        if (!task.isCompleted()) {
            task.markCompleted();
        }
        completedTasks++;
        totalTasks++;
    }
    
    // Rejestracja zadania, które nie jest jeszcze ukończone
    public void recordTask(Task task) {
        totalTasks++;
    }
    
    // Generowanie raportu produktywności
    public String generateReport() {
        double efficiency = (totalTasks > 0) ? (completedTasks * 100.0 / totalTasks) : 0;
        return "Zakończone zadania: " + completedTasks + "/" + totalTasks + 
               " (" + String.format("%.2f", efficiency) + "% efektywności)";
    }
}
