'use strict';

/**
 * Multimodal AI Aviation Research Framework
 * กรอบการวิจัยการบินด้วย AI หลายโมดัล สำหรับ Aviation Management
 *
 * อ้างอิง: Multimodal Aviation Intelligence Framework (2024–2026)
 * ครอบคลุม: Computer Vision, Digital Twin, Graph AI, SEM/PLS-SEM,
 *            Spatial AI, Heatmap Analytics, Airport Resilience
 */

// ── 1. Computer Vision → Passenger Density Variables ──────────────────────────

/**
 * แปลงผลลัพธ์ Computer Vision เป็นตัวแปรเชิงสถิติ
 * จำลองการนับจำนวนคนจากภาพ CCTV ด้วย YOLO/Detectron
 *
 * @param {Array<{zone, detectedCount, frameWidth, frameHeight, timestamp}>} frames
 * @returns Object with density, queue, and occupancy metrics
 */
function analyzePassengerDensity(frames) {
  if (!frames || frames.length === 0) throw new Error('ต้องมีข้อมูล frame อย่างน้อย 1 รายการ');

  const zoneStats = {};

  for (const frame of frames) {
    const { zone, detectedCount, frameWidth, frameHeight } = frame;
    const area = frameWidth * frameHeight;
    const density = detectedCount / (area / 10000); // คนต่อตารางเมตร (scaled)

    if (!zoneStats[zone]) {
      zoneStats[zone] = { counts: [], densities: [] };
    }
    zoneStats[zone].counts.push(detectedCount);
    zoneStats[zone].densities.push(density);
  }

  const result = {};
  for (const [zone, data] of Object.entries(zoneStats)) {
    const avgCount = data.counts.reduce((a, b) => a + b, 0) / data.counts.length;
    const maxCount = Math.max(...data.counts);
    const avgDensity = data.densities.reduce((a, b) => a + b, 0) / data.densities.length;
    const occupancyRate = Math.min((avgDensity / 2) * 100, 100); // สมมติ 2 คน/ตร.ม. = 100%

    const congestionLevel =
      avgDensity >= 1.5 ? 'วิกฤต' :
      avgDensity >= 1.0 ? 'แออัดมาก' :
      avgDensity >= 0.5 ? 'แออัดปานกลาง' : 'ปกติ';

    result[zone] = {
      passengerDensity: parseFloat(avgDensity.toFixed(3)),
      queueLength: Math.round(avgCount),
      peakCount: maxCount,
      occupancyRate: parseFloat(occupancyRate.toFixed(1)),
      congestionLevel,
    };
  }

  return result;
}

// ── 2. Satellite Image → Airport Infrastructure Index ─────────────────────────

/**
 * วิเคราะห์ภาพดาวเทียมเพื่อสร้าง Airport Infrastructure Index
 * จำลองการสกัด features ด้วย CNN จากภาพดาวเทียม
 *
 * @param {Object} satelliteFeatures
 * @param {number} satelliteFeatures.apronUtilization    - 0–100%
 * @param {number} satelliteFeatures.cargoAreaExpansion  - ตร.ม.
 * @param {number} satelliteFeatures.runwayActivity      - เที่ยวบิน/ชม.
 * @param {number} satelliteFeatures.greenCoverageRatio  - 0–1
 * @param {number} satelliteFeatures.constructionArea    - ตร.ม.
 */
function calculateAirportInfrastructureIndex(satelliteFeatures) {
  const {
    apronUtilization,
    cargoAreaExpansion,
    runwayActivity,
    greenCoverageRatio,
    constructionArea,
  } = satelliteFeatures;

  const apronScore   = Math.min(apronUtilization, 100);
  const cargoScore   = Math.min((cargoAreaExpansion / 50000) * 100, 100);
  const runwayScore  = Math.min((runwayActivity / 60) * 100, 100);
  const greenScore   = greenCoverageRatio * 100;
  const devScore     = Math.min((constructionArea / 100000) * 100, 100);

  const aii =
    apronScore  * 0.30 +
    cargoScore  * 0.20 +
    runwayScore * 0.25 +
    greenScore  * 0.15 +
    devScore    * 0.10;

  const grade =
    aii >= 80 ? 'A - โครงสร้างพื้นฐานยอดเยี่ยม' :
    aii >= 60 ? 'B - โครงสร้างพื้นฐานดี' :
    aii >= 40 ? 'C - โครงสร้างพื้นฐานปานกลาง' : 'D - ต้องพัฒนา';

  return {
    scores: { apronScore, cargoScore, runwayScore, greenScore, devScore },
    airportInfrastructureIndex: parseFloat(aii.toFixed(2)),
    grade,
  };
}

