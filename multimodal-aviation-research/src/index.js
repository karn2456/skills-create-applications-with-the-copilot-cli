#!/usr/bin/env node
/**
 * Multimodal Aviation Research CLI
 * Evidence-Grounded Research Framework for Aviation Management (2024–2026)
 *
 * Commands:
 *   demo       - run a full end-to-end demonstration of all modules
 *   etf        - demonstrate the Evidence Traceability Framework
 *   integrator - demonstrate multimodal data integration
 *   analyzer   - demonstrate the aviation analytics models
 *   help       - show this help message
 */

'use strict';

const { EvidenceTraceabilityFramework, LAYERS } = require('./etf');
const { MultimodalIntegrator } = require('./multimodal-integrator');
const {
  computeAirportResilienceIndex,
  predictCargoCongestion,
  computeBehavioralWTP,
  computeAirlineResilience,
} = require('./aviation-analyzer');

const command = process.argv[2] || 'demo';

const COMMANDS = {
  demo:       runDemo,
  etf:        runETFDemo,
  integrator: runIntegratorDemo,
  analyzer:   runAnalyzerDemo,
  help:       showHelp,
};

const handler = COMMANDS[command];
if (!handler) {
  console.error(`Unknown command: "${command}". Run with "help" to see available commands.`);
  process.exit(1);
}
handler();

// ── ETF Demo ─────────────────────────────────────────────────────────────────

function runETFDemo() {
  console.log('\n=== Evidence Traceability Framework (ETF) ===\n');

  const etf = new EvidenceTraceabilityFramework();

  // Layer 0 – Raw Evidence
  const raw1 = etf.addEvidence({
    layer: LAYERS.RAW,
    content: 'Satellite image of Suvarnabhumi Airport apron, 2024-11-15 09:30 UTC',
    source: 'Planet Labs satellite feed',
    sourceType: 'visual',
  });
  const raw2 = etf.addEvidence({
    layer: LAYERS.RAW,
    content: 'AOT operational KPI report Q3-2024: on-time departure rate 78.4%',
    source: 'AOT Annual Report 2024, p.45',
    sourceType: 'numerical',
    page: 45,
  });

  // Layer 1 – Extracted Evidence
  const ext1 = etf.addEvidence({
    layer: LAYERS.EXTRACTED,
    content: 'Aircraft density score: 72/100; Ground vehicle congestion score: 58/100',
    source: raw1.source,
    sourceType: 'visual',
    confidence: 0.88,
    parentId: raw1.id,
  });

  // Layer 2 – Synthesized Knowledge
  const syn1 = etf.addEvidence({
    layer: LAYERS.SYNTHESIZED,
    content: 'Apron congestion correlates (r=0.71) with on-time departure rate decline during peak hours',
    source: 'AI synthesis from satellite + KPI data',
    sourceType: 'numerical',
    confidence: 0.82,
    parentId: ext1.id,
  });

  // Layer 3 – Research Interpretation
  etf.addEvidence({
    layer: LAYERS.INTERPRETED,
    content: 'Airport resilience requires real-time apron monitoring integrated with operational KPI dashboards',
    source: 'Researcher synthesis',
    sourceType: 'text',
    confidence: 0.90,
    parentId: syn1.id,
  });

  console.log('Evidence chain for synthesized finding:');
  const chain = etf.getChain(syn1.id);
  chain.forEach((e, i) => {
    console.log(`  ${'  '.repeat(i)}[${e.layerLabel}] ${e.id}: ${e.content.substring(0, 70)}...`);
  });

  const traceability = etf.verifyTraceability();
  console.log(`\nTraceability check: ${traceability.valid ? '✓ All synthesized entries are traceable' : '✗ Issues found'}`);
  if (!traceability.valid) console.log('  Issues:', traceability.issues);

  console.log('\nETF Summary:');
  const summary = etf.summary();
  summary.layers.forEach(l => console.log(`  Layer ${l.layer} (${l.label}): ${l.count} entries`));
  console.log(`  Total entries: ${summary.totalEntries}`);
}

// ── Integrator Demo ───────────────────────────────────────────────────────────

