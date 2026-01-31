//
//  EAS_RULE_ENGINE.swift
//  AVRT_iOS
//
//  EaaS - Ethics-as-a-Service Rule Engine
//  Dynamic ethical rule evaluation and enforcement
//
//  Patent: USPTO 19/236,935
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation
import Combine

// MARK: - EaaS Rule Engine

/// Ethics-as-a-Service Rule Engine for AVRT
/// Provides dynamic ethical rule evaluation with configurable policies
@MainActor
public final class EASRuleEngine: ObservableObject {

    // MARK: - Singleton
    public static let shared = EASRuleEngine()

    // MARK: - Published Properties
    @Published public private(set) var isActive: Bool = true
    @Published public private(set) var activeRuleCount: Int = 0
    @Published public private(set) var lastEvaluation: EASEvaluationResult?
    @Published public private(set) var complianceScore: Double = 100.0

    // MARK: - Rules Storage
    private var rules: [String: EASRule] = [:]
    private var ruleGroups: [String: EASRuleGroup] = [:]
    private var customEvaluators: [String: (String) -> EASRuleMatch?] = [:]

    // MARK: - Configuration
    private var config: EASConfiguration

    // MARK: - Metrics
    private var evaluationMetrics = EASMetrics()

    // MARK: - Initialization
    private init() {
        self.config = EASConfiguration.default
        loadDefaultRules()
        activeRuleCount = rules.count
    }

    // MARK: - Rule Loading

    private func loadDefaultRules() {
        // THT Protocol Rules (Truth, Honesty, Transparency)
        addRule(EASRule(
            id: "tht_truth_001",
            name: "Truth Verification",
            description: "Detect absolute claims without evidence",
            category: .truth,
            severity: .high,
            patterns: [
                "definitely true", "100% certain", "guaranteed fact",
                "absolutely proven", "undeniable truth"
            ],
            action: .flag,
            isEnabled: true
        ))

        addRule(EASRule(
            id: "tht_honesty_001",
            name: "Honesty Check",
            description: "Detect deceptive or manipulative language",
            category: .honesty,
            severity: .critical,
            patterns: [
                "just trust me", "believe me", "don't tell anyone",
                "keep this secret", "between us only"
            ],
            action: .block,
            isEnabled: true
        ))

        addRule(EASRule(
            id: "tht_transparency_001",
            name: "Transparency Enforcement",
            description: "Ensure explainable reasoning",
            category: .transparency,
            severity: .medium,
            requiresExplanation: true,
            action: .warn,
            isEnabled: true
        ))

        // Safety Rules
        addRule(EASRule(
            id: "safety_harm_001",
            name: "Harmful Content Prevention",
            description: "Block content that could cause physical harm",
            category: .safety,
            severity: .critical,
            patterns: [
                "how to hurt", "how to kill", "how to attack",
                "make a weapon", "cause harm", "inflict pain"
            ],
            action: .block,
            isEnabled: true
        ))

        addRule(EASRule(
            id: "safety_selfharm_001",
            name: "Self-Harm Prevention",
            description: "Detect and prevent self-harm content",
            category: .safety,
            severity: .critical,
            patterns: [
                "hurt myself", "end my life", "self-harm",
                "suicide methods", "want to die"
            ],
            action: .escalate,
            escalationMessage: "If you're having thoughts of self-harm, please reach out to a crisis helpline.",
            isEnabled: true
        ))

        // Ethics Rules
        addRule(EASRule(
            id: "ethics_discrimination_001",
            name: "Anti-Discrimination",
            description: "Prevent discriminatory content",
            category: .ethics,
            severity: .high,
            patterns: [
                "those people are", "all [group] are", "typical [group]",
                "they don't belong", "inferior race"
            ],
            action: .block,
            isEnabled: true
        ))

        addRule(EASRule(
            id: "ethics_privacy_001",
            name: "Privacy Protection",
            description: "Protect personal information",
            category: .privacy,
            severity: .high,
            patterns: [
                "social security", "credit card number", "bank account",
                "password is", "private address"
            ],
            action: .redact,
            isEnabled: true
        ))

        // Manipulation Rules
        addRule(EASRule(
            id: "manipulation_001",
            name: "Manipulation Detection",
            description: "Detect manipulative persuasion tactics",
            category: .manipulation,
            severity: .medium,
            patterns: [
                "you must", "you have to", "no choice but",
                "only option is", "or else"
            ],
            action: .flag,
            isEnabled: true
        ))

        // Create rule groups
        ruleGroups["tht_protocol"] = EASRuleGroup(
            id: "tht_protocol",
            name: "THT Protocol",
            description: "Truth, Honesty, Transparency rules",
            ruleIds: ["tht_truth_001", "tht_honesty_001", "tht_transparency_001"],
            isEnabled: true
        )

        ruleGroups["safety_critical"] = EASRuleGroup(
            id: "safety_critical",
            name: "Safety Critical",
            description: "Critical safety rules",
            ruleIds: ["safety_harm_001", "safety_selfharm_001"],
            isEnabled: true
        )
    }

