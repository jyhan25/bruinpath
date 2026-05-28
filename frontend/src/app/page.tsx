export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center space-y-6">
        <div className="space-y-2">
          <h1 className="text-5xl font-bold text-indigo-900 tracking-tight">
            BruinPath
          </h1>
          <p className="text-xl text-indigo-600 font-medium">
            UCLA Degree Planning Assistant
          </p>
        </div>

        <p className="text-gray-600 text-lg leading-relaxed">
          Upload your transcript and Degree Audit Report to get a personalized
          quarter-by-quarter plan toward graduation.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8">
          {[
            { step: "1", label: "Upload Transcript", desc: "PDF from MyUCLA" },
            { step: "2", label: "Upload DAR", desc: "Degree Audit Report" },
            { step: "3", label: "Get Your Plan", desc: "Quarter-by-quarter" },
          ].map(({ step, label, desc }) => (
            <div
              key={step}
              className="bg-white rounded-2xl shadow-sm p-6 border border-indigo-100"
            >
              <div className="text-3xl font-bold text-indigo-400 mb-2">{step}</div>
              <div className="font-semibold text-gray-800">{label}</div>
              <div className="text-sm text-gray-500">{desc}</div>
            </div>
          ))}
        </div>

        <a
          href="/plan"
          className="inline-block mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3 rounded-full transition-colors shadow-md"
        >
          Get Started
        </a>
      </div>
    </main>
  );
}
