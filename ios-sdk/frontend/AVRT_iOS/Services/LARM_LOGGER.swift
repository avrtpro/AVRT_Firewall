//
//  LARM_LOGGER.swift
//  AVRT_iOS
//
//  LARM - Logging, Audit, Reporting & Monitoring
//  Encrypted audit trail with SHA-256 integrity verification
//
//  Patent: USPTO 19/236,935
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation
import CryptoKit
import os.log

// MARK: - LARM Logger

/// LARM: Logging, Audit, Reporting & Monitoring system for AVRT
/// Provides encrypted, tamper-evident audit trails with real-time monitoring
@MainActor
public final class LARMLogger: ObservableObject {

    // MARK: - Singleton
    public static let shared = LARMLogger()

    // MARK: - Published Properties
    @Published public private(set) var isLogging: Bool = true
    @Published public private(set) var logCount: Int = 0
    @Published public private(set) var lastLogEntry: LARMLogEntry?
    @Published public private(set) var systemHealth: SystemHealthStatus = .healthy

    // MARK: - Private Properties
    private let logQueue = DispatchQueue(label: "com.avrt.larm.logging", qos: .utility)
    private var logEntries: [LARMLogEntry] = []
    private var encryptedLogData: Data?
    private let maxLogEntries = 50000
    private let encryptionKey: SymmetricKey
    private let osLog = OSLog(subsystem: "com.bgbhthreads.avrt", category: "LARM")

    // MARK: - File Storage
    private let logFileURL: URL
    private let auditFileURL: URL

    // MARK: - Metrics
    private var sessionMetrics = SessionMetrics()

    // MARK: - Initialization
    private init() {
        // Generate or retrieve encryption key
        if let storedKey = LARMLogger.retrieveStoredKey() {
            self.encryptionKey = storedKey
        } else {
            self.encryptionKey = SymmetricKey(size: .bits256)
            LARMLogger.storeKey(encryptionKey)
        }

        // Setup file URLs
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let larmDirectory = documentsPath.appendingPathComponent("LARM", isDirectory: true)

        // Create directory if needed
        try? FileManager.default.createDirectory(at: larmDirectory, withIntermediateDirectories: true)

        self.logFileURL = larmDirectory.appendingPathComponent("avrt_log.enc")
        self.auditFileURL = larmDirectory.appendingPathComponent("avrt_audit.json")

        // Load existing logs
        loadExistingLogs()

        // Log initialization
        log(event: .systemStart, message: "LARM Logger initialized", level: .info)
    }

    // MARK: - Key Management

