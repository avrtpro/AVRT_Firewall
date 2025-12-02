/**
 * THT Indicator Component
 * Displays THT™ Protocol validation status
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface THTStatus {
  truth_verified: boolean;
  honesty_verified: boolean;
  transparency_verified: boolean;
  confidence_score: number;
  issues?: string[];
}

interface THTIndicatorProps {
  status: THTStatus;
}

export default function THTIndicator({ status }: THTIndicatorProps) {
  const isCompliant = status.truth_verified &&
                      status.honesty_verified &&
                      status.transparency_verified &&
                      status.confidence_score >= 0.8;

  const renderCheck = (label: string, verified: boolean) => (
    <View style={styles.checkRow} key={label}>
      <View style={[
        styles.checkIcon,
        verified ? styles.checkIconVerified : styles.checkIconFailed
      ]}>
        <Text style={styles.checkIconText}>{verified ? '✓' : '✗'}</Text>
      </View>
      <Text style={styles.checkLabel}>{label}</Text>
      <Text style={[
        styles.checkStatus,
        verified ? styles.checkStatusVerified : styles.checkStatusFailed
      ]}>
        {verified ? 'Verified' : 'Failed'}
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Overall Status Badge */}
      <View style={[
        styles.statusBadge,
        isCompliant ? styles.statusBadgePass : styles.statusBadgeFail
      ]}>
        <Text style={styles.statusBadgeIcon}>
          {isCompliant ? '✅' : '🚫'}
        </Text>
        <View>
          <Text style={styles.statusBadgeTitle}>
            {isCompliant ? 'THT™ Passed' : 'THT™ Failed'}
          </Text>
          <Text style={styles.statusBadgeSubtitle}>
            Confidence: {(status.confidence_score * 100).toFixed(0)}%
          </Text>
        </View>
      </View>

      {/* Individual Checks */}
      <View style={styles.checksContainer}>
        {renderCheck('Truth', status.truth_verified)}
        {renderCheck('Honesty', status.honesty_verified)}
        {renderCheck('Transparency', status.transparency_verified)}
      </View>

      {/* Issues */}
      {status.issues && status.issues.length > 0 && (
        <View style={styles.issuesContainer}>
          <Text style={styles.issuesTitle}>⚠️ Issues Detected:</Text>
          {status.issues.map((issue, index) => (
            <Text key={index} style={styles.issueText}>
              • {issue}
            </Text>
          ))}
        </View>
      )}

      {/* Protocol Info */}
      <View style={styles.infoBox}>
        <Text style={styles.infoTitle}>THT™ Protocol</Text>
        <Text style={styles.infoText}>
          Truth, Honesty, and Transparency validation ensures AI outputs are
          factually accurate, ethically sound, and clearly explainable.
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  statusBadgePass: {
    backgroundColor: '#34C75920',
    borderWidth: 2,
    borderColor: '#34C759',
  },
  statusBadgeFail: {
    backgroundColor: '#FF3B3020',
    borderWidth: 2,
    borderColor: '#FF3B30',
  },
  statusBadgeIcon: {
    fontSize: 32,
    marginRight: 12,
  },
  statusBadgeTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  statusBadgeSubtitle: {
    fontSize: 13,
    color: '#FFFFFF',
    opacity: 0.8,
    marginTop: 2,
  },
  checksContainer: {
    marginBottom: 16,
  },
  checkRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#2A2A2A',
  },
  checkIcon: {
    width: 28,
    height: 28,
    borderRadius: 14,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  checkIconVerified: {
    backgroundColor: '#34C759',
  },
  checkIconFailed: {
    backgroundColor: '#FF3B30',
  },
  checkIconText: {
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  checkLabel: {
    flex: 1,
    fontSize: 15,
    color: '#FFFFFF',
    fontWeight: '500',
  },
  checkStatus: {
    fontSize: 13,
    fontWeight: '600',
  },
  checkStatusVerified: {
    color: '#34C759',
  },
  checkStatusFailed: {
    color: '#FF3B30',
  },
  issuesContainer: {
    backgroundColor: '#FF9500' + '20',
    borderLeftWidth: 3,
    borderLeftColor: '#FF9500',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  issuesTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FF9500',
    marginBottom: 8,
  },
  issueText: {
    fontSize: 13,
    color: '#FFFFFF',
    marginBottom: 4,
    opacity: 0.9,
  },
  infoBox: {
    backgroundColor: '#00D9FF' + '10',
    borderWidth: 1,
    borderColor: '#00D9FF' + '40',
    padding: 12,
    borderRadius: 8,
  },
  infoTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#00D9FF',
    marginBottom: 6,
  },
  infoText: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.7,
    lineHeight: 18,
  },
});
