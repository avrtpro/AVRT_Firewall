//
//  AVRTModels.swift
//  AVRT_iOS
//
//  Core data models for AVRT SDK
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation

// MARK: - Validation Status
enum ValidationStatus: String, Codable {
    case safe
    case blocked
    case warning
    case reviewRequired = "review_required"
    case error
}

// MARK: - Violation Types
enum ViolationType: String, Codable, CaseIterable {
    case harmfulContent = "harmful_content"
    case misinformation
    case manipulation
    case bias
    case privacyViolation = "privacy_violation"
    case hallucination
    case ethicalViolation = "ethical_violation"

    var displayName: String {
        switch self {
        case .harmfulContent: return "Harmful Content"
        case .misinformation: return "Misinformation"
        case .manipulation: return "Manipulation"
        case .bias: return "Bias Detected"
        case .privacyViolation: return "Privacy Violation"
        case .hallucination: return "Hallucination"
        case .ethicalViolation: return "Ethical Violation"
        }
    }
}

// MARK: - SPIEL Score
struct SPIELScore: Codable, Equatable {
    let safety: Double
    let personalization: Double
    let integrity: Double
    let ethics: Double
    let logic: Double
    let composite: Double
    let timestamp: Date

    init(
        safety: Double = 0,
        personalization: Double = 0,
        integrity: Double = 0,
        ethics: Double = 0,
        logic: Double = 0,
        composite: Double? = nil,
        timestamp: Date = Date()
    ) {
        self.safety = safety
        self.personalization = personalization
        self.integrity = integrity
        self.ethics = ethics
        self.logic = logic
        self.composite = composite ?? (safety + personalization + integrity + ethics + logic) / 5.0
        self.timestamp = timestamp
    }

    func isPassing(threshold: Double = 85.0) -> Bool {
        return safety >= threshold &&
               integrity >= threshold &&
               ethics >= threshold &&
               composite >= threshold
    }

    static let sample = SPIELScore(
        safety: 92.0,
        personalization: 88.0,
        integrity: 90.0,
        ethics: 95.0,
        logic: 87.0
    )
}

// MARK: - THT Validation
struct THTValidation: Codable, Equatable {
    let truthVerified: Bool
    let honestyVerified: Bool
    let transparencyVerified: Bool
    let confidenceScore: Double
    let issues: [String]
    let timestamp: Date

    var isCompliant: Bool {
        return truthVerified &&
               honestyVerified &&
               transparencyVerified &&
               confidenceScore >= 0.8
    }

    static let sample = THTValidation(
        truthVerified: true,
        honestyVerified: true,
        transparencyVerified: true,
        confidenceScore: 0.95,
        issues: [],
        timestamp: Date()
    )

    static let failed = THTValidation(
        truthVerified: false,
        honestyVerified: true,
        transparencyVerified: false,
        confidenceScore: 0.6,
        issues: ["Truth verification failed", "Transparency check failed"],
        timestamp: Date()
    )
}

// MARK: - Validation Result
struct ValidationResult: Codable, Identifiable {
    let id: UUID
    let requestId: String
    let status: ValidationStatus
    let isSafe: Bool
    let message: String
    let originalInput: String
    let originalOutput: String
    let spielScore: SPIELScore?
    let thtValidation: THTValidation?
    let violations: [ViolationType]
    let reason: String?
    let suggestedAlternative: String?
    let confidence: Double
    let processingTimeMs: Double
    let timestamp: Date
    let integrityHash: String

    init(
        id: UUID = UUID(),
        requestId: String = UUID().uuidString,
        status: ValidationStatus,
        isSafe: Bool,
        message: String,
        originalInput: String = "",
        originalOutput: String = "",
        spielScore: SPIELScore? = nil,
        thtValidation: THTValidation? = nil,
        violations: [ViolationType] = [],
        reason: String? = nil,
        suggestedAlternative: String? = nil,
        confidence: Double = 0.0,
        processingTimeMs: Double = 0.0,
        timestamp: Date = Date(),
        integrityHash: String = ""
    ) {
        self.id = id
        self.requestId = requestId
        self.status = status
        self.isSafe = isSafe
        self.message = message
        self.originalInput = originalInput
        self.originalOutput = originalOutput
        self.spielScore = spielScore
        self.thtValidation = thtValidation
        self.violations = violations
        self.reason = reason
        self.suggestedAlternative = suggestedAlternative
        self.confidence = confidence
        self.processingTimeMs = processingTimeMs
        self.timestamp = timestamp
        self.integrityHash = integrityHash
    }

