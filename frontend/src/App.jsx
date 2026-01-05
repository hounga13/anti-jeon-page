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
      return <div className="min-h-screen bg-gray-100 flex items-center justify-center text-2xl font-bold">신탁을 조회하는 중입니다...</div>;
  }

  if (!data) {
      return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center flex-col">
            <div className="text-xl font-bold text-red-600 mb-4">데이터 로드 실패</div>
            <p className="text-gray-600">백엔드 스크립트가 실행되었는지 확인해주세요.</p>
        </div>
      );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10 text-center">
            <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-2">
                청개구리 신탁 (The Anti-Jeon)
            </h1>
            <p className="text-xl text-gray-600">"그가 팔라고 하면 사고, 사라고 하면 팔아라."</p>
            <p className="text-sm text-gray-400 mt-2">마지막 업데이트: {new Date(data.last_updated).toLocaleString('ko-KR')}</p>
        </header>

        <JeonIndexCard jeonIndex={data.jeon_index} />

        <div className="mt-12">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">최신 신탁 (반대 매매 전략)</h3>
            {data.videos.map(video => (
                <VideoAnalysisCard key={video.id} video={video} />
            ))}
        </div>

        <footer className="mt-16 text-center text-gray-500 text-sm">
            <p>면책 조항: 본 서비스는 유머와 풍자를 목적으로 하는 프로젝트이며, 실제 투자 조언이 아닙니다. 모든 투자의 책임은 본인에게 있습니다.</p>
            <p className="mt-2">Powered by Google Gemini & GitHub Actions</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
