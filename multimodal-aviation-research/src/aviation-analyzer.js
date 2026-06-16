/**
 * Aviation Research Analyzer
 * Provides domain-specific analysis tools for Aviation Management research:
 *   - Airport Resilience Index
 *   - Cargo Terminal Congestion Model
 *   - Passenger Willingness-to-Pay (WTP) behavioral model
 *   - Airline Resilience (Multimodal)
 */

// Weights are illustrative defaults; calibrate against real data.
const RESILIENCE_WEIGHTS = Object.freeze({
  operationalRecovery: 0.30,
  networkRedundancy:   0.25,
  resourceAvailability: 0.20,
  passengerImpact:     0.15,
  financialAbsorption: 0.10,
});

const CONGESTION_WEIGHTS = Object.freeze({
  visualDensityScore:  0.35,
  cargoThroughput:     0.25,
  uldMovementRate:     0.20,
  truckArrivalRate:    0.20,
});

/**
 * Compute a 0–100 Airport Resilience Index from multimodal inputs.
 * @param {object} indicators - keyed by RESILIENCE_WEIGHTS fields, values 0–100
 */
function computeAirportResilienceIndex(indicators) {
  _validateScores(indicators, Object.keys(RESILIENCE_WEIGHTS));
  const score = Object.entries(RESILIENCE_WEIGHTS).reduce((sum, [key, weight]) => {
    return sum + (indicators[key] ?? 0) * weight;
  }, 0);
  return { index: Math.round(score * 10) / 10, grade: _grade(score), weights: RESILIENCE_WEIGHTS };
}

/**
 * Predict cargo terminal congestion (0–100) from multimodal sensor data.
 * @param {object} inputs - visual features + operational KPIs
 */
function predictCargoCongestion(inputs) {
  _validateScores(inputs, Object.keys(CONGESTION_WEIGHTS));
  const score = Object.entries(CONGESTION_WEIGHTS).reduce((sum, [key, weight]) => {
    return sum + (inputs[key] ?? 0) * weight;
  }, 0);
  const level = score >= 75 ? 'Critical' : score >= 50 ? 'High' : score >= 25 ? 'Moderate' : 'Low';
  return { congestionScore: Math.round(score * 10) / 10, level, weights: CONGESTION_WEIGHTS };
}

/**
 * Behavioral WTP model: extends self-report WTP with visual behavioral observation.
 * Returns a composite Behavioral WTP Score (0–100).
 * @param {object} params
 * @param {number} params.surveyWTP       - stated WTP from survey (0–100)
 * @param {number} params.queueTolerance  - patience score from queue video analysis (0–100)
 * @param {number} params.wayfindingEase  - wayfinding behavior score from heatmap (0–100)
 * @param {number} params.serviceUsage    - actual digital service usage rate (0–100)
 */
function computeBehavioralWTP({ surveyWTP, queueTolerance, wayfindingEase, serviceUsage }) {
  const weights = { surveyWTP: 0.40, queueTolerance: 0.25, wayfindingEase: 0.20, serviceUsage: 0.15 };
  _validateScores({ surveyWTP, queueTolerance, wayfindingEase, serviceUsage }, Object.keys(weights));
  const score = Object.entries(weights).reduce((sum, [k, w]) => sum + (arguments[0][k] ?? 0) * w, 0);
  return { behavioralWTP: Math.round(score * 10) / 10, grade: _grade(score), weights };
}

/**
 * Compute Airline Resilience Score from multimodal data fusion.
 * @param {object} params
 * @param {number} params.cfaResilienceScore - score from existing CFA/SEM model (0–100)
 * @param {number} params.weatherImpact      - derived from satellite weather images (0–100, inverted: low=resilient)
 * @param {number} params.networkCoverage    - from flight network map analysis (0–100)
 * @param {number} params.financialHealth    - from financial reports (0–100)
 */
function computeAirlineResilience({ cfaResilienceScore, weatherImpact, networkCoverage, financialHealth }) {
  const adjustedWeather = 100 - (weatherImpact ?? 0);   // invert: lower impact = higher resilience
  const weights = { cfaResilienceScore: 0.40, adjustedWeather: 0.20, networkCoverage: 0.25, financialHealth: 0.15 };
  const score =
    cfaResilienceScore * 0.40 +
    adjustedWeather    * 0.20 +
    (networkCoverage  ?? 0)  * 0.25 +
    (financialHealth  ?? 0)  * 0.15;
  return { airlineResilienceScore: Math.round(score * 10) / 10, grade: _grade(score), adjustedWeather };
}

// ── helpers ──────────────────────────────────────────────────────────────────

function _validateScores(obj, keys) {
  for (const k of keys) {
    const v = obj[k];
    if (v !== undefined && v !== null && (typeof v !== 'number' || v < 0 || v > 100)) {
      throw new Error(`${k} must be a number between 0 and 100, got: ${v}`);
    }
  }
}

function _grade(score) {
  if (score >= 80) return 'A';
  if (score >= 65) return 'B';
  if (score >= 50) return 'C';
  if (score >= 35) return 'D';
  return 'F';
}

module.exports = {
  computeAirportResilienceIndex,
  predictCargoCongestion,
  computeBehavioralWTP,
  computeAirlineResilience,
  RESILIENCE_WEIGHTS,
  CONGESTION_WEIGHTS,
};
