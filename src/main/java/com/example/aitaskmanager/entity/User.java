package com.example.aitaskmanager.entity;

import jakarta.persistence.*;

/**
 * Encja reprezentująca użytkownika.
 */
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false)
    private String hashedPassword;

    // Domyślnie "user", może być "admin"
    @Column(nullable = false)
    private String role = "user";

    // Gettery i settery
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getHashedPassword() { return hashedPassword; }
    public void setHashedPassword(String hashedPassword) { this.hashedPassword = hashedPassword; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
}
