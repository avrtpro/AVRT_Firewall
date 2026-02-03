//
//  HashService.swift
//  AVRT_iOS
//
//  SHA-256 hashing service for integrity verification
//
//  (c) 2025 Jason I. Proper, BGBH Threads LLC
//

import Foundation
import CryptoKit

struct HashService {
    /// Generate SHA-256 hash of a string
    /// - Parameter input: String to hash
    /// - Returns: Hexadecimal string representation of the hash
    static func sha256(_ input: String) -> String {
        let data = Data(input.utf8)
        let hash = SHA256.hash(data: data)
        return hash.map { String(format: "%02x", $0) }.joined()
    }

    /// Generate SHA-256 hash of data
    /// - Parameter data: Data to hash
    /// - Returns: Hexadecimal string representation of the hash
    static func sha256(_ data: Data) -> String {
        let hash = SHA256.hash(data: data)
        return hash.map { String(format: "%02x", $0) }.joined()
    }

    /// Verify a hash matches the expected value
    /// - Parameters:
    ///   - input: Original string
    ///   - expectedHash: Expected hash value
    /// - Returns: True if hashes match
    static func verify(_ input: String, expectedHash: String) -> Bool {
        let computedHash = sha256(input)
        return computedHash.lowercased() == expectedHash.lowercased()
    }

    /// Generate integrity hash for validation result
    /// - Parameters:
    ///   - input: User input
    ///   - output: AI output
    ///   - timestamp: Timestamp
    /// - Returns: Integrity hash
    static func generateIntegrityHash(input: String, output: String, timestamp: Date = Date()) -> String {
        let combined = "\(input)|\(output)|\(timestamp.timeIntervalSince1970)"
        return sha256(combined)
    }

    /// Generate HMAC-SHA256 for authenticated hashing
    /// - Parameters:
    ///   - message: Message to hash
    ///   - key: Secret key
    /// - Returns: HMAC hash string
    static func hmacSHA256(message: String, key: String) -> String {
        let keyData = SymmetricKey(data: Data(key.utf8))
        let messageData = Data(message.utf8)

        let hmac = HMAC<SHA256>.authenticationCode(for: messageData, using: keyData)
        return Data(hmac).map { String(format: "%02x", $0) }.joined()
    }
}

// MARK: - Audit Trail Hashing
extension HashService {
    /// Generate hash chain for audit trail
    /// - Parameters:
    ///   - entries: Array of audit entries
    /// - Returns: Chain hash representing the entire audit trail
    static func generateAuditChainHash(entries: [AuditEntry]) -> String {
        var chainHash = "genesis"

        for entry in entries {
            let entryData = """
            \(entry.requestId)|\(entry.inputText)|\(entry.outputText)|\(entry.timestamp.timeIntervalSince1970)
            """
            let entryHash = sha256(entryData)
            chainHash = sha256("\(chainHash)|\(entryHash)")
        }

        return chainHash
    }

    /// Verify audit trail integrity
    /// - Parameters:
    ///   - entries: Audit entries to verify
    ///   - expectedChainHash: Expected chain hash
    /// - Returns: True if chain is valid
    static func verifyAuditChain(entries: [AuditEntry], expectedChainHash: String) -> Bool {
        let computedHash = generateAuditChainHash(entries: entries)
        return computedHash == expectedChainHash
    }
}
