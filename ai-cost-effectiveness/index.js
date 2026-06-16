'use strict';

/**
 * AI Utilization Value Index (AUVI)
 * กรอบการประเมินความคุ้มค่าในการใช้ AI สำหรับองค์กร
 *
 * อ้างอิง: Technology Acceptance Model (TAM), DeLone & McLean IS Success Model,
 * Balanced Scorecard (BSC)
 */

// ── 1. ROI (Return on Investment) ──────────────────────────────────────────

/**
 * คำนวณผลตอบแทนจากการลงทุน
 * ROI = ((ผลประโยชน์ - ต้นทุน) / ต้นทุน) × 100
 */
function calculateROI(totalBenefit, totalCost) {
  if (totalCost <= 0) throw new Error('ต้นทุนต้องมากกว่าศูนย์');
  return ((totalBenefit - totalCost) / totalCost) * 100;
}

// ── 2. Cost Reduction ──────────────────────────────────────────────────────

/**
 * คำนวณมูลค่าการลดต้นทุนรวม
 * @param {Object} costs - { labor, time, error, training }
 * @param {Object} savings - { labor, time, error, training }
 */
function calculateCostReduction(costs, savings) {
  const categories = ['labor', 'time', 'error', 'training'];
  const result = {};
  let totalReduction = 0;

  for (const cat of categories) {
    const before = costs[cat] || 0;
    const after = savings[cat] || 0;
    const reduction = before - after;
    const pct = before > 0 ? (reduction / before) * 100 : 0;
    result[cat] = { before, after, reduction, reductionPct: pct };
    totalReduction += reduction;
  }

  result.total = totalReduction;
  return result;
}

// ── 3. Productivity Improvement ────────────────────────────────────────────

/**
 * คำนวณการเพิ่มประสิทธิภาพการทำงาน
 * @param {Array<{task, hoursBefore, hoursAfter}>} tasks
 */
function calculateProductivity(tasks) {
  return tasks.map(t => {
    const saved = t.hoursBefore - t.hoursAfter;
    const improvement = t.hoursBefore > 0 ? (saved / t.hoursBefore) * 100 : 0;
    return { ...t, hoursSaved: saved, improvementPct: improvement };
  });
}

// ── 4. Accuracy & Quality ──────────────────────────────────────────────────

/**
 * เปรียบเทียบความแม่นยำก่อน/หลังใช้ AI
 * @param {number} accuracyBefore - 0–100
 * @param {number} accuracyAfter  - 0–100
 */
function assessAccuracy(accuracyBefore, accuracyAfter) {
  const gain = accuracyAfter - accuracyBefore;
  const qualitative =
    gain >= 20 ? 'ดีมาก' : gain >= 10 ? 'ดี' : gain >= 5 ? 'พอใช้' : 'ต้องปรับปรุง';
  return { accuracyBefore, accuracyAfter, gain, qualitative };
}

// ── 5. Payback Period ──────────────────────────────────────────────────────

/**
 * คำนวณระยะเวลาคืนทุน (ปี)
 * Payback Period = เงินลงทุน / ผลประโยชน์สุทธิต่อปี
 */
function calculatePaybackPeriod(investment, annualNetBenefit) {
  if (annualNetBenefit <= 0) throw new Error('ผลประโยชน์สุทธิต่อปีต้องมากกว่าศูนย์');
  const years = investment / annualNetBenefit;
  const rating = years <= 1 ? 'ดีเยี่ยม' : years <= 2 ? 'ดี' : years <= 3 ? 'น่าสนใจ' : 'ควรพิจารณาใหม่';
  return { investment, annualNetBenefit, paybackYears: years, rating };
}

// ── 6. Strategic Value ─────────────────────────────────────────────────────

/**
 * ประเมินคุณค่าเชิงกลยุทธ์ (Balanced Scorecard)
 * @param {Object} bsc - { financial, customer, internal, learning } ค่า 0–100 แต่ละมิติ
 */
function assessStrategicValue(bsc) {
  const dimensions = ['financial', 'customer', 'internal', 'learning'];
  const weights = { financial: 0.3, customer: 0.25, internal: 0.25, learning: 0.2 };

  let weightedScore = 0;
  for (const dim of dimensions) {
    weightedScore += (bsc[dim] || 0) * weights[dim];
  }

  const level =
    weightedScore >= 80 ? 'สูงมาก' :
    weightedScore >= 60 ? 'สูง' :
    weightedScore >= 40 ? 'ปานกลาง' : 'ต่ำ';

  return { scores: bsc, weights, weightedScore, level };
}

