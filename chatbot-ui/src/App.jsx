// src/App.jsx
import React, { useState, useEffect } from 'react';
import ChatInterface from './ChatInterface';

export default function App() {
  const apiBase = import.meta.env.VITE_API_URL || '';
  const params   = new URLSearchParams(window.location.search);
  const isEmbed  = params.get('embed') === '1';
  const clientId = params.get('client_id');

  const [open, setOpen]     = useState(isEmbed);
  const [mode, setMode]     = useState('chat');
  const [branding, setBrand] = useState(null);

  // In embed mode, fetch branding from your API
  useEffect(() => {
    if (!isEmbed || !clientId) return;
    fetch(`${apiBase}/api/clients/${clientId}`)
      .then(r => r.json())
      .then(data => data.branding && setBrand(data.branding))
      .catch(console.error);
  }, [isEmbed, clientId]);

  // Non-embed demo: floating buttons
  if (!isEmbed) {
    return (
      <>
        <div className="fixed bottom-6 right-6 flex space-x-2 z-50">
          <button
            className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-full shadow-lg"
            onClick={() => { setMode('chat'); setOpen(true); }}
            aria-label="Chat"
          >💬</button>
          <button
            className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-full shadow-lg"
            onClick={() => { setMode('flight'); setOpen(true); }}
            aria-label="Flight Search"
          >✈️</button>
        </div>

        {open && (
          <div className="fixed bottom-20 right-6 w-80 h-[500px] bg-white rounded-xl shadow-2xl flex flex-col overflow-hidden z-50">
            <ChatInterface
            
              siteId={import.meta.env.VITE_SITE_ID}
              mode={mode}
              branding={branding}
              onModeChange={setMode}
              onClose={() => setOpen(false)}
            />
          </div>
        )}
      </>
    );
  }

  // --- Embed mode / inside iframe ---
  if (!clientId) {
    return <div className="p-4 text-red-600">Error: no client_id provided</div>;
  }
  return (
    <div id="embed-container" className="w-full h-full">
      <ChatInterface
        siteId={clientId}
        mode={mode}
        branding={branding}
        onModeChange={setMode}
        onClose={() => {
          // iframe parent handles closing
          window.parent.postMessage({ action: 'close_chat' }, '*');
        }}
      />
    </div>
  );
}