    // MARK: - Rule Management

    /// Add a new rule
    public func addRule(_ rule: EASRule) {
        rules[rule.id] = rule
        activeRuleCount = rules.filter { $0.value.isEnabled }.count
    }

    /// Remove a rule
    public func removeRule(id: String) {
        rules.removeValue(forKey: id)
        activeRuleCount = rules.filter { $0.value.isEnabled }.count
    }

    /// Enable/disable a rule
    public func setRuleEnabled(id: String, enabled: Bool) {
        rules[id]?.isEnabled = enabled
        activeRuleCount = rules.filter { $0.value.isEnabled }.count
    }

    /// Add custom evaluator function
    public func addCustomEvaluator(id: String, evaluator: @escaping (String) -> EASRuleMatch?) {
        customEvaluators[id] = evaluator
    }

    // MARK: - Core Evaluation

    /// Evaluate content against all active rules
    public func evaluate(_ content: String, context: EASContext? = nil) async -> EASEvaluationResult {
        let startTime = Date()
        var matches: [EASRuleMatch] = []
        var actions: [EASAction] = []

        let lowercased = content.lowercased()

        // Evaluate standard rules
        for (_, rule) in rules where rule.isEnabled {
            if let match = evaluateRule(rule, content: lowercased, context: context) {
                matches.append(match)
                actions.append(rule.action)
            }
        }

        // Evaluate custom evaluators
        for (id, evaluator) in customEvaluators {
            if let match = evaluator(content) {
                var customMatch = match
                customMatch.evaluatorId = id
                matches.append(customMatch)
            }
        }

        // Determine final action (most severe wins)
        let finalAction = determineFinalAction(actions)

        // Calculate compliance score
        let compliance = calculateComplianceScore(matches: matches)
        complianceScore = compliance

        // Generate safe content if needed
        let safeContent = generateSafeContent(content, matches: matches, action: finalAction)

        let processingTime = Date().timeIntervalSince(startTime) * 1000

        // Update metrics
        evaluationMetrics.totalEvaluations += 1
        evaluationMetrics.totalProcessingTime += processingTime
        if !matches.isEmpty {
            evaluationMetrics.violationCount += matches.count
        }

        let result = EASEvaluationResult(
            id: UUID(),
            timestamp: Date(),
            originalContent: content,
            safeContent: safeContent,
            matches: matches,
            finalAction: finalAction,
            complianceScore: compliance,
            processingTimeMs: processingTime,
            context: context
        )

        lastEvaluation = result
        return result
    }

    private func evaluateRule(_ rule: EASRule, content: String, context: EASContext?) -> EASRuleMatch? {
        // Pattern-based evaluation
        for pattern in rule.patterns {
            if content.contains(pattern.lowercased()) {
                return EASRuleMatch(
                    ruleId: rule.id,
                    ruleName: rule.name,
                    category: rule.category,
                    severity: rule.severity,
                    matchedPattern: pattern,
                    action: rule.action,
                    description: rule.description
                )
            }
        }

        // Transparency check (requires explanation markers)
        if rule.requiresExplanation {
            let explanationMarkers = ["because", "the reason", "this is due to", "explained by"]
            let hasExplanation = explanationMarkers.contains { content.contains($0) }

            if !hasExplanation && content.count > 100 {
                return EASRuleMatch(
                    ruleId: rule.id,
                    ruleName: rule.name,
                    category: rule.category,
                    severity: rule.severity,
                    matchedPattern: "[lacks explanation]",
                    action: rule.action,
                    description: "Response lacks transparent explanation"
                )
            }
        }

        return nil
    }

