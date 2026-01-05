export default function VideoAnalysisCard({ video }) {
    const { title, thumbnail, publishedAt, oracle_advice, confidence, summary, counter_argument, timestamp_link, assets, jeon_sentiment } = video;

    const adviceColor = oracle_advice === "BUY" || oracle_advice === "STRONG BUY" ? "text-green-600" : "text-red-600";
    const borderColor = oracle_advice === "BUY" || oracle_advice === "STRONG BUY" ? "border-green-400" : "border-red-400";

    return (
        <div className={`bg-white rounded-lg shadow-md overflow-hidden mb-6 border-l-8 ${borderColor} transition-transform hover:scale-[1.01]`}>
            <div className="md:flex">
                <div className="md:w-1/3">
                    <img className="h-48 w-full object-cover md:h-full" src={thumbnail} alt={title} />
                </div>
                <div className="p-6 md:w-2/3">
                    <div className="uppercase tracking-wide text-sm text-indigo-500 font-semibold">{new Date(publishedAt).toLocaleDateString()}</div>
                    <a href={timestamp_link || `https://www.youtube.com/watch?v=${video.id}`} target="_blank" rel="noopener noreferrer" className="block mt-1 text-lg leading-tight font-medium text-black hover:underline">
                        {title}
                    </a>
                    <div className="mt-4 grid grid-cols-2 gap-4">
                        <div>
                            <span className="text-gray-500 text-sm">Jeon Says:</span>
                            <div className="font-bold text-gray-800">{jeon_sentiment}</div>
                        </div>
                        <div>
                            <span className="text-gray-500 text-sm">Oracle Says:</span>
                            <div className={`font-extrabold text-xl ${adviceColor}`}>{oracle_advice}</div>
                        </div>
                    </div>

                    <div className="mt-4">
                        <p className="text-gray-600 text-sm"><span className="font-semibold">Reasoning:</span> {counter_argument}</p>
                    </div>

                    <div className="mt-4 flex flex-wrap gap-2">
                        {assets && assets.map((asset, idx) => (
                            <span key={idx} className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">
                                #{asset}
                            </span>
                        ))}
                    </div>
                     <div className="mt-2 text-xs text-gray-400">
                        Confidence Score: {(confidence * 100).toFixed(0)}%
                    </div>
                </div>
            </div>
        </div>
    );
}
