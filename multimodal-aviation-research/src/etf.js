/**
 * Evidence Traceability Framework (ETF)
 * Manages layered evidence for Aviation Management research:
 *   Layer 0 - Raw Evidence   : original source data
 *   Layer 1 - Extracted      : content pulled from source
 *   Layer 2 - Synthesized    : AI-composed knowledge
 *   Layer 3 - Interpreted    : researcher judgment/conclusion
 */

const LAYERS = Object.freeze({
  RAW: 0,
  EXTRACTED: 1,
  SYNTHESIZED: 2,
  INTERPRETED: 3,
});

const LAYER_LABELS = ['Raw Evidence', 'Extracted Evidence', 'Synthesized Knowledge', 'Research Interpretation'];

class EvidenceEntry {
  constructor({ id, layer, content, source, sourceType, page = null, confidence = 1.0, parentId = null }) {
    if (!Object.values(LAYERS).includes(layer)) {
      throw new Error(`Invalid layer: ${layer}. Must be 0-3.`);
    }
    if (confidence < 0 || confidence > 1) {
      throw new Error('Confidence must be between 0 and 1.');
    }
    this.id = id;
    this.layer = layer;
    this.layerLabel = LAYER_LABELS[layer];
    this.content = content;
    this.source = source;
    this.sourceType = sourceType;   // 'visual' | 'text' | 'numerical' | 'spatial'
    this.page = page;
    this.confidence = confidence;
    this.parentId = parentId;       // link back to raw/extracted evidence
    this.timestamp = new Date().toISOString();
  }

  toJSON() {
    return { ...this };
  }
}

class EvidenceTraceabilityFramework {
  constructor() {
    this._entries = new Map();   // id → EvidenceEntry
    this._nextId = 1;
  }

  _generateId(layer) {
    return `ETF-L${layer}-${String(this._nextId++).padStart(4, '0')}`;
  }

  addEvidence(params) {
    const id = params.id || this._generateId(params.layer);
    const entry = new EvidenceEntry({ ...params, id });
    this._entries.set(id, entry);
    return entry;
  }

  getById(id) {
    return this._entries.get(id) || null;
  }

  getByLayer(layer) {
    return [...this._entries.values()].filter(e => e.layer === layer);
  }

  getChain(id) {
    const chain = [];
    let current = this._entries.get(id);
    while (current) {
      chain.unshift(current);
      current = current.parentId ? this._entries.get(current.parentId) : null;
    }
    return chain;
  }

  // Verify that every synthesized/interpreted entry traces back to a raw source.
  verifyTraceability() {
    const issues = [];
    for (const entry of this._entries.values()) {
      if (entry.layer >= LAYERS.SYNTHESIZED && !entry.parentId) {
        issues.push({ id: entry.id, issue: 'No parent evidence linked — traceability broken.' });
      }
    }
    return { valid: issues.length === 0, issues };
  }

  summary() {
    const counts = LAYER_LABELS.map((label, i) => ({
      layer: i,
      label,
      count: this.getByLayer(i).length,
    }));
    return { totalEntries: this._entries.size, layers: counts };
  }

  exportJSON() {
    const entries = [...this._entries.values()].map(e => e.toJSON());
    return JSON.stringify({ framework: 'ETF', exportedAt: new Date().toISOString(), entries }, null, 2);
  }
}

module.exports = { EvidenceTraceabilityFramework, EvidenceEntry, LAYERS, LAYER_LABELS };
