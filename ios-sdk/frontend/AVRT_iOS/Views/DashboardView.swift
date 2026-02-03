//
//  DashboardView.swift
//  AVRT_iOS
//
//  Analytics and monitoring dashboard for AVRT
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import SwiftUI
import Charts

struct DashboardView: View {
    @EnvironmentObject var avrtService: AVRTService
    @State private var statistics: AVRTStatistics?
    @State private var recentValidations: [ValidationResult] = []
    @State private var isLoading = true

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Summary Cards
                SummaryCardsRow(statistics: statistics)

                // SPIEL Score Chart
                SPIELChartView(recentValidations: recentValidations)

                // Recent Activity
                RecentActivitySection(validations: recentValidations)

                // System Status
                SystemStatusCard()
            }
            .padding()
        }
        .refreshable {
            await loadData()
        }
        .task {
            await loadData()
        }
    }

    private func loadData() async {
        isLoading = true

        do {
            statistics = try await avrtService.getStatistics()
            recentValidations = try await avrtService.getRecentValidations(limit: 10)
        } catch {
            print("Failed to load dashboard data: \(error)")
        }

        isLoading = false
    }
}

// MARK: - Summary Cards Row
struct SummaryCardsRow: View {
    let statistics: AVRTStatistics?

    var body: some View {
        LazyVGrid(columns: [
            GridItem(.flexible()),
            GridItem(.flexible())
        ], spacing: 16) {
            SummaryCard(
                title: "Total Validations",
                value: "\(statistics?.totalValidations ?? 0)",
                icon: "shield.checkered",
                color: .avrtPrimary
            )

            SummaryCard(
                title: "Blocked",
                value: "\(statistics?.blockedCount ?? 0)",
                icon: "xmark.shield.fill",
                color: .red
            )

            SummaryCard(
                title: "Avg SPIEL",
                value: String(format: "%.1f", statistics?.averageSPIELScore ?? 0),
                icon: "chart.bar.fill",
                color: .green
            )

            SummaryCard(
                title: "THT Rate",
                value: String(format: "%.0f%%", (statistics?.thtComplianceRate ?? 0) * 100),
                icon: "checkmark.seal.fill",
                color: .purple
            )
        }
    }
}

struct SummaryCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(color)
                Spacer()
            }

            Text(value)
                .font(.title)
                .fontWeight(.bold)

            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

// MARK: - SPIEL Chart
struct SPIELChartView: View {
    let recentValidations: [ValidationResult]

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "chart.line.uptrend.xyaxis")
                    .foregroundColor(.avrtPrimary)
                Text("SPIEL Score Trend")
                    .font(.headline)
            }

            if #available(iOS 16.0, *), !recentValidations.isEmpty {
                Chart(recentValidations.indices, id: \.self) { index in
                    let validation = recentValidations[index]
                    if let score = validation.spielScore {
                        LineMark(
                            x: .value("Index", index),
                            y: .value("Score", score.composite)
                        )
                        .foregroundStyle(Color.avrtPrimary)

                        PointMark(
                            x: .value("Index", index),
                            y: .value("Score", score.composite)
                        )
                        .foregroundStyle(Color.avrtPrimary)
                    }
                }
                .frame(height: 150)
                .chartYScale(domain: 0...100)
            } else {
                Text("No data available")
                    .foregroundColor(.secondary)
                    .frame(height: 150)
                    .frame(maxWidth: .infinity)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Recent Activity
struct RecentActivitySection: View {
    let validations: [ValidationResult]

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "clock.fill")
                    .foregroundColor(.avrtPrimary)
                Text("Recent Activity")
                    .font(.headline)
            }

            if validations.isEmpty {
                Text("No recent validations")
                    .foregroundColor(.secondary)
                    .padding()
            } else {
                ForEach(validations.prefix(5), id: \.requestId) { validation in
                    RecentActivityRow(validation: validation)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

struct RecentActivityRow: View {
    let validation: ValidationResult

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: validation.isSafe ? "checkmark.circle.fill" : "xmark.circle.fill")
                .foregroundColor(validation.isSafe ? .green : .red)

            VStack(alignment: .leading, spacing: 2) {
                Text(validation.message.prefix(50) + (validation.message.count > 50 ? "..." : ""))
                    .font(.subheadline)
                    .lineLimit(1)

                Text(validation.timestamp.formatted(date: .abbreviated, time: .shortened))
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }

            Spacer()

            if let score = validation.spielScore {
                Text("\(Int(score.composite))")
                    .font(.caption)
                    .fontWeight(.medium)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(scoreColor(score.composite).opacity(0.2))
                    .foregroundColor(scoreColor(score.composite))
                    .cornerRadius(8)
            }
        }
        .padding(.vertical, 8)
    }

    private func scoreColor(_ score: Double) -> Color {
        if score >= 85 { return .green }
        if score >= 70 { return .orange }
        return .red
    }
}

// MARK: - System Status
struct SystemStatusCard: View {
    @EnvironmentObject var avrtService: AVRTService

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "server.rack")
                    .foregroundColor(.avrtPrimary)
                Text("System Status")
                    .font(.headline)
            }

            VStack(spacing: 8) {
                StatusRow(label: "AVRT Backend", status: avrtService.isConnected)
                StatusRow(label: "SPIEL Engine", status: true)
                StatusRow(label: "THT Protocol", status: true)
                StatusRow(label: "License", status: avrtService.isLicenseValid)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

struct StatusRow: View {
    let label: String
    let status: Bool

    var body: some View {
        HStack {
            Text(label)
                .font(.subheadline)
            Spacer()
            HStack(spacing: 4) {
                Circle()
                    .fill(status ? Color.green : Color.red)
                    .frame(width: 8, height: 8)
                Text(status ? "Online" : "Offline")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}

// MARK: - Preview
#Preview {
    DashboardView()
        .environmentObject(AVRTService.shared)
}
