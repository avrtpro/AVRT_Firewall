//
//  VoiceService.swift
//  AVRT_iOS
//
//  Voice input and speech recognition service
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation
import Speech
import AVFoundation

@MainActor
class VoiceService: ObservableObject {
    static let shared = VoiceService()

    // MARK: - Published Properties
    @Published var isRecording = false
    @Published var transcription = ""
    @Published var audioLevel: Double = 0.0
    @Published var isAuthorized = false
    @Published var errorMessage: String?

    // MARK: - Private Properties
    private var audioEngine: AVAudioEngine?
    private var speechRecognizer: SFSpeechRecognizer?
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private var audioSession: AVAudioSession?

    private let language: String

    // MARK: - Initialization
    private init(language: String = "en-US") {
        self.language = language
        self.speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: language))
    }

    // MARK: - Permissions
    func requestPermissions() {
        // Request speech recognition permission
        SFSpeechRecognizer.requestAuthorization { [weak self] status in
            Task { @MainActor in
                switch status {
                case .authorized:
                    self?.isAuthorized = true
                    self?.requestMicrophonePermission()
                case .denied, .restricted:
                    self?.isAuthorized = false
                    self?.errorMessage = "Speech recognition permission denied"
                case .notDetermined:
                    self?.isAuthorized = false
                @unknown default:
                    self?.isAuthorized = false
                }
            }
        }
    }

    private func requestMicrophonePermission() {
        AVAudioApplication.requestRecordPermission { [weak self] granted in
            Task { @MainActor in
                if !granted {
                    self?.isAuthorized = false
                    self?.errorMessage = "Microphone permission denied"
                }
            }
        }
    }

    // MARK: - Recording
    func startRecording() {
        guard isAuthorized else {
            errorMessage = "Not authorized for speech recognition"
            return
        }

        guard let speechRecognizer = speechRecognizer, speechRecognizer.isAvailable else {
            errorMessage = "Speech recognizer not available"
            return
        }

        // Reset state
        transcription = ""
        errorMessage = nil

        do {
            // Configure audio session
            audioSession = AVAudioSession.sharedInstance()
            try audioSession?.setCategory(.record, mode: .measurement, options: .duckOthers)
            try audioSession?.setActive(true, options: .notifyOthersOnDeactivation)

            // Create audio engine
            audioEngine = AVAudioEngine()

            guard let audioEngine = audioEngine else {
                errorMessage = "Could not create audio engine"
                return
            }

            let inputNode = audioEngine.inputNode

            // Create recognition request
            recognitionRequest = SFSpeechAudioBufferRecognitionRequest()

            guard let recognitionRequest = recognitionRequest else {
                errorMessage = "Could not create recognition request"
                return
            }

            recognitionRequest.shouldReportPartialResults = true
            recognitionRequest.requiresOnDeviceRecognition = false

            // Start recognition task
            recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { [weak self] result, error in
                Task { @MainActor in
                    if let result = result {
                        self?.transcription = result.bestTranscription.formattedString
                    }

                    if let error = error {
                        self?.handleRecognitionError(error)
                    }

                    if result?.isFinal == true {
                        self?.stopRecording()
                    }
                }
            }

            // Configure audio input
            let recordingFormat = inputNode.outputFormat(forBus: 0)

            inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, _ in
                self?.recognitionRequest?.append(buffer)

                // Calculate audio level for visualization
                let level = self?.calculateAudioLevel(buffer: buffer) ?? 0
                Task { @MainActor in
                    self?.audioLevel = level
                }
            }

            // Start audio engine
            audioEngine.prepare()
            try audioEngine.start()

            isRecording = true

            print("AVRT Voice: Recording started")

        } catch {
            errorMessage = "Recording failed: \(error.localizedDescription)"
            print("AVRT Voice Error: \(error)")
        }
    }

    func stopRecording() {
        guard isRecording else { return }

        audioEngine?.stop()
        audioEngine?.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        recognitionTask?.cancel()

        recognitionRequest = nil
        recognitionTask = nil
        audioEngine = nil

        isRecording = false
        audioLevel = 0.0

        // Deactivate audio session
        try? audioSession?.setActive(false)

        print("AVRT Voice: Recording stopped")
    }

    // MARK: - Private Helpers
    private func calculateAudioLevel(buffer: AVAudioPCMBuffer) -> Double {
        guard let channelData = buffer.floatChannelData?[0] else { return 0 }

        let frameLength = Int(buffer.frameLength)
        var sum: Float = 0

        for i in 0..<frameLength {
            sum += abs(channelData[i])
        }

        let average = sum / Float(frameLength)
        return Double(min(1.0, average * 10)) // Normalize to 0-1
    }

    private func handleRecognitionError(_ error: Error) {
        let nsError = error as NSError

        if nsError.domain == "kAFAssistantErrorDomain" {
            switch nsError.code {
            case 1110: // No speech detected
                errorMessage = nil // Not really an error
            default:
                errorMessage = "Recognition error: \(error.localizedDescription)"
            }
        } else {
            errorMessage = "Recognition error: \(error.localizedDescription)"
        }

        if isRecording {
            stopRecording()
        }
    }
}

// MARK: - Text-to-Speech Support
extension VoiceService {
    func speak(_ text: String, rate: Float = 0.5) {
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = rate
        utterance.voice = AVSpeechSynthesisVoice(language: language)

        let synthesizer = AVSpeechSynthesizer()
        synthesizer.speak(utterance)
    }
}
