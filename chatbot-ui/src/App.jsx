// File: src/App.jsx
import React, { useState, useEffect } from 'react';
import ChatInterface from './ChatInterface';

export default function App() {
  const embedConfig = window.ChatbotConfig || {};
  const apiBase = embedConfig.apiUrl || import.meta.env.VITE_API_URL || '';
  const apiKey = embedConfig.apiKey || import.meta.env.VITE_API_KEY || '';
  const params = new URLSearchParams(window.location.search);
  const isEmbed = Boolean(embedConfig.clientId) || params.get('embed') === '1';
  const clientId = embedConfig.clientId || params.get('client_id') || import.meta.env.VITE_SITE_ID;

  const [open, setOpen] = useState(isEmbed);
  const [mode, setMode] = useState('chat');
  const [branding, setBrand] = useState(embedConfig.theme || null);

  useEffect(() => {
    if (!embedConfig.theme && clientId) {
      fetch(`${apiBase}/v1/clients/${clientId}`, {
        headers: { 'X-API-KEY': apiKey }
      })
        .then(res => res.json())
        .then(data => data.branding && setBrand(data.branding))
        .catch(console.error);
    }
  }, [embedConfig.theme, apiBase, apiKey, clientId]);

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
              apiBase={apiBase}
              apiKey={apiKey}
              siteId={clientId}
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

  if (!clientId) {
    return <div className="p-4 text-red-600">Error: no client_id provided</div>;
  }
  return (
    <div id="embed-container" className="w-full h-full">
      <ChatInterface
        apiBase={apiBase}
        apiKey={apiKey}
        siteId={clientId}
        mode={mode}
        branding={branding}
        onModeChange={setMode}
        onClose={() => window.parent.postMessage({ action: 'close_chat' }, '*')}
      />
    </div>
  );
}