// ── 3. Heatmap Analytics ───────────────────────────────────────────────────────

/**
 * วิเคราะห์ Passenger Heatmap จาก WiFi/Bluetooth Tracking
 * จำแนกโซนตามความหนาแน่นและประเมินผลกระทบต่อรายได้
 *
 * @param {Array<{zoneId, zoneName, avgDwellTime, footfall, retailRevenue}>} zones
 */
function analyzeHeatmap(zones) {
  if (!zones || zones.length === 0) throw new Error('ต้องมีข้อมูลโซนอย่างน้อย 1 โซน');

  const totalFootfall = zones.reduce((s, z) => s + z.footfall, 0);

  return zones.map(zone => {
    const flowShare = totalFootfall > 0 ? (zone.footfall / totalFootfall) * 100 : 0;
    const revenuePerPassenger = zone.footfall > 0
      ? zone.retailRevenue / zone.footfall
      : 0;

    const zoneType =
      flowShare >= 20 ? 'High Density Zone' :
      flowShare >= 10 ? 'Medium Density Zone' :
      flowShare >= 3  ? 'Low Density Zone' : 'Dead Space';

    const serviceRecommendation =
      zoneType === 'High Density Zone'   ? 'เพิ่มจุดบริการและบุคลากร' :
      zoneType === 'Medium Density Zone' ? 'ปรับปรุง Signage และ Wayfinding' :
      zoneType === 'Low Density Zone'    ? 'พิจารณาจัดกิจกรรมดึงดูดผู้โดยสาร' :
                                          'ทบทวนการออกแบบพื้นที่';

    return {
      zoneId: zone.zoneId,
      zoneName: zone.zoneName,
      footfall: zone.footfall,
      flowSharePct: parseFloat(flowShare.toFixed(1)),
      avgDwellTime: zone.avgDwellTime,
      revenuePerPassenger: parseFloat(revenuePerPassenger.toFixed(2)),
      zoneType,
      serviceRecommendation,
    };
  });
}

// ── 4. Flight Network Graph Analysis (GNN simulation) ─────────────────────────

/**
 * วิเคราะห์เครือข่ายเที่ยวบินด้วย Graph-based approach
 * แทนสนามบินด้วย Node และเส้นทางบินด้วย Edge
 *
 * @param {Array<{id, name, country}>} airports - Nodes
 * @param {Array<{from, to, frequency, avgDelay, onTimeRate}>} routes  - Edges
 */
