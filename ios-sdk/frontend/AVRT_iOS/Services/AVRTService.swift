//
//  AVRTService.swift
//  AVRT_iOS
//
//  Core AVRT service for API communication and validation
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation
import Combine

@MainActor
class AVRTService: ObservableObject {
    static let shared = AVRTService()

    // MARK: - Published Properties
    @Published var isConnected = false
    @Published var isLicenseValid = false
    @Published var lastError: Error?

    // MARK: - Configuration
    private var licenseKey: String = ""
    private var baseURL: URL = URL(string: "https://avrt.pro/api")!

    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    // MARK: - Initialization
    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 60
        self.session = URLSession(configuration: config)

        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.decoder.dateDecodingStrategy = .iso8601

        self.encoder = JSONEncoder()
        self.encoder.keyEncodingStrategy = .convertToSnakeCase
        self.encoder.dateEncodingStrategy = .iso8601

        // Load from UserDefaults if available
        if let savedKey = UserDefaults.standard.string(forKey: "AVRT_LICENSE_KEY") {
            configure(licenseKey: savedKey)
        }
    }

    // MARK: - Configuration
    func configure(licenseKey: String, baseURL: String? = nil) {
        self.licenseKey = licenseKey
        if let baseURL = baseURL, let url = URL(string: baseURL) {
            self.baseURL = url
        }

        // Save to UserDefaults
        UserDefaults.standard.set(licenseKey, forKey: "AVRT_LICENSE_KEY")

        // Validate license
        Task {
            await validateLicense()
        }
    }

    // MARK: - License Validation
    func validateLicense() async {
        guard !licenseKey.isEmpty else {
            isLicenseValid = false
            return
        }

        do {
            var request = createRequest(endpoint: "/license/validate", method: "POST")
            let body = ["license_key": licenseKey]
            request.httpBody = try encoder.encode(body)

            let (data, response) = try await session.data(for: request)

            if let httpResponse = response as? HTTPURLResponse {
                isConnected = true
                isLicenseValid = httpResponse.statusCode == 200

                if !isLicenseValid {
                    print("AVRT License validation failed: \(httpResponse.statusCode)")
                }
            }
        } catch {
            // For demo/development, allow offline mode
            isConnected = false
            isLicenseValid = !licenseKey.isEmpty
            print("AVRT License validation error (offline mode): \(error)")
        }
    }

    // MARK: - Validation
    func validateInput(input: String, context: [String: String]? = nil) async throws -> ValidationResult {
        // First, get AI response (simulated for SDK demo)
        let aiOutput = await simulateAIResponse(for: input)

        return try await validate(input: input, output: aiOutput, context: context)
    }

    func validate(input: String, output: String, context: [String: String]? = nil, userId: String? = nil) async throws -> ValidationResult {
        // Create request
        let validationRequest = ValidationRequest(
            input: input,
            output: output,
            context: context,
            userId: userId
        )

        do {
            var request = createRequest(endpoint: "/validate", method: "POST")
            request.httpBody = try encoder.encode(validationRequest)

            let (data, response) = try await session.data(for: request)

            guard let httpResponse = response as? HTTPURLResponse else {
                throw AVRTError.invalidResponse
            }

            isConnected = true

            if httpResponse.statusCode == 200 {
                let validationResponse = try decoder.decode(ValidationResponse.self, from: data)
                return mapResponse(validationResponse, input: input, output: output)
            } else {
                throw AVRTError.serverError(statusCode: httpResponse.statusCode)
            }
        } catch is URLError {
            // Offline mode: perform local validation
            isConnected = false
            return performLocalValidation(input: input, output: output, context: context)
        }
    }

    // MARK: - Start My Day
    func startMyDay(preferences: [String: Any]) async throws -> ValidationResult {
        let request = StartMyDayRequest(
            preferences: preferences.mapValues { AnyCodable($0) }
        )

        do {
            var urlRequest = createRequest(endpoint: "/start-my-day", method: "POST")
            urlRequest.httpBody = try encoder.encode(request)

            let (data, response) = try await session.data(for: urlRequest)

            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                throw AVRTError.invalidResponse
            }

            let startMyDayResponse = try decoder.decode(StartMyDayResponse.self, from: data)

            return ValidationResult(
                status: .safe,
                isSafe: true,
                message: """
                \(startMyDayResponse.greeting)

                Today's Focus: \(startMyDayResponse.focusAreas.joined(separator: ", "))

                \(startMyDayResponse.reflectionPrompt)
                """,
                spielScore: SPIELScore.sample,
                thtValidation: THTValidation.sample,
                confidence: 1.0,
                integrityHash: HashService.sha256(startMyDayResponse.greeting)
            )
        } catch is URLError {
            // Offline mode
            return generateOfflineStartMyDay(preferences: preferences)
        }
    }

    // MARK: - Statistics
    func getStatistics() async throws -> AVRTStatistics {
        do {
            let request = createRequest(endpoint: "/statistics", method: "GET")
            let (data, _) = try await session.data(for: request)
            return try decoder.decode(AVRTStatistics.self, from: data)
        } catch {
            // Return sample data for offline mode
            return AVRTStatistics.sample
        }
    }

    func getRecentValidations(limit: Int = 10) async throws -> [ValidationResult] {
        // For demo, return empty array (would connect to backend in production)
        return []
    }

    // MARK: - Private Helpers
    private func createRequest(endpoint: String, method: String) -> URLRequest {
        let url = baseURL.appendingPathComponent(endpoint)
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(licenseKey)", forHTTPHeaderField: "Authorization")
        request.setValue("AVRT-iOS-SDK/1.0.0", forHTTPHeaderField: "User-Agent")
        return request
    }

    private func mapResponse(_ response: ValidationResponse, input: String, output: String) -> ValidationResult {
        let spielScore: SPIELScore?
        if let spiel = response.spielScore {
            spielScore = SPIELScore(
                safety: spiel.safety,
                personalization: spiel.personalization,
                integrity: spiel.integrity,
                ethics: spiel.ethics,
                logic: spiel.logic,
                composite: spiel.composite
            )
        } else {
            spielScore = nil
        }

        let thtValidation: THTValidation?
        if let tht = response.thtValidation {
            thtValidation = THTValidation(
                truthVerified: tht.truthVerified,
                honestyVerified: tht.honestyVerified,
                transparencyVerified: tht.transparencyVerified,
                confidenceScore: tht.confidenceScore,
                issues: tht.issues,
                timestamp: Date()
            )
        } else {
            thtValidation = nil
        }

        let violations = response.violations.compactMap { ViolationType(rawValue: $0) }

        return ValidationResult(
            status: ValidationStatus(rawValue: response.status) ?? .error,
            isSafe: response.isSafe,
            message: response.message,
            originalInput: input,
            originalOutput: output,
            spielScore: spielScore,
            thtValidation: thtValidation,
            violations: violations,
            reason: response.reason,
            suggestedAlternative: response.suggestedAlternative,
            confidence: response.confidence,
            processingTimeMs: response.processingTimeMs,
            integrityHash: response.integrityHash
        )
    }

    // MARK: - Local Validation (Offline Mode)
    private func performLocalValidation(input: String, output: String, context: [String: String]?) -> ValidationResult {
        let startTime = Date()

        // Local SPIEL analysis
        let spielScore = performLocalSPIELAnalysis(text: output)

        // Local THT validation
        let thtValidation = performLocalTHTValidation(text: output)

        // Determine safety
        let isSafe = spielScore.isPassing() && thtValidation.isCompliant
        var violations: [ViolationType] = []

        if spielScore.safety < 85 {
            violations.append(.harmfulContent)
        }
        if spielScore.ethics < 90 {
            violations.append(.ethicalViolation)
        }

        let processingTime = Date().timeIntervalSince(startTime) * 1000
        let hash = HashService.sha256("\(input)|\(output)|\(Date().timeIntervalSince1970)")

        return ValidationResult(
            status: isSafe ? .safe : .blocked,
            isSafe: isSafe,
            message: isSafe ? output : "Response blocked by AVRT safety filters.",
            originalInput: input,
            originalOutput: output,
            spielScore: spielScore,
            thtValidation: thtValidation,
            violations: violations,
            reason: isSafe ? nil : "Failed SPIEL/THT validation",
            confidence: spielScore.composite / 100.0,
            processingTimeMs: processingTime,
            integrityHash: hash
        )
    }

    private func performLocalSPIELAnalysis(text: String) -> SPIELScore {
        let lowercased = text.lowercased()

        // Safety analysis
        var safetyScore = 100.0
        let harmfulPatterns = ["harm", "hurt", "attack", "kill", "destroy", "hate", "violence"]
        for pattern in harmfulPatterns {
            if lowercased.contains(pattern) {
                safetyScore -= 15.0
            }
        }

        // Personalization analysis
        var personalizationScore = 85.0
        let personalMarkers = ["you", "your", "i can help"]
        for marker in personalMarkers {
            if lowercased.contains(marker) {
                personalizationScore += 5.0
            }
        }

        // Integrity analysis
        var integrityScore = 90.0
        let dishonestPatterns = ["just trust me", "believe me", "i guarantee"]
        for pattern in dishonestPatterns {
            if lowercased.contains(pattern) {
                integrityScore -= 15.0
            }
        }

        // Ethics analysis
        var ethicsScore = 95.0
        let unethicalPatterns = ["cheat", "lie", "deceive", "manipulate"]
        for pattern in unethicalPatterns {
            if lowercased.contains(pattern) {
                ethicsScore -= 20.0
            }
        }

        // Logic analysis
        var logicScore = 88.0
        if text.contains("because") || text.contains("therefore") {
            logicScore += 5.0
        }

        return SPIELScore(
            safety: max(0, min(100, safetyScore)),
            personalization: min(100, personalizationScore),
            integrity: max(0, integrityScore),
            ethics: max(0, ethicsScore),
            logic: min(100, logicScore)
        )
    }

    private func performLocalTHTValidation(text: String) -> THTValidation {
        let lowercased = text.lowercased()

        // Truth verification
        let falsePatterns = ["definitely", "absolutely certain", "100% guarantee"]
        let truthVerified = !falsePatterns.contains { lowercased.contains($0) }

        // Honesty verification
        let dishonestPatterns = ["just between us", "don't tell", "keep this secret"]
        let honestyVerified = !dishonestPatterns.contains { lowercased.contains($0) }

        // Transparency verification
        let transparentMarkers = ["because", "the reason", "this is based on"]
        let transparencyVerified = transparentMarkers.contains { lowercased.contains($0) } || text.count < 50

        var issues: [String] = []
        if !truthVerified { issues.append("Truth verification failed") }
        if !honestyVerified { issues.append("Honesty check failed") }
        if !transparencyVerified { issues.append("Transparency check failed") }

        let confidence = Double([truthVerified, honestyVerified, transparencyVerified].filter { $0 }.count) / 3.0

        return THTValidation(
            truthVerified: truthVerified,
            honestyVerified: honestyVerified,
            transparencyVerified: transparencyVerified,
            confidenceScore: confidence,
            issues: issues,
            timestamp: Date()
        )
    }

    private func simulateAIResponse(for input: String) async -> String {
        // Simulated AI response for demo purposes
        return "I understand you're asking about '\(input)'. Here's what I can help you with..."
    }

    private func generateOfflineStartMyDay(preferences: [String: Any]) -> ValidationResult {
        let focusAreas = (preferences["focus_areas"] as? [String]) ?? ["health", "productivity", "gratitude"]
        let tone = (preferences["tone"] as? String) ?? "encouraging"

        let greeting = "Good morning! Let's start your day with intention and purpose."

        let reflectionPrompts: [String: String] = [
            "health": "How are you feeling physically and emotionally today?",
            "productivity": "What's the most important thing to accomplish today?",
            "gratitude": "What are you grateful for this morning?"
        ]

        let reflections = focusAreas.compactMap { reflectionPrompts[$0] }.joined(separator: " ")

        return ValidationResult(
            status: .safe,
            isSafe: true,
            message: """
            \(greeting)

            Today's Focus: \(focusAreas.joined(separator: ", "))

            \(reflections)

            Remember: Be Good. Be Humble.
            """,
            spielScore: SPIELScore(
                safety: 100,
                personalization: 95,
                integrity: 100,
                ethics: 100,
                logic: 90
            ),
            thtValidation: THTValidation.sample,
            confidence: 1.0,
            integrityHash: HashService.sha256(greeting)
        )
    }
}

// MARK: - Errors
enum AVRTError: LocalizedError {
    case invalidResponse
    case serverError(statusCode: Int)
    case validationFailed(reason: String)
    case networkError(Error)

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "Invalid response from AVRT server"
        case .serverError(let code):
            return "Server error: \(code)"
        case .validationFailed(let reason):
            return "Validation failed: \(reason)"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        }
    }
}
