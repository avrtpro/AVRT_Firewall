/**
 * AVRT™ SPIEL™ Scoring Engine
 * Safety, Personalization, Integrity, Ethics, Logic
 *
 * © 2025 Jason I. Proper / BGBH Threads LLC
 * Patent: USPTO #19/236,935
 */

export class SPIELScorer {
  constructor(config = {}) {
    this.thresholds = {
      safety: config.safetyThreshold || 85.0,
      personalization: config.personalizationThreshold || 75.0,
      integrity: config.integrityThreshold || 80.0,
      ethics: config.ethicsThreshold || 90.0,
      logic: config.logicThreshold || 80.0,
      composite: config.compositeThreshold || 85.0
    };

    // Harmful content patterns
    this.harmfulPatterns = [
      /\b(harm|hurt|attack|kill|destroy|murder|violence)\b/gi,
      /\b(hate|abuse|exploit|manipulate|deceive)\b/gi,
      /\b(dangerous|threat|weapon|explosive)\b/gi
    ];

    // Dishonesty markers
    this.dishonestyPatterns = [
      /\b(just trust me|believe me|i guarantee)\b/gi,
      /\b(secret|don't tell|keep this hidden)\b/gi,
      /\b(you can trust me|between us)\b/gi
    ];

    // Unethical patterns
    this.unethicalPatterns = [
      /\b(cheat|lie|deceive|scam|fraud)\b/gi,
      /\b(manipulate|exploit|abuse|coerce)\b/gi
    ];

    // Personalization markers
    this.personalizationMarkers = [
      /\b(you|your|I can help|let me assist)\b/gi,
      /\b(for you|your needs|personalized)\b/gi
    ];

    // Logical coherence markers
    this.logicalMarkers = [
      /\b(because|therefore|thus|hence|consequently)\b/gi,
      /\b(this means|as a result|due to)\b/gi
    ];
  }

  /**
   * Analyze text using SPIEL™ framework
   * @param {string} text - Text to analyze
   * @param {object} context - Optional context
   * @returns {object} SPIEL scores and composite
   */
  analyze(text, context = {}) {
    const safety = this._analyzeSafety(text);
    const personalization = this._analyzePersonalization(text, context);
    const integrity = this._analyzeIntegrity(text);
    const ethics = this._analyzeEthics(text);
    const logic = this._analyzeLogic(text);

    const composite = (safety + personalization + integrity + ethics + logic) / 5.0;

    const scores = {
      safety,
      personalization,
      integrity,
      ethics,
      logic,
      composite,
      timestamp: new Date().toISOString()
    };

    const isPassing = this._isPassing(scores);

    return {
      scores,
      isPassing,
      violations: this._identifyViolations(scores),
      details: this._generateDetails(scores)
    };
  }

  /**
   * Analyze Safety dimension
   * @private
   */
  _analyzeSafety(text) {
    let score = 100.0;
    const textLower = text.toLowerCase();

    // Check harmful patterns
    for (const pattern of this.harmfulPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score -= matches.length * 10.0;
      }
    }

    // Check for explicit violence
    if (textLower.includes('violent') || textLower.includes('kill')) {
      score -= 20.0;
    }

    return Math.max(0.0, Math.min(100.0, score));
  }

  /**
   * Analyze Personalization dimension
   * @private
   */
  _analyzePersonalization(text, context) {
    let score = 75.0; // Base score

    // Check for personalization markers
    for (const pattern of this.personalizationMarkers) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 3.0;
      }
    }

    // Bonus for context awareness
    if (context.userName || context.preferences) {
      score += 10.0;
    }

    return Math.min(100.0, score);
  }

  /**
   * Analyze Integrity dimension
   * @private
   */
  _analyzeIntegrity(text) {
    let score = 90.0; // Base score

    // Check for dishonesty patterns
    for (const pattern of this.dishonestyPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score -= matches.length * 15.0;
      }
    }

    // Check for weasel words
    const weaselWords = ['maybe', 'probably', 'might', 'could possibly'];
    const weaselCount = weaselWords.filter(word =>
      text.toLowerCase().includes(word)
    ).length;

    if (weaselCount > 3) {
      score -= 10.0;
    }

    return Math.max(0.0, score);
  }

  /**
   * Analyze Ethics dimension
   * @private
   */
  _analyzeEthics(text) {
    let score = 95.0; // Base score

    // Check for unethical patterns
    for (const pattern of this.unethicalPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score -= matches.length * 20.0;
      }
    }

    // Check for bias indicators
    const biasPatterns = [
      /\b(always wrong|never right|all of them)\b/gi,
      /\b(everyone knows|obviously|clearly)\b/gi
    ];

    for (const pattern of biasPatterns) {
      if (pattern.test(text)) {
        score -= 5.0;
      }
    }

    return Math.max(0.0, score);
  }

  /**
   * Analyze Logic dimension
   * @private
   */
  _analyzeLogic(text) {
    let score = 85.0; // Base score

    // Check for logical coherence markers
    for (const pattern of this.logicalMarkers) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 3.0;
      }
    }

    // Penalize very short responses (likely incomplete)
    if (text.trim().length < 10) {
      score -= 20.0;
    }

    // Check for contradictions (simplified)
    const contradictionMarkers = ['but', 'however', 'although', 'despite'];
    const contradictions = contradictionMarkers.filter(marker =>
      text.toLowerCase().includes(marker)
    ).length;

    // Contradictions aren't bad, but too many suggest confusion
    if (contradictions > 5) {
      score -= 10.0;
    }

    return Math.max(0.0, Math.min(100.0, score));
  }

  /**
   * Check if scores pass all thresholds
   * @private
   */
  _isPassing(scores) {
    return (
      scores.safety >= this.thresholds.safety &&
      scores.integrity >= this.thresholds.integrity &&
      scores.ethics >= this.thresholds.ethics &&
      scores.composite >= this.thresholds.composite
    );
  }

  /**
   * Identify specific violations
   * @private
   */
  _identifyViolations(scores) {
    const violations = [];

    if (scores.safety < this.thresholds.safety) {
      violations.push({
        type: 'SAFETY',
        score: scores.safety,
        threshold: this.thresholds.safety,
        severity: 'high'
      });
    }

    if (scores.integrity < this.thresholds.integrity) {
      violations.push({
        type: 'INTEGRITY',
        score: scores.integrity,
        threshold: this.thresholds.integrity,
        severity: 'medium'
      });
    }

    if (scores.ethics < this.thresholds.ethics) {
      violations.push({
        type: 'ETHICS',
        score: scores.ethics,
        threshold: this.thresholds.ethics,
        severity: 'high'
      });
    }

    if (scores.logic < this.thresholds.logic) {
      violations.push({
        type: 'LOGIC',
        score: scores.logic,
        threshold: this.thresholds.logic,
        severity: 'low'
      });
    }

    return violations;
  }

  /**
   * Generate human-readable details
   * @private
   */
  _generateDetails(scores) {
    return {
      safety: this._getScoreLabel(scores.safety),
      personalization: this._getScoreLabel(scores.personalization),
      integrity: this._getScoreLabel(scores.integrity),
      ethics: this._getScoreLabel(scores.ethics),
      logic: this._getScoreLabel(scores.logic),
      composite: this._getScoreLabel(scores.composite)
    };
  }

  /**
   * Get label for score
   * @private
   */
  _getScoreLabel(score) {
    if (score >= 90) return 'Excellent';
    if (score >= 80) return 'Good';
    if (score >= 70) return 'Fair';
    if (score >= 60) return 'Poor';
    return 'Critical';
  }
}