function analyzeFlightNetwork(airports, routes) {
  const nodeMap = Object.fromEntries(airports.map(a => [a.id, { ...a, inbound: 0, outbound: 0, totalDelay: 0, routeCount: 0 }]));

  for (const route of routes) {
    if (nodeMap[route.from]) {
      nodeMap[route.from].outbound += route.frequency;
      nodeMap[route.from].totalDelay += route.avgDelay * route.frequency;
      nodeMap[route.from].routeCount += 1;
    }
    if (nodeMap[route.to]) {
      nodeMap[route.to].inbound += route.frequency;
      nodeMap[route.to].totalDelay += route.avgDelay * route.frequency;
      nodeMap[route.to].routeCount += 1;
    }
  }

  const networkStats = airports.map(airport => {
    const node = nodeMap[airport.id];
    const totalFlights = node.inbound + node.outbound;
    const avgDelay = totalFlights > 0 ? node.totalDelay / totalFlights : 0;
    const connectivityScore = Math.min((node.routeCount / routes.length) * 100, 100);
    const hubScore = Math.min((totalFlights / 200) * 100, 100); // 200 flights/day = max

    const hubClassification =
      hubScore >= 75 ? 'Major Hub' :
      hubScore >= 50 ? 'Secondary Hub' :
      hubScore >= 25 ? 'Regional Airport' : 'Local Airport';

    const delayRisk =
      avgDelay >= 30 ? 'สูงมาก' :
      avgDelay >= 20 ? 'สูง' :
      avgDelay >= 10 ? 'ปานกลาง' : 'ต่ำ';

    return {
      airportId: airport.id,
      airportName: airport.name,
      country: airport.country,
      inboundFlights: node.inbound,
      outboundFlights: node.outbound,
      totalRoutes: node.routeCount,
      avgDelayMinutes: parseFloat(avgDelay.toFixed(1)),
      connectivityScore: parseFloat(connectivityScore.toFixed(1)),
      hubScore: parseFloat(hubScore.toFixed(1)),
      hubClassification,
      delayRisk,
    };
  });

  const avgNetworkDelay = routes.reduce((s, r) => s + r.avgDelay, 0) / routes.length;
  const avgOnTimeRate   = routes.reduce((s, r) => s + r.onTimeRate, 0) / routes.length;
  const networkResilience = avgOnTimeRate >= 85 ? 'สูง' : avgOnTimeRate >= 70 ? 'ปานกลาง' : 'ต้องปรับปรุง';

  return {
    airports: networkStats,
    networkSummary: {
      totalAirports: airports.length,
      totalRoutes: routes.length,
      avgNetworkDelay: parseFloat(avgNetworkDelay.toFixed(1)),
      avgOnTimeRate: parseFloat(avgOnTimeRate.toFixed(1)),
      networkResilience,
    },
  };
}

// ── 5. Airport Digital Twin Simulation ────────────────────────────────────────

/**
 * จำลอง Digital Twin สนามบินเพื่อคาดการณ์ผลกระทบ
 * เชื่อม Physical World กับ Digital World
 *
 * @param {Object} currentState   - สภาพจริงของสนามบิน ณ ปัจจุบัน
 * @param {Object} disruptionEvent - เหตุการณ์รบกวน (พายุ, ความล่าช้า, ฯลฯ)
 */
function simulateDigitalTwin(currentState, disruptionEvent) {
  const { passengerLoad, gateCount, checkInCounters, securityLanes } = currentState;
  const { type, severity, affectedGates, weatherImpact } = disruptionEvent;

  const severityMultiplier = { ต่ำ: 0.2, ปานกลาง: 0.5, สูง: 0.8, วิกฤต: 1.0 }[severity] || 0.5;
  const operationalGates = gateCount - Math.round(affectedGates * severityMultiplier);
  const weatherPenalty   = weatherImpact ? severityMultiplier * 0.3 : 0;

  const throughputCapacity  = (operationalGates / gateCount) * 100 * (1 - weatherPenalty);
  const checkInQueue        = Math.round(passengerLoad * severityMultiplier * 1.5 / checkInCounters);
  const securityWaitTime    = Math.round((passengerLoad * severityMultiplier) / (securityLanes * 30)); // นาที
  const estimatedDelayMins  = Math.round(severityMultiplier * 45 + weatherPenalty * 30);

  const resilienceScore = Math.max(0, 100 - severityMultiplier * 60 - weatherPenalty * 20);
  const actionPriority =
    resilienceScore < 30 ? 'ต้องดำเนินการทันที - เปิดใช้แผน Contingency' :
    resilienceScore < 60 ? 'ดำเนินการเชิงรุก - เพิ่มกำลังบุคลากร' :
                           'ติดตามสถานการณ์ต่อเนื่อง';

  return {
    disruptionType: type,
    severity,
    simulation: {
      operationalGates,
      throughputCapacityPct: parseFloat(throughputCapacity.toFixed(1)),
      checkInQueuePerCounter: checkInQueue,
      securityWaitTimeMinutes: securityWaitTime,
      estimatedFlightDelayMinutes: estimatedDelayMins,
    },
    resilienceScore: parseFloat(resilienceScore.toFixed(1)),
    actionPriority,
  };
}

// ── 6. Sustainability Analytics ────────────────────────────────────────────────