    private static func storeKey(_ key: SymmetricKey) {
        let keyData = key.withUnsafeBytes { Data($0) }
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: "com.avrt.larm.encryption",
            kSecAttrAccount as String: "master_key",
            kSecValueData as String: keyData
        ]
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }

    private static func retrieveStoredKey() -> SymmetricKey? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: "com.avrt.larm.encryption",
            kSecAttrAccount as String: "master_key",
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess, let keyData = result as? Data else {
            return nil
        }

        return SymmetricKey(data: keyData)
    }

    // MARK: - Core Logging

    /// Log an event with full audit trail
    public func log(
        event: LARMEventType,
        message: String,
        level: LARMLogLevel = .info,
        metadata: [String: String]? = nil,
        userId: String? = nil,
        sessionId: String? = nil
    ) {
        guard isLogging else { return }

        let entry = LARMLogEntry(
            id: UUID(),
            timestamp: Date(),
            event: event,
            message: message,
            level: level,
            metadata: metadata,
            userId: userId,
            sessionId: sessionId,
            contentHash: generateHash(message),
            previousHash: logEntries.last?.contentHash
        )

        // Add to in-memory store
        logEntries.append(entry)
        logCount = logEntries.count
        lastLogEntry = entry

        // Update metrics
        updateMetrics(for: entry)

        // OS Log for debugging
        logToSystem(entry)

        // Trim if needed
        if logEntries.count > maxLogEntries {
            logEntries.removeFirst(logEntries.count - maxLogEntries)
        }

        // Persist asynchronously
        persistLogAsync(entry)
    }

    /// Log a voice interaction
    public func logVoiceInteraction(
        transcription: String,
        response: String,
        spielScore: Double,
        action: String,
        processingTimeMs: Double
    ) {
        let metadata: [String: String] = [
            "transcription_hash": generateHash(transcription),
            "response_hash": generateHash(response),
            "spiel_score": String(format: "%.2f", spielScore),
            "action": action,
            "processing_time_ms": String(format: "%.2f", processingTimeMs)
        ]

        log(
            event: .voiceInteraction,
            message: "Voice interaction processed",
            level: spielScore >= 85 ? .info : .warning,
            metadata: metadata
        )

        sessionMetrics.voiceInteractions += 1
        sessionMetrics.totalProcessingTime += processingTimeMs
    }

    /// Log a validation result
    public func logValidation(
        input: String,
        output: String,
        result: ValidationLogResult
    ) {
        let metadata: [String: String] = [
            "input_hash": generateHash(input),
            "output_hash": generateHash(output),
            "is_safe": String(result.isSafe),
            "composite_score": String(format: "%.2f", result.compositeScore),
            "violations": result.violations.joined(separator: ","),
            "action": result.action
        ]

        log(
            event: .validation,
            message: "Content validation completed",
            level: result.isSafe ? .info : .warning,
            metadata: metadata
        )

        if result.isSafe {
            sessionMetrics.passedValidations += 1
        } else {
            sessionMetrics.blockedValidations += 1
        }
    }

    /// Log a security event
    public func logSecurityEvent(
        type: SecurityEventType,
        description: String,
        severity: LARMLogLevel
    ) {
        log(
            event: .security,
            message: description,
            level: severity,
            metadata: ["security_type": type.rawValue]
        )

        if severity == .critical || severity == .error {
            systemHealth = .degraded
        }
    }

    // MARK: - Hash Generation

    private func generateHash(_ content: String) -> String {
        let data = Data(content.utf8)
        let hash = SHA256.hash(data: data)
        return hash.compactMap { String(format: "%02x", $0) }.joined()
    }

    /// Generate hash for external content
    public func sha256(_ content: String) -> String {
        return generateHash(content)
    }

    // MARK: - System Logging

    private func logToSystem(_ entry: LARMLogEntry) {
        let logType: OSLogType
        switch entry.level {
        case .debug: logType = .debug
        case .info: logType = .info
        case .warning: logType = .default
        case .error: logType = .error
        case .critical: logType = .fault
        }

        os_log("%{public}@ [%{public}@] %{public}@",
               log: osLog,
               type: logType,
               entry.event.rawValue,
               entry.level.rawValue,
               entry.message)
    }

    // MARK: - Persistence

    private func loadExistingLogs() {
        // Load from encrypted file
        guard FileManager.default.fileExists(atPath: logFileURL.path),
              let encryptedData = try? Data(contentsOf: logFileURL) else {
            return
        }

        do {
            let sealedBox = try AES.GCM.SealedBox(combined: encryptedData)
            let decryptedData = try AES.GCM.open(sealedBox, using: encryptionKey)
            logEntries = try JSONDecoder().decode([LARMLogEntry].self, from: decryptedData)
            logCount = logEntries.count
        } catch {
            os_log("Failed to load existing logs: %{public}@", log: osLog, type: .error, error.localizedDescription)
        }
    }

    private func persistLogAsync(_ entry: LARMLogEntry) {
        logQueue.async { [weak self] in
            self?.persistLogSync()
        }
    }

    private func persistLogSync() {
        do {
            let data = try JSONEncoder().encode(logEntries)
            let sealedBox = try AES.GCM.seal(data, using: encryptionKey)
            try sealedBox.combined?.write(to: logFileURL)
        } catch {
            os_log("Failed to persist logs: %{public}@", log: osLog, type: .error, error.localizedDescription)
        }
    }

    // MARK: - Metrics

    private func updateMetrics(for entry: LARMLogEntry) {
        sessionMetrics.totalEvents += 1

        switch entry.level {
        case .error, .critical:
            sessionMetrics.errorCount += 1
        case .warning:
            sessionMetrics.warningCount += 1
        default:
            break
        }
    }

    /// Get current session metrics
    public func getSessionMetrics() -> SessionMetrics {
        return sessionMetrics
    }

    /// Reset session metrics
    public func resetSessionMetrics() {
        sessionMetrics = SessionMetrics()
    }

    // MARK: - Export Functions

    /// Export logs as encrypted data
    public func exportEncryptedLogs() -> Data? {
        do {
            let data = try JSONEncoder().encode(logEntries)
            let sealedBox = try AES.GCM.seal(data, using: encryptionKey)
            return sealedBox.combined
        } catch {
            return nil
        }
    }

    /// Export audit summary as JSON
    public func exportAuditSummary() -> Data? {
        let summary = AuditSummary(
            exportDate: Date(),
            totalEntries: logEntries.count,
            sessionMetrics: sessionMetrics,
            eventCounts: Dictionary(grouping: logEntries, by: { $0.event })
                .mapValues { $0.count },
            levelCounts: Dictionary(grouping: logEntries, by: { $0.level })
                .mapValues { $0.count },
            chainIntegrity: verifyChainIntegrity()
        )

        return try? JSONEncoder().encode(summary)
    }

    /// Export SHA256SUMS for verification
    public func exportSHA256SUMS() -> String {
        var sums = "# AVRT LARM SHA256SUMS\n"
        sums += "# Generated: \(Date().ISO8601Format())\n"
        sums += "# Entries: \(logEntries.count)\n\n"

        for entry in logEntries.suffix(100) {
            sums += "\(entry.contentHash)  \(entry.id.uuidString)\n"
        }

        return sums
    }

    // MARK: - Integrity Verification

    /// Verify the hash chain integrity
    public func verifyChainIntegrity() -> Bool {
        for i in 1..<logEntries.count {
            if logEntries[i].previousHash != logEntries[i-1].contentHash {
                return false
            }
        }
        return true
    }

    // MARK: - Log Queries

    /// Get recent log entries
    public func getRecentLogs(limit: Int = 100) -> [LARMLogEntry] {
        return Array(logEntries.suffix(limit))
    }

    /// Get logs by event type
    public func getLogs(byEvent event: LARMEventType, limit: Int = 100) -> [LARMLogEntry] {
        return logEntries.filter { $0.event == event }.suffix(limit).map { $0 }
    }

    /// Get logs by level
    public func getLogs(byLevel level: LARMLogLevel, limit: Int = 100) -> [LARMLogEntry] {
        return logEntries.filter { $0.level == level }.suffix(limit).map { $0 }
    }

    /// Get logs in date range
    public func getLogs(from startDate: Date, to endDate: Date) -> [LARMLogEntry] {
        return logEntries.filter { $0.timestamp >= startDate && $0.timestamp <= endDate }
    }

    // MARK: - Control

    /// Pause logging
    public func pause() {
        isLogging = false
        log(event: .systemEvent, message: "Logging paused", level: .info)
    }

    /// Resume logging
    public func resume() {
        isLogging = true
        log(event: .systemEvent, message: "Logging resumed", level: .info)
    }

    /// Clear all logs (requires confirmation)
    public func clearLogs(confirmationCode: String) -> Bool {
        guard confirmationCode == "CLEAR_LARM_LOGS_\(Date().ISO8601Format().prefix(10))" else {
            return false
        }

        log(event: .security, message: "Log clear initiated", level: .warning)
        logEntries.removeAll()
        logCount = 0
        try? FileManager.default.removeItem(at: logFileURL)
        return true
    }
}

