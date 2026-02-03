//
//  AVRT_iOSApp.swift
//  AVRT_iOS
//
//  AVRT - Advanced Voice Reasoning Technology
//  Voice-First Ethical Middleware Firewall for AI
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//  Patent: USPTO 19/236,935
//  Trademarks: AVRT, SPIEL, THT, AWOGO, BeGoodBeHumble
//

import SwiftUI

@main
struct AVRT_iOSApp: App {
    @StateObject private var avrtService = AVRTService.shared
    @StateObject private var voiceService = VoiceService.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(avrtService)
                .environmentObject(voiceService)
                .onAppear {
                    setupAVRT()
                }
        }
    }

    private func setupAVRT() {
        // Initialize AVRT with license key
        if let licenseKey = Bundle.main.object(forInfoDictionaryKey: "AVRT_LICENSE_KEY") as? String {
            avrtService.configure(licenseKey: licenseKey)
        }

        // Request speech recognition permissions
        voiceService.requestPermissions()

        print("""
        ═══════════════════════════════════════════════════════════════
           AVRT iOS SDK Initialized
           Advanced Voice Reasoning Technology

           SPIEL Framework: Active
           THT Protocol: Active
           Voice-First Mode: Enabled
        ═══════════════════════════════════════════════════════════════
        """)
    }
}