/**
 * วิเคราะห์ความยั่งยืนของสนามบินจากข้อมูลดาวเทียมและ Operational Data
 *
 * @param {Object} params
 * @param {number} params.annualFlightMovements  - จำนวนเที่ยวบินต่อปี
 * @param {number} params.avgAircraftAge         - อายุเครื่องบินเฉลี่ย (ปี)
 * @param {number} params.renewableEnergyRatio   - 0–1
 * @param {number} params.greenBuildingArea      - ตร.ม.
 * @param {number} params.totalBuildingArea      - ตร.ม.
 * @param {number} params.carbonOffsetTonnes     - ตันคาร์บอนที่ชดเชย
 */
function calculateSustainabilityIndex(params) {
  const {
    annualFlightMovements,
    avgAircraftAge,
    renewableEnergyRatio,
    greenBuildingArea,
    totalBuildingArea,
    carbonOffsetTonnes,
  } = params;

  const aircraftEmissionFactor = Math.max(0, 100 - avgAircraftAge * 3); // เครื่องใหม่ = ปล่อยน้อย
  const carbonPerFlight        = 15 - (renewableEnergyRatio * 5);        // ตัน CO₂ สมมติ
  const totalCarbon            = annualFlightMovements * carbonPerFlight;
  const netCarbon              = Math.max(0, totalCarbon - carbonOffsetTonnes);

  const energyScore      = renewableEnergyRatio * 100;
  const buildingScore    = (greenBuildingArea / totalBuildingArea) * 100;
  const emissionScore    = aircraftEmissionFactor;
  const offsetScore      = Math.min((carbonOffsetTonnes / totalCarbon) * 100, 100);

  const greenAirportIndex =
    energyScore   * 0.30 +
    buildingScore * 0.20 +
    emissionScore * 0.25 +
    offsetScore   * 0.25;

  const esgRating =
    greenAirportIndex >= 80 ? 'AAA - Green Airport ชั้นนำ' :
    greenAirportIndex >= 60 ? 'AA - มุ่งสู่ความยั่งยืน' :
    greenAirportIndex >= 40 ? 'A - กำลังพัฒนา' : 'B - ต้องปรับปรุงเร่งด่วน';

  return {
    carbonMetrics: {
      totalCarbonTonnes: Math.round(totalCarbon),
      carbonOffsetTonnes,
      netCarbonTonnes: Math.round(netCarbon),
    },
    scores: {
      energyScore: parseFloat(energyScore.toFixed(1)),
      buildingScore: parseFloat(buildingScore.toFixed(1)),
      emissionScore: parseFloat(emissionScore.toFixed(1)),
      offsetScore: parseFloat(offsetScore.toFixed(1)),
    },
    greenAirportIndex: parseFloat(greenAirportIndex.toFixed(2)),
    esgRating,
  };
}

// ── 7. Aviation Research Intelligence Index (ARII) ────────────────────────────

/**
 * ดัชนีความฉลาดของการวิจัยการบินแบบหลายโมดัล (ARII)
 * ผสานผลลัพธ์จากทุก Technique เข้าเป็นคะแนนรวม
 *
 * @param {Object} params
 * @param {number} params.densityScore         - คะแนนจาก Computer Vision (0–100)
 * @param {number} params.infrastructureIndex  - Airport Infrastructure Index (0–100)
 * @param {number} params.heatmapCoverageScore - ความครอบคลุมของ Heatmap Analytics (0–100)
 * @param {number} params.networkResilience    - คะแนน Flight Network Resilience (0–100)
 * @param {number} params.digitalTwinResilience- Digital Twin Resilience Score (0–100)
 * @param {number} params.greenAirportIndex    - Sustainability Index (0–100)
 */
