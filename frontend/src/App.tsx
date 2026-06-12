import React, { useState } from 'react';
import { Upload, Activity, AlertTriangle, FileText, ActivitySquare } from 'lucide-react';
import './index.css';

export default function App() {
  const [file, setFile] = useState<File | null>(null);

  return (
    <div className="min-h-screen bg-slate-50 p-8 font-sans text-slate-800">
      <header className="mb-12">
        <h1 className="text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 tracking-tight">
          RetinaMind AI
        </h1>
        <p className="text-slate-500 text-lg mt-2 font-medium">Diabetic Retinopathy Intelligence Platform</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Upload Section */}
        <div className="glass-panel p-8 col-span-1 flex flex-col items-center justify-center text-center transition-all hover:shadow-2xl border border-slate-200">
          <div className="bg-blue-50 p-6 rounded-full mb-6">
            <Upload size={48} className="text-blue-500" />
          </div>
          <h2 className="text-2xl font-bold mb-4 text-slate-700">Upload Fundus Image</h2>
          <p className="text-slate-500 mb-8">Supports JPG, PNG, DICOM</p>
          <button className="bg-indigo-600 text-white px-8 py-3 rounded-full font-semibold shadow-lg hover:bg-indigo-700 hover:scale-105 transition-transform">
            Select File
          </button>
        </div>

        {/* Dashboard Preview */}
        <div className="col-span-1 lg:col-span-2 grid grid-cols-2 gap-6">
          <div className="glass-panel p-6 border border-slate-200 hover:border-blue-300 transition-colors">
            <div className="flex items-center gap-4 mb-4">
              <Activity className="text-green-500" />
              <h3 className="font-bold text-lg text-slate-700">Severity Assessment</h3>
            </div>
            <div className="text-3xl font-black text-slate-800">Moderate NPDR</div>
            <div className="text-sm font-semibold text-green-600 mt-2">Confidence: 89%</div>
          </div>
          
          <div className="glass-panel p-6 border border-slate-200 hover:border-red-300 transition-colors">
            <div className="flex items-center gap-4 mb-4">
              <AlertTriangle className="text-red-500" />
              <h3 className="font-bold text-lg text-slate-700">Progression Risk</h3>
            </div>
            <div className="text-3xl font-black text-slate-800">High Risk</div>
            <div className="text-sm font-semibold text-red-600 mt-2">65% chance within 3 years</div>
          </div>

          <div className="glass-panel p-6 border border-slate-200 col-span-2">
            <div className="flex items-center gap-4 mb-4">
              <ActivitySquare className="text-indigo-500" />
              <h3 className="font-bold text-lg text-slate-700">Lesion Analysis</h3>
            </div>
            <div className="flex justify-around mt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-slate-800">12</div>
                <div className="text-slate-500 text-sm">Microaneurysms</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-slate-800">450px</div>
                <div className="text-slate-500 text-sm">Hemorrhage Area</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-500">Detected</div>
                <div className="text-slate-500 text-sm">Hard Exudates</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
