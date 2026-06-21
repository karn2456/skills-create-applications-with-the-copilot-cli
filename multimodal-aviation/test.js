'use strict';

const {
  analyzePassengerDensity,
  calculateAirportInfrastructureIndex,
  analyzeHeatmap,
  analyzeFlightNetwork,
  simulateDigitalTwin,
  calculateSustainabilityIndex,
  calculateARII,
} = require('./index');

let passed = 0;
let failed = 0;

function assert(label, condition) {
  if (condition) {
    console.log(`  ✓ ${label}`);
    passed++;
  } else {
    console.error(`  ✗ ${label}`);
    failed++;
  }
}

// ── 1. Passenger Density ──────────────────────────────────────────────────────
console.log('\n[1] analyzePassengerDensity');
const frames = [
  { zone: 'Gate A', detectedCount: 100, frameWidth: 1920, frameHeight: 1080, timestamp: '09:00' },
  { zone: 'Gate A', detectedCount: 120, frameWidth: 1920, frameHeight: 1080, timestamp: '09:15' },
  { zone: 'Security', detectedCount: 250, frameWidth: 1920, frameHeight: 1080, timestamp: '09:00' },
];
const density = analyzePassengerDensity(frames);
assert('คืนค่า zone ถูกต้อง', Object.keys(density).includes('Gate A'));
assert('occupancyRate อยู่ใน range 0–100', density['Gate A'].occupancyRate >= 0 && density['Gate A'].occupancyRate <= 100);
assert('congestionLevel มีค่า', typeof density['Gate A'].congestionLevel === 'string');

let threw = false;
try { analyzePassengerDensity([]); } catch { threw = true; }
assert('throw เมื่อ frames ว่าง', threw);

// ── 2. Airport Infrastructure Index ──────────────────────────────────────────
console.log('\n[2] calculateAirportInfrastructureIndex');
const aii = calculateAirportInfrastructureIndex({
  apronUtilization: 80,
  cargoAreaExpansion: 40000,
  runwayActivity: 50,
  greenCoverageRatio: 0.25,
  constructionArea: 80000,
});
assert('AII อยู่ระหว่าง 0–100', aii.airportInfrastructureIndex >= 0 && aii.airportInfrastructureIndex <= 100);
assert('grade มีค่า', typeof aii.grade === 'string');
assert('scores มี 5 dimensions', Object.keys(aii.scores).length === 5);

// ── 3. Heatmap Analytics ──────────────────────────────────────────────────────
console.log('\n[3] analyzeHeatmap');
const zones = [
  { zoneId: 'Z1', zoneName: 'Departure Hall', avgDwellTime: 40, footfall: 9000, retailRevenue: 450000 },
  { zoneId: 'Z2', zoneName: 'Retail A',       avgDwellTime: 25, footfall: 2000, retailRevenue: 300000 },
];
const heatmap = analyzeHeatmap(zones);
assert('ส่งคืนผลลัพธ์ทุก zone', heatmap.length === 2);
assert('flowSharePct รวมไม่เกิน 100', heatmap.reduce((s, z) => s + z.flowSharePct, 0) <= 100.1);
assert('zoneType มีค่า', heatmap.every(z => typeof z.zoneType === 'string'));
assert('revenuePerPassenger คำนวณถูก (Z2)', Math.abs(heatmap[1].revenuePerPassenger - 150) < 0.1);

let threwHeatmap = false;
try { analyzeHeatmap([]); } catch { threwHeatmap = true; }
assert('throw เมื่อ zones ว่าง', threwHeatmap);

// ── 4. Flight Network Analysis ─────────────────────────────────────────────────
console.log('\n[4] analyzeFlightNetwork');
const airports = [
  { id: 'BKK', name: 'Suvarnabhumi', country: 'Thailand' },
  { id: 'SIN', name: 'Changi',       country: 'Singapore' },
];
const routes = [
  { from: 'BKK', to: 'SIN', frequency: 20, avgDelay: 10, onTimeRate: 90 },
  { from: 'SIN', to: 'BKK', frequency: 18, avgDelay: 8,  onTimeRate: 92 },
];
const net = analyzeFlightNetwork(airports, routes);
assert('networkSummary มี totalAirports', net.networkSummary.totalAirports === 2);
assert('networkSummary มี totalRoutes',   net.networkSummary.totalRoutes === 2);
assert('airports array ถูกต้อง', net.airports.length === 2);
assert('avgOnTimeRate คำนวณถูก', Math.abs(net.networkSummary.avgOnTimeRate - 91) < 0.1);

// ── 5. Digital Twin Simulation ────────────────────────────────────────────────
console.log('\n[5] simulateDigitalTwin');
const twin = simulateDigitalTwin(
  { passengerLoad: 2000, gateCount: 15, checkInCounters: 30, securityLanes: 10 },
  { type: 'ฝนตกหนัก', severity: 'ปานกลาง', affectedGates: 3, weatherImpact: true }
);
assert('resilienceScore อยู่ใน 0–100', twin.resilienceScore >= 0 && twin.resilienceScore <= 100);
assert('simulation มี operationalGates', typeof twin.simulation.operationalGates === 'number');
assert('actionPriority มีค่า', typeof twin.actionPriority === 'string');

// ── 6. Sustainability Index ────────────────────────────────────────────────────
console.log('\n[6] calculateSustainabilityIndex');
const sustain = calculateSustainabilityIndex({
  annualFlightMovements: 200000,
  avgAircraftAge: 10,
  renewableEnergyRatio: 0.4,
  greenBuildingArea: 50000,
  totalBuildingArea: 180000,
  carbonOffsetTonnes: 600000,
});
assert('greenAirportIndex อยู่ใน 0–100', sustain.greenAirportIndex >= 0 && sustain.greenAirportIndex <= 100);
assert('esgRating มีค่า', typeof sustain.esgRating === 'string');
assert('carbonMetrics มีครบ', ['totalCarbonTonnes', 'carbonOffsetTonnes', 'netCarbonTonnes'].every(k => k in sustain.carbonMetrics));

// ── 7. ARII Composite ─────────────────────────────────────────────────────────
console.log('\n[7] calculateARII');
const ariiResult = calculateARII({
  densityScore: 70,
  infrastructureIndex: 75,
  heatmapCoverageScore: 65,
  networkResilience: 80,
  digitalTwinResilience: 60,
  greenAirportIndex: 55,
});
assert('ARII อยู่ใน 0–100', ariiResult.arii >= 0 && ariiResult.arii <= 100);
assert('researchReadiness มีค่า', typeof ariiResult.researchReadiness === 'string');
assert('suggestedJournals เป็น array', Array.isArray(ariiResult.suggestedJournals));
assert('ARII ≈ 69.25 ตาม weights', Math.abs(ariiResult.arii - 69.25) < 0.1);

// ── Summary ────────────────────────────────────────────────────────────────────
console.log(`\n=== Test Summary: ${passed} passed, ${failed} failed ===`);
if (failed > 0) process.exit(1);
