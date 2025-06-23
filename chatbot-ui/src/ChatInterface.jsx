// File: src/ChatInterface.jsx
import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import FlightCard from './FlightCard';

export default function ChatInterface({ apiBase = '', apiKey = '', siteId, mode, branding, onModeChange, onClose }) {
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const sessionIdRef = useRef(crypto.randomUUID());
  const [loading, setLoading] = useState(false);
  const [offers, setOffers] = useState([]);
  const [showOffers, setShowOffers] = useState(false);
  const scrollRef = useRef(null);

  const [flightForm, setFlightForm] = useState({
    origin: '',
    destination: '',
    departure_date: '',
    adults: 1
  });

  useEffect(() => {
    setMessages([{ sender: 'bot', text: branding?.welcomeMessage || 'Hello! What is your name?' }]);
  }, [branding]);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, offers]);

  const isValidEmail = (e) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text) return;
    setMessages(prev => [...prev, { sender: 'user', text }]);
    setInput('');

    if (step === 1) {
      setName(text);
      setMessages(prev => [...prev, { sender: 'bot', text: `Nice to meet you, ${text}! Could you share your phone number?` }]);
      setStep(2);
      return;
    }
    if (step === 2) {
      setPhone(text);
      setMessages(prev => [...prev, { sender: 'bot', text: 'Great, and what is your email address?' }]);
      setStep(3);
      return;
    }
    if (step === 3) {
      setEmail(text);
      if (!isValidEmail(text)) {
        setMessages(prev => [...prev, { sender: 'bot', text: '❌ Please enter a valid email address.' }]);
        return;
      }
      try {
        const res = await fetch(`${apiBase}/v1/leads`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-API-KEY': apiKey },
          body: JSON.stringify({ name, phone, email: text })
        });
        if (!res.ok) throw new Error();
      } catch {
        setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, could not save your details.' }]);
        return;
      }
      setMessages(prev => [...prev, { sender: 'bot', text: `Thanks, ${name}! How can I assist you today?` }]);
      setStep(4);
      return;
    }

    setLoading(true);
    if (mode === 'flight') {
      setLoading(false);
      return;
    } else {
      try {
        const res = await fetch(`${apiBase}/v1/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-API-KEY': apiKey },
          body: JSON.stringify({ site_id: siteId, session_id: sessionIdRef.current, message: text })
        });
        const { response } = await res.json();
        setMessages(prev => [...prev, { sender: 'bot', text: response }]);
      } catch {
        setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, something went wrong.' }]);
      }
    }
    setLoading(false);
  };

  // Handle Enter key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleFlightFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setShowOffers(false);
    const { origin, destination, departure_date, adults } = flightForm;
    if (!origin || !destination || !departure_date) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Please fill all fields.' }]);
      setLoading(false);
      return;
    }
    try {
      const res = await fetch(`${apiBase}/v1/flights/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-KEY': apiKey },
        body: JSON.stringify({ origin, destination, depart_date: departure_date, return_date: null, adults })
      });
      const data = await res.json();
      setOffers(data);
      setShowOffers(true);
      setMessages(prev => [...prev, { sender: 'bot', text: `Here are flights from ${origin} to ${destination}:` }]);
    } catch {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, I could not fetch flights.' }]);
    }
    setLoading(false);
    onModeChange('chat');
  };

  return (
    <div className="chat-interface flex flex-col h-full bg-white rounded-t-lg">
      {/* Message list and scroll container */}
      <div ref={scrollRef} className="flex-1 overflow-auto p-4 space-y-2">
        {messages.map((m, i) => (
          <div key={i} className={m.sender === 'bot' ? 'text-left' : 'text-right'}>
            <div className={`inline-block px-3 py-2 rounded ${m.sender==='bot'? 'bg-gray-100':'bg-indigo-500 text-white'}`}>{m.text}</div>
          </div>
        ))}
        {showOffers && (
          <div className="flex space-x-2 overflow-x-auto p-4">
            {offers.map(o => <FlightCard key={o.id} offer={o} onSelect={() => setMessages(prev => [...prev, { sender: 'user', text: `BOOK:${o.id}` }])} />)}
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="p-4 border-t flex items-center space-x-2">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          className="flex-1 resize-none border rounded p-2 focus:outline-none"
          placeholder="Type a message..."
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >Send</button>
      </div>
    </div>
  );
}