function runIntegratorDemo() {
  console.log('\n=== Multimodal Data Integrator ===\n');

  const integrator = new MultimodalIntegrator();

  integrator.registerSource({ type: 'visual',    subtype: 'satellite', label: 'BKK-Apron-Satellite-Nov2024' });
  integrator.registerSource({ type: 'visual',    subtype: 'cctv',      label: 'Terminal2-CCTV-PassengerFlow' });
  integrator.registerSource({ type: 'numerical', subtype: 'kpi',       label: 'AOT-Q3-2024-KPI' });
  integrator.registerSource({ type: 'numerical', subtype: 'delay-data',label: 'IATA-BKK-Delay-2024' });
  integrator.registerSource({ type: 'spatial',   subtype: 'gis',       label: 'BKK-GIS-Cargo-Zone' });
  integrator.registerSource({ type: 'text',      subtype: 'safety-report', label: 'CATC-Safety-Report-2024' });

  console.log('Registered sources:');
  integrator.listSources().forEach(s => {
    console.log(`  [${s.type.toUpperCase().padEnd(9)}] ${s.subtype.padEnd(15)} → ${s.label}`);
  });

  integrator.extractVisualFeatures('BKK-Apron-Satellite-Nov2024', {
    aircraftDensity: 72,
    groundVehicleDensity: 58,
    congestionScore: 65,
    occupancyRate: 81,
  });

  const fused = integrator.fuseFeatures();
  console.log('\nFused multimodal feature vector:');
  Object.entries(fused).forEach(([k, v]) => console.log(`  ${k}: ${v}`));

  console.log('\nIntegrator Summary:');
  const s = integrator.summary();
  console.log(`  Total sources: ${s.totalSources}`);
  Object.entries(s.byType).forEach(([t, c]) => console.log(`  ${t}: ${c}`));
}

// ── Analyzer Demo ─────────────────────────────────────────────────────────────

function runAnalyzerDemo() {
  console.log('\n=== Aviation Research Analyzer ===\n');

  // 1. Airport Resilience Index
  const resilience = computeAirportResilienceIndex({
    operationalRecovery: 74,
    networkRedundancy: 68,
    resourceAvailability: 82,
    passengerImpact: 55,
    financialAbsorption: 70,
  });
  console.log('Airport Resilience Index (Suvarnabhumi):');
  console.log(`  Score: ${resilience.index}/100  Grade: ${resilience.grade}`);

  // 2. Cargo Congestion
  const congestion = predictCargoCongestion({
    visualDensityScore: 65,
    cargoThroughput: 78,
    uldMovementRate: 60,
    truckArrivalRate: 72,
  });
  console.log('\nCargo Terminal Congestion (BKK Cargo):');
  console.log(`  Score: ${congestion.congestionScore}/100  Level: ${congestion.level}`);

  // 3. Behavioral WTP
  const wtp = computeBehavioralWTP({
    surveyWTP: 68,
    queueTolerance: 55,
    wayfindingEase: 72,
    serviceUsage: 61,
  });
  console.log('\nPassenger Behavioral WTP (Digital Services):');
  console.log(`  Score: ${wtp.behavioralWTP}/100  Grade: ${wtp.grade}`);

  // 4. Airline Resilience
  const airlineRes = computeAirlineResilience({
    cfaResilienceScore: 71,
    weatherImpact: 38,
    networkCoverage: 80,
    financialHealth: 65,
  });
  console.log('\nAirline Resilience (Thai carriers multimodal):');
  console.log(`  Score: ${airlineRes.airlineResilienceScore}/100  Grade: ${airlineRes.grade}`);
  console.log(`  Weather-adjusted resilience contribution: ${airlineRes.adjustedWeather}`);
}

// ── Full Demo ────────────────────────────────────────────────────────────────

function runDemo() {
  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║  Multimodal Aviation Research Framework – Full Demo          ║');
  console.log('║  Evidence Traceability Framework (ETF) | CATC / Aviation Sci ║');
  console.log('╚══════════════════════════════════════════════════════════════╝');
  runETFDemo();
  runIntegratorDemo();
  runAnalyzerDemo();
  console.log('\n✓ Demo complete. All modules operational.\n');
}

// ── Help ─────────────────────────────────────────────────────────────────────

function showHelp() {
  console.log(`
Multimodal Aviation Research CLI
Usage: node src/index.js [command]

Commands:
  demo        Run a full end-to-end demonstration (default)
  etf         Demonstrate the Evidence Traceability Framework
  integrator  Demonstrate multimodal data source integration
  analyzer    Demonstrate aviation analytics models
  help        Show this help message

Modules:
  src/etf.js                 Evidence Traceability Framework (4-layer model)
  src/multimodal-integrator.js  Visual / Text / Numerical / Spatial data manager
  src/aviation-analyzer.js   Airport Resilience, Cargo Congestion, WTP, Airline Resilience
`);
}