    private func determineFinalAction(_ actions: [EASAction]) -> EASAction {
        // Priority order: escalate > block > redact > flag > warn > allow
        let priority: [EASAction] = [.escalate, .block, .redact, .flag, .warn, .allow]

        for action in priority {
            if actions.contains(action) {
                return action
            }
        }

        return .allow
    }

    private func calculateComplianceScore(matches: [EASRuleMatch]) -> Double {
        if matches.isEmpty { return 100.0 }

        var penalty = 0.0
        for match in matches {
            switch match.severity {
            case .critical: penalty += 30.0
            case .high: penalty += 20.0
            case .medium: penalty += 10.0
            case .low: penalty += 5.0
            }
        }

        return max(0.0, 100.0 - penalty)
    }

    private func generateSafeContent(_ original: String, matches: [EASRuleMatch], action: EASAction) -> String {
        switch action {
        case .allow:
            return original

        case .warn:
            return original // Content allowed but flagged

        case .flag:
            return original // Content allowed but flagged for review

        case .redact:
            var redacted = original
            for match in matches where match.action == .redact {
                redacted = redacted.replacingOccurrences(
                    of: match.matchedPattern,
                    with: "[REDACTED]",
                    options: .caseInsensitive
                )
            }
            return redacted

        case .block:
            let primaryMatch = matches.first { $0.severity == .critical } ?? matches.first
            return generateBlockMessage(for: primaryMatch?.category ?? .ethics)

        case .escalate:
            let escalationMatch = matches.first { $0.action == .escalate }
            if let rule = rules[escalationMatch?.ruleId ?? ""], let message = rule.escalationMessage {
                return message
            }
            return "This request requires human review. Please contact support."
        }
    }

    private func generateBlockMessage(for category: EASCategory) -> String {
        switch category {
        case .safety:
            return "I'm unable to provide that information as it could potentially cause harm. How can I help you in a safe way?"
        case .ethics:
            return "I cannot fulfill this request as it raises ethical concerns. Let me know how I can assist you appropriately."
        case .truth:
            return "I cannot verify this as factual. Would you like me to help you find reliable sources?"
        case .honesty:
            return "I want to be transparent with you. This request involves information I cannot honestly provide."
        case .transparency:
            return "I need to provide clearer context. Could you help me understand what specific information would be most helpful?"
        case .privacy:
            return "I cannot share or process that information to protect privacy. How else can I assist you?"
        case .manipulation:
            return "I aim to provide helpful information without pressure. What would genuinely help you right now?"
        }
    }

    // MARK: - Batch Evaluation

    /// Evaluate multiple content items
    public func evaluateBatch(_ contents: [String]) async -> [EASEvaluationResult] {
        var results: [EASEvaluationResult] = []

        for content in contents {
            let result = await evaluate(content)
            results.append(result)
        }

        return results
    }

    // MARK: - Rule Queries

    /// Get all rules by category
    public func getRules(byCategory category: EASCategory) -> [EASRule] {
        return rules.values.filter { $0.category == category }
    }

    /// Get all active rules
    public func getActiveRules() -> [EASRule] {
        return rules.values.filter { $0.isEnabled }
    }

    /// Get rule by ID
    public func getRule(id: String) -> EASRule? {
        return rules[id]
    }

    // MARK: - Metrics

    /// Get current metrics
    public func getMetrics() -> EASMetrics {
        return evaluationMetrics
    }

    /// Reset metrics
    public func resetMetrics() {
        evaluationMetrics = EASMetrics()
    }

    // MARK: - Configuration

    /// Update configuration
    public func updateConfiguration(_ newConfig: EASConfiguration) {
        config = newConfig
    }

    /// Enable/disable the engine
    public func setActive(_ active: Bool) {
        isActive = active
    }

    // MARK: - Export

    /// Export rules as JSON
    public func exportRules() -> Data? {
        let rulesList = Array(rules.values)
        return try? JSONEncoder().encode(rulesList)
    }

