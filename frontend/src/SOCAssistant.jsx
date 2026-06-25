import React, { useState, useEffect } from 'react';

const SOCAssistant = () => {
  const [alerts, setAlerts] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('alerts');
  const [incidents, setIncidents] = useState([]);
  const [logs, setLogs] = useState([]);
  const [threatIntel, setThreatIntel] = useState(null);

  // Fetch alerts from backend
  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/alerts');
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
    setLoading(false);
  };

  // Analyze alert with Claude AI
  const analyzeAlert = async (alert) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          alert: alert,
          context: 'security_operations'
        })
      });
      const data = await response.json();
      setAnalysis(data);
      setSelectedAlert(alert);
    } catch (error) {
      console.error('Error analyzing alert:', error);
    }
    setLoading(false);
  };

  // Get incident response recommendations
  const getIncidentResponse = async () => {
    if (!selectedAlert) return;
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/incident-response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ alert: selectedAlert })
      });
      const data = await response.json();
      setAnalysis(prev => ({ ...prev, incident_response: data }));
    } catch (error) {
      console.error('Error getting incident response:', error);
    }
    setLoading(false);
  };

  // Map to MITRE ATT&CK
  const getMITREMapping = async () => {
    if (!selectedAlert) return;
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/mitre-mapping', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ alert: selectedAlert })
      });
      const data = await response.json();
      setAnalysis(prev => ({ ...prev, mitre: data }));
    } catch (error) {
      console.error('Error getting MITRE mapping:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  // Alert severity badge
  // Returns a style OBJECT (not a CSS string) so it can be spread safely into JSX.
  const getSeverityColor = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'critical': return { background: 'var(--color-background-danger)', color: 'var(--color-text-danger)' };
      case 'high': return { background: 'var(--color-background-warning)', color: 'var(--color-text-warning)' };
      case 'medium': return { background: 'var(--color-background-info)', color: 'var(--color-text-info)' };
      case 'low': return { background: 'var(--color-background-success)', color: 'var(--color-text-success)' };
      default: return { background: 'var(--color-background-secondary)', color: 'var(--color-text-secondary)' };
    }
  };

  const getSeverityIcon = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'critical': return 'ti-alert-triangle';
      case 'high': return 'ti-alert-circle';
      case 'medium': return 'ti-exclamation-mark';
      default: return 'ti-info-circle';
    }
  };

  return (
    <div style={{ padding: '2rem', backgroundColor: 'var(--color-background-tertiary)' }}>
      
      {/* Header */}
      <div style={{ marginBottom: '2rem', paddingBottom: '1.5rem', borderBottom: '0.5px solid var(--color-border-tertiary)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '0.5rem' }}>
          <i className="ti ti-shield-alert" style={{ fontSize: '28px', color: 'var(--color-text-danger)' }} aria-hidden="true"></i>
          <h1 style={{ margin: 0, fontSize: '24px', fontWeight: '500', color: 'var(--color-text-primary)' }}>AI Security Operations Center</h1>
        </div>
        <p style={{ margin: '0.5rem 0 0', fontSize: '14px', color: 'var(--color-text-secondary)' }}>Real-time threat detection, analysis & incident response</p>
      </div>

      {/* Dashboard Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '12px', marginBottom: '2rem' }}>
        <div style={{ background: 'var(--color-background-secondary)', padding: '1rem', borderRadius: 'var(--border-radius-md)' }}>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: 0, marginBottom: '0.5rem' }}>Active Alerts</p>
          <p style={{ fontSize: '24px', fontWeight: '500', margin: 0, color: 'var(--color-text-danger)' }}>{alerts.length}</p>
        </div>
        <div style={{ background: 'var(--color-background-secondary)', padding: '1rem', borderRadius: 'var(--border-radius-md)' }}>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: 0, marginBottom: '0.5rem' }}>Critical</p>
          <p style={{ fontSize: '24px', fontWeight: '500', margin: 0, color: 'var(--color-text-danger)' }}>{alerts.filter(a => a.severity === 'critical').length}</p>
        </div>
        <div style={{ background: 'var(--color-background-secondary)', padding: '1rem', borderRadius: 'var(--border-radius-md)' }}>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: 0, marginBottom: '0.5rem' }}>Detection Rate</p>
          <p style={{ fontSize: '24px', fontWeight: '500', margin: 0, color: 'var(--color-text-info)' }}>98.5%</p>
        </div>
        <div style={{ background: 'var(--color-background-secondary)', padding: '1rem', borderRadius: 'var(--border-radius-md)' }}>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: 0, marginBottom: '0.5rem' }}>Response Time</p>
          <p style={{ fontSize: '24px', fontWeight: '500', margin: 0, color: 'var(--color-text-success)' }}>3.2s</p>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '1.5rem', borderBottom: '0.5px solid var(--color-border-tertiary)', paddingBottom: '1rem' }}>
        {['alerts', 'incidents', 'logs', 'threat-intel'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              background: activeTab === tab ? 'var(--color-background-primary)' : 'transparent',
              border: activeTab === tab ? '0.5px solid var(--color-border-secondary)' : 'none',
              padding: '8px 16px',
              borderRadius: 'var(--border-radius-md)',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500',
              color: activeTab === tab ? 'var(--color-text-primary)' : 'var(--color-text-secondary)',
              transition: 'all 0.2s'
            }}
          >
            {tab === 'alerts' && <><i className="ti ti-bell" style={{ marginRight: '6px' }} aria-hidden="true"></i>Alerts</>}
            {tab === 'incidents' && <><i className="ti ti-alert-triangle" style={{ marginRight: '6px' }} aria-hidden="true"></i>Incidents</>}
            {tab === 'logs' && <><i className="ti ti-file-text" style={{ marginRight: '6px' }} aria-hidden="true"></i>Logs</>}
            {tab === 'threat-intel' && <><i className="ti ti-world" style={{ marginRight: '6px' }} aria-hidden="true"></i>Threat Intel</>}
          </button>
        ))}
      </div>

      {/* Alerts Tab */}
      {activeTab === 'alerts' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          
          {/* Alert List */}
          <div>
            <h2 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '1rem' }}>Recent Alerts</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {alerts.length === 0 ? (
                <div style={{ padding: '1rem', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
                  {loading ? 'Loading alerts...' : 'No alerts found'}
                </div>
              ) : (
                alerts.slice(0, 10).map((alert, idx) => (
                  <button
                    key={idx}
                    onClick={() => analyzeAlert(alert)}
                    style={{
                      background: selectedAlert === alert ? 'var(--color-background-secondary)' : 'var(--color-background-primary)',
                      border: '0.5px solid var(--color-border-tertiary)',
                      borderRadius: 'var(--border-radius-md)',
                      padding: '12px',
                      textAlign: 'left',
                      cursor: 'pointer',
                      transition: 'all 0.2s'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <i className={`ti ${getSeverityIcon(alert.severity)}`} style={{ fontSize: '16px', ...getSeverityColor(alert.severity), background: 'transparent' }} aria-hidden="true"></i>
                      <div style={{ flex: 1 }}>
                        <p style={{ margin: 0, fontSize: '13px', fontWeight: '500', color: 'var(--color-text-primary)' }}>{alert.type || 'Security Alert'}</p>
                        <p style={{ margin: '2px 0 0', fontSize: '12px', color: 'var(--color-text-secondary)' }}>{alert.source || 'Unknown Source'}</p>
                      </div>
                      <span style={{ ...getSeverityColor(alert.severity), padding: '4px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 500 }}>{alert.severity}</span>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>

          {/* Analysis Panel */}
          <div>
            {selectedAlert ? (
              <div style={{ background: 'var(--color-background-primary)', border: '0.5px solid var(--color-border-tertiary)', borderRadius: 'var(--border-radius-lg)', padding: '1.25rem' }}>
                <h2 style={{ fontSize: '16px', fontWeight: '500', margin: '0 0 1rem' }}>Alert Analysis</h2>
                
                {loading ? (
                  <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-text-secondary)' }}>
                    <p>Analyzing with AI...</p>
                  </div>
                ) : analysis ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    
                    {/* Threat Summary */}
                    {analysis.threat_summary && (
                      <div>
                        <p style={{ fontSize: '12px', fontWeight: '500', color: 'var(--color-text-secondary)', textTransform: 'uppercase', margin: '0 0 8px' }}>Threat Summary</p>
                        <p style={{ margin: 0, fontSize: '13px', lineHeight: '1.6', color: 'var(--color-text-primary)' }}>{analysis.threat_summary}</p>
                      </div>
                    )}

                    {/* Risk Assessment */}
                    {analysis.risk_level && (
                      <div style={{ padding: '12px', background: 'var(--color-background-secondary)', borderRadius: 'var(--border-radius-md)' }}>
                        <p style={{ fontSize: '12px', fontWeight: '500', color: 'var(--color-text-secondary)', margin: '0 0 4px' }}>Risk Level</p>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div style={{ width: '100%', height: '8px', background: 'var(--color-background-tertiary)', borderRadius: '4px', overflow: 'hidden' }}>
                            <div style={{ width: `${analysis.risk_score * 10}%`, height: '100%', background: analysis.risk_level === 'CRITICAL' ? 'var(--color-text-danger)' : analysis.risk_level === 'HIGH' ? 'var(--color-text-warning)' : 'var(--color-text-info)' }}></div>
                          </div>
                          <span style={{ fontSize: '12px', fontWeight: '500' }}>{analysis.risk_level}</span>
                        </div>
                      </div>
                    )}

                    {/* MITRE Mapping */}
                    {analysis.mitre && (
                      <div>
                        <p style={{ fontSize: '12px', fontWeight: '500', color: 'var(--color-text-secondary)', textTransform: 'uppercase', margin: '0 0 8px' }}>MITRE ATT&CK</p>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                          {analysis.mitre.techniques?.slice(0, 3).map((tech, idx) => (
                            <span key={idx} style={{ background: 'var(--color-background-info)', color: 'var(--color-text-info)', padding: '4px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: '500' }}>{tech}</span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Recommendation */}
                    {analysis.recommendation && (
                      <div style={{ padding: '12px', background: 'var(--color-background-success)', color: 'var(--color-text-success)', borderRadius: 'var(--border-radius-md)' }}>
                        <p style={{ fontSize: '11px', fontWeight: '500', textTransform: 'uppercase', margin: '0 0 4px' }}>Recommended Action</p>
                        <p style={{ margin: 0, fontSize: '13px' }}>{analysis.recommendation}</p>
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginTop: '1rem', paddingTop: '1rem', borderTop: '0.5px solid var(--color-border-tertiary)' }}>
                      <button onClick={getMITREMapping} style={{ background: 'transparent', border: '0.5px solid var(--color-border-secondary)', padding: '8px', borderRadius: 'var(--border-radius-md)', cursor: 'pointer', fontSize: '12px', fontWeight: '500', color: 'var(--color-text-primary)' }}>
                        <i className="ti ti-map-2" aria-hidden="true"></i> MITRE Map
                      </button>
                      <button onClick={getIncidentResponse} style={{ background: 'var(--color-background-info)', border: 'none', padding: '8px', borderRadius: 'var(--border-radius-md)', cursor: 'pointer', fontSize: '12px', fontWeight: '500', color: 'var(--color-text-info)' }}>
                        <i className="ti ti-shield" aria-hidden="true"></i> Response
                      </button>
                    </div>
                  </div>
                ) : (
                  <p style={{ textAlign: 'center', color: 'var(--color-text-secondary)' }}>Select an alert to analyze</p>
                )}
              </div>
            ) : (
              <div style={{ background: 'var(--color-background-secondary)', border: '0.5px solid var(--color-border-tertiary)', borderRadius: 'var(--border-radius-lg)', padding: '2rem', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
                <p>Select an alert to see detailed analysis</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Incidents Tab */}
      {activeTab === 'incidents' && (
        <div style={{ background: 'var(--color-background-primary)', border: '0.5px solid var(--color-border-tertiary)', borderRadius: 'var(--border-radius-lg)', padding: '1.25rem' }}>
          <h2 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '1rem' }}>Active Incidents</h2>
          <p style={{ color: 'var(--color-text-secondary)', fontSize: '13px' }}>Incident management and response tracking coming soon...</p>
        </div>
      )}

      {/* Logs Tab */}
      {activeTab === 'logs' && (
        <div style={{ background: 'var(--color-background-primary)', border: '0.5px solid var(--color-border-tertiary)', borderRadius: 'var(--border-radius-lg)', padding: '1.25rem' }}>
          <h2 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '1rem' }}>Log Analysis</h2>
          <p style={{ color: 'var(--color-text-secondary)', fontSize: '13px' }}>Real-time log processing and correlation coming soon...</p>
        </div>
      )}

      {/* Threat Intel Tab */}
      {activeTab === 'threat-intel' && (
        <div style={{ background: 'var(--color-background-primary)', border: '0.5px solid var(--color-border-tertiary)', borderRadius: 'var(--border-radius-lg)', padding: '1.25rem' }}>
          <h2 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '1rem' }}>Threat Intelligence</h2>
          <p style={{ color: 'var(--color-text-secondary)', fontSize: '13px' }}>IOC tracking, reputation analysis, and threat feeds coming soon...</p>
        </div>
      )}

    </div>
  );
};

export default SOCAssistant;
