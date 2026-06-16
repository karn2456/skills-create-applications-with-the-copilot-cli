'use strict';

const { EvidenceTraceabilityFramework, LAYERS } = require('../etf');
const { MultimodalIntegrator } = require('../multimodal-integrator');
const {
  computeAirportResilienceIndex,
  predictCargoCongestion,
  computeBehavioralWTP,
  computeAirlineResilience,
} = require('../aviation-analyzer');

let passed = 0;
let failed = 0;

function assert(description, condition) {
  if (condition) {
    console.log(`  ✓ ${description}`);
    passed++;
  } else {
    console.error(`  ✗ ${description}`);
    failed++;
  }
}

function assertThrows(description, fn) {
  try {
    fn();
    console.error(`  ✗ ${description} (expected an error but none was thrown)`);
    failed++;
  } catch {
    console.log(`  ✓ ${description}`);
    passed++;
  }
}

// ── ETF tests ────────────────────────────────────────────────────────────────

console.log('\n[1] EvidenceTraceabilityFramework');

const etf = new EvidenceTraceabilityFramework();

const raw = etf.addEvidence({ layer: LAYERS.RAW, content: 'Satellite image', source: 'Planet Labs', sourceType: 'visual' });
assert('adds raw evidence entry', raw.layer === LAYERS.RAW);
assert('auto-generates id', typeof raw.id === 'string' && raw.id.length > 0);
assert('sets layerLabel', raw.layerLabel === 'Raw Evidence');

const ext = etf.addEvidence({ layer: LAYERS.EXTRACTED, content: 'Density score 72', source: 'Planet Labs', sourceType: 'visual', confidence: 0.9, parentId: raw.id });
assert('adds extracted entry with parentId', ext.parentId === raw.id);
assert('stores confidence', ext.confidence === 0.9);

assertThrows('rejects invalid layer', () => etf.addEvidence({ layer: 99, content: 'x', source: 'y', sourceType: 'text' }));
assertThrows('rejects confidence > 1', () => etf.addEvidence({ layer: LAYERS.RAW, content: 'x', source: 'y', sourceType: 'text', confidence: 1.5 }));

const syn = etf.addEvidence({ layer: LAYERS.SYNTHESIZED, content: 'Correlation r=0.71', source: 'AI', sourceType: 'numerical', parentId: ext.id });
const chain = etf.getChain(syn.id);
assert('getChain returns 3-level chain', chain.length === 3);
assert('chain starts with raw entry', chain[0].layer === LAYERS.RAW);

const validity = etf.verifyTraceability();
assert('traceability is valid when all synthesis has parents', validity.valid === true);

etf.addEvidence({ layer: LAYERS.SYNTHESIZED, content: 'Orphan', source: 'AI', sourceType: 'text' });
const validity2 = etf.verifyTraceability();
assert('detects broken traceability for orphan synthesis', validity2.valid === false && validity2.issues.length > 0);

const summary = etf.summary();
assert('summary counts entries per layer', summary.layers[LAYERS.RAW].count === 1);

// ── Multimodal Integrator tests ───────────────────────────────────────────────

console.log('\n[2] MultimodalIntegrator');

const integrator = new MultimodalIntegrator();
integrator.registerSource({ type: 'visual',    subtype: 'satellite', label: 'img1' });
integrator.registerSource({ type: 'numerical', subtype: 'kpi',       label: 'kpi1' });
integrator.registerSource({ type: 'spatial',   subtype: 'gis',       label: 'gis1' });

assert('registers multiple sources', integrator.listSources().length === 3);
assert('summary counts by type', integrator.summary().byType.visual === 1);
assertThrows('rejects unsupported data type', () => integrator.registerSource({ type: 'audio', subtype: 'x', label: 'y' }));

const features = integrator.extractVisualFeatures('img1', { aircraftDensity: 70, congestionScore: 55 });
assert('extracts visual features', features.features.aircraftDensity === 70);

const fused = integrator.fuseFeatures();
assert('fuses features into flat record', fused.congestionScore === 55);

assertThrows('throws when visual source not found', () => integrator.extractVisualFeatures('nonexistent', {}));

// ── Aviation Analyzer tests ───────────────────────────────────────────────────

console.log('\n[3] computeAirportResilienceIndex');

const res = computeAirportResilienceIndex({
  operationalRecovery: 80,
  networkRedundancy: 80,
  resourceAvailability: 80,
  passengerImpact: 80,
  financialAbsorption: 80,
});
assert('perfect score returns 80 index', res.index === 80);
assert('grade A for score ≥ 80', res.grade === 'A');

const resLow = computeAirportResilienceIndex({
  operationalRecovery: 0, networkRedundancy: 0, resourceAvailability: 0, passengerImpact: 0, financialAbsorption: 0,
});
assert('zero inputs return 0 index', resLow.index === 0);
assert('grade F for score < 35', resLow.grade === 'F');

assertThrows('rejects score > 100', () => computeAirportResilienceIndex({ operationalRecovery: 150, networkRedundancy: 50, resourceAvailability: 50, passengerImpact: 50, financialAbsorption: 50 }));

console.log('\n[4] predictCargoCongestion');

const cong = predictCargoCongestion({ visualDensityScore: 100, cargoThroughput: 100, uldMovementRate: 100, truckArrivalRate: 100 });
assert('max inputs return Critical congestion', cong.level === 'Critical');

const congLow = predictCargoCongestion({ visualDensityScore: 10, cargoThroughput: 10, uldMovementRate: 10, truckArrivalRate: 10 });
assert('low inputs return Low congestion', congLow.level === 'Low');

console.log('\n[5] computeBehavioralWTP');

const wtp = computeBehavioralWTP({ surveyWTP: 100, queueTolerance: 100, wayfindingEase: 100, serviceUsage: 100 });
assert('max WTP inputs return score 100', wtp.behavioralWTP === 100);
assert('grade A for max WTP', wtp.grade === 'A');

console.log('\n[6] computeAirlineResilience');

const airline = computeAirlineResilience({ cfaResilienceScore: 80, weatherImpact: 0, networkCoverage: 80, financialHealth: 80 });
assert('zero weather impact contributes full resilience', airline.adjustedWeather === 100);
assert('high inputs return grade A', airline.grade === 'A');

const airlinePoor = computeAirlineResilience({ cfaResilienceScore: 0, weatherImpact: 100, networkCoverage: 0, financialHealth: 0 });
assert('severe weather impact reduces resilience', airlinePoor.airlineResilienceScore < 30);

// ── Summary ───────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(50)}`);
console.log(`Tests: ${passed + failed} total  ✓ ${passed} passed  ✗ ${failed} failed`);

if (failed > 0) {
  process.exit(1);
}
