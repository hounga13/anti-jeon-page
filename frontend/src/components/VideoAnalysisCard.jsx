export default function VideoAnalysisCard({ video }) {
    const { title, thumbnail, publishedAt, oracle_advice, confidence, summary, counter_argument, timestamp_link, assets, jeon_sentiment } = video;

    const adviceColor = oracle_advice === "BUY" || oracle_advice === "STRONG BUY" ? "text-green-600" : "text-red-600";
    const borderColor = oracle_advice === "BUY" || oracle_advice === "STRONG BUY" ? "border-green-400" : "border-red-400";

    // Simple translation mapping for Oracle Advice
    const adviceText = (oracle_advice === "BUY" || oracle_advice === "STRONG BUY") ? "강력 매수" : (oracle_advice === "HOLD" ? "관망" : "전량 매도");
    const jeonSentimentKR = jeon_sentiment === "Negative" ? "부정적 (매도 의견)" : (jeon_sentiment === "Positive" ? "긍정적 (매수 의견)" : "중립");

    return (
        <div className={`bg-white rounded-lg shadow-md overflow-hidden mb-6 border-l-8 ${borderColor} transition-transform hover:scale-[1.01]`}>
            <div className="md:flex">
                <div className="md:w-1/3">
                    <img className="h-48 w-full object-cover md:h-full" src={thumbnail} alt={title} />
                </div>
                <div className="p-6 md:w-2/3">
                    <div className="uppercase tracking-wide text-sm text-indigo-500 font-semibold">{new Date(publishedAt).toLocaleDateString('ko-KR')}</div>
                    <a href={timestamp_link || `https://www.youtube.com/watch?v=${video.id}`} target="_blank" rel="noopener noreferrer" className="block mt-1 text-lg leading-tight font-medium text-black hover:underline">
                        {title}
                    </a>
                    <div className="mt-4 grid grid-cols-2 gap-4">
                        <div>
                            <span className="text-gray-500 text-sm">전인구의 관점:</span>
                            <div className="font-bold text-gray-800">{jeonSentimentKR}</div>
                        </div>
                        <div>
                            <span className="text-gray-500 text-sm">청개구리 신탁:</span>
                            <div className={`font-extrabold text-xl ${adviceColor}`}>{adviceText}</div>
                        </div>
                    </div>

                    <div className="mt-4">
                        <p className="text-gray-600 text-sm"><span className="font-semibold">반대 매매 논리:</span> {counter_argument}</p>
                    </div>

                    <div className="mt-4 flex flex-wrap gap-2">
                        {assets && assets.map((asset, idx) => (
                            <span key={idx} className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">
                                #{asset}
                            </span>
                        ))}
                    </div>
                     <div className="mt-2 text-xs text-gray-400">
                        확신도: {(confidence * 100).toFixed(0)}%
                    </div>
                </div>
            </div>
        </div>
    );
}
