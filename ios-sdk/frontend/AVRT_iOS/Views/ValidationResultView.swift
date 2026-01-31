//
//  ValidationResultView.swift
//  AVRT_iOS
//
//  Displays AVRT validation results with SPIEL scores
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import SwiftUI

struct ValidationResultView: View {
    let result: ValidationResult
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Status Banner
                    StatusBanner(result: result)

                    // SPIEL Scores
                    if let spielScore = result.spielScore {
                        SPIELScoreCard(score: spielScore)
                    }

                    // THT Validation
                    if let thtResult = result.thtValidation {
                        THTValidationCard(validation: thtResult)
                    }

                    // Message Content
                    MessageCard(
                        title: "Response",
                        content: result.message,
                        isSafe: result.isSafe
                    )

                    // Violations (if any)
                    if !result.violations.isEmpty {
                        ViolationsCard(violations: result.violations)
                    }

                    // Hash Verification
                    HashVerificationCard(hash: result.integrityHash)

                    // Metadata
                    MetadataCard(result: result)
                }
                .padding()
            }
            .navigationTitle("Validation Result")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// MARK: - Status Banner
struct StatusBanner: View {
    let result: ValidationResult

    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: result.isSafe ? "checkmark.shield.fill" : "xmark.shield.fill")
                .font(.largeTitle)
                .foregroundColor(result.isSafe ? .green : .red)

            VStack(alignment: .leading, spacing: 4) {
                Text(result.isSafe ? "VALIDATED" : "BLOCKED")
                    .font(.headline)
                    .fontWeight(.bold)

                Text(result.status.rawValue.capitalized)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }

            Spacer()

            // Confidence Badge
            VStack {
                Text("\(Int(result.confidence * 100))%")
                    .font(.title2)
                    .fontWeight(.bold)
                Text("Confidence")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(result.isSafe ? Color.green.opacity(0.1) : Color.red.opacity(0.1))
        .cornerRadius(12)
    }
}

// MARK: - SPIEL Score Card
struct SPIELScoreCard: View {
    let score: SPIELScore

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Image(systemName: "chart.bar.fill")
                    .foregroundColor(.avrtPrimary)
                Text("SPIEL Framework")
                    .font(.headline)
                Spacer()
                Text("\(Int(score.composite))/100")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(.avrtPrimary)
            }

            VStack(spacing: 12) {
                ScoreRow(label: "Safety", value: score.safety, color: .red, icon: "shield.fill")
                ScoreRow(label: "Personalization", value: score.personalization, color: .blue, icon: "person.fill")
                ScoreRow(label: "Integrity", value: score.integrity, color: .purple, icon: "lock.fill")
                ScoreRow(label: "Ethics", value: score.ethics, color: .green, icon: "heart.fill")
                ScoreRow(label: "Logic", value: score.logic, color: .orange, icon: "brain.head.profile")
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

struct ScoreRow: View {
    let label: String
    let value: Double
    let color: Color
    let icon: String

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .foregroundColor(color)
                .frame(width: 24)

            Text(label)
                .font(.subheadline)

            Spacer()

            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    Rectangle()
                        .fill(Color(.systemGray5))
                        .frame(height: 8)
                        .cornerRadius(4)

                    Rectangle()
                        .fill(color)
                        .frame(width: geometry.size.width * (value / 100), height: 8)
                        .cornerRadius(4)
                }
            }
            .frame(width: 100, height: 8)

            Text("\(Int(value))")
                .font(.subheadline)
                .fontWeight(.medium)
                .frame(width: 30, alignment: .trailing)
        }
    }
}

// MARK: - THT Validation Card
struct THTValidationCard: View {
    let validation: THTValidation

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Image(systemName: "checkmark.seal.fill")
                    .foregroundColor(.avrtSecondary)
                Text("THT Protocol")
                    .font(.headline)
                Spacer()
                Text(validation.isCompliant ? "Compliant" : "Issues Found")
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(validation.isCompliant ? Color.green.opacity(0.2) : Color.orange.opacity(0.2))
                    .foregroundColor(validation.isCompliant ? .green : .orange)
                    .cornerRadius(8)
            }

            HStack(spacing: 24) {
                THTIndicator(label: "Truth", isVerified: validation.truthVerified)
                THTIndicator(label: "Honesty", isVerified: validation.honestyVerified)
                THTIndicator(label: "Transparency", isVerified: validation.transparencyVerified)
            }

            if !validation.issues.isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    Text("Issues:")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    ForEach(validation.issues, id: \.self) { issue in
                        Text("• \(issue)")
                            .font(.caption)
                            .foregroundColor(.orange)
                    }
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

struct THTIndicator: View {
    let label: String
    let isVerified: Bool

    var body: some View {
        VStack(spacing: 4) {
            Image(systemName: isVerified ? "checkmark.circle.fill" : "xmark.circle.fill")
                .foregroundColor(isVerified ? .green : .red)
            Text(label)
                .font(.caption2)
                .foregroundColor(.secondary)
        }
    }
}

// MARK: - Message Card
struct MessageCard: View {
    let title: String
    let content: String
    let isSafe: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: "text.bubble.fill")
                    .foregroundColor(.avrtPrimary)
                Text(title)
                    .font(.headline)
            }

            Text(content)
                .font(.body)
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color(.secondarySystemBackground))
                .cornerRadius(8)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Violations Card
struct ViolationsCard: View {
    let violations: [ViolationType]

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "exclamationmark.triangle.fill")
                    .foregroundColor(.red)
                Text("Violations Detected")
                    .font(.headline)
            }

            ForEach(violations, id: \.self) { violation in
                HStack {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.red)
                    Text(violation.displayName)
                        .font(.subheadline)
                }
            }
        }
        .padding()
        .background(Color.red.opacity(0.05))
        .cornerRadius(12)
    }
}

// MARK: - Hash Verification Card
struct HashVerificationCard: View {
    let hash: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: "number.circle.fill")
                    .foregroundColor(.purple)
                Text("SHA-256 Integrity Hash")
                    .font(.headline)

                Spacer()

                Button(action: copyHash) {
                    Image(systemName: "doc.on.doc")
                        .foregroundColor(.avrtPrimary)
                }
            }

            Text(hash)
                .font(.system(.caption, design: .monospaced))
                .foregroundColor(.secondary)
                .lineLimit(2)
                .truncationMode(.middle)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }

    private func copyHash() {
        UIPasteboard.general.string = hash
    }
}

// MARK: - Metadata Card
struct MetadataCard: View {
    let result: ValidationResult

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: "info.circle.fill")
                    .foregroundColor(.gray)
                Text("Metadata")
                    .font(.headline)
            }

            VStack(spacing: 4) {
                MetadataRow(label: "Request ID", value: result.requestId)
                MetadataRow(label: "Processing Time", value: "\(String(format: "%.2f", result.processingTimeMs))ms")
                MetadataRow(label: "Timestamp", value: result.timestamp.formatted())
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

struct MetadataRow: View {
    let label: String
    let value: String

    var body: some View {
        HStack {
            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
                .font(.caption)
                .foregroundColor(.primary)
        }
    }
}

// MARK: - Preview
#Preview {
    ValidationResultView(result: ValidationResult.sample)
}
