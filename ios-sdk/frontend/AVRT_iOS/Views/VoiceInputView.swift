//
//  VoiceInputView.swift
//  AVRT_iOS
//
//  Voice-first input interface with AVRT validation
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import SwiftUI
import AVFoundation

struct VoiceInputView: View {
    @EnvironmentObject var avrtService: AVRTService
    @EnvironmentObject var voiceService: VoiceService

    @State private var transcribedText = ""
    @State private var validationResult: ValidationResult?
    @State private var isProcessing = false
    @State private var showResult = false
    @State private var animateWave = false

    var body: some View {
        VStack(spacing: 24) {
            // Status Header
            StatusHeader(isRecording: voiceService.isRecording)

            Spacer()

            // Voice Waveform Animation
            VoiceWaveformView(isActive: voiceService.isRecording, amplitude: voiceService.audioLevel)
                .frame(height: 100)

            // Transcription Display
            TranscriptionCard(text: transcribedText, isRecording: voiceService.isRecording)

            Spacer()

            // Record Button
            RecordButton(
                isRecording: voiceService.isRecording,
                isProcessing: isProcessing
            ) {
                toggleRecording()
            }

            // Quick Actions
            QuickActionsRow(onStartMyDay: startMyDay, onClearHistory: clearHistory)
        }
        .padding()
        .sheet(isPresented: $showResult) {
            if let result = validationResult {
                ValidationResultView(result: result)
            }
        }
        .onChange(of: voiceService.transcription) { _, newValue in
            transcribedText = newValue
        }
    }

    private func toggleRecording() {
        if voiceService.isRecording {
            stopRecordingAndValidate()
        } else {
            voiceService.startRecording()
            transcribedText = ""
            validationResult = nil
        }
    }

    private func stopRecordingAndValidate() {
        voiceService.stopRecording()

        guard !transcribedText.isEmpty else { return }

        isProcessing = true

        Task {
            do {
                // Send to AVRT for validation
                let result = try await avrtService.validateInput(
                    input: transcribedText,
                    context: ["source": "voice", "language": "en-US"]
                )

                await MainActor.run {
                    validationResult = result
                    isProcessing = false
                    showResult = true
                }
            } catch {
                await MainActor.run {
                    validationResult = ValidationResult.error(message: error.localizedDescription)
                    isProcessing = false
                    showResult = true
                }
            }
        }
    }

    private func startMyDay() {
        Task {
            isProcessing = true
            do {
                let result = try await avrtService.startMyDay(preferences: [
                    "focus_areas": ["health", "productivity", "gratitude"],
                    "tone": "encouraging"
                ])
                await MainActor.run {
                    validationResult = result
                    isProcessing = false
                    showResult = true
                }
            } catch {
                await MainActor.run {
                    isProcessing = false
                }
            }
        }
    }

    private func clearHistory() {
        transcribedText = ""
        validationResult = nil
    }
}

// MARK: - Status Header
struct StatusHeader: View {
    let isRecording: Bool

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(isRecording ? "Listening..." : "Ready")
                    .font(.headline)

                Text("SPIEL + THT Active")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()

            // AVRT Shield Logo
            Image(systemName: "shield.checkered")
                .font(.title)
                .foregroundColor(.avrtPrimary)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Voice Waveform
struct VoiceWaveformView: View {
    let isActive: Bool
    let amplitude: Double

    @State private var phase: Double = 0

    var body: some View {
        GeometryReader { geometry in
            Canvas { context, size in
                let midY = size.height / 2
                let width = size.width
                let waveAmplitude = isActive ? amplitude * 40 : 10

                var path = Path()
                path.move(to: CGPoint(x: 0, y: midY))

                for x in stride(from: 0, through: width, by: 2) {
                    let relativeX = x / width
                    let sine = sin(relativeX * .pi * 4 + phase)
                    let y = midY + sine * waveAmplitude
                    path.addLine(to: CGPoint(x: x, y: y))
                }

                context.stroke(
                    path,
                    with: .linearGradient(
                        Gradient(colors: [.avrtPrimary, .avrtSecondary]),
                        startPoint: .leading,
                        endPoint: .trailing
                    ),
                    lineWidth: 3
                )
            }
        }
        .onAppear {
            withAnimation(.linear(duration: 1).repeatForever(autoreverses: false)) {
                phase = .pi * 2
            }
        }
    }
}

// MARK: - Transcription Card
struct TranscriptionCard: View {
    let text: String
    let isRecording: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: "text.quote")
                    .foregroundColor(.avrtPrimary)
                Text("Transcription")
                    .font(.subheadline)
                    .fontWeight(.medium)
                Spacer()

                if isRecording {
                    ProgressView()
                        .scaleEffect(0.8)
                }
            }

            if text.isEmpty {
                Text("Tap the microphone to start speaking...")
                    .font(.body)
                    .foregroundColor(.secondary)
                    .italic()
            } else {
                Text(text)
                    .font(.body)
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color(.secondarySystemBackground))
                    .cornerRadius(8)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Record Button
struct RecordButton: View {
    let isRecording: Bool
    let isProcessing: Bool
    let action: () -> Void

    @State private var isPulsing = false

    var body: some View {
        Button(action: action) {
            ZStack {
                // Pulse ring
                if isRecording {
                    Circle()
                        .stroke(Color.red.opacity(0.3), lineWidth: 4)
                        .scaleEffect(isPulsing ? 1.3 : 1.0)
                        .opacity(isPulsing ? 0 : 0.8)
                        .animation(.easeOut(duration: 1).repeatForever(autoreverses: false), value: isPulsing)
                }

                // Main button
                Circle()
                    .fill(isRecording ? Color.red : Color.avrtPrimary)
                    .frame(width: 80, height: 80)
                    .shadow(color: (isRecording ? Color.red : Color.avrtPrimary).opacity(0.4), radius: 10, x: 0, y: 5)

                // Icon
                if isProcessing {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        .scaleEffect(1.2)
                } else {
                    Image(systemName: isRecording ? "stop.fill" : "mic.fill")
                        .font(.title)
                        .foregroundColor(.white)
                }
            }
        }
        .disabled(isProcessing)
        .onChange(of: isRecording) { _, newValue in
            isPulsing = newValue
        }
    }
}

// MARK: - Quick Actions
struct QuickActionsRow: View {
    let onStartMyDay: () -> Void
    let onClearHistory: () -> Void

    var body: some View {
        HStack(spacing: 16) {
            Button(action: onStartMyDay) {
                Label("Start My Day", systemImage: "sun.max.fill")
                    .font(.subheadline)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 10)
                    .background(Color.avrtPrimary.opacity(0.1))
                    .foregroundColor(.avrtPrimary)
                    .cornerRadius(20)
            }

            Button(action: onClearHistory) {
                Label("Clear", systemImage: "trash")
                    .font(.subheadline)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 10)
                    .background(Color(.secondarySystemBackground))
                    .foregroundColor(.secondary)
                    .cornerRadius(20)
            }
        }
    }
}

// MARK: - Preview
#Preview {
    VoiceInputView()
        .environmentObject(AVRTService.shared)
        .environmentObject(VoiceService.shared)
}
