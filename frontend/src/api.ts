// API types and functions for communicating with the backend

export interface CircularEclipseRequest {
  altitude_km: number;
  beta_deg: number;
}

export interface CircularEclipseResponse {
  altitude_km: number;
  beta_deg: number;
  orbit_radius_km: number;
  period_sec: number;
  period_min: number;
  beta_crit_deg: number;
  eclipse_sec: number;
  eclipse_min: number;
}

export interface YearlyEclipseRequest {
  altitude_km: number;
  inclination_deg: number;
  raan_deg: number;
  start_utc: string;
  days: number;
  step_hours: number;
}

export interface EclipseSample {
  t_utc: string;
  beta_deg: number;
  eclipse_min: number;
}

export interface EclipseSummary {
  max_eclipse_min: number;
  min_eclipse_min: number;
  days_with_eclipse: number;
}

export interface YearlyEclipseResponse {
  altitude_km: number;
  inclination_deg: number;
  raan_deg: number;
  orbit_radius_km: number;
  period_sec: number;
  period_min: number;
  beta_crit_deg: number;
  samples: EclipseSample[];
  summary: EclipseSummary;
}

const API_BASE = '/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message = errorData.detail || `HTTP error ${response.status}`;
    throw new Error(message);
  }
  return response.json();
}

export async function computeCircularEclipse(
  request: CircularEclipseRequest
): Promise<CircularEclipseResponse> {
  const response = await fetch(`${API_BASE}/eclipse/circular`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  return handleResponse<CircularEclipseResponse>(response);
}

export async function computeYearlyEclipse(
  request: YearlyEclipseRequest
): Promise<YearlyEclipseResponse> {
  const response = await fetch(`${API_BASE}/eclipse/yearly`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  return handleResponse<YearlyEclipseResponse>(response);
}
