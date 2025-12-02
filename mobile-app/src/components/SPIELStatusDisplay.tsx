/**
 * SPIEL Status Display Component
 * Visualizes SPIEL™ Framework scores
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface SPIELScore {
  safety: number;
  personalization: number;
  integrity: number;
  ethics: number;
  logic: number;
  composite: number;
}

interface SPIELStatusDisplayProps {
  score: SPIELScore;
}

export default function SPIELStatusDisplay({ score }: SPIELStatusDisplayProps) {
  const getScoreColor = (value: number): string => {
    if (value >= 90) return '#34C759'; // Green
    if (value >= 80) return '#00D9FF'; // Blue
    if (value >= 70) return '#FF9500'; // Orange
    return '#FF3B30'; // Red
  };

  const getScoreStatus = (value: number): string => {
    if (value >= 90) return '✅';
    if (value >= 80) return '⚠️';
    return '🚫';
  };

  const renderScoreBar = (label: string, value: number) => (
    <View style={styles.scoreRow} key={label}>
      <View style={styles.scoreLabel}>
        <Text style={styles.scoreEmoji}>{getScoreStatus(value)}</Text>
        <Text style={styles.scoreLabelText}>{label}</Text>
      </View>
      <View style={styles.scoreBarContainer}>
        <View
          style={[
            styles.scoreBarFill,
            {
              width: `${value}%`,
              backgroundColor: getScoreColor(value)
            }
          ]}
        />
      </View>
      <Text style={[styles.scoreValue, { color: getScoreColor(value) }]}>
        {value.toFixed(1)}
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Component Scores */}
      {renderScoreBar('Safety', score.safety)}
      {renderScoreBar('Personalization', score.personalization)}
      {renderScoreBar('Integrity', score.integrity)}
      {renderScoreBar('Ethics', score.ethics)}
      {renderScoreBar('Logic', score.logic)}

      {/* Composite Score */}
      <View style={styles.compositeContainer}>
        <View style={styles.compositeLine} />
        <View style={styles.compositeRow}>
          <Text style={styles.compositeLabel}>Composite Score</Text>
          <Text
            style={[
              styles.compositeValue,
              { color: getScoreColor(score.composite) }
            ]}
          >
            {score.composite.toFixed(1)} / 100
          </Text>
        </View>
        <View style={styles.compositeBar}>
          <View
            style={[
              styles.compositeBarFill,
              {
                width: `${score.composite}%`,
                backgroundColor: getScoreColor(score.composite)
              }
            ]}
          />
        </View>
      </View>

      {/* Legend */}
      <View style={styles.legend}>
        <Text style={styles.legendTitle}>SPIEL™ Framework</Text>
        <Text style={styles.legendText}>
          Safety · Personalization · Integrity · Ethics · Logic
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  scoreRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  scoreLabel: {
    flexDirection: 'row',
    alignItems: 'center',
    width: 140,
  },
  scoreEmoji: {
    fontSize: 16,
    marginRight: 6,
  },
  scoreLabelText: {
    fontSize: 13,
    color: '#FFFFFF',
    fontWeight: '500',
  },
  scoreBarContainer: {
    flex: 1,
    height: 8,
    backgroundColor: '#2A2A2A',
    borderRadius: 4,
    overflow: 'hidden',
    marginHorizontal: 8,
  },
  scoreBarFill: {
    height: '100%',
    borderRadius: 4,
  },
  scoreValue: {
    fontSize: 14,
    fontWeight: '700',
    width: 40,
    textAlign: 'right',
  },
  compositeContainer: {
    marginTop: 16,
    paddingTop: 16,
  },
  compositeLine: {
    height: 1,
    backgroundColor: '#333333',
    marginBottom: 12,
  },
  compositeRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  compositeLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: '#00D9FF',
  },
  compositeValue: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  compositeBar: {
    height: 12,
    backgroundColor: '#2A2A2A',
    borderRadius: 6,
    overflow: 'hidden',
  },
  compositeBarFill: {
    height: '100%',
    borderRadius: 6,
  },
  legend: {
    marginTop: 16,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#333333',
  },
  legendTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#00D9FF',
    marginBottom: 4,
  },
  legendText: {
    fontSize: 11,
    color: '#FFFFFF',
    opacity: 0.6,
  },
});
