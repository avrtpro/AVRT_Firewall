//
//  SPIEL_POLICY_ENFORCER.swift
//  AVRT_iOS
//
//  SPIEL Framework Policy Enforcement Engine
//  Safety | Personalization | Integrity | Ethics | Logic
//
//  Patent: USPTO 19/236,935
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation
import CryptoKit

// MARK: - SPIEL Policy Enforcement Engine

/// Core SPIEL Policy Enforcer for AVRT middleware
/// Implements fail-closed behavior with configurable thresholds
@MainActor
public final class SPIELPolicyEnforcer: ObservableObject {

    // MARK: - Singleton
    public static let shared = SPIELPolicyEnforcer()

    // MARK: - Published Properties
    @Published public private(set) var isEnforcing: Bool = false
    @Published public private(set) var lastEnforcementResult: EnforcementResult?
    @Published public private(set) var policyViolations: [PolicyViolation] = []

    // MARK: - Configuration
    private var thresholds: SPIELThresholds
    private var policies: [String: PolicyRule] = [:]
    private let enforcementQueue = DispatchQueue(label: "com.avrt.spiel.enforcement", qos: .userInitiated)

    // MARK: - Audit Trail
    private var auditLog: [EnforcementAuditEntry] = []
    private let maxAuditEntries = 10000

    // MARK: - Initialization
    private init() {
        self.thresholds = SPIELThresholds.default
        loadPoliciesFromStore()
    }

