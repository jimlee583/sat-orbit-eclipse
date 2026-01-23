import { useState } from 'react';
import Plot from 'react-plotly.js';
import {
  computeCircularEclipse,
  computeYearlyEclipse,
  CircularEclipseResponse,
  YearlyEclipseResponse,
} from '../api';

const cardStyles: React.CSSProperties = {
  maxWidth: '1200px',
  margin: '0 auto',
  background: 'rgba(30, 30, 50, 0.9)',
  borderRadius: '16px',
  padding: '2rem',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
  border: '1px solid rgba(100, 181, 246, 0.2)',
};

const sectionStyles: React.CSSProperties = {
  marginBottom: '2rem',
};

const sectionTitleStyles: React.CSSProperties = {
  fontSize: '1.25rem',
  fontWeight: 600,
  color: '#64b5f6',
  marginBottom: '1rem',
  borderBottom: '1px solid rgba(100, 181, 246, 0.3)',
  paddingBottom: '0.5rem',
};

const inputGridStyles: React.CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
  gap: '1rem',
  marginBottom: '1rem',
};

const inputGroupStyles: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: '0.5rem',
};

const labelStyles: React.CSSProperties = {
  fontSize: '0.875rem',
  color: '#aaa',
  fontWeight: 500,
};

const inputStyles: React.CSSProperties = {
  background: 'rgba(0, 0, 0, 0.3)',
  border: '1px solid rgba(100, 181, 246, 0.3)',
  borderRadius: '8px',
  padding: '0.75rem 1rem',
  color: '#fff',
  fontSize: '1rem',
  outline: 'none',
  transition: 'border-color 0.2s',
};

const buttonStyles: React.CSSProperties = {
  background: 'linear-gradient(135deg, #1e88e5, #1565c0)',
  color: '#fff',
  border: 'none',
  borderRadius: '8px',
  padding: '0.875rem 1.5rem',
  fontSize: '1rem',
  fontWeight: 600,
  cursor: 'pointer',
  transition: 'transform 0.2s, box-shadow 0.2s',
  marginRight: '1rem',
  marginBottom: '0.5rem',
};

const resultCardStyles: React.CSSProperties = {
  background: 'rgba(0, 0, 0, 0.2)',
  borderRadius: '12px',
  padding: '1.5rem',
  marginTop: '1.5rem',
};

const statGridStyles: React.CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
  gap: '1rem',
};

const statItemStyles: React.CSSProperties = {
  textAlign: 'center',
  padding: '1rem',
  background: 'rgba(100, 181, 246, 0.1)',
  borderRadius: '8px',
};

const statValueStyles: React.CSSProperties = {
  fontSize: '1.5rem',
  fontWeight: 700,
  color: '#81c784',
};

const statLabelStyles: React.CSSProperties = {
  fontSize: '0.75rem',
  color: '#888',
  marginTop: '0.25rem',
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
};

const errorStyles: React.CSSProperties = {
  background: 'rgba(244, 67, 54, 0.2)',
  border: '1px solid rgba(244, 67, 54, 0.5)',
  borderRadius: '8px',
  padding: '1rem',
  color: '#ef5350',
  marginTop: '1rem',
};

const advancedToggleStyles: React.CSSProperties = {
  background: 'none',
  border: 'none',
  color: '#64b5f6',
  cursor: 'pointer',
  fontSize: '0.875rem',
  padding: '0.5rem 0',
  marginBottom: '1rem',
};

