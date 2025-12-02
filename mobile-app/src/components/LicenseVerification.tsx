/**
 * License Verification Component
 * Displays AVRT licensing and verification information
 */

import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Linking } from 'react-native';
import { AVRTConfig } from '../config';

export default function LicenseVerification() {
  const openURL = (url: string) => {
    Linking.openURL(url).catch(err =>
      console.error('Failed to open URL:', err)
    );
  };

  return (
    <View style={styles.container}>
      {/* License Badge */}
      <View style={styles.badge}>
        <Text style={styles.badgeIcon}>🛡️</Text>
        <View style={styles.badgeContent}>
          <Text style={styles.badgeTitle}>Licensed AVRT™ System</Text>
          <Text style={styles.badgeSubtitle}>
            {AVRTConfig.LICENSE.TYPE}
          </Text>
        </View>
      </View>

      {/* Verification Details */}
      <View style={styles.detailsContainer}>
        {/* GitHub Repository */}
        <TouchableOpacity
          style={styles.detailRow}
          onPress={() => openURL(AVRTConfig.LICENSE.GITHUB_REPO)}
        >
          <Text style={styles.detailLabel}>GitHub Repository</Text>
          <Text style={styles.detailLink}>View Source →</Text>
        </TouchableOpacity>

        {/* SHA-256 Hash */}
        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>SHA-256 Hash</Text>
          <Text style={styles.detailValue} numberOfLines={1} ellipsizeMode="middle">
            {AVRTConfig.LICENSE.SHA256_HASH}
          </Text>
        </View>

        {/* Patent */}
        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>Patent</Text>
          <Text style={styles.detailValue}>{AVRTConfig.LICENSE.PATENT}</Text>
        </View>

        {/* Stripe Enterprise */}
        <TouchableOpacity
          style={styles.detailRow}
          onPress={() => openURL(AVRTConfig.LICENSE.STRIPE_ENTERPRISE)}
        >
          <Text style={styles.detailLabel}>Enterprise License</Text>
          <Text style={styles.detailLink}>Purchase →</Text>
        </TouchableOpacity>
      </View>

      {/* Copyright */}
      <View style={styles.copyrightContainer}>
        <Text style={styles.copyrightText}>
          {AVRTConfig.LICENSE.COPYRIGHT}
        </Text>
        <Text style={styles.copyrightSubtext}>
          All Rights Reserved
        </Text>
      </View>

      {/* Verification Badge */}
      <View style={styles.verificationBadge}>
        <View style={styles.verificationCheck}>
          <Text style={styles.verificationCheckText}>✓</Text>
        </View>
        <View>
          <Text style={styles.verificationText}>Verified Authentic</Text>
          <Text style={styles.verificationSubtext}>
            AVRT™ Firewall v5.1.0
          </Text>
        </View>
      </View>

      {/* Legal */}
      <View style={styles.legalContainer}>
        <Text style={styles.legalTitle}>License Terms</Text>
        <Text style={styles.legalText}>
          • Non-commercial use permitted under CC BY-NC 4.0
        </Text>
        <Text style={styles.legalText}>
          • Commercial use requires Stripe Enterprise license
        </Text>
        <Text style={styles.legalText}>
          • Attribution required for all use cases
        </Text>
        <Text style={styles.legalText}>
          • Legal representation: Falcon Rappaport & Berkman LLP
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#00D9FF' + '20',
    borderWidth: 2,
    borderColor: '#00D9FF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  badgeIcon: {
    fontSize: 36,
    marginRight: 12,
  },
  badgeContent: {
    flex: 1,
  },
  badgeTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#00D9FF',
  },
  badgeSubtitle: {
    fontSize: 13,
    color: '#FFFFFF',
    opacity: 0.8,
    marginTop: 2,
  },
  detailsContainer: {
    marginBottom: 16,
  },
  detailRow: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#2A2A2A',
  },
  detailLabel: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.6,
    marginBottom: 4,
  },
  detailValue: {
    fontSize: 13,
    color: '#FFFFFF',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  detailLink: {
    fontSize: 14,
    color: '#00D9FF',
    fontWeight: '600',
  },
  copyrightContainer: {
    alignItems: 'center',
    paddingVertical: 16,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: '#2A2A2A',
    marginBottom: 16,
  },
  copyrightText: {
    fontSize: 13,
    color: '#FFFFFF',
    fontWeight: '600',
  },
  copyrightSubtext: {
    fontSize: 11,
    color: '#FFFFFF',
    opacity: 0.5,
    marginTop: 4,
  },
  verificationBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#34C759' + '20',
    borderWidth: 1,
    borderColor: '#34C759',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  verificationCheck: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#34C759',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  verificationCheckText: {
    fontSize: 20,
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  verificationText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#34C759',
  },
  verificationSubtext: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.7,
    marginTop: 2,
  },
  legalContainer: {
    backgroundColor: '#2A2A2A',
    borderRadius: 8,
    padding: 12,
  },
  legalTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  legalText: {
    fontSize: 11,
    color: '#FFFFFF',
    opacity: 0.6,
    marginBottom: 4,
    lineHeight: 16,
  },
});
