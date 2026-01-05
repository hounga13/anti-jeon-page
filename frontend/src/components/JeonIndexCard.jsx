export default function JeonIndexCard({ jeonIndex }) {
    if (!jeonIndex) return null;

    const { score, sentiment, description } = jeonIndex;

    // Determine color based on "Fear" (Buy) or "Greed" (Sell)
    // High Jeon Index (Fear/Negative) -> High Reversal Score -> Green
    // Wait, let's clarify the logic.
    // If Jeon is Negative, Oracle is Positive (Buy).
    // If Jeon is Positive, Oracle is Negative (Sell).

    // Let's assume the score passed here is the "Jeon Index" which represents HIS intensity.
    // 0 = Neutral, 100 = Extreme.
    // Combined with sentiment.

    const isBullishSignal = sentiment === "Negative" || sentiment === "Fear";
    const signalColor = isBullishSignal ? "bg-green-500" : "bg-red-500";
    const signalText = isBullishSignal ? "STRONG BUY (Full Maesu)" : "STRONG SELL (Run Away)";

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6 border-2 border-gray-800">
            <h2 className="text-2xl font-bold mb-4 text-gray-900">Today's Jeon Index</h2>
            <div className="flex items-center justify-between">
                <div className="flex-1">
                    <div className="text-4xl font-extrabold text-blue-900 mb-2">
                        {score} <span className="text-lg font-normal text-gray-500">/ 100</span>
                    </div>
                    <p className="text-gray-600 italic">"{description}"</p>
                </div>
                <div className={`w-32 h-32 rounded-full flex items-center justify-center text-white text-center font-bold p-4 ${signalColor} animate-pulse shadow-inner`}>
                    {signalText}
                </div>
            </div>
            <div className="mt-4 p-3 bg-gray-100 rounded text-sm text-gray-700">
                <span className="font-bold">Interpretation:</span> When Jeon is {sentiment}, the Oracle says do the opposite.
            </div>
        </div>
    );
}
