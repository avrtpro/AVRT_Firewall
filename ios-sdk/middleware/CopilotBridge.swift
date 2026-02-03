//
//  CopilotBridge.swift
//  AVRT Middleware
//
//  Copilot Integration Bridge for AVRT SDK
//  Exports SPIEL + THT scores as JSON for external AI assistants
//
//  Patent: USPTO 19/236,935
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation

// MARK: - Copilot Bridge

/// Bridge interface for AI assistant integrations (Copilot, etc.)
/// Exports AVRT validation scores in JSON format for external consumption
public final class CopilotBridge {

    // MARK: - Singleton
    public static let shared = CopilotBridge()

    // MARK: - Configuration
    private let version = "1.0.0"
    private let sdkTag = "ios-v1.0.0-avrt"

    // MARK: - Initialization
    private init() {}

    // MARK: - Core Export Function

    /// Export AVRT scores as JSON for a given prompt
    /// - Parameter prompt: The input prompt to analyze
    /// - Returns: JSON string containing SPIEL + THT scores
    public func exportAVRTScoresAsJSON(for prompt: String) -> String {
        let timestamp = ISO8601DateFormatter().string(from: Date())

        // Analyze with SPIEL
        let spielScores = analyzeSPIEL(prompt: prompt)

        // Validate with THT
        let thtScores = validateTHT(prompt: prompt)

        // Calculate composite
        let compositeScore = (spielScores.safety + spielScores.personalization +
                             spielScores.integrity + spielScores.ethics +
                             spielScores.logic) / 5.0

        // Build JSON response
        let response = AVRTScoreResponse(
            version: version,
            sdkTag: sdkTag,
            timestamp: timestamp,
            prompt: PromptInfo(
                text: prompt,
                length: prompt.count,
                hash: sha256(prompt)
            ),
            spiel: spielScores,
            tht: thtScores,
            composite: CompositeScore(
                score: compositeScore,
                grade: calculateGrade(compositeScore),
                passing: compositeScore >= 85.0
            ),
            recommendation: generateRecommendation(spiel: spielScores, tht: thtScores),
            patent: "USPTO 19/236,935"
        )

        // Encode to JSON
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

        guard let jsonData = try? encoder.encode(response),
              let jsonString = String(data: jsonData, encoding: .utf8) else {
            return errorJSON("Failed to encode AVRT scores")
        }

        return jsonString
    }

    // MARK: - SPIEL Analysis

    private func analyzeSPIEL(prompt: String) -> SPIELScores {
        let lowercased = prompt.lowercased()

        // Safety analysis
        var safety = 100.0
        let harmfulPatterns = ["harm", "hurt", "attack", "kill", "destroy", "hate", "violence"]
        for pattern in harmfulPatterns {
            if lowercased.contains(pattern) { safety -= 15.0 }
        }

        // Personalization analysis
        var personalization = 80.0
        let personalMarkers = ["you", "your", "help", "assist"]
        for marker in personalMarkers {
            if lowercased.contains(marker) { personalization += 5.0 }
        }

        // Integrity analysis
        var integrity = 90.0
        let dishonestPatterns = ["trust me", "believe me", "guaranteed", "secret"]
        for pattern in dishonestPatterns {
            if lowercased.contains(pattern) { integrity -= 20.0 }
        }

        // Ethics analysis
        var ethics = 95.0
        let unethicalPatterns = ["cheat", "lie", "deceive", "manipulate", "exploit"]
        for pattern in unethicalPatterns {
            if lowercased.contains(pattern) { ethics -= 25.0 }
        }

        // Logic analysis
        var logic = 85.0
        let logicMarkers = ["because", "therefore", "thus", "reason"]
        for marker in logicMarkers {
            if lowercased.contains(marker) { logic += 5.0 }
        }

        return SPIELScores(
            safety: clamp(safety),
            personalization: clamp(personalization),
            integrity: clamp(integrity),
            ethics: clamp(ethics),
            logic: clamp(logic)
        )
    }

    // MARK: - THT Validation