function EclipseTool() {
  // Yearly eclipse inputs
  const [altitude, setAltitude] = useState(400);
  const [inclination, setInclination] = useState(51.6);
  const [raan, setRaan] = useState(0);
  const [startDate, setStartDate] = useState('2026-01-01T00:00:00Z');
  const [stepHours, setStepHours] = useState(24);
  const [days, setDays] = useState(365);

  // Circular eclipse inputs
  const [betaDeg, setBetaDeg] = useState(0);

  // Results
  const [yearlyResult, setYearlyResult] = useState<YearlyEclipseResponse | null>(null);
  const [circularResult, setCircularResult] = useState<CircularEclipseResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // UI state
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleComputeYearly = async () => {
    setError(null);
    setLoading(true);
    try {
      const result = await computeYearlyEclipse({
        altitude_km: altitude,
        inclination_deg: inclination,
        raan_deg: raan,
        start_utc: startDate,
        days,
        step_hours: stepHours,
      });
      setYearlyResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleComputeCircular = async () => {
    setError(null);
    setLoading(true);
    try {
      const result = await computeCircularEclipse({
        altitude_km: altitude,
        beta_deg: betaDeg,
      });
      setCircularResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // Prepare plot data
  const plotData = yearlyResult
    ? [
        {
          x: yearlyResult.samples.map((s) => s.t_utc.split('T')[0]),
          y: yearlyResult.samples.map((s) => s.eclipse_min),
          type: 'scatter' as const,
          mode: 'lines' as const,
          name: 'Eclipse Duration (min)',
          line: { color: '#81c784', width: 2 },
        },
        {
          x: yearlyResult.samples.map((s) => s.t_utc.split('T')[0]),
          y: yearlyResult.samples.map((s) => s.beta_deg),
          type: 'scatter' as const,
          mode: 'lines' as const,
          name: 'Beta Angle (deg)',
          yaxis: 'y2',
          line: { color: '#64b5f6', width: 2, dash: 'dot' as const },
        },
      ]
    : [];

  const plotLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0.2)',
    font: { color: '#e0e0e0' },
    margin: { t: 40, r: 80, b: 60, l: 60 },
    xaxis: {
      title: 'Date',
      gridcolor: 'rgba(255,255,255,0.1)',
      tickangle: -45,
    },
    yaxis: {
      title: 'Eclipse Duration (min)',
      gridcolor: 'rgba(255,255,255,0.1)',
      titlefont: { color: '#81c784' },
      tickfont: { color: '#81c784' },
    },
    yaxis2: {
      title: 'Beta Angle (deg)',
      overlaying: 'y' as const,
      side: 'right' as const,
      titlefont: { color: '#64b5f6' },
      tickfont: { color: '#64b5f6' },
      gridcolor: 'rgba(255,255,255,0.05)',
    },
    legend: {
      x: 0,
      y: 1.15,
      orientation: 'h' as const,
    },
    showlegend: true,
  };

  return (
    <div style={cardStyles}>
      {/* Orbital Parameters Section */}
      <div style={sectionStyles}>
        <h2 style={sectionTitleStyles}>Orbital Parameters</h2>
        <div style={inputGridStyles}>
          <div style={inputGroupStyles}>
            <label style={labelStyles}>Altitude (km)</label>
            <input
              type="number"
              value={altitude}
              onChange={(e) => setAltitude(parseFloat(e.target.value) || 0)}
              style={inputStyles}
              min={0}
            />
          </div>
          <div style={inputGroupStyles}>
            <label style={labelStyles}>Inclination (deg)</label>
            <input
              type="number"
              value={inclination}
              onChange={(e) => setInclination(parseFloat(e.target.value) || 0)}
              style={inputStyles}
              min={0}
              max={180}
            />
          </div>
          <div style={inputGroupStyles}>
            <label style={labelStyles}>RAAN (deg)</label>
            <input
              type="number"
              value={raan}
              onChange={(e) => setRaan(parseFloat(e.target.value) || 0)}
              style={inputStyles}
              min={0}
              max={360}
            />
          </div>
          <div style={inputGroupStyles}>
            <label style={labelStyles}>Start Date (UTC)</label>
            <input
              type="text"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              style={inputStyles}
              placeholder="2026-01-01T00:00:00Z"
            />
          </div>
          <div style={inputGroupStyles}>
            <label style={labelStyles}>Step (hours)</label>
            <input
              type="number"
              value={stepHours}
              onChange={(e) => setStepHours(parseFloat(e.target.value) || 24)}
              style={inputStyles}
              min={1}
              max={168}
            />
          </div>
          <div style={inputGroupStyles}>
            <label style={labelStyles}>Days</label>
            <input
              type="number"
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value) || 365)}
              style={inputStyles}
              min={1}
              max={730}
            />
          </div>
        </div>
        <button
          style={buttonStyles}
          onClick={handleComputeYearly}
          disabled={loading}
        >
          {loading ? 'Computing...' : 'Compute Yearly Curve'}
        </button>
      </div>

      {/* Advanced Section */}
      <button
        style={advancedToggleStyles}
        onClick={() => setShowAdvanced(!showAdvanced)}
      >
        {showAdvanced ? '▼' : '▶'} Advanced: Compute from Beta Angle
      </button>

      {showAdvanced && (
        <div style={{ ...sectionStyles, marginTop: '0' }}>
          <div style={inputGridStyles}>
            <div style={inputGroupStyles}>
              <label style={labelStyles}>Beta Angle (deg)</label>
              <input
                type="number"
                value={betaDeg}
                onChange={(e) => setBetaDeg(parseFloat(e.target.value) || 0)}
                style={inputStyles}
                min={-90}
                max={90}
              />
            </div>
          </div>
          <button
            style={{ ...buttonStyles, background: 'linear-gradient(135deg, #7b1fa2, #512da8)' }}
            onClick={handleComputeCircular}
            disabled={loading}
          >
            Compute Circular Eclipse
          </button>

          {circularResult && (
            <div style={resultCardStyles}>
              <h3 style={{ ...sectionTitleStyles, marginTop: 0 }}>Circular Eclipse Result</h3>
              <div style={statGridStyles}>
                <div style={statItemStyles}>
                  <div style={statValueStyles}>{circularResult.period_min.toFixed(2)}</div>
                  <div style={statLabelStyles}>Period (min)</div>
                </div>
                <div style={statItemStyles}>
                  <div style={statValueStyles}>{circularResult.beta_crit_deg.toFixed(2)}°</div>
                  <div style={statLabelStyles}>Beta Critical</div>
                </div>
                <div style={statItemStyles}>
                  <div style={statValueStyles}>{circularResult.eclipse_min.toFixed(2)}</div>
                  <div style={statLabelStyles}>Eclipse (min)</div>
                </div>
                <div style={statItemStyles}>
                  <div style={statValueStyles}>{circularResult.orbit_radius_km.toFixed(1)}</div>
                  <div style={statLabelStyles}>Orbit Radius (km)</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && <div style={errorStyles}>{error}</div>}

      {/* Yearly Results */}
      {yearlyResult && (
        <div style={resultCardStyles}>
          <h3 style={{ ...sectionTitleStyles, marginTop: 0 }}>Yearly Eclipse Analysis</h3>

          {/* Summary Stats */}
          <div style={statGridStyles}>
            <div style={statItemStyles}>
              <div style={statValueStyles}>{yearlyResult.period_min.toFixed(2)}</div>
              <div style={statLabelStyles}>Period (min)</div>
            </div>
            <div style={statItemStyles}>
              <div style={statValueStyles}>{yearlyResult.beta_crit_deg.toFixed(2)}°</div>
              <div style={statLabelStyles}>Beta Critical</div>
            </div>
            <div style={statItemStyles}>
              <div style={statValueStyles}>{yearlyResult.summary.max_eclipse_min.toFixed(2)}</div>
              <div style={statLabelStyles}>Max Eclipse (min)</div>
            </div>
            <div style={statItemStyles}>
              <div style={statValueStyles}>{yearlyResult.summary.min_eclipse_min.toFixed(2)}</div>
              <div style={statLabelStyles}>Min Eclipse (min)</div>
            </div>
            <div style={statItemStyles}>
              <div style={statValueStyles}>{yearlyResult.summary.days_with_eclipse}</div>
              <div style={statLabelStyles}>Days with Eclipse</div>
            </div>
            <div style={statItemStyles}>
              <div style={statValueStyles}>{yearlyResult.orbit_radius_km.toFixed(1)}</div>
              <div style={statLabelStyles}>Orbit Radius (km)</div>
            </div>
          </div>

          {/* Plot */}
          <div style={{ marginTop: '1.5rem' }}>
            <Plot
              data={plotData}
              layout={plotLayout}
              style={{ width: '100%', height: '400px' }}
              config={{ responsive: true, displayModeBar: false }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default EclipseTool;
