/**
 * AVRT™ THT™ Validation Engine
 * Truth, Honesty, Transparency
 *
 * © 2025 Jason I. Proper / BGBH Threads LLC
 * Patent: USPTO #19/236,935
 */

export class THTValidator {
  constructor(config = {}) {
    this.enableTruth = config.enableTruth !== false;
    this.enableHonesty = config.enableHonesty !== false;
    this.enableTransparency = config.enableTransparency !== false;
    this.confidenceThreshold = config.confidenceThreshold || 0.8;

    // Truth verification patterns
    this.falsehoodPatterns = [
      /\b(definitely|absolutely certain|100% guarantee)\b/gi,
      /\b(always true|never wrong|impossible to)\b/gi,
      /\b(everyone agrees|nobody disagrees)\b/gi
    ];

    // Honesty check patterns
    this.dishonestyPatterns = [
      /\b(just between us|don't tell|keep this secret)\b/gi,
      /\b(you can trust me|believe me|I promise)\b/gi,
      /\b(won't tell anyone|our little secret)\b/gi
    ];

    // Transparency markers
    this.transparencyMarkers = [
      /\b(because|the reason|this is based on)\b/gi,
      /\b(according to|evidence suggests|research shows)\b/gi,
      /\b(in my opinion|I believe|it seems)\b/gi,
      /\b(source:|reference:|based on)\b/gi
    ];

    // Claim patterns
    this.claimPatterns = [
      /\b(is|are|will|should|must)\b/gi
    ];
  }

  /**
   * Validate text using THT™ protocol
   * @param {string} text - Text to validate
   * @param {object} context - Optional context
   * @returns {object} THT validation results
   */
  validate(text, context = {}) {
    const truthVerified = this.enableTruth ? this._verifyTruth(text) : true;
    const honestyVerified = this.enableHonesty ? this._verifyHonesty(text) : true;
    const transparencyVerified = this.enableTransparency ?
      this._verifyTransparency(text) : true;

    const issues = [];

    if (!truthVerified) {
      issues.push('Truth verification failed: Contains absolute statements without evidence');
    }

    if (!honestyVerified) {
      issues.push('Honesty check failed: Contains manipulative or secretive language');
    }

    if (!transparencyVerified) {
      issues.push('Transparency check failed: Makes claims without proper attribution');
    }

    // Calculate confidence score
    const passedChecks = [truthVerified, honestyVerified, transparencyVerified]
      .filter(Boolean).length;
    const totalChecks = [this.enableTruth, this.enableHonesty, this.enableTransparency]
      .filter(Boolean).length;

    const confidenceScore = totalChecks > 0 ? passedChecks / totalChecks : 1.0;

    const isCompliant = (
      truthVerified &&
      honestyVerified &&
      transparencyVerified &&
      confidenceScore >= this.confidenceThreshold
    );

    return {
      truthVerified,
      honestyVerified,
      transparencyVerified,
      confidenceScore,
      isCompliant,
      issues,
      timestamp: new Date().toISOString(),
      details: this._generateDetails({
        truthVerified,
        honestyVerified,
        transparencyVerified,
        confidenceScore
      })
    };
  }

  /**
   * Verify Truth (factual accuracy checks)
   * @private
   */
  _verifyTruth(text) {
    // Check for obvious falsehoods or absolute statements without evidence
    for (const pattern of this.falsehoodPatterns) {
      if (pattern.test(text)) {
        return false;
      }
    }

    return true;
  }

  /**
   * Verify Honesty (transparent intent)
   * @private
   */
  _verifyHonesty(text) {
    // Check for dishonest or manipulative patterns
    for (const pattern of this.dishonestyPatterns) {
      if (pattern.test(text)) {
        return false;
      }
    }

    return true;
  }

  /**
   * Verify Transparency (explainable reasoning)
   * @private
   */
  _verifyTransparency(text) {
    const textLower = text.toLowerCase();

    // Check if text makes claims
    const hasClaims = this.claimPatterns.some(pattern => pattern.test(text));

    if (!hasClaims) {
      // No claims made, transparency not required
      return true;
    }

    // If making claims, should have transparency markers
    const hasTransparency = this.transparencyMarkers.some(pattern =>
      pattern.test(text)
    );

    // Short responses (< 50 chars) get a pass
    if (text.length < 50) {
      return true;
    }

    return hasTransparency;
  }

  /**
   * Generate human-readable details
   * @private
   */
  _generateDetails(validation) {
    return {
      truth: validation.truthVerified ? 'Verified' : 'Failed',
      honesty: validation.honestyVerified ? 'Verified' : 'Failed',
      transparency: validation.transparencyVerified ? 'Verified' : 'Failed',
      confidence: `${(validation.confidenceScore * 100).toFixed(1)}%`,
      status: validation.confidenceScore >= this.confidenceThreshold ?
        'Compliant' : 'Non-Compliant'
    };
  }

  /**
   * Generate safe alternative response
   * @param {string} originalText - Original text that failed
   * @param {array} issues - Array of issues found
   * @returns {string} Safe alternative
   */
  generateSafeAlternative(originalText, issues) {
    return {
      message: "I need to rephrase that response to meet AVRT™ THT™ standards.",
      suggestion: "How can I provide you with accurate, honest, and transparent information?",
      issues: issues,
      originalLength: originalText.length
    };
  }
}
