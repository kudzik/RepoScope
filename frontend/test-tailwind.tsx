// Test file for Tailwind CSS
export default function TestTailwind() {
  return (
    <div className="bg-blue-500 text-white p-4 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-2">Tailwind CSS Test</h1>
      <p className="text-sm opacity-90">This component uses Tailwind CSS classes for styling.</p>
      <button className="mt-4 bg-white text-blue-500 px-4 py-2 rounded hover:bg-gray-100 transition-colors">
        Test Button
      </button>
    </div>
  );
}
