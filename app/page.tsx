export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center p-8">
        <h1 className="text-5xl font-bold mb-6 text-gray-900">Sturgeon AI</h1>
        <p className="text-xl text-gray-600 mb-8">Government Contract Assistant</p>
        <div className="space-x-4">
          <a
            href="/signup"
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Get Started
          </a>
          <a
            href="/login"
            className="inline-block px-6 py-3 bg-white text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition"
          >
            Log In
          </a>
        </div>
      </div>
    </main>
  )
}
