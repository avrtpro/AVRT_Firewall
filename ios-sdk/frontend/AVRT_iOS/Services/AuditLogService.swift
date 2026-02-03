//
//  AuditLogService.swift
//  AVRT_iOS
//
//  Encrypted audit logging service for compliance
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation
import CryptoKit

class AuditLogService {
    static let shared = AuditLogService()

    private let fileManager = FileManager.default
    private let encoder = JSONEncoder()
    private let decoder = JSONDecoder()

    private var auditEntries: [AuditEntry] = []
    private var encryptionKey: SymmetricKey?

    private var auditLogURL: URL? {
        fileManager.urls(for: .documentDirectory, in: .userDomainMask).first?
            .appendingPathComponent("avrt_audit_log.encrypted")
    }

    // MARK: - Initialization
    private init() {
        encoder.dateEncodingStrategy = .iso8601
        decoder.dateDecodingStrategy = .iso8601
        loadEncryptionKey()
        loadAuditLog()
    }

    // MARK: - Encryption Key Management
    private func loadEncryptionKey() {
        // Try to load from Keychain, or generate new key
        if let keyData = KeychainService.load(key: "AVRT_AUDIT_KEY") {
            encryptionKey = SymmetricKey(data: keyData)
        } else {
            let newKey = SymmetricKey(size: .bits256)
            let keyData = newKey.withUnsafeBytes { Data($0) }
            KeychainService.save(key: "AVRT_AUDIT_KEY", data: keyData)
            encryptionKey = newKey
        }
    }

    // MARK: - Audit Logging
    func log(validation: ValidationResult, input: String, output: String, context: [String: String] = [:], userId: String? = nil) {
        let entry = AuditEntry(
            inputText: input,
            outputText: output,
            validationResult: validation,
            context: context
        )

        auditEntries.append(entry)

        // Keep only last 1000 entries in memory
        if auditEntries.count > 1000 {
            auditEntries = Array(auditEntries.suffix(1000))
        }

        // Persist to encrypted file
        saveAuditLog()

        print("AVRT Audit: Logged entry \(entry.requestId)")
    }

    func getEntries(limit: Int = 100) -> [AuditEntry] {
        return Array(auditEntries.suffix(limit))
    }

    func getEntry(byId id: String) -> AuditEntry? {
        return auditEntries.first { $0.requestId == id }
    }

    func getChainHash() -> String {
        return HashService.generateAuditChainHash(entries: auditEntries)
    }

    func verifyIntegrity() -> Bool {
        // Verify each entry's hash
        for entry in auditEntries {
            let expectedHash = HashService.generateIntegrityHash(
                input: entry.inputText,
                output: entry.outputText,
                timestamp: entry.timestamp
            )

            if entry.validationResult.integrityHash != expectedHash {
                print("AVRT Audit: Integrity check failed for entry \(entry.requestId)")
                return false
            }
        }

        return true
    }

    // MARK: - Persistence
    private func saveAuditLog() {
        guard let url = auditLogURL,
              let key = encryptionKey else { return }

        do {
            let data = try encoder.encode(auditEntries)
            let encryptedData = try encrypt(data: data, using: key)
            try encryptedData.write(to: url)
        } catch {
            print("AVRT Audit: Failed to save audit log: \(error)")
        }
    }

    private func loadAuditLog() {
        guard let url = auditLogURL,
              let key = encryptionKey,
              fileManager.fileExists(atPath: url.path) else { return }

        do {
            let encryptedData = try Data(contentsOf: url)
            let decryptedData = try decrypt(data: encryptedData, using: key)
            auditEntries = try decoder.decode([AuditEntry].self, from: decryptedData)
        } catch {
            print("AVRT Audit: Failed to load audit log: \(error)")
            auditEntries = []
        }
    }

    // MARK: - Encryption
    private func encrypt(data: Data, using key: SymmetricKey) throws -> Data {
        let sealedBox = try AES.GCM.seal(data, using: key)
        guard let combined = sealedBox.combined else {
            throw AuditError.encryptionFailed
        }
        return combined
    }

    private func decrypt(data: Data, using key: SymmetricKey) throws -> Data {
        let sealedBox = try AES.GCM.SealedBox(combined: data)
        return try AES.GCM.open(sealedBox, using: key)
    }

    // MARK: - Export
    func exportAuditLog() -> Data? {
        do {
            return try encoder.encode(auditEntries)
        } catch {
            print("AVRT Audit: Export failed: \(error)")
            return nil
        }
    }

    func clearAuditLog() {
        auditEntries = []
        if let url = auditLogURL {
            try? fileManager.removeItem(at: url)
        }
    }
}

// MARK: - Errors
enum AuditError: Error {
    case encryptionFailed
    case decryptionFailed
    case saveFailed
    case loadFailed
}

// MARK: - Keychain Service
struct KeychainService {
    static func save(key: String, data: Data) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]

        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }

    static func load(key: String) -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        if status == errSecSuccess {
            return result as? Data
        }

        return nil
    }

    static func delete(key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]

        SecItemDelete(query as CFDictionary)
    }
}
