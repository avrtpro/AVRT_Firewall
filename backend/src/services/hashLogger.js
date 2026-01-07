/**
 * AVRT™ SHA-256 Hash Logger
 * Cryptographic verification and audit trail
 *
 * © 2025 Jason I. Proper / BGBH Threads LLC
 * OriginStamp ready
 */

import crypto from 'crypto';
import fs from 'fs/promises';
import path from 'path';

export class HashLogger {
  constructor(config = {}) {
    this.logDir = config.logDir || './logs';
    this.hashFile = config.hashFile || 'interaction_hashes.json';
    this.enableOriginStamp = config.enableOriginStamp || false;
    this.initialized = false;
  }

  /**
   * Initialize logger (create log directory)
   */
  async initialize() {
    try {
      await fs.mkdir(this.logDir, { recursive: true });
      this.initialized = true;
    } catch (error) {
      console.error('Failed to initialize hash logger:', error);
      throw error;
    }
  }

  /**
   * Generate SHA-256 hash of interaction
   * @param {object} interaction - Interaction data
   * @returns {string} SHA-256 hash
   */
  generateHash(interaction) {
    const data = JSON.stringify({
      timestamp: interaction.timestamp,
      input: interaction.input,
      output: interaction.output,
      spielScore: interaction.spielScore,
      thtValidation: interaction.thtValidation,
      status: interaction.status
    });

    return crypto
      .createHash('sha256')
      .update(data)
      .digest('hex');
  }

  /**
   * Log interaction with hash
   * @param {object} interaction - Full interaction data
   * @returns {object} Hash entry
   */
  async logInteraction(interaction) {
    if (!this.initialized) {
      await this.initialize();
    }

    const hash = this.generateHash(interaction);
    const timestamp = new Date().toISOString();

    const hashEntry = {
      hash,
      timestamp,
      interactionId: interaction.id || this._generateId(),
      userId: interaction.userId || 'anonymous',
      status: interaction.status,
      spielComposite: interaction.spielScore?.composite || 0,
      thtCompliant: interaction.thtValidation?.isCompliant || false,
      blockchainReady: this.enableOriginStamp
    };

    // Append to hash log file
    await this._appendHashLog(hashEntry);

    // Also save full interaction to separate file (optional)
    if (interaction.saveFullLog) {
      await this._saveFullInteraction(interaction, hash);
    }

    return hashEntry;
  }

  /**
   * Append hash entry to log file
   * @private
   */
  async _appendHashLog(hashEntry) {
    const filePath = path.join(this.logDir, this.hashFile);

    try {
      // Read existing logs
      let logs = [];
      try {
        const content = await fs.readFile(filePath, 'utf-8');
        logs = JSON.parse(content);
      } catch (error) {
        // File doesn't exist yet, start fresh
        logs = [];
      }

      // Append new entry
      logs.push(hashEntry);

      // Write back to file
      await fs.writeFile(filePath, JSON.stringify(logs, null, 2), 'utf-8');
    } catch (error) {
      console.error('Failed to append hash log:', error);
      throw error;
    }
  }

  /**
   * Save full interaction data
   * @private
   */
  async _saveFullInteraction(interaction, hash) {
    const fileName = `interaction_${hash.substring(0, 16)}.json`;
    const filePath = path.join(this.logDir, fileName);

    try {
      await fs.writeFile(
        filePath,
        JSON.stringify({
          ...interaction,
          hash,
          savedAt: new Date().toISOString()
        }, null, 2),
        'utf-8'
      );
    } catch (error) {
      console.error('Failed to save full interaction:', error);
    }
  }

  /**
   * Get recent hash logs
   * @param {number} limit - Number of recent logs to retrieve
   * @returns {array} Recent hash entries
   */
  async getRecentLogs(limit = 100) {
    if (!this.initialized) {
      await this.initialize();
    }

    const filePath = path.join(this.logDir, this.hashFile);

    try {
      const content = await fs.readFile(filePath, 'utf-8');
      const logs = JSON.parse(content);
      return logs.slice(-limit);
    } catch (error) {
      // File doesn't exist or is empty
      return [];
    }
  }

  /**
   * Verify hash integrity
   * @param {object} interaction - Interaction to verify
   * @param {string} expectedHash - Expected hash value
   * @returns {boolean} True if hash matches
   */
  verifyHash(interaction, expectedHash) {
    const actualHash = this.generateHash(interaction);
    return actualHash === expectedHash;
  }

  /**
   * Export logs for OriginStamp
   * @returns {object} OriginStamp-ready data
   */
  async exportForOriginStamp() {
    const logs = await this.getRecentLogs(1000);

    return {
      service: 'AVRT',
      version: '1.0.0',
      patent: 'USPTO #19/236,935',
      exportDate: new Date().toISOString(),
      totalEntries: logs.length,
      hashes: logs.map(log => ({
        hash: log.hash,
        timestamp: log.timestamp,
        interactionId: log.interactionId
      }))
    };
  }

  /**
   * Generate unique interaction ID
   * @private
   */
  _generateId() {
    return `avrt_${Date.now()}_${crypto.randomBytes(8).toString('hex')}`;
  }

  /**
   * Get statistics
   * @returns {object} Hash log statistics
   */
  async getStatistics() {
    const logs = await this.getRecentLogs(10000);

    const totalInteractions = logs.length;
    const blockedCount = logs.filter(log => log.status === 'blocked').length;
    const thtCompliantCount = logs.filter(log => log.thtCompliant).length;

    return {
      totalInteractions,
      blockedCount,
      blockedRate: totalInteractions > 0 ? blockedCount / totalInteractions : 0,
      thtCompliantCount,
      thtComplianceRate: totalInteractions > 0 ? thtCompliantCount / totalInteractions : 0,
      averageSpielScore: logs.reduce((sum, log) => sum + (log.spielComposite || 0), 0) /
        (totalInteractions || 1),
      oldestEntry: logs[0]?.timestamp,
      newestEntry: logs[logs.length - 1]?.timestamp
    };
  }
}
