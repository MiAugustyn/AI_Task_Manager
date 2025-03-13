package com.example.aitaskmanager.controller;

import com.example.aitaskmanager.security.JwtUtil;
import com.example.aitaskmanager.entity.User;
import com.example.aitaskmanager.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
public class AuthController {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtUtil jwtUtil;

    private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    // Endpoint logowania – przyjmujemy JSON z "username" i "password"
    @PostMapping("/token")
    public ResponseEntity<Map<String, String>> login(@RequestBody Map<String, String> loginData) {
        String username = loginData.get("username");
        String password = loginData.get("password");

        User user = userRepository.findByUsername(username);
        if (user == null || !passwordEncoder.matches(password, user.getHashedPassword())) {
            return ResponseEntity.badRequest().body(Map.of("detail", "Nieprawidłowa nazwa użytkownika lub hasło"));
        }

        Map<String, Object> claims = new HashMap<>();
        String token = jwtUtil.generateToken(claims, username);

        Map<String, String> response = new HashMap<>();
        response.put("access_token", token);
        response.put("token_type", "bearer");
        return ResponseEntity.ok(response);
    }
}
