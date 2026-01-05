import { useState, useEffect } from 'react';
import JeonIndexCard from './components/JeonIndexCard';
import VideoAnalysisCard from './components/VideoAnalysisCard';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In production, this would fetch from the public folder or an API
    fetch('/analysis.json')
      .then(res => {
          if (!res.ok) {
              throw new Error("Failed to fetch data");
          }
          return res.json();
      })
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching data:", err);
        // Fallback for development if file isn't in public yet
        setLoading(false);
      });
  }, []);

  if (loading) {
      return <div className="min-h-screen bg-gray-100 flex items-center justify-center text-2xl font-bold">Consulting the Oracle...</div>;
  }

  if (!data) {
      return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center flex-col">
            <div className="text-xl font-bold text-red-600 mb-4">Error loading Oracle Data.</div>
            <p className="text-gray-600">Please ensure the backend script has run.</p>
        </div>
      );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10 text-center">
            <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-2">
                The Anti-Jeon Oracle
            </h1>
            <p className="text-xl text-gray-600">"If he says sell, you BUY."</p>
            <p className="text-sm text-gray-400 mt-2">Last Updated: {new Date(data.last_updated).toLocaleString()}</p>
        </header>

        <JeonIndexCard jeonIndex={data.jeon_index} />

        <div className="mt-12">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">Recent Prophecies (Reversed)</h3>
            {data.videos.map(video => (
                <VideoAnalysisCard key={video.id} video={video} />
            ))}
        </div>

        <footer className="mt-16 text-center text-gray-500 text-sm">
            <p>Disclaimer: This is a parody project for entertainment purposes only. Do not make financial decisions based on AI sarcasm.</p>
            <p className="mt-2">Powered by Google Gemini & GitHub Actions</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