    // MARK: - Policy Loading
    private func loadPoliciesFromStore() {
        // Load from bundled policy_store.json
        guard let url = Bundle.main.url(forResource: "policy_store", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let store = try? JSONDecoder().decode(PolicyStore.self, from: data) else {
            // Use default policies if store not found
            policies = PolicyRule.defaultPolicies
            return
        }

        for rule in store.rules {
            policies[rule.id] = rule
        }

        if let customThresholds = store.thresholds {
            thresholds = customThresholds
        }
    }

    // MARK: - Core Enforcement

    /// Enforce SPIEL policies on content
    /// - Parameters:
    ///   - input: User input text
    ///   - output: AI-generated output to validate
    ///   - context: Optional context information
    /// - Returns: Enforcement result with action and details
    public func enforce(
        input: String,
        output: String,
        context: EnforcementContext? = nil
    ) async -> EnforcementResult {
        isEnforcing = true
        defer { isEnforcing = false }

        let startTime = Date()
        var violations: [PolicyViolation] = []
        var scores = SPIELDimensionScores()

        // Analyze each SPIEL dimension
        scores.safety = await analyzeSafety(output)
        scores.personalization = await analyzePersonalization(output, context: context)
        scores.integrity = await analyzeIntegrity(output)
        scores.ethics = await analyzeEthics(output)
        scores.logic = await analyzeLogic(output)

        // Check threshold violations
        if scores.safety < thresholds.safety {
            violations.append(PolicyViolation(
                dimension: .safety,
                score: scores.safety,
                threshold: thresholds.safety,
                severity: .critical,
                description: "Safety score below threshold"
            ))
        }

        if scores.integrity < thresholds.integrity {
            violations.append(PolicyViolation(
                dimension: .integrity,
                score: scores.integrity,
                threshold: thresholds.integrity,
                severity: .high,
                description: "Integrity score below threshold"
            ))
        }

        if scores.ethics < thresholds.ethics {
            violations.append(PolicyViolation(
                dimension: .ethics,
                score: scores.ethics,
                threshold: thresholds.ethics,
                severity: .critical,
                description: "Ethics score below threshold"
            ))
        }

        if scores.personalization < thresholds.personalization {
            violations.append(PolicyViolation(
                dimension: .personalization,
                score: scores.personalization,
                threshold: thresholds.personalization,
                severity: .medium,
                description: "Personalization score below threshold"
            ))
        }

        if scores.logic < thresholds.logic {
            violations.append(PolicyViolation(
                dimension: .logic,
                score: scores.logic,
                threshold: thresholds.logic,
                severity: .low,
                description: "Logic score below threshold"
            ))
        }

        // Run custom policy rules
        for (_, rule) in policies where rule.isEnabled {
            if let violation = await evaluateRule(rule, output: output) {
                violations.append(violation)
            }
        }

        // Determine enforcement action (fail-closed principle)
        let action = determineAction(violations: violations, scores: scores)

        // Calculate composite score
        let compositeScore = (scores.safety + scores.personalization + scores.integrity + scores.ethics + scores.logic) / 5.0

        // Generate content hash
        let contentHash = generateSHA256(input + output)

        let processingTime = Date().timeIntervalSince(startTime) * 1000

        let result = EnforcementResult(
            action: action,
            scores: scores,
            compositeScore: compositeScore,
            violations: violations,
            contentHash: contentHash,
            processingTimeMs: processingTime,
            timestamp: Date(),
            safeOutput: action == .allow ? output : generateSafeAlternative(violations)
        )

        // Update state
        lastEnforcementResult = result
        policyViolations = violations

        // Add to audit trail
        addAuditEntry(input: input, output: output, result: result)

        return result
    }

    // MARK: - SPIEL Dimension Analysis

    private func analyzeSafety(_ text: String) async -> Double {
        var score = 100.0
        let lowercased = text.lowercased()

        // Critical harmful patterns
        let criticalPatterns = [
            "kill", "murder", "attack", "weapon", "bomb", "terrorist",
            "suicide", "self-harm", "hurt yourself"
        ]

        for pattern in criticalPatterns {
            if lowercased.contains(pattern) {
                score -= 30.0
            }
        }

        // High-risk patterns
        let highRiskPatterns = [
            "harm", "hurt", "destroy", "violence", "dangerous",
            "threat", "hate", "abuse"
        ]

        for pattern in highRiskPatterns {
            if lowercased.contains(pattern) {
                score -= 15.0
            }
        }

        // Medium-risk patterns
        let mediumPatterns = [
            "illegal", "drugs", "hack", "exploit", "bypass"
        ]

        for pattern in mediumPatterns {
            if lowercased.contains(pattern) {
                score -= 10.0
            }
        }

        return max(0.0, min(100.0, score))
    }

    private func analyzePersonalization(_ text: String, context: EnforcementContext?) async -> Double {
        var score = 80.0
        let lowercased = text.lowercased()

        // Positive personalization markers
        let positiveMarkers = ["you", "your", "help you", "for you", "based on your"]
        for marker in positiveMarkers {
            if lowercased.contains(marker) {
                score += 5.0
            }
        }

        // Check for context awareness
        if context != nil {
            score += 10.0
        }

        // Empathetic language
        let empathyMarkers = ["understand", "feel", "appreciate", "thank you"]
        for marker in empathyMarkers {
            if lowercased.contains(marker) {
                score += 3.0
            }
        }

        return min(100.0, score)
    }

    private func analyzeIntegrity(_ text: String) async -> Double {
        var score = 90.0
        let lowercased = text.lowercased()

        // Deceptive patterns
        let deceptivePatterns = [
            "just trust me", "believe me", "i guarantee",
            "100% certain", "definitely true", "never wrong",
            "secret method", "don't tell anyone"
        ]

        for pattern in deceptivePatterns {
            if lowercased.contains(pattern) {
                score -= 20.0
            }
        }

        // Positive integrity markers
        let integrityMarkers = [
            "according to", "research shows", "evidence suggests",
            "in my understanding", "it appears that"
        ]

        for marker in integrityMarkers {
            if lowercased.contains(marker) {
                score += 5.0
            }
        }

        return max(0.0, min(100.0, score))
    }

    private func analyzeEthics(_ text: String) async -> Double {
        var score = 95.0
        let lowercased = text.lowercased()

        // Unethical patterns
        let unethicalPatterns = [
            "cheat", "lie", "deceive", "manipulate", "exploit",
            "abuse", "discriminate", "stereotype", "bias against"
        ]

        for pattern in unethicalPatterns {
            if lowercased.contains(pattern) {
                score -= 25.0
            }
        }

        // Privacy violation patterns
        let privacyPatterns = [
            "personal information", "private data", "without consent",
            "track you", "spy on"
        ]

        for pattern in privacyPatterns {
            if lowercased.contains(pattern) {
                score -= 15.0
            }
        }

        return max(0.0, min(100.0, score))
    }

    private func analyzeLogic(_ text: String) async -> Double {
        var score = 85.0
        let lowercased = text.lowercased()

        // Logical reasoning markers
        let logicMarkers = [
            "because", "therefore", "thus", "hence", "consequently",
            "as a result", "this means", "in conclusion"
        ]

        for marker in logicMarkers {
            if lowercased.contains(marker) {
                score += 5.0
            }
        }

        // Check for contradictions (simplified)
        if lowercased.contains("but also") && lowercased.contains("however") {
            score -= 5.0
        }

        // Very short responses may lack logical depth
        if text.count < 20 {
            score -= 10.0
        }

        return max(0.0, min(100.0, score))
    }

    // MARK: - Policy Rule Evaluation

    private func evaluateRule(_ rule: PolicyRule, output: String) async -> PolicyViolation? {
        let lowercased = output.lowercased()

        for pattern in rule.patterns {
            if lowercased.contains(pattern.lowercased()) {
                return PolicyViolation(
                    dimension: rule.dimension,
                    score: 0,
                    threshold: 100,
                    severity: rule.severity,
                    description: rule.description,
                    ruleId: rule.id
                )
            }
        }

        return nil
    }

    // MARK: - Action Determination (Fail-Closed)

    private func determineAction(violations: [PolicyViolation], scores: SPIELDimensionScores) -> EnforcementAction {
        // Fail-closed: any critical violation blocks
        if violations.contains(where: { $0.severity == .critical }) {
            return .block
        }

        // Multiple high-severity violations
        let highViolations = violations.filter { $0.severity == .high }
        if highViolations.count >= 2 {
            return .block
        }

        // Single high-severity requires review
        if !highViolations.isEmpty {
            return .review
        }

        // Medium violations trigger warning
        if violations.contains(where: { $0.severity == .medium }) {
            return .warn
        }

        // Composite score check
        let composite = (scores.safety + scores.integrity + scores.ethics) / 3.0
        if composite < 70.0 {
            return .block
        }

        if composite < 80.0 {
            return .warn
        }

        return .allow
    }

    // MARK: - Safe Alternative Generation

    private func generateSafeAlternative(_ violations: [PolicyViolation]) -> String {
        let primaryViolation = violations.first { $0.severity == .critical } ?? violations.first

        switch primaryViolation?.dimension {
        case .safety:
            return "I'm unable to provide that response as it may involve harmful content. How can I help you in a safe and constructive way?"
        case .ethics:
            return "I need to decline that request as it raises ethical concerns. Let me know how I can assist you appropriately."
        case .integrity:
            return "I want to be transparent with you - I cannot verify that information. Would you like me to help you find reliable sources?"
        case .personalization:
            return "I'd like to better understand your needs. Could you tell me more about what you're looking for?"
        case .logic:
            return "Let me provide a clearer response. Could you help me understand what specific information would be most helpful?"
        case .none:
            return "I apologize, but I'm unable to provide that response. How else can I assist you?"
        }
    }

    // MARK: - SHA-256 Hashing

    private func generateSHA256(_ content: String) -> String {
        let data = Data(content.utf8)
        let hash = SHA256.hash(data: data)
        return hash.compactMap { String(format: "%02x", $0) }.joined()
    }

    // MARK: - Audit Trail

    private func addAuditEntry(input: String, output: String, result: EnforcementResult) {
        let entry = EnforcementAuditEntry(
            id: UUID(),
            timestamp: Date(),
            inputHash: generateSHA256(input),
            outputHash: generateSHA256(output),
            action: result.action,
            compositeScore: result.compositeScore,
            violationCount: result.violations.count
        )

        auditLog.append(entry)

        // Trim if exceeds max
        if auditLog.count > maxAuditEntries {
            auditLog.removeFirst(auditLog.count - maxAuditEntries)
        }
    }

    /// Export audit trail as JSON
    public func exportAuditTrail() -> Data? {
        try? JSONEncoder().encode(auditLog)
    }

    // MARK: - Configuration Updates

    /// Update SPIEL thresholds
    public func updateThresholds(_ newThresholds: SPIELThresholds) {
        thresholds = newThresholds
    }

    /// Add custom policy rule
    public func addPolicyRule(_ rule: PolicyRule) {
        policies[rule.id] = rule
    }

    /// Remove policy rule
    public func removePolicyRule(id: String) {
        policies.removeValue(forKey: id)
    }
}

// MARK: - Supporting Types

public enum SPIELDimension: String, Codable {
    case safety = "safety"
    case personalization = "personalization"
    case integrity = "integrity"
    case ethics = "ethics"
    case logic = "logic"
}

public enum EnforcementAction: String, Codable {
    case allow = "allow"
    case warn = "warn"
    case review = "review"
    case block = "block"
}

public enum ViolationSeverity: String, Codable, Comparable {
    case low = "low"
    case medium = "medium"
    case high = "high"
    case critical = "critical"