    static func error(message: String) -> ValidationResult {
        return ValidationResult(
            status: .error,
            isSafe: false,
            message: message,
            reason: message,
            integrityHash: HashService.sha256(message)
        )
    }

    static let sample = ValidationResult(
        status: .safe,
        isSafe: true,
        message: "It's sunny and 72F in San Francisco today.",
        originalInput: "What's the weather like?",
        originalOutput: "It's sunny and 72F in San Francisco today.",
        spielScore: .sample,
        thtValidation: .sample,
        confidence: 0.92,
        processingTimeMs: 45.3,
        integrityHash: "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678"
    )
}

// MARK: - Statistics
struct AVRTStatistics: Codable {
    let totalValidations: Int
    let blockedCount: Int
    let blockedRate: Double
    let averageSPIELScore: Double
    let thtComplianceRate: Double
    let thtEnabled: Bool

    static let sample = AVRTStatistics(
        totalValidations: 156,
        blockedCount: 12,
        blockedRate: 0.077,
        averageSPIELScore: 88.5,
        thtComplianceRate: 0.94,
        thtEnabled: true
    )
}

// MARK: - API Request/Response Models
struct ValidationRequest: Codable {
    let input: String
    let output: String?
    let context: [String: String]?
    let userId: String?
}

struct ValidationResponse: Codable {
    let status: String
    let isSafe: Bool
    let message: String
    let originalInput: String
    let originalOutput: String
    let violations: [String]
    let reason: String?
    let suggestedAlternative: String?
    let confidence: Double
    let processingTimeMs: Double
    let timestamp: String
    let spielScore: SPIELScoreResponse?
    let thtValidation: THTValidationResponse?
    let integrityHash: String

    struct SPIELScoreResponse: Codable {
        let safety: Double
        let personalization: Double
        let integrity: Double
        let ethics: Double
        let logic: Double
        let composite: Double
    }

    struct THTValidationResponse: Codable {
        let truthVerified: Bool
        let honestyVerified: Bool
        let transparencyVerified: Bool
        let confidenceScore: Double
        let issues: [String]
    }
}

// MARK: - Start My Day
struct StartMyDayRequest: Codable {
    let preferences: [String: AnyCodable]
}

struct StartMyDayResponse: Codable {
    let greeting: String
    let focusAreas: [String]
    let reflectionPrompt: String
    let tone: String
    let timestamp: String
}

// MARK: - AnyCodable Helper
struct AnyCodable: Codable {
    let value: Any

    init(_ value: Any) {
        self.value = value
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if let string = try? container.decode(String.self) {
            value = string
        } else if let int = try? container.decode(Int.self) {
            value = int
        } else if let double = try? container.decode(Double.self) {
            value = double
        } else if let bool = try? container.decode(Bool.self) {
            value = bool
        } else if let array = try? container.decode([String].self) {
            value = array
        } else {
            value = ""
        }
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        if let string = value as? String {
            try container.encode(string)
        } else if let int = value as? Int {
            try container.encode(int)
        } else if let double = value as? Double {
            try container.encode(double)
        } else if let bool = value as? Bool {
            try container.encode(bool)
        } else if let array = value as? [String] {
            try container.encode(array)
        }
    }
}

// MARK: - Audit Entry
struct AuditEntry: Codable, Identifiable {
    let id: UUID
    let requestId: String
    let userId: String?
    let inputText: String
    let outputText: String
    let validationResult: ValidationResult
    let context: [String: String]
    let timestamp: Date

    init(
        id: UUID = UUID(),
        requestId: String = UUID().uuidString,
        userId: String? = nil,
        inputText: String,
        outputText: String,
        validationResult: ValidationResult,
        context: [String: String] = [:],
        timestamp: Date = Date()
    ) {
        self.id = id
        self.requestId = requestId
        self.userId = userId
        self.inputText = inputText
        self.outputText = outputText
        self.validationResult = validationResult
        self.context = context
        self.timestamp = timestamp
    }
}