function calculateARII(params) {
  const {
    densityScore,
    infrastructureIndex,
    heatmapCoverageScore,
    networkResilience,
    digitalTwinResilience,
    greenAirportIndex,
  } = params;

  const arii =
    densityScore          * 0.20 +
    infrastructureIndex   * 0.20 +
    heatmapCoverageScore  * 0.15 +
    networkResilience     * 0.20 +
    digitalTwinResilience * 0.15 +
    greenAirportIndex     * 0.10;

  const researchReadiness =
    arii >= 80 ? 'พร้อมตีพิมพ์ Scopus Q1/Q2 — งานวิจัยระดับนานาชาติ' :
    arii >= 60 ? 'เหมาะสำหรับ Scopus Q2/Q3 — ต้องเสริมข้อมูลบางส่วน' :
    arii >= 40 ? 'ต้องพัฒนาเพิ่ม — เติมช่องว่างวิจัยก่อนส่งตีพิมพ์' :
                 'ยังอยู่ในขั้น Exploratory Research — ต้องเก็บข้อมูลเพิ่ม';

  const suggestedJournals =
    arii >= 80
      ? ['Journal of Air Transport Management (Q1)', 'Transportation Research Part E (Q1)', 'Journal of Transport Geography (Q1)']
      : arii >= 60
      ? ['Journal of Airport Management (Q2)', 'Research in Transportation Business & Management (Q2)']
      : ['Asia Pacific Journal of Tourism Research (Q3)', 'Journal of Aviation Technology and Engineering'];

  return {
    componentScores: params,
    arii: parseFloat(arii.toFixed(2)),
    researchReadiness,
    suggestedJournals,
  };
}

// ── Demo ──────────────────────────────────────────────────────────────────────