    public static func < (lhs: ViolationSeverity, rhs: ViolationSeverity) -> Bool {
        let order: [ViolationSeverity] = [.low, .medium, .high, .critical]
        return order.firstIndex(of: lhs)! < order.firstIndex(of: rhs)!
    }
}

public struct SPIELThresholds: Codable {
    public var safety: Double
    public var personalization: Double
    public var integrity: Double
    public var ethics: Double
    public var logic: Double

    public static let `default` = SPIELThresholds(
        safety: 85.0,
        personalization: 70.0,
        integrity: 80.0,
        ethics: 90.0,
        logic: 75.0
    )
}

public struct SPIELDimensionScores: Codable {
    public var safety: Double = 0
    public var personalization: Double = 0
    public var integrity: Double = 0
    public var ethics: Double = 0
    public var logic: Double = 0
}

public struct PolicyViolation: Codable, Identifiable {
    public let id = UUID()
    public let dimension: SPIELDimension
    public let score: Double
    public let threshold: Double
    public let severity: ViolationSeverity
    public let description: String
    public var ruleId: String?
}

public struct PolicyRule: Codable, Identifiable {
    public let id: String
    public let dimension: SPIELDimension
    public let patterns: [String]
    public let severity: ViolationSeverity
    public let description: String
    public var isEnabled: Bool

