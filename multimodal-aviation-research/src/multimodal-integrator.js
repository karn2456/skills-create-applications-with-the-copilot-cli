/**
 * Multimodal Data Integrator
 * Handles four source types used in Aviation Management research:
 *   - visual   : satellite images, CCTV, drone footage, thermal maps
 *   - text     : safety reports, survey responses, operational documents
 *   - numerical: KPIs, delay data, cargo throughput, financial metrics
 *   - spatial  : GIS layers, flight routes, apron/terminal layouts
 */

const SUPPORTED_TYPES = ['visual', 'text', 'numerical', 'spatial'];

const VISUAL_SOURCES = ['satellite', 'cctv', 'drone', 'thermal', 'heatmap', 'lidar', 'bim'];
const TEXT_SOURCES   = ['safety-report', 'survey', 'interview', 'operational-document', 'passenger-feedback'];
const NUM_SOURCES    = ['kpi', 'delay-data', 'cargo-throughput', 'flight-schedule', 'financial', 'wtp-survey'];
const SPATIAL_SOURCES = ['gis', 'flight-route', 'apron-layout', 'terminal-map', 'digital-twin'];

class DataSource {
  constructor({ type, subtype, label, metadata = {} }) {
    if (!SUPPORTED_TYPES.includes(type)) {
      throw new Error(`Unsupported data type: ${type}. Use: ${SUPPORTED_TYPES.join(', ')}`);
    }
    this.type = type;
    this.subtype = subtype;
    this.label = label;
    this.metadata = metadata;
    this.registeredAt = new Date().toISOString();
  }
}

class MultimodalIntegrator {
  constructor() {
    this._sources = [];
    this._features = [];  // extracted feature vectors ready for statistical models
  }

  registerSource(params) {
    const src = new DataSource(params);
    this._sources.push(src);
    return src;
  }

  // Simulate feature extraction from a visual source (e.g., CNN → density score)
  extractVisualFeatures(sourceLabel, features = {}) {
    const src = this._sources.find(s => s.label === sourceLabel && s.type === 'visual');
    if (!src) throw new Error(`Visual source not found: ${sourceLabel}`);

    const extracted = {
      sourceLabel,
      sourceType: 'visual',
      features: {
        aircraftDensity: features.aircraftDensity ?? null,
        groundVehicleDensity: features.groundVehicleDensity ?? null,
        congestionScore: features.congestionScore ?? null,
        occupancyRate: features.occupancyRate ?? null,
        ...features,
      },
      extractedAt: new Date().toISOString(),
    };
    this._features.push(extracted);
    return extracted;
  }

  // Merge numerical features from all registered feature vectors into one flat record.
  fuseFeatures() {
    if (this._features.length === 0) return {};
    return this._features.reduce((acc, f) => {
      Object.entries(f.features).forEach(([k, v]) => {
        if (v !== null && v !== undefined) acc[k] = v;
      });
      return acc;
    }, {});
  }

  listSources() {
    return this._sources.map(s => ({
      label: s.label,
      type: s.type,
      subtype: s.subtype,
    }));
  }

  summary() {
    const byType = SUPPORTED_TYPES.reduce((acc, t) => {
      acc[t] = this._sources.filter(s => s.type === t).length;
      return acc;
    }, {});
    return { totalSources: this._sources.length, byType, featuresExtracted: this._features.length };
  }
}

module.exports = {
  MultimodalIntegrator,
  DataSource,
  SUPPORTED_TYPES,
  VISUAL_SOURCES,
  TEXT_SOURCES,
  NUM_SOURCES,
  SPATIAL_SOURCES,
};