// MARK: - Supporting Types

public enum LARMEventType: String, Codable {
    case voiceInteraction = "voice_interaction"
    case validation = "validation"
    case security = "security"
    case systemStart = "system_start"
    case systemEvent = "system_event"
    case userAction = "user_action"
    case apiCall = "api_call"
    case error = "error"
    case policyEnforcement = "policy_enforcement"
}

public enum LARMLogLevel: String, Codable, Comparable {
    case debug = "debug"
    case info = "info"
    case warning = "warning"
    case error = "error"
    case critical = "critical"

    public static func < (lhs: LARMLogLevel, rhs: LARMLogLevel) -> Bool {
        let order: [LARMLogLevel] = [.debug, .info, .warning, .error, .critical]
        return order.firstIndex(of: lhs)! < order.firstIndex(of: rhs)!
    }
}

public enum SecurityEventType: String, Codable {
    case authFailure = "auth_failure"
    case rateLimitExceeded = "rate_limit_exceeded"
    case tamperDetected = "tamper_detected"
    case policyViolation = "policy_violation"
    case suspiciousActivity = "suspicious_activity"
}

public enum SystemHealthStatus: String, Codable {
    case healthy = "healthy"
    case degraded = "degraded"
    case critical = "critical"
}

public struct LARMLogEntry: Codable, Identifiable {
    public let id: UUID
    public let timestamp: Date
    public let event: LARMEventType
    public let message: String
    public let level: LARMLogLevel
    public let metadata: [String: String]?
    public let userId: String?
    public let sessionId: String?
    public let contentHash: String
    public let previousHash: String?
}

public struct ValidationLogResult {
    public let isSafe: Bool
    public let compositeScore: Double
    public let violations: [String]
    public let action: String

    public init(isSafe: Bool, compositeScore: Double, violations: [String], action: String) {
        self.isSafe = isSafe
        self.compositeScore = compositeScore
        self.violations = violations
        self.action = action
    }
}

public struct SessionMetrics: Codable {
    public var totalEvents: Int = 0
    public var voiceInteractions: Int = 0
    public var passedValidations: Int = 0
    public var blockedValidations: Int = 0
    public var errorCount: Int = 0
    public var warningCount: Int = 0
    public var totalProcessingTime: Double = 0
    public var sessionStartTime: Date = Date()

    public var averageProcessingTime: Double {
        guard voiceInteractions > 0 else { return 0 }
        return totalProcessingTime / Double(voiceInteractions)
    }

    public var blockRate: Double {
        let total = passedValidations + blockedValidations
        guard total > 0 else { return 0 }
        return Double(blockedValidations) / Double(total)
    }
}

public struct AuditSummary: Codable {
    public let exportDate: Date
    public let totalEntries: Int
    public let sessionMetrics: SessionMetrics
    public let eventCounts: [LARMEventType: Int]
    public let levelCounts: [LARMLogLevel: Int]
    public let chainIntegrity: Bool
}