    public static let defaultPolicies: [String: PolicyRule] = [
        "harmful_content": PolicyRule(
            id: "harmful_content",
            dimension: .safety,
            patterns: ["kill", "murder", "attack", "weapon"],
            severity: .critical,
            description: "Harmful content detected",
            isEnabled: true
        ),
        "deception": PolicyRule(
            id: "deception",
            dimension: .integrity,
            patterns: ["just trust me", "believe me", "guaranteed"],
            severity: .high,
            description: "Deceptive language detected",
            isEnabled: true
        )
    ]
}

public struct PolicyStore: Codable {
    public let version: String
    public let rules: [PolicyRule]
    public let thresholds: SPIELThresholds?
}

public struct EnforcementResult: Codable {
    public let action: EnforcementAction
    public let scores: SPIELDimensionScores
    public let compositeScore: Double
    public let violations: [PolicyViolation]
    public let contentHash: String
    public let processingTimeMs: Double
    public let timestamp: Date
    public let safeOutput: String
}

public struct EnforcementContext: Codable {
    public let userId: String?
    public let sessionId: String?
    public let previousInteractions: Int
    public let userPreferences: [String: String]?
}

public struct EnforcementAuditEntry: Codable, Identifiable {
    public let id: UUID
    public let timestamp: Date
    public let inputHash: String
    public let outputHash: String
    public let action: EnforcementAction
    public let compositeScore: Double
    public let violationCount: Int
}