// ── AUVI Composite Index ────────────────────────────────────────────────────

/**
 * คำนวณ AUVI (AI Utilization Value Index) รวม
 * ผสมผสาน ROI, ประสิทธิภาพ, คุณภาพ และผลลัพธ์องค์กร
 *
 * @param {Object} params
 * @param {number} params.roi              - ROI (%)
 * @param {number} params.productivityGain - ค่าเฉลี่ยการเพิ่มประสิทธิภาพ (%)
 * @param {number} params.accuracyGain     - การเพิ่มความแม่นยำ (%)
 * @param {number} params.strategicScore   - คะแนนกลยุทธ์ 0–100
 * @param {number} params.paybackYears     - ระยะเวลาคืนทุน
 */
function calculateAUVI({ roi, productivityGain, accuracyGain, strategicScore, paybackYears }) {
  const roiNorm = Math.min(roi / 3, 100);
  const paybackNorm = Math.max(0, 100 - paybackYears * 20);

  const auvi =
    roiNorm * 0.25 +
    productivityGain * 0.20 +
    accuracyGain * 0.20 +
    strategicScore * 0.20 +
    paybackNorm * 0.15;

  const grade =
    auvi >= 80 ? 'A - คุ้มค่าสูงมาก' :
    auvi >= 60 ? 'B - คุ้มค่าดี' :
    auvi >= 40 ? 'C - คุ้มค่าปานกลาง' : 'D - ควรทบทวนการลงทุน';

  return { auvi, grade };
}

// ── Demo / Example ──────────────────────────────────────────────────────────

function runDemo() {
  console.log('=== AI Utilization Value Index (AUVI) ===\n');

  // ROI
  const roi = calculateROI(300_000, 100_000);
  console.log(`1. ROI: ${roi.toFixed(1)}%`);

  // Cost Reduction
  const cr = calculateCostReduction(
    { labor: 200_000, time: 50_000, error: 30_000, training: 20_000 },
    { labor: 80_000,  time: 20_000, error: 5_000,  training: 15_000 }
  );
  console.log(`2. ลดต้นทุนรวม: ${cr.total.toLocaleString()} บาท`);

  // Productivity
  const tasks = [
    { task: 'ตรวจข้อสอบ',   hoursBefore: 10, hoursAfter: 2 },
    { task: 'เขียนรายงาน',  hoursBefore: 5,  hoursAfter: 1 },
    { task: 'วิเคราะห์ข้อมูล', hoursBefore: 8, hoursAfter: 2 },
  ];
  const prod = calculateProductivity(tasks);
  const avgImprovement = prod.reduce((s, t) => s + t.improvementPct, 0) / prod.length;
  console.log('3. การเพิ่มประสิทธิภาพ:');
  prod.forEach(t =>
    console.log(`   - ${t.task}: ${t.hoursBefore}h → ${t.hoursAfter}h (${t.improvementPct.toFixed(0)}%)`)
  );

  // Accuracy
  const acc = assessAccuracy(75, 92);
  console.log(`4. ความแม่นยำ: ${acc.accuracyBefore}% → ${acc.accuracyAfter}% (+${acc.gain}%, ${acc.qualitative})`);

  // Payback Period
  const pb = calculatePaybackPeriod(500_000, 250_000);
  console.log(`5. ระยะเวลาคืนทุน: ${pb.paybackYears.toFixed(1)} ปี (${pb.rating})`);

  // Strategic Value (BSC)
  const sv = assessStrategicValue({ financial: 80, customer: 75, internal: 70, learning: 85 });
  console.log(`6. คุณค่าเชิงกลยุทธ์: ${sv.weightedScore.toFixed(1)}/100 (${sv.level})`);

  // AUVI Composite
  const { auvi, grade } = calculateAUVI({
    roi,
    productivityGain: avgImprovement,
    accuracyGain: acc.gain,
    strategicScore: sv.weightedScore,
    paybackYears: pb.paybackYears,
  });
  console.log(`\n=== AUVI Score: ${auvi.toFixed(1)} | ${grade} ===`);
}

runDemo();

module.exports = {
  calculateROI,
  calculateCostReduction,
  calculateProductivity,
  assessAccuracy,
  calculatePaybackPeriod,
  assessStrategicValue,
  calculateAUVI,
};
