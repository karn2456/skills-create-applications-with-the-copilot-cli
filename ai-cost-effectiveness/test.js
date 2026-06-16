'use strict';

const {
  calculateROI,
  calculateCostReduction,
  calculateProductivity,
  assessAccuracy,
  calculatePaybackPeriod,
  assessStrategicValue,
  calculateAUVI,
} = require('./index');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    console.log(`  ✓ ${label}`);
    passed++;
  } else {
    console.error(`  ✗ ${label}`);
    failed++;
  }
}

// ROI
console.log('ROI:');
assert(calculateROI(300_000, 100_000) === 200, 'ROI 200%');
assert(calculateROI(100_000, 100_000) === 0, 'ROI 0% (break-even)');
try { calculateROI(0, 0); assert(false, 'should throw on zero cost'); }
catch { assert(true, 'throws on zero cost'); }

// Cost Reduction
console.log('Cost Reduction:');
const cr = calculateCostReduction(
  { labor: 200_000, time: 50_000, error: 30_000, training: 20_000 },
  { labor: 80_000,  time: 20_000, error: 5_000,  training: 15_000 }
);
assert(cr.total === 180_000, `total reduction 180,000 (got ${cr.total})`);
assert(cr.labor.reductionPct === 60, 'labor reduction 60%');

// Productivity
console.log('Productivity:');
const prod = calculateProductivity([{ task: 'X', hoursBefore: 10, hoursAfter: 2 }]);
assert(prod[0].hoursSaved === 8, 'saved 8 hours');
assert(prod[0].improvementPct === 80, 'improvement 80%');

// Accuracy
console.log('Accuracy:');
const acc = assessAccuracy(75, 92);
assert(acc.gain === 17, 'gain 17');
assert(acc.qualitative === 'ดี', 'qualitative ดี (gain 17, threshold 20 for ดีมาก)');

// Payback Period
console.log('Payback Period:');
const pb = calculatePaybackPeriod(500_000, 250_000);
assert(pb.paybackYears === 2, 'payback 2 years');
assert(pb.rating === 'ดี', 'rating ดี');

// Strategic Value
console.log('Strategic Value:');
const sv = assessStrategicValue({ financial: 80, customer: 75, internal: 70, learning: 85 });
assert(Math.round(sv.weightedScore * 100) / 100 === 77.25, `weighted score 77.25 (got ${sv.weightedScore})`);
assert(sv.level === 'สูง', 'level สูง');

// AUVI
console.log('AUVI:');
const { auvi, grade } = calculateAUVI({
  roi: 200, productivityGain: 80, accuracyGain: 17, strategicScore: 77.5, paybackYears: 2,
});
assert(auvi > 0 && auvi <= 100, `AUVI in range (${auvi.toFixed(1)})`);
assert(grade.startsWith('A') || grade.startsWith('B'), `grade is A or B (${grade})`);

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