    /// Import rules from JSON
    public func importRules(from data: Data) throws {
        let importedRules = try JSONDecoder().decode([EASRule].self, from: data)
        for rule in importedRules {
            rules[rule.id] = rule
        }
        activeRuleCount = rules.filter { $0.value.isEnabled }.count
    }
}

// MARK: - Supporting Types

public enum EASCategory: String, Codable {
    case safety = "safety"
    case ethics = "ethics"
    case truth = "truth"
    case honesty = "honesty"
    case transparency = "transparency"
    case privacy = "privacy"
    case manipulation = "manipulation"
}

public enum EASSeverity: String, Codable, Comparable {
    case low = "low"
    case medium = "medium"
    case high = "high"
    case critical = "critical"

    public static func < (lhs: EASSeverity, rhs: EASSeverity) -> Bool {
        let order: [EASSeverity] = [.low, .medium, .high, .critical]
        return order.firstIndex(of: lhs)! < order.firstIndex(of: rhs)!
    }
}

public enum EASAction: String, Codable {
    case allow = "allow"
    case warn = "warn"
    case flag = "flag"
    case redact = "redact"
    case block = "block"
    case escalate = "escalate"
}

public struct EASRule: Codable, Identifiable {
    public let id: String
    public let name: String
    public let description: String
    public let category: EASCategory
    public let severity: EASSeverity
    public var patterns: [String] = []
    public var requiresExplanation: Bool = false
    public var action: EASAction
    public var escalationMessage: String?
    public var isEnabled: Bool

    public init(
        id: String,
        name: String,
        description: String,
        category: EASCategory,
        severity: EASSeverity,
        patterns: [String] = [],
        requiresExplanation: Bool = false,
        action: EASAction,
        escalationMessage: String? = nil,
        isEnabled: Bool = true
    ) {
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.severity = severity
        self.patterns = patterns
        self.requiresExplanation = requiresExplanation
        self.action = action
        self.escalationMessage = escalationMessage
        self.isEnabled = isEnabled
    }
}

public struct EASRuleGroup: Codable, Identifiable {
    public let id: String
    public let name: String
    public let description: String
    public var ruleIds: [String]
    public var isEnabled: Bool
}

public struct EASRuleMatch: Codable {
    public let ruleId: String
    public let ruleName: String
    public let category: EASCategory
    public let severity: EASSeverity
    public let matchedPattern: String
    public let action: EASAction
    public let description: String
    public var evaluatorId: String?
}

public struct EASEvaluationResult: Codable, Identifiable {
    public let id: UUID
    public let timestamp: Date
    public let originalContent: String
    public let safeContent: String
    public let matches: [EASRuleMatch]
    public let finalAction: EASAction
    public let complianceScore: Double
    public let processingTimeMs: Double
    public let context: EASContext?
}

public struct EASContext: Codable {
    public let userId: String?
    public let sessionId: String?
    public let interactionType: String?
    public let additionalMetadata: [String: String]?

    public init(
        userId: String? = nil,
        sessionId: String? = nil,
        interactionType: String? = nil,
        additionalMetadata: [String: String]? = nil
    ) {
        self.userId = userId
        self.sessionId = sessionId
        self.interactionType = interactionType
        self.additionalMetadata = additionalMetadata
    }
}

public struct EASConfiguration: Codable {
    public var enableStrictMode: Bool
    public var defaultAction: EASAction
    public var maxProcessingTimeMs: Double
    public var enableCustomEvaluators: Bool

    public static let `default` = EASConfiguration(
        enableStrictMode: true,
        defaultAction: .warn,
        maxProcessingTimeMs: 100.0,
        enableCustomEvaluators: true
    )
}

public struct EASMetrics: Codable {
    public var totalEvaluations: Int = 0
    public var violationCount: Int = 0
    public var totalProcessingTime: Double = 0

    public var averageProcessingTime: Double {
        guard totalEvaluations > 0 else { return 0 }
        return totalProcessingTime / Double(totalEvaluations)
    }

    public var violationRate: Double {
        guard totalEvaluations > 0 else { return 0 }
        return Double(violationCount) / Double(totalEvaluations)
    }
}
