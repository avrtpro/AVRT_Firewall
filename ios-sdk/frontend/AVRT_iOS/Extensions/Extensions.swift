//
//  Extensions.swift
//  AVRT_iOS
//
//  Swift extensions for AVRT SDK
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import SwiftUI

// MARK: - Color Extensions
extension Color {
    /// AVRT Primary Brand Color
    static let avrtPrimary = Color(red: 0.2, green: 0.4, blue: 0.8)

    /// AVRT Secondary Brand Color
    static let avrtSecondary = Color(red: 0.3, green: 0.7, blue: 0.5)

    /// AVRT Accent Color
    static let avrtAccent = Color(red: 0.9, green: 0.6, blue: 0.2)

    /// Safe status color
    static let avrtSafe = Color.green

    /// Blocked status color
    static let avrtBlocked = Color.red

    /// Warning status color
    static let avrtWarning = Color.orange
}

// MARK: - View Extensions
extension View {
    /// Apply AVRT card styling
    func avrtCard() -> some View {
        self
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }

    /// Apply AVRT button styling
    func avrtButton(isEnabled: Bool = true) -> some View {
        self
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(isEnabled ? Color.avrtPrimary : Color.gray)
            .foregroundColor(.white)
            .cornerRadius(25)
            .shadow(color: (isEnabled ? Color.avrtPrimary : Color.gray).opacity(0.3), radius: 5, x: 0, y: 3)
    }
}

// MARK: - String Extensions
extension String {
    /// Generate SHA-256 hash of the string
    var sha256: String {
        return HashService.sha256(self)
    }

    /// Truncate string to specified length
    func truncated(to length: Int, trailing: String = "...") -> String {
        if self.count <= length {
            return self
        }
        return String(self.prefix(length)) + trailing
    }

    /// Check if string contains any harmful patterns
    var containsHarmfulContent: Bool {
        let patterns = ["harm", "hurt", "attack", "kill", "destroy", "hate", "violence"]
        let lowercased = self.lowercased()
        return patterns.contains { lowercased.contains($0) }
    }
}

// MARK: - Date Extensions
extension Date {
    /// Format date for display
    var displayString: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter.string(from: self)
    }

    /// ISO8601 string
    var iso8601: String {
        let formatter = ISO8601DateFormatter()
        return formatter.string(from: self)
    }
}

// MARK: - Double Extensions
extension Double {
    /// Format as percentage
    var percentageString: String {
        return String(format: "%.1f%%", self)
    }

    /// Format as score (0-100)
    var scoreString: String {
        return String(format: "%.0f", self)
    }
}

// MARK: - ValidationResult Extensions
extension ValidationResult {
    /// Get status color
    var statusColor: Color {
        switch status {
        case .safe:
            return .avrtSafe
        case .blocked:
            return .avrtBlocked
        case .warning:
            return .avrtWarning
        case .reviewRequired:
            return .orange
        case .error:
            return .red
        }
    }

    /// Get status icon
    var statusIcon: String {
        switch status {
        case .safe:
            return "checkmark.shield.fill"
        case .blocked:
            return "xmark.shield.fill"
        case .warning:
            return "exclamationmark.shield.fill"
        case .reviewRequired:
            return "questionmark.circle.fill"
        case .error:
            return "exclamationmark.triangle.fill"
        }
    }
}

// MARK: - SPIELScore Extensions
extension SPIELScore {
    /// Get color based on composite score
    var scoreColor: Color {
        if composite >= 85 { return .green }
        if composite >= 70 { return .orange }
        return .red
    }

    /// Get grade (A-F)
    var grade: String {
        if composite >= 90 { return "A" }
        if composite >= 80 { return "B" }
        if composite >= 70 { return "C" }
        if composite >= 60 { return "D" }
        return "F"
    }
}

// MARK: - Array Extensions
extension Array where Element == ValidationResult {
    /// Calculate average SPIEL score
    var averageSPIELScore: Double {
        let scores = self.compactMap { $0.spielScore?.composite }
        guard !scores.isEmpty else { return 0 }
        return scores.reduce(0, +) / Double(scores.count)
    }

    /// Count blocked results
    var blockedCount: Int {
        return self.filter { !$0.isSafe }.count
    }

    /// Calculate block rate
    var blockRate: Double {
        guard !isEmpty else { return 0 }
        return Double(blockedCount) / Double(count)
    }
}

// MARK: - Bundle Extensions
extension Bundle {
    /// AVRT SDK version
    var avrtVersion: String {
        return infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0"
    }

    /// AVRT build number
    var avrtBuild: String {
        return infoDictionary?["CFBundleVersion"] as? String ?? "1"
    }
}