    private func validateTHT(prompt: String) -> THTScores {
        let lowercased = prompt.lowercased()

        // Truth verification
        var truthScore = 90.0
        let falsePatterns = ["definitely", "100% certain", "guaranteed fact", "always true"]
        for pattern in falsePatterns {
            if lowercased.contains(pattern) { truthScore -= 20.0 }
        }

        // Honesty check
        var honestyScore = 90.0
        let deceptivePatterns = ["just between us", "don't tell", "keep secret"]
        for pattern in deceptivePatterns {
            if lowercased.contains(pattern) { honestyScore -= 25.0 }
        }

        // Transparency check
        var transparencyScore = 85.0
        let transparentMarkers = ["because", "the reason", "evidence", "according to"]
        for marker in transparentMarkers {
            if lowercased.contains(marker) { transparencyScore += 5.0 }
        }

        return THTScores(
            truth: clamp(truthScore),
            honesty: clamp(honestyScore),
            transparency: clamp(transparencyScore),
            compliant: truthScore >= 80.0 && honestyScore >= 80.0 && transparencyScore >= 80.0
        )
    }

    // MARK: - Helpers

    private func clamp(_ value: Double) -> Double {
        return max(0.0, min(100.0, value))
    }

    private func calculateGrade(_ score: Double) -> String {
        if score >= 90 { return "A" }
        if score >= 80 { return "B" }
        if score >= 70 { return "C" }
        if score >= 60 { return "D" }
        return "F"
    }

    private func sha256(_ string: String) -> String {
        guard let data = string.data(using: .utf8) else { return "" }
        var hash = [UInt8](repeating: 0, count: 32)
        data.withUnsafeBytes { buffer in
            _ = CC_SHA256(buffer.baseAddress, CC_LONG(buffer.count), &hash)
        }
        return hash.map { String(format: "%02x", $0) }.joined()
    }

    private func generateRecommendation(spiel: SPIELScores, tht: THTScores) -> Recommendation {
        var action = "allow"
        var reason = "Content passes all AVRT validation checks"

        if spiel.safety < 85 {
            action = "block"
            reason = "Safety score below threshold"
        } else if spiel.ethics < 90 {
            action = "block"
            reason = "Ethics score below threshold"
        } else if !tht.compliant {
            action = "review"
            reason = "THT protocol compliance issues"
        } else if spiel.integrity < 80 {
            action = "warn"
            reason = "Integrity score requires attention"
        }

        return Recommendation(action: action, reason: reason)
    }

    private func errorJSON(_ message: String) -> String {
        return """
        {
          "error": "\(message)",
          "version": "\(version)",
          "sdkTag": "\(sdkTag)"
        }
        """
    }

    // MARK: - Batch Export

    /// Export scores for multiple prompts
    public func exportBatchScores(for prompts: [String]) -> String {
        var results: [String] = []
        for prompt in prompts {
            results.append(exportAVRTScoresAsJSON(for: prompt))
        }

        return "[\n" + results.joined(separator: ",\n") + "\n]"
    }

    // MARK: - Metadata Export

    /// Export SDK metadata
    public func exportMetadata() -> String {
        return """
        {
          "sdk": "AVRT",
          "version": "\(version)",
          "tag": "\(sdkTag)",
          "patent": "USPTO 19/236,935",
          "frameworks": ["SPIEL", "THT", "EaaS", "LARM"],
          "trademarks": ["AVRT", "SPIEL", "THT", "EaaS", "LARM", "AWOGO", "BeGoodBeHumble"],
          "copyright": "(c) 2025 Jason I. Proper, BGBH Threads LLC"
        }
        """
    }
}

// MARK: - Response Models

struct AVRTScoreResponse: Codable {
    let version: String
    let sdkTag: String
    let timestamp: String
    let prompt: PromptInfo
    let spiel: SPIELScores
    let tht: THTScores
    let composite: CompositeScore
    let recommendation: Recommendation
    let patent: String
}

struct PromptInfo: Codable {
    let text: String
    let length: Int
    let hash: String
}

struct SPIELScores: Codable {
    let safety: Double
    let personalization: Double
    let integrity: Double
    let ethics: Double
    let logic: Double
}

struct THTScores: Codable {
    let truth: Double
    let honesty: Double
    let transparency: Double
    let compliant: Bool
}

struct CompositeScore: Codable {
    let score: Double
    let grade: String
    let passing: Bool
}

struct Recommendation: Codable {
    let action: String
    let reason: String
}

// MARK: - CommonCrypto Bridge (for SHA-256)

import CommonCrypto

private func CC_SHA256(_ data: UnsafeRawPointer?, _ len: CC_LONG, _ md: UnsafeMutablePointer<UInt8>?) -> UnsafeMutablePointer<UInt8>? {
    return CommonCrypto.CC_SHA256(data, len, md)
}
