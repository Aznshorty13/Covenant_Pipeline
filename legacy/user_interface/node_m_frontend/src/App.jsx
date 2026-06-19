import { useState, useEffect, useMemo } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

function App() {
  const [payload, setPayload] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedCovenant, setSelectedCovenant] = useState(null);
  const [selectedTerm, setSelectedTerm] = useState('');
  const [numPages, setNumPages] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/document-data')
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch pipeline data");
        return res.json();
      })
      .then((data) => {
        setPayload(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // NEW: The Deduplicator
  // Scans the incoming payload and removes any covenant with a duplicate Agent name
  const uniqueCovenants = useMemo(() => {
    if (!payload?.Phase1_Extracted_Covenants) return [];
    const seen = new Set();
    return payload.Phase1_Extracted_Covenants.filter(cov => {
      if (!cov.Agent) return false;
      const isDuplicate = seen.has(cov.Agent);
      seen.add(cov.Agent);
      return !isDuplicate;
    });
  }, [payload]);

  const pagesToRender = useMemo(() => {
    if (!selectedCovenant?.Receipt) return [1];
    const match = selectedCovenant.Receipt.match(/PDF Pages? (\d+)(?:-(\d+))?/);
    if (!match) return [1];
    
    const start = parseInt(match[1], 10);
    const end = match[2] ? parseInt(match[2], 10) : start;
    
    const range = [];
    for (let i = start; i <= end; i++) range.push(i);
    return range;
  }, [selectedCovenant]);

  const availableTerms = useMemo(() => {
    if (!selectedCovenant || !payload?.Phase2_Master_Glossary) return [];
    
    const jsonString = JSON.stringify(selectedCovenant.Extracted_Data);
    const regex = /\[\$REF:\s*(.*?)\]/g;
    const foundTerms = new Set();
    
    let match;
    while ((match = regex.exec(jsonString)) !== null) {
      foundTerms.add(match[1]);
    }

    const expandedTerms = new Set(foundTerms);
    foundTerms.forEach(term => {
      const def = payload.Phase2_Master_Glossary[term];
      if (def?.nested_references) {
        def.nested_references.forEach(nested => expandedTerms.add(nested));
      }
    });

    return Array.from(expandedTerms).sort();
  }, [selectedCovenant, payload]);

  useEffect(() => {
    setSelectedTerm(availableTerms.length > 0 ? availableTerms[0] : '');
  }, [availableTerms]);

  const formatAgentName = (name) => {
    if (!name) return 'Unknown Agent';
    return name.replace(/([A-Z])/g, ' $1').trim();
  };

  const renderFormattedData = (data) => {
    if (typeof data !== 'object' || data === null) {
      if (typeof data === 'string' && data.includes('[$REF:')) {
        return <span className="text-blue-400 font-semibold">{data}</span>;
      }
      return <span className="text-slate-200">{String(data)}</span>;
    }
    
    if (Array.isArray(data)) {
      return (
        <ul className="list-disc pl-5 mt-2 space-y-2">
          {data.map((item, i) => <li key={i}>{renderFormattedData(item)}</li>)}
        </ul>
      );
    }
    
    return (
      <div className="space-y-3 mt-2">
        {Object.entries(data).map(([key, value]) => {
          const skipKeys = ['is_false_flag', 'false_flag_reason', 'is_applicable', 'confidence_score'];
          if (skipKeys.includes(key.toLowerCase())) return null;

          return (
            <div key={key} className="bg-slate-800/80 p-3 rounded border border-slate-700/50">
              <span className="font-bold text-slate-400 uppercase tracking-wider text-xs">
                {key.replace(/_/g, ' ')}
              </span>
              <div className="mt-1">{renderFormattedData(value)}</div>
            </div>
          );
        })}
      </div>
    );
  };

  if (loading) return <div className="flex h-screen items-center justify-center bg-slate-900 text-blue-400 font-bold">Initializing Node M...</div>;
  if (error) return <div className="flex h-screen items-center justify-center bg-slate-900 text-red-500 font-bold">Error: {error}</div>;

  return (
    <div className="flex h-screen w-full bg-slate-900 text-slate-100 overflow-hidden font-sans">
      
      {/* COLUMN 1: The Queue */}
      <div className="w-1/4 border-r border-slate-700 bg-slate-800 p-4 flex flex-col">
        <h2 className="text-lg font-bold mb-4 text-blue-400 tracking-wider">PHASE 1 QUEUE</h2>
        <div className="text-sm text-slate-400 mb-4 pb-2 border-b border-slate-700">
          {/* Update the counter to reflect the unique list */}
          {uniqueCovenants.length} Unique Covenants
        </div>
        <div className="flex-1 overflow-y-auto pr-2 space-y-2">
            {/* Map over the new uniqueCovenants array instead of the raw payload */}
            {uniqueCovenants.map((cov, index) => {
              
              // NEW: The Catch-All Receipt Logic
              const receiptParts = cov.Receipt ? cov.Receipt.split('|') : [];
              const pageReceipt = receiptParts[0]?.trim();
              // Grab everything after the first pipe and stitch it back together
              const sectionReceipt = receiptParts.slice(1).join(' | ').trim();

              return (
                <button
                  key={index}
                  onClick={() => setSelectedCovenant(cov)}
                  className={`w-full text-left p-3 rounded border transition-all duration-200 ${
                    selectedCovenant === cov
                      ? 'bg-blue-900/40 border-blue-500 text-blue-100 shadow-md' 
                      : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700 hover:border-slate-500'
                  }`}
                >
                  <div className="font-semibold text-sm flex items-center justify-between">
                    {formatAgentName(cov.Agent)}
                    {cov.Extracted_Data?.is_false_flag === true && (
                      <span className="text-red-400 text-xs bg-red-900/30 px-2 py-0.5 rounded">Flagged</span>
                    )}
                  </div>
                  <div className="text-xs mt-2 text-slate-400 space-y-1">
                    {pageReceipt && <div>{pageReceipt}</div>}
                    {sectionReceipt && <div className="text-slate-500">{sectionReceipt}</div>}
                  </div>
                </button>
              );
            })}
        </div>
      </div>

      {/* COLUMN 2: Document Provenance */}
      <div className="w-2/4 flex flex-col p-4 bg-slate-900 relative">
        <h2 className="text-lg font-bold mb-4 text-blue-400 tracking-wider flex justify-between items-center">
          <span>SOURCE DOCUMENT PROVENANCE</span>
          {selectedCovenant && (
            <span className="text-sm text-slate-500 font-normal border border-slate-700 px-2 py-1 rounded bg-slate-800">
              Pages {pagesToRender[0]} {pagesToRender.length > 1 ? `- ${pagesToRender[pagesToRender.length - 1]}` : ''} of {numPages || '?'}
            </span>
          )}
        </h2>
        <div className="flex-1 border border-slate-700 rounded bg-slate-800/30 overflow-y-auto flex flex-col items-center p-4 space-y-6">
           <Document
             file="http://127.0.0.1:8000/api/pdf"
             onLoadSuccess={({ numPages }) => setNumPages(numPages)}
             loading={<span className="text-slate-500 font-medium animate-pulse">Rendering Document Spread...</span>}
           >
             {pagesToRender.map((pageNum) => (
               <div key={pageNum} className="mb-6 shadow-2xl drop-shadow-2xl rounded overflow-hidden border border-slate-700">
                 <Page 
                   pageNumber={pageNum} 
                   width={700} 
                   renderTextLayer={false} 
                   renderAnnotationLayer={false}
                 />
               </div>
             ))}
           </Document>
        </div>
      </div>

      {/* COLUMN 3: Audit & Glossary */}
      <div className="w-1/4 border-l border-slate-700 bg-slate-800 flex flex-col">
        <div className="p-4 h-3/5 border-b border-slate-700 flex flex-col">
            <h2 className="text-lg font-bold mb-4 text-blue-400 tracking-wider shrink-0">EXTRACTED MATH</h2>
            
            <div className="flex-1 overflow-y-auto pr-2">
              {selectedCovenant ? (
                <>
                  {(() => {
                    const data = selectedCovenant.Extracted_Data || {};
                    const conf = data.confidence_score !== undefined ? data.confidence_score : 1; 
                    const isFlagged = data.is_false_flag === true || conf < 1;
                    const reason = data.false_flag_reason;

                    return (
                      <div className="mb-4 bg-slate-900 border border-slate-700 p-3 rounded flex flex-col gap-2 shadow-sm">
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-400 uppercase tracking-wider font-bold">Confidence Score</span>
                          <span className={`text-sm font-bold ${conf < 1 ? 'text-yellow-400' : 'text-green-400'}`}>
                            {(conf * 100).toFixed(0)}%
                          </span>
                        </div>
                        
                        {isFlagged && reason && reason !== 'null' && (
                          <div className="text-xs text-red-400 border-t border-slate-700 pt-2 mt-1">
                            <span className="font-bold">Flag Reason: </span>{reason}
                          </div>
                        )}
                      </div>
                    );
                  })()}

                  {renderFormattedData(selectedCovenant.Extracted_Data)}
                </>
              ) : (
                <div className="text-sm text-slate-400 italic">Select an item from the queue to view data.</div>
              )}
            </div>
        </div>
        
        <div className="p-4 flex-1 flex flex-col overflow-hidden">
            <h2 className="text-lg font-bold mb-4 text-blue-400 tracking-wider shrink-0">DYNAMIC GLOSSARY</h2>
            
            {!selectedCovenant ? (
              <div className="text-sm text-slate-400 italic">Select an item from the queue.</div>
            ) : availableTerms.length === 0 ? (
              <div className="text-sm text-slate-500">No legal terms detected in this covenant.</div>
            ) : (
              <div className="flex flex-col h-full">
                <select 
                  className="w-full bg-slate-900 border border-slate-600 text-slate-200 text-sm rounded p-2 mb-4 focus:ring-1 focus:ring-blue-500 outline-none"
                  value={selectedTerm}
                  onChange={(e) => setSelectedTerm(e.target.value)}
                >
                  {availableTerms.map(term => (
                    <option key={term} value={term}>{term}</option>
                  ))}
                </select>
                
                <div className="flex-1 overflow-y-auto bg-slate-900/50 p-3 rounded border border-slate-700/50">
                  {selectedTerm && payload?.Phase2_Master_Glossary[selectedTerm] ? (
                    <p className="text-sm text-slate-300 leading-relaxed">
                      {payload.Phase2_Master_Glossary[selectedTerm].raw_definition_text}
                    </p>
                  ) : (
                    <span className="text-red-400 text-sm">Definition not found in Phase 2 payload.</span>
                  )}
                </div>
              </div>
            )}
        </div>
      </div>

    </div>
  );
}

export default App;