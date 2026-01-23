import EclipseTool from './components/EclipseTool';

const appStyles: React.CSSProperties = {
  minHeight: '100vh',
  padding: '2rem',
};

const headerStyles: React.CSSProperties = {
  textAlign: 'center',
  marginBottom: '2rem',
};

const titleStyles: React.CSSProperties = {
  fontSize: '2.5rem',
  fontWeight: 700,
  background: 'linear-gradient(90deg, #64b5f6, #81c784)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  marginBottom: '0.5rem',
};

const subtitleStyles: React.CSSProperties = {
  color: '#888',
  fontSize: '1rem',
};

function App() {
  return (
    <div style={appStyles}>
      <header style={headerStyles}>
        <h1 style={titleStyles}>Orbit Eclipse Calculator</h1>
        <p style={subtitleStyles}>
          Compute orbital eclipse durations for circular Earth orbits
        </p>
      </header>
      <main>
        <EclipseTool />
      </main>
    </div>
  );
}

export default App;