function runDemo() {
  console.log('=== Multimodal AI Aviation Research Framework ===\n');
  console.log('กรอบการวิจัยการบินด้วย AI หลายโมดัล (2024–2026)\n');

  // 1. Computer Vision → Passenger Density
  const frames = [
    { zone: 'Gate A1', detectedCount: 85, frameWidth: 1920, frameHeight: 1080, timestamp: '08:00' },
    { zone: 'Gate A1', detectedCount: 120, frameWidth: 1920, frameHeight: 1080, timestamp: '08:15' },
    { zone: 'Security Check', detectedCount: 200, frameWidth: 1920, frameHeight: 1080, timestamp: '08:00' },
    { zone: 'Security Check', detectedCount: 240, frameWidth: 1920, frameHeight: 1080, timestamp: '08:15' },
    { zone: 'Check-in Hall', detectedCount: 60, frameWidth: 1920, frameHeight: 1080, timestamp: '08:00' },
  ];
  const density = analyzePassengerDensity(frames);
  console.log('1. Computer Vision → Passenger Density (CCTV Analysis):');
  for (const [zone, stats] of Object.entries(density)) {
    console.log(`   [${zone}] ความหนาแน่น: ${stats.passengerDensity} คน/ตร.ม. | Occupancy: ${stats.occupancyRate}% | สถานะ: ${stats.congestionLevel}`);
  }

  // 2. Satellite → Infrastructure Index
  const aii = calculateAirportInfrastructureIndex({
    apronUtilization: 78,
    cargoAreaExpansion: 35000,
    runwayActivity: 48,
    greenCoverageRatio: 0.18,
    constructionArea: 65000,
  });
  console.log(`\n2. Satellite Image → Airport Infrastructure Index:`);
  console.log(`   AII Score: ${aii.airportInfrastructureIndex}/100 | ${aii.grade}`);

  // 3. Heatmap Analytics
  const zones = [
    { zoneId: 'Z1', zoneName: 'Departure Hall', avgDwellTime: 45, footfall: 8500, retailRevenue: 425000 },
    { zoneId: 'Z2', zoneName: 'Retail Zone A',  avgDwellTime: 22, footfall: 3200, retailRevenue: 640000 },
    { zoneId: 'Z3', zoneName: 'Food Court',     avgDwellTime: 35, footfall: 4100, retailRevenue: 328000 },
    { zoneId: 'Z4', zoneName: 'Prayer Room',    avgDwellTime: 12, footfall: 480,  retailRevenue: 0 },
  ];
  const heatmap = analyzeHeatmap(zones);
  console.log('\n3. Heatmap Analytics (WiFi/BT Tracking):');
  heatmap.forEach(z =>
    console.log(`   [${z.zoneName}] ${z.zoneType} | Flow: ${z.flowSharePct}% | Rev/Pax: ฿${z.revenuePerPassenger}`)
  );

  // 4. Flight Network (GNN)
  const airports = [
    { id: 'BKK', name: 'Suvarnabhumi', country: 'Thailand' },
    { id: 'DMK', name: 'Don Mueang',   country: 'Thailand' },
    { id: 'SIN', name: 'Changi',       country: 'Singapore' },
    { id: 'KUL', name: 'KLIA',         country: 'Malaysia' },
  ];
  const routes = [
    { from: 'BKK', to: 'SIN', frequency: 18, avgDelay: 12, onTimeRate: 88 },
    { from: 'BKK', to: 'KUL', frequency: 14, avgDelay: 8,  onTimeRate: 91 },
    { from: 'DMK', to: 'SIN', frequency: 10, avgDelay: 15, onTimeRate: 82 },
    { from: 'SIN', to: 'KUL', frequency: 22, avgDelay: 5,  onTimeRate: 95 },
    { from: 'KUL', to: 'BKK', frequency: 16, avgDelay: 10, onTimeRate: 89 },
  ];
  const network = analyzeFlightNetwork(airports, routes);
  console.log('\n4. Flight Network Graph Analysis (GNN):');
  network.airports.forEach(a =>
    console.log(`   [${a.airportId}] ${a.hubClassification} | Delay Risk: ${a.delayRisk} | Connectivity: ${a.connectivityScore}%`)
  );
  console.log(`   Network Resilience: ${network.networkSummary.networkResilience} | Avg On-Time: ${network.networkSummary.avgOnTimeRate}%`);

  // 5. Digital Twin Simulation
  const twin = simulateDigitalTwin(
    { passengerLoad: 3500, gateCount: 20, checkInCounters: 40, securityLanes: 12 },
    { type: 'พายุฤดูร้อน', severity: 'สูง', affectedGates: 6, weatherImpact: true }
  );
  console.log('\n5. Airport Digital Twin Simulation:');
  console.log(`   เหตุการณ์: ${twin.disruptionType} (${twin.severity})`);
  console.log(`   Throughput Capacity: ${twin.simulation.throughputCapacityPct}% | Estimated Delay: ${twin.simulation.estimatedFlightDelayMinutes} นาที`);
  console.log(`   Resilience Score: ${twin.resilienceScore}/100 | Action: ${twin.actionPriority}`);

  // 6. Sustainability
  const sustain = calculateSustainabilityIndex({
    annualFlightMovements: 280000,
    avgAircraftAge: 8,
    renewableEnergyRatio: 0.35,
    greenBuildingArea: 45000,
    totalBuildingArea: 200000,
    carbonOffsetTonnes: 800000,
  });
  console.log('\n6. Sustainability Analytics (Satellite + Operational Data):');
  console.log(`   Green Airport Index: ${sustain.greenAirportIndex}/100 | ESG Rating: ${sustain.esgRating}`);
  console.log(`   Net Carbon: ${sustain.carbonMetrics.netCarbonTonnes.toLocaleString()} ตัน CO₂`);

  // 7. ARII Composite Index
  const { arii, researchReadiness, suggestedJournals } = calculateARII({
    densityScore: 74,
    infrastructureIndex: aii.airportInfrastructureIndex,
    heatmapCoverageScore: 68,
    networkResilience: 82,
    digitalTwinResilience: twin.resilienceScore,
    greenAirportIndex: sustain.greenAirportIndex,
  });
  console.log('\n=== Aviation Research Intelligence Index (ARII) ===');
  console.log(`ARII Score: ${arii}/100`);
  console.log(`Research Readiness: ${researchReadiness}`);
  console.log('Suggested Journals:');
  suggestedJournals.forEach(j => console.log(`  - ${j}`));
  console.log('\n[Multimodal AI Aviation Research Framework — Ready for PhD-Level Research 2026–2030]');
}

runDemo();

module.exports = {
  analyzePassengerDensity,
  calculateAirportInfrastructureIndex,
  analyzeHeatmap,
  analyzeFlightNetwork,
  simulateDigitalTwin,
  calculateSustainabilityIndex,
  calculateARII,
};
