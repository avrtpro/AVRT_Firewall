//
//  ContentView.swift
//  AVRT_iOS
//
//  Main navigation and content view for AVRT iOS App
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var avrtService: AVRTService
    @EnvironmentObject var voiceService: VoiceService

    @State private var selectedTab: Tab = .voice

    enum Tab {
        case voice
        case dashboard
        case settings
    }

    var body: some View {
        NavigationStack {
            TabView(selection: $selectedTab) {
                VoiceInputView()
                    .tabItem {
                        Label("Voice", systemImage: "waveform.circle.fill")
                    }
                    .tag(Tab.voice)

                DashboardView()
                    .tabItem {
                        Label("Dashboard", systemImage: "chart.bar.fill")
                    }
                    .tag(Tab.dashboard)

                SettingsView()
                    .tabItem {
                        Label("Settings", systemImage: "gear")
                    }
                    .tag(Tab.settings)
            }
            .tint(.avrtPrimary)
            .navigationTitle(navigationTitle)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    HStack(spacing: 8) {
                        ConnectionStatusView()
                        SPIELStatusIndicator()
                    }
                }
            }
        }
    }

    private var navigationTitle: String {
        switch selectedTab {
        case .voice:
            return "AVRT Voice"
        case .dashboard:
            return "Dashboard"
        case .settings:
            return "Settings"
        }
    }
}

// MARK: - Connection Status
struct ConnectionStatusView: View {
    @EnvironmentObject var avrtService: AVRTService

    var body: some View {
        Circle()
            .fill(avrtService.isConnected ? Color.green : Color.red)
            .frame(width: 8, height: 8)
            .overlay(
                Circle()
                    .stroke(Color.primary.opacity(0.2), lineWidth: 1)
            )
    }
}

// MARK: - SPIEL Status Indicator
struct SPIELStatusIndicator: View {
    @EnvironmentObject var avrtService: AVRTService

    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: "shield.checkered")
                .foregroundColor(.avrtPrimary)
            Text("SPIEL")
                .font(.caption2)
                .fontWeight(.semibold)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(Color.avrtPrimary.opacity(0.1))
        .cornerRadius(8)
    }
}

// MARK: - Settings View
struct SettingsView: View {
    @EnvironmentObject var avrtService: AVRTService
    @AppStorage("enableTHT") private var enableTHT = true
    @AppStorage("safetyThreshold") private var safetyThreshold = 85.0
    @AppStorage("ethicsThreshold") private var ethicsThreshold = 90.0

    var body: some View {
        Form {
            Section("AVRT Configuration") {
                Toggle("THT Protocol", isOn: $enableTHT)

                VStack(alignment: .leading) {
                    Text("Safety Threshold: \(Int(safetyThreshold))%")
                    Slider(value: $safetyThreshold, in: 50...100, step: 5)
                }

                VStack(alignment: .leading) {
                    Text("Ethics Threshold: \(Int(ethicsThreshold))%")
                    Slider(value: $ethicsThreshold, in: 50...100, step: 5)
                }
            }

            Section("License") {
                HStack {
                    Text("Status")
                    Spacer()
                    Text(avrtService.isLicenseValid ? "Active" : "Inactive")
                        .foregroundColor(avrtService.isLicenseValid ? .green : .red)
                }

                if !avrtService.isLicenseValid {
                    Link("Get License", destination: URL(string: "https://buy.stripe.com/8wMaGE3kV0f61jW6oo")!)
                }
            }

            Section("About") {
                HStack {
                    Text("Version")
                    Spacer()
                    Text("1.0.0")
                        .foregroundColor(.secondary)
                }

                HStack {
                    Text("Patent")
                    Spacer()
                    Text("USPTO 19/236,935")
                        .foregroundColor(.secondary)
                }

                Link("AVRT Website", destination: URL(string: "https://avrt.pro")!)
                Link("Contact Support", destination: URL(string: "mailto:info@avrt.pro")!)
            }

            Section {
                Text("AVRT - Protect the Input Before the Output Can Cause Harm.")
                    .font(.footnote)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .multilineTextAlignment(.center)
            }
        }
    }
}

// MARK: - Previews
#Preview {
    ContentView()
        .environmentObject(AVRTService.shared)
        .environmentObject(VoiceService.shared)
